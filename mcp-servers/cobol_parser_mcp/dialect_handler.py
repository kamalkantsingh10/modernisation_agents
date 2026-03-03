import re

_EXEC_SQL_RE = re.compile(r"EXEC\s+SQL\b(.+?)END-EXEC", re.IGNORECASE | re.DOTALL)
_EXEC_CICS_RE = re.compile(r"EXEC\s+CICS\b(.+?)END-EXEC", re.IGNORECASE | re.DOTALL)


def _line_number(source: str, offset: int) -> int:
    return source[:offset].count("\n") + 1


def find_exec_sql_blocks(source: str) -> list[dict]:
    blocks = []
    for m in _EXEC_SQL_RE.finditer(source):
        blocks.append(
            {
                "location": None,
                "line_start": _line_number(source, m.start()),
                "line_end": _line_number(source, m.end()),
            }
        )
    return blocks


def find_exec_cics_blocks(source: str) -> list[dict]:
    blocks = []
    for m in _EXEC_CICS_RE.finditer(source):
        blocks.append(
            {
                "location": None,
                "line_start": _line_number(source, m.start()),
                "line_end": _line_number(source, m.end()),
            }
        )
    return blocks


def detect_dialect(source: str) -> str:
    upper = source.upper()
    if any(m in upper for m in ("EXEC CICS", "EXEC SQL", "GOBACK", "SERVICE LABEL")):
        return "IBM_ENTERPRISE"
    if any(m in upper for m in ("END-IF", "END-PERFORM", "END-READ", "END-WRITE")):
        return "COBOL_85"
    return "UNKNOWN"
