import re

from cobol_parser_mcp.cobol_parser import _SESSION_CACHE
from cobol_parser_mcp.result import make_error, make_result

_PERFORM_RE = re.compile(
    r"\bPERFORM\s+([A-Z0-9][A-Z0-9\-]*)(?:\s+THRU\s+([A-Z0-9][A-Z0-9\-]*))?",
    re.IGNORECASE,
)

# COBOL keywords that may follow PERFORM but are not paragraph names
_PERFORM_KEYWORDS = frozenset(
    {"VARYING", "UNTIL", "TIMES", "TEST", "WITH", "NO", "INLINE"}
)


def _find_perform_statements(source: str, paragraphs: list[dict]) -> list[dict]:
    if not paragraphs:
        return []

    sorted_paras = sorted(paragraphs, key=lambda p: p["line"])

    def _context(line_num: int) -> str | None:
        current = None
        for p in sorted_paras:
            if p["line"] <= line_num:
                current = p["name"]
            else:
                break
        return current

    performs: list[dict] = []
    for line_num, line in enumerate(source.splitlines(), 1):
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        for m in _PERFORM_RE.finditer(line):
            target = m.group(1).upper()
            if target in _PERFORM_KEYWORDS:
                continue
            performs.append(
                {
                    "from": _context(line_num),
                    "to": target,
                    "thru": m.group(2).upper() if m.group(2) else None,
                    "line": line_num,
                }
            )
    return performs


def _expand_perform_thru(
    paragraphs: list[dict], thru_start: str, thru_end: str
) -> list[str]:
    sorted_paras = sorted(paragraphs, key=lambda p: p["line"])
    names = [p["name"] for p in sorted_paras]

    try:
        start_idx = names.index(thru_start)
        end_idx = names.index(thru_end)
    except ValueError:
        return []

    if start_idx > end_idx:
        start_idx, end_idx = end_idx, start_idx

    return names[start_idx : end_idx + 1]


def build_call_graph(program_name: str) -> dict:
    try:
        if program_name not in _SESSION_CACHE:
            return make_error(
                f"Program '{program_name}' not found in session cache."
                " Call parse_module first.",
                flags=["CACHE_MISS"],
            )

        cached = _SESSION_CACHE[program_name]
        paragraphs = cached.get("paragraphs", [])
        source = cached.get("_source", "")

        performs = _find_perform_statements(source, paragraphs)

        nodes = [p["name"] for p in sorted(paragraphs, key=lambda p: p["line"])]
        edges: list[dict] = []

        for perform in performs:
            from_para = perform["from"]
            if not from_para:
                continue
            target = perform["to"]
            thru = perform["thru"]

            if thru:
                for t in _expand_perform_thru(paragraphs, target, thru):
                    edges.append({"from": from_para, "to": t})
            else:
                edges.append({"from": from_para, "to": target})

        return make_result(
            data={"program_name": program_name, "nodes": nodes, "edges": edges}
        )

    except Exception as e:
        return make_error(f"build_call_graph failed: {e}", flags=["GRAPH_ERROR"])
