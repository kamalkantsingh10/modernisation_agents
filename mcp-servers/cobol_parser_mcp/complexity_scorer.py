"""
Complexity scoring for parsed COBOL modules.

Thresholds (documented for analyst calibration):
  Low:    paragraph_count <= 20  AND  max_perform_nesting_depth <= 3
          AND  redefines_count <= 3  AND  goto_count == 0
  High:   paragraph_count > 50   OR   max_perform_nesting_depth > 5
          OR   redefines_count > 10  OR   goto_count >= 5
  Medium: all other cases
"""

import re

from cobol_parser_mcp.cobol_parser import _SESSION_CACHE
from cobol_parser_mcp.result import make_error, make_result

_GOTO_RE = re.compile(r"\bGO\s+TO\b", re.IGNORECASE)
_REDEFINES_RE = re.compile(r"\b([A-Z][A-Z0-9\-]*)\s+REDEFINES\b", re.IGNORECASE)


def _calculate_perform_nesting_depth(call_graph_edges: list[dict]) -> int:
    """Return the maximum PERFORM call-chain depth (number of edges in longest path)."""
    if not call_graph_edges:
        return 0

    adj: dict[str, set[str]] = {}
    all_nodes: set[str] = set()
    all_targets: set[str] = set()

    for edge in call_graph_edges:
        f, t = edge["from"], edge["to"]
        all_nodes.update([f, t])
        all_targets.add(t)
        adj.setdefault(f, set()).add(t)

    max_depth = [0]

    def _dfs(node: str, path: set[str], depth: int) -> None:
        if node in path:
            return  # cycle guard
        path.add(node)
        if depth > max_depth[0]:
            max_depth[0] = depth
        for child in adj.get(node, set()):
            _dfs(child, path, depth + 1)
        path.remove(node)

    roots = all_nodes - all_targets or all_nodes
    for root in roots:
        _dfs(root, set(), 0)

    return max_depth[0]


def _count_redefines(source: str) -> int:
    """Count non-FILLER REDEFINES clauses in the DATA DIVISION."""
    count = 0
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
        if "REDEFINES" in upper:
            for m in _REDEFINES_RE.finditer(line):
                if m.group(1).upper() != "FILLER":
                    count += 1
    return count


def _count_gotos(source: str) -> int:
    """Count GO TO statements in the PROCEDURE DIVISION."""
    count = 0
    in_proc = False
    for line in source.splitlines():
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        upper = line.upper()
        if "PROCEDURE" in upper and "DIVISION" in upper:
            in_proc = True
            continue
        if in_proc:
            count += len(_GOTO_RE.findall(line))
    return count


def _compute_rating(
    paragraph_count: int,
    nesting_depth: int,
    redefines_count: int,
    goto_count: int,
) -> str:
    if paragraph_count <= 20 and nesting_depth <= 3 and redefines_count <= 3 and goto_count == 0:
        return "Low"
    if paragraph_count > 50 or nesting_depth > 5 or redefines_count > 10 or goto_count >= 5:
        return "High"
    return "Medium"


def score_complexity(program_name: str) -> dict:
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

        from cobol_parser_mcp.call_graph import build_call_graph

        cg = build_call_graph(program_name)
        edges = cg.get("data", {}).get("edges", []) if cg.get("status") == "ok" else []

        paragraph_count = len(paragraphs)
        nesting_depth = _calculate_perform_nesting_depth(edges)
        redefines_count = _count_redefines(source)
        goto_count = _count_gotos(source)

        rating = _compute_rating(paragraph_count, nesting_depth, redefines_count, goto_count)

        return make_result(
            data={
                "program_name": program_name,
                "rating": rating,
                "factors": {
                    "paragraph_count": paragraph_count,
                    "max_perform_nesting_depth": nesting_depth,
                    "redefines_count": redefines_count,
                    "goto_count": goto_count,
                },
            }
        )

    except Exception as e:
        return make_error(f"score_complexity failed: {e}", flags=["SCORE_ERROR"])
