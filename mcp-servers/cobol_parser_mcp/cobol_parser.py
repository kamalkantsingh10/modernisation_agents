import re
from pathlib import Path

from cobol_parser_mcp.dialect_handler import find_exec_cics_blocks, find_exec_sql_blocks
from cobol_parser_mcp.result import make_error, make_result

# Server-level session cache: keyed by COBOL PROGRAM-ID (verbatim, uppercase).
# Persists for the lifetime of the server process (one IDE session).
_SESSION_CACHE: dict[str, dict] = {}

_PROGRAM_ID_RE = re.compile(
    r"PROGRAM-ID\.[ \t]+([A-Z0-9][A-Z0-9\-]*)\.?",
    re.IGNORECASE,
)
_PARA_RE = re.compile(r"^([A-Z0-9][A-Z0-9\-]*)\.(?:\s|$)", re.IGNORECASE)
_COPY_RE = re.compile(r"\bCOPY\s+([A-Z0-9][A-Z0-9\-]*)\b", re.IGNORECASE)
_CALL_RE = re.compile(r"\bCALL\s+['\"]([A-Z0-9][A-Z0-9\-\._]*)['\"]", re.IGNORECASE)
_DELTA_MACRO_RE = re.compile(r"\b(DLTM-[A-Z0-9][A-Z0-9\-]*)\b", re.IGNORECASE)


def _extract_program_id(source: str) -> str:
    m = _PROGRAM_ID_RE.search(source)
    if not m:
        raise ValueError("PROGRAM-ID not found in source")
    return m.group(1).upper()


def _find_paragraphs(source: str) -> list[dict]:
    paragraphs: list[dict] = []
    seen: set[str] = set()
    in_proc = False

    for line_num, line in enumerate(source.splitlines(), 1):
        if len(line) <= 7:
            continue
        # Column 7 (index 6): '*' or '/' marks a comment line
        if line[6] in ("*", "/"):
            continue

        upper_line = line.upper()

        # Track entry into PROCEDURE DIVISION
        if "PROCEDURE" in upper_line and "DIVISION" in upper_line:
            in_proc = True
            continue

        if not in_proc:
            continue

        # Exclude section declarations
        if "SECTION" in upper_line:
            continue

        area_a = line[7:]
        m = _PARA_RE.match(area_a)
        if not m:
            continue

        name = m.group(1).upper()
        if name not in seen:
            seen.add(name)
            paragraphs.append({"name": name, "line": line_num})

    return paragraphs


def _extract_copy_refs(source: str) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()
    for line in source.splitlines():
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        for m in _COPY_RE.finditer(line):
            name = m.group(1).upper()
            if name not in seen:
                seen.add(name)
                refs.append(name)
    return refs


def _extract_call_targets(source: str) -> list[str]:
    targets: list[str] = []
    seen: set[str] = set()
    for line in source.splitlines():
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        for m in _CALL_RE.finditer(line):
            name = m.group(1).upper()
            if name not in seen:
                seen.add(name)
                targets.append(name)
    return targets


def _find_delta_macros(source: str) -> list[dict]:
    macros: list[dict] = []
    seen: set[str] = set()
    for line_num, line in enumerate(source.splitlines(), 1):
        if len(line) > 6 and line[6] in ("*", "/"):
            continue
        for m in _DELTA_MACRO_RE.finditer(line):
            name = m.group(1).upper()
            if name not in seen:
                seen.add(name)
                macros.append({"name": name, "line": line_num})
    return macros


def parse_module(program_name: str, source_path: str) -> dict:
    try:
        path = Path(source_path)
        if not path.exists():
            return make_error(
                f"File not found: {source_path}", flags=["FILE_NOT_FOUND"]
            )

        source = path.read_text(encoding="utf-8", errors="replace")

        try:
            canonical_id = _extract_program_id(source)
        except ValueError:
            canonical_id = program_name.upper()

        paragraphs = _find_paragraphs(source)
        copy_refs = _extract_copy_refs(source)
        call_targets = _extract_call_targets(source)
        delta_macros = _find_delta_macros(source)
        exec_sql = find_exec_sql_blocks(source)
        exec_cics = find_exec_cics_blocks(source)

        result_data = {
            "program_name": canonical_id,
            "paragraphs": paragraphs,
            "copy_refs": copy_refs,
            "call_targets": call_targets,
            "exec_sql_blocks": exec_sql,
            "exec_cics_blocks": exec_cics,
            "delta_macros": delta_macros,
        }

        _SESSION_CACHE[canonical_id] = {**result_data, "_source": source}

        return make_result(data=result_data)

    except Exception as e:
        return make_error(f"parse_module failed: {e}", flags=["PARSE_ERROR"])
