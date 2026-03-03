from cobol_parser_mcp import dialect_handler

EXEC_SQL_SOURCE = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DB-ACCESS.
       PROCEDURE DIVISION.
       TEST-PARA.
           EXEC SQL
               SELECT 1 INTO :WS-X FROM SYSIBM.SYSDUMMY1
           END-EXEC.
           STOP RUN.
"""

EXEC_CICS_SOURCE = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CICS-TEST.
       PROCEDURE DIVISION.
       SEND-PARA.
           EXEC CICS
               SEND TEXT FROM(WS-MSG) LENGTH(80)
           END-EXEC.
           STOP RUN.
"""

BOTH_SOURCE = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. MIXED-TEST.
       PROCEDURE DIVISION.
       FIRST-PARA.
           EXEC SQL
               SELECT 1 INTO :WS-X FROM SYSIBM.SYSDUMMY1
           END-EXEC.
       SECOND-PARA.
           EXEC CICS
               RETURN
           END-EXEC.
           STOP RUN.
"""


def test_find_exec_sql_blocks_detects_locations():
    blocks = dialect_handler.find_exec_sql_blocks(EXEC_SQL_SOURCE)
    assert len(blocks) == 1
    b = blocks[0]
    assert "line_start" in b
    assert "line_end" in b
    assert b["line_start"] == 5
    assert b["line_end"] == 7


def test_find_exec_cics_blocks_detects_locations():
    blocks = dialect_handler.find_exec_cics_blocks(EXEC_CICS_SOURCE)
    assert len(blocks) == 1
    b = blocks[0]
    assert b["line_start"] == 5
    assert b["line_end"] == 7


def test_find_exec_sql_returns_empty_when_none():
    blocks = dialect_handler.find_exec_sql_blocks("       IDENTIFICATION DIVISION.\n")
    assert blocks == []


def test_find_exec_cics_returns_empty_when_none():
    blocks = dialect_handler.find_exec_cics_blocks("       IDENTIFICATION DIVISION.\n")
    assert blocks == []


def test_find_exec_sql_multiple_blocks():
    source = """\
       PROCEDURE DIVISION.
       PARA-1.
           EXEC SQL SELECT 1 INTO :X FROM SYSIBM.SYSDUMMY1 END-EXEC.
       PARA-2.
           EXEC SQL SELECT 2 INTO :Y FROM SYSIBM.SYSDUMMY1 END-EXEC.
"""
    blocks = dialect_handler.find_exec_sql_blocks(source)
    assert len(blocks) == 2


def test_find_both_block_types_independently():
    sql_blocks = dialect_handler.find_exec_sql_blocks(BOTH_SOURCE)
    cics_blocks = dialect_handler.find_exec_cics_blocks(BOTH_SOURCE)
    assert len(sql_blocks) == 1
    assert len(cics_blocks) == 1
    assert sql_blocks[0]["line_start"] < cics_blocks[0]["line_start"]
