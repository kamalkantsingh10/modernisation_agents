import re

from cobol_parser_mcp.cobol_parser import _SESSION_CACHE
from cobol_parser_mcp.result import make_error, make_result

_GOTO_RE = re.compile(r"\bGO\s+TO\b", re.IGNORECASE)
_ALTER_RE = re.compile(r"\bALTER\b", re.IGNORECASE)
_REDEFINES_RE = re.compile(r"\b([A-Z][A-Z0-9\-]*)\s+REDEFINES\b", re.IGNORECASE)
_PERFORM_THRU_RE = re.compile(
    r"\bPERFORM\s+([A-Z0-9][A-Z0-9\-]*)\s+THRU\s+([A-Z0-9][A-Z0-9\-]*)",
    re.IGNORECASE,
)


def _get_context(line_num: int, sorted_paras: list[dict]) -> str | None:
    current = None
    for p in sorted_paras:
        if p["line"] <= line_num:
            current = p["name"]
        else:
            break
    return current


def _detect_gotos(source: str, paragraphs: list[dict]) -> list[dict]:
    results: list[dict] = []
    sorted_paras = sorted(paragraphs, key=lambda p: p["line"])
    in_proc = False

    for line_num, line in enumerate(source.splitlines(), 1):
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        upper = line.upper()
        if "PROCEDURE" in upper and "DIVISION" in upper:
            in_proc = True
            continue
        if not in_proc:
            continue
        if _GOTO_RE.search(line):
            ctx = _get_context(line_num, sorted_paras)
            location = f"{ctx}:{line_num}" if ctx else f":{line_num}"
            results.append(
                {
                    "type": "GOTO",
                    "location": location,
                    "description": f"Unconditional GO TO at line {line_num}",
                }
            )
    return results


def _detect_alters(source: str, paragraphs: list[dict]) -> list[dict]:
    results: list[dict] = []
    sorted_paras = sorted(paragraphs, key=lambda p: p["line"])
    in_proc = False

    for line_num, line in enumerate(source.splitlines(), 1):
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        upper = line.upper()
        if "PROCEDURE" in upper and "DIVISION" in upper:
            in_proc = True
            continue
        if not in_proc:
            continue
        if _ALTER_RE.search(line):
            ctx = _get_context(line_num, sorted_paras)
            location = f"{ctx}:{line_num}" if ctx else f":{line_num}"
            results.append(
                {
                    "type": "ALTER",
                    "location": location,
                    "description": f"ALTER statement at line {line_num} (deprecated COBOL construct)",
                }
            )
    return results


def _detect_nested_perform_thru(source: str, paragraphs: list[dict]) -> list[dict]:
    from cobol_parser_mcp.call_graph import _expand_perform_thru

    if not paragraphs:
        return []

    results: list[dict] = []
    seen: set[str] = set()
    sorted_paras = sorted(paragraphs, key=lambda p: p["line"])
    source_lines = source.splitlines()

    # Build paragraph boundaries: name -> (start_line, exclusive_end_line)
    para_bounds: dict[str, tuple[int, float]] = {}
    for i, p in enumerate(sorted_paras):
        next_start = sorted_paras[i + 1]["line"] if i + 1 < len(sorted_paras) else float("inf")
        para_bounds[p["name"]] = (p["line"], next_start)

    def lines_of(para_name: str) -> list[tuple[int, str]]:
        start, end = para_bounds.get(para_name, (None, None))
        if start is None:
            return []
        return [
            (i + 1, ln)
            for i, ln in enumerate(source_lines)
            if start <= i + 1 < end
        ]

    # Scan for every PERFORM THRU in source and check for nesting
    for line_num, line in enumerate(source_lines, 1):
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        m = _PERFORM_THRU_RE.search(line)
        if not m:
            continue
        thru_start = m.group(1).upper()
        thru_end = m.group(2).upper()

        for para_name in _expand_perform_thru(sorted_paras, thru_start, thru_end):
            for inner_ln, inner_line in lines_of(para_name):
                if len(inner_line) > 6 and inner_line[6] in ("*", "/"):
                    continue
                if _PERFORM_THRU_RE.search(inner_line):
                    loc_key = f"{para_name}:{inner_ln}"
                    if loc_key not in seen:
                        seen.add(loc_key)
                        results.append(
                            {
                                "type": "NESTED_PERFORM_THRU",
                                "location": loc_key,
                                "description": (
                                    f"Paragraph '{para_name}' at line {inner_ln} "
                                    "contains PERFORM THRU and is within a PERFORM THRU range"
                                ),
                            }
                        )
    return results


