import re

from cobol_parser_mcp.cobol_parser import _SESSION_CACHE
from cobol_parser_mcp.result import make_error, make_result, make_warning

# Match data item definitions: level-number + field-name in DATA DIVISION
_FIELD_RE = re.compile(r"^\s*\d{1,2}\s+([A-Z][A-Z0-9\-]*)(?:\s|\.)", re.IGNORECASE)


def _extract_data_division_fields(source: str) -> list[str]:
    """Return uppercase non-FILLER field names from the DATA DIVISION."""
    fields: list[str] = []
    seen: set[str] = set()
    in_data_div = False

    for line in source.splitlines():
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        upper = line.upper()
        if "DATA" in upper and "DIVISION" in upper:
            in_data_div = True
            continue
        if in_data_div and "PROCEDURE" in upper and "DIVISION" in upper:
            break
        if not in_data_div:
            continue
        m = _FIELD_RE.match(line.strip() if line.strip() else "")
        if m:
            name = m.group(1).upper()
            if name != "FILLER" and name not in seen:
                seen.add(name)
                fields.append(name)
    return fields


def _validate_single_cluster(cluster: dict, valid_paragraphs: set[str]) -> list[dict]:
    flags: list[dict] = []

    name = cluster.get("name", "")
    if not isinstance(name, str) or not name.strip():
        flags.append(
            {
                "code": "INVALID_CLUSTER_DATA",
                "message": "Cluster 'name' must be a non-empty string",
                "location": "",
            }
        )

    paras = cluster.get("paragraphs", [])
    if not isinstance(paras, list) or len(paras) == 0:
        flags.append(
            {
                "code": "INVALID_CLUSTER_DATA",
                "message": "Cluster 'paragraphs' must be a non-empty list",
                "location": name or "",
            }
        )
    else:
        for para in paras:
            if para not in valid_paragraphs:
                flags.append(
                    {
                        "code": "INVALID_CLUSTER_DATA",
                        "message": f"Paragraph '{para}' not found in parsed module",
                        "location": name or "",
                    }
                )
    return flags


def build_cluster_context(program_name: str) -> dict:
    """Return ONLY paragraph names, PERFORM edges, and DATA DIVISION field names
    for a previously parsed module.  NO raw COBOL source is included — this is the
    privacy enforcement point before data is passed to the LLM agent (NFR7)."""
    try:
        if program_name not in _SESSION_CACHE:
            return make_error(
                f"Module not parsed in this session:"
                " run parse_module and extract_call_graph first",
                flags=["CACHE_MISS"],
            )

        cached = _SESSION_CACHE[program_name]
        paragraphs: list[dict] = cached.get("paragraphs", [])
        source: str = cached.get("_source", "")

        from cobol_parser_mcp.call_graph import build_call_graph

        cg = build_call_graph(program_name)
        edges = cg.get("data", {}).get("edges", []) if cg.get("status") == "ok" else []

        data_fields = _extract_data_division_fields(source)

        return make_result(
            data={
                "program_name": program_name,
                "paragraph_names": [p["name"] for p in paragraphs],
                "perform_edges": edges,
                "data_division_fields": data_fields,
            }
        )

    except Exception as e:
        return make_error(f"build_cluster_context failed: {e}", flags=["CONTEXT_ERROR"])


def validate_cluster_output(program_name: str, clusters: list) -> dict:
    """Validate cluster groupings produced by the Viper agent and store them in session
    cache.  Returns ok if valid, warning if structural issues found, error on cache miss."""
    try:
        if program_name not in _SESSION_CACHE:
            return make_error(
                f"Module not parsed in this session: run parse_module first",
                flags=["CACHE_MISS"],
            )

        cached = _SESSION_CACHE[program_name]
        valid_paragraphs = {p["name"] for p in cached.get("paragraphs", [])}

        all_flags: list[dict] = []
        for i, cluster in enumerate(clusters):
            for flag in _validate_single_cluster(cluster, valid_paragraphs):
                flag["cluster_index"] = i
                all_flags.append(flag)

        # Always store (best effort) so Viper workflow can read even on warning
        _SESSION_CACHE[program_name]["clusters"] = clusters

        if all_flags:
            return make_warning(
                data={"program_name": program_name, "clusters": clusters},
                message="Cluster validation found issues",
                flags=all_flags,
            )

        return make_result(data={"program_name": program_name, "clusters": clusters})

    except Exception as e:
        return make_error(
            f"validate_cluster_output failed: {e}", flags=["VALIDATE_ERROR"]
        )
