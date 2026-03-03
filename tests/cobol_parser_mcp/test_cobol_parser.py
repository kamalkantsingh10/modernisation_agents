from pathlib import Path

import pytest

from cobol_parser_mcp import cobol_parser

FIXTURES = Path(__file__).parent / "fixtures"
BLACKJACK_SRC = FIXTURES / "blackjack" / "src"


def test_parse_module_extracts_program_id_verbatim():
    result = cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    assert result["status"] == "ok"
    assert result["data"]["program_name"] == "PAYROLL-CALC"


def test_parse_module_extracts_paragraphs_with_line_numbers():
    result = cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    paras = result["data"]["paragraphs"]
    names = [p["name"] for p in paras]
    assert "MAIN-PARA" in names
    assert "CALC-PARA" in names
    assert "FINAL-PARA" in names
    for p in paras:
        assert isinstance(p["line"], int)
        assert p["line"] > 0


def test_parse_module_extracts_copy_refs():
    result = cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    assert "PAYROLL-WS" in result["data"]["copy_refs"]


def test_parse_module_extracts_call_targets():
    result = cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    assert "TAX-CALC" in result["data"]["call_targets"]


def test_parse_module_finds_exec_sql_blocks():
    result = cobol_parser.parse_module("DB-ACCESS", str(FIXTURES / "exec_blocks.cbl"))
    assert result["status"] == "ok"
    blocks = result["data"]["exec_sql_blocks"]
    assert len(blocks) >= 1
    assert "line_start" in blocks[0]
    assert "line_end" in blocks[0]
    assert blocks[0]["line_start"] < blocks[0]["line_end"]


def test_parse_module_finds_exec_cics_blocks():
    result = cobol_parser.parse_module("DB-ACCESS", str(FIXTURES / "exec_blocks.cbl"))
    assert result["status"] == "ok"
    blocks = result["data"]["exec_cics_blocks"]
    assert len(blocks) >= 1
    assert "line_start" in blocks[0]
    assert "line_end" in blocks[0]


def test_parse_module_finds_delta_macros():
    result = cobol_parser.parse_module("MACRO-TEST", str(FIXTURES / "delta_macros.cbl"))
    assert result["status"] == "ok"
    macros = result["data"]["delta_macros"]
    names = [m["name"] for m in macros]
    assert "DLTM-ACCT-LOCK" in names


def test_parse_module_stores_result_in_session_cache():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    assert "PAYROLL-CALC" in cobol_parser._SESSION_CACHE


def test_parse_module_file_not_found_returns_error_not_raises():
    result = cobol_parser.parse_module("MISSING", "/nonexistent/path/missing.cbl")
    assert result["status"] == "error"
    assert result["data"] is None


def test_parse_module_never_raises_on_malformed_source(tmp_path):
    bad = tmp_path / "bad.cbl"
    bad.write_bytes(b"\x00\x01\x02\x03\xff" * 100)
    result = cobol_parser.parse_module("BAD", str(bad))
    assert result["status"] in ("ok", "error", "warning")


@pytest.mark.skipif(not BLACKJACK_SRC.exists(), reason="BlackJack corpus not available")
def test_blackjack_corpus_all_modules_parse_successfully():
    cob_files = list(BLACKJACK_SRC.glob("*.cob"))
    assert len(cob_files) > 0
    for cob_file in cob_files:
        program_name = cob_file.stem.upper().replace("-", "-")
        result = cobol_parser.parse_module(program_name, str(cob_file))
        assert result["status"] == "ok", (
            f"parse_module failed for {cob_file.name}: {result.get('message', '')}"
        )