def _detect_redefines_non_filler(source: str) -> list[dict]:
    results: list[dict] = []
    in_data_div = False

    for line_num, line in enumerate(source.splitlines(), 1):
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
        if "REDEFINES" in upper:
            m = _REDEFINES_RE.search(line)
            if m and m.group(1).upper() != "FILLER":
                item_name = m.group(1).upper()
                results.append(
                    {
                        "type": "REDEFINES_NON_FILLER",
                        "location": f":{line_num}",
                        "description": (
                            f"REDEFINES clause on non-FILLER item '{item_name}' at line {line_num}"
                        ),
                    }
                )
    return results


def _detect_fallthrough_paragraphs(
    paragraphs: list[dict], perform_targets: list[str]
) -> list[dict]:
    if not paragraphs:
        return []

    sorted_paras = sorted(paragraphs, key=lambda p: p["line"])
    first_name = sorted_paras[0]["name"]
    target_set = set(perform_targets)
    results: list[dict] = []

    for p in sorted_paras:
        if p["name"] == first_name:
            continue
        if p["name"] not in target_set:
            results.append(
                {
                    "type": "FALLTHROUGH_PARAGRAPH",
                    "location": f"{p['name']}:{p['line']}",
                    "description": (
                        f"Paragraph '{p['name']}' at line {p['line']} "
                        "is not explicitly PERFORMed (reachable only by fall-through)"
                    ),
                }
            )
    return results


def detect_antipatterns(program_name: str) -> dict:
    try:
        if program_name not in _SESSION_CACHE:
            return make_error(
                f"Program '{program_name}' not parsed in this session."
                " Call parse_module first.",
                flags=["CACHE_MISS"],
            )

        cached = _SESSION_CACHE[program_name]
        source: str = cached.get("_source", "")
        paragraphs: list[dict] = cached.get("paragraphs", [])
        exec_cics_blocks: list[dict] = cached.get("exec_cics_blocks", [])
        exec_sql_blocks: list[dict] = cached.get("exec_sql_blocks", [])

        from cobol_parser_mcp.call_graph import build_call_graph

        cg = build_call_graph(program_name)
        edges = cg.get("data", {}).get("edges", []) if cg.get("status") == "ok" else []
        perform_targets = list({e["to"] for e in edges})

        antipatterns: list[dict] = []
        antipatterns.extend(_detect_gotos(source, paragraphs))
        antipatterns.extend(_detect_alters(source, paragraphs))
        antipatterns.extend(_detect_nested_perform_thru(source, paragraphs))
        antipatterns.extend(_detect_redefines_non_filler(source))
        antipatterns.extend(_detect_fallthrough_paragraphs(paragraphs, perform_targets))

        flags: list[dict] = []
        for block in exec_cics_blocks:
            flags.append(
                {
                    "code": "CICS_CONSTRUCT",
                    "message": f"EXEC CICS block at lines {block['line_start']}-{block['line_end']}",
                    "location": f":{block['line_start']}",
                }
            )
        for block in exec_sql_blocks:
            flags.append(
                {
                    "code": "DB2_SQL_CONSTRUCT",
                    "message": f"EXEC SQL block at lines {block['line_start']}-{block['line_end']}",
                    "location": f":{block['line_start']}",
                }
            )

        message = "No anti-patterns detected" if not antipatterns else ""
        return make_result(data={"antipatterns": antipatterns}, flags=flags, message=message)

    except Exception as e:
        return make_error(f"detect_antipatterns failed: {e}", flags=["DETECT_ERROR"])
