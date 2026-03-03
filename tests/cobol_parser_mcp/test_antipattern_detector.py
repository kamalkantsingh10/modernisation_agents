from pathlib import Path

import pytest

from cobol_parser_mcp import cobol_parser
from cobol_parser_mcp.antipattern_detector import detect_antipatterns

FIXTURES = Path(__file__).parent / "fixtures"
BLACKJACK_SRC = FIXTURES / "blackjack" / "src"


def test_detect_antipatterns_finds_goto():
    cobol_parser.parse_module("GOTO-COMPLEX", str(FIXTURES / "goto_complex.cbl"))
    result = detect_antipatterns("GOTO-COMPLEX")
    assert result["status"] == "ok"
    types = [ap["type"] for ap in result["data"]["antipatterns"]]
    assert "GOTO" in types


def test_detect_antipatterns_finds_alter():
    cobol_parser.parse_module("ALTER-TEST", str(FIXTURES / "alter.cbl"))
    result = detect_antipatterns("ALTER-TEST")
    assert result["status"] == "ok"
    types = [ap["type"] for ap in result["data"]["antipatterns"]]
    assert "ALTER" in types


def test_detect_antipatterns_finds_nested_perform_thru():
    cobol_parser.parse_module("NESTED-TEST", str(FIXTURES / "nested_thru.cbl"))
    result = detect_antipatterns("NESTED-TEST")
    assert result["status"] == "ok"
    types = [ap["type"] for ap in result["data"]["antipatterns"]]
    assert "NESTED_PERFORM_THRU" in types


def test_detect_antipatterns_finds_redefines_non_filler():
    cobol_parser.parse_module("REDEF-TEST", str(FIXTURES / "redefines.cbl"))
    result = detect_antipatterns("REDEF-TEST")
    assert result["status"] == "ok"
    types = [ap["type"] for ap in result["data"]["antipatterns"]]
    assert "REDEFINES_NON_FILLER" in types


def test_detect_antipatterns_flags_cics_construct():
    cobol_parser.parse_module("DB-ACCESS", str(FIXTURES / "exec_blocks.cbl"))
    result = detect_antipatterns("DB-ACCESS")
    assert result["status"] == "ok"
    flag_codes = [f["code"] for f in result["flags"]]
    assert "CICS_CONSTRUCT" in flag_codes


def test_detect_antipatterns_flags_db2_sql_construct():
    cobol_parser.parse_module("DB-ACCESS", str(FIXTURES / "exec_blocks.cbl"))
    result = detect_antipatterns("DB-ACCESS")
    assert result["status"] == "ok"
    flag_codes = [f["code"] for f in result["flags"]]
    assert "DB2_SQL_CONSTRUCT" in flag_codes


def test_detect_antipatterns_empty_result_when_no_antipatterns():
    cobol_parser.parse_module("CLEAN-TEST", str(FIXTURES / "clean.cbl"))
    result = detect_antipatterns("CLEAN-TEST")
    assert result["status"] == "ok"
    assert result["data"]["antipatterns"] == []
    assert result["flags"] == []
    assert result["message"] == "No anti-patterns detected"


def test_detect_antipatterns_no_cache_returns_error():
    result = detect_antipatterns("NONEXISTENT-XYZ-99")
    assert result["status"] == "error"
    assert result["data"] is None


def test_detect_antipatterns_never_raises():
    try:
        result = detect_antipatterns("TOTALLY-MISSING-XYZ")
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"detect_antipatterns raised: {e}")


@pytest.mark.skipif(not BLACKJACK_SRC.exists(), reason="BlackJack corpus not available")
def test_blackjack_corpus_detect_antipatterns_all_ok():
    for cob_file in BLACKJACK_SRC.glob("*.cob"):
        program_name = cob_file.stem.upper()
        cobol_parser.parse_module(program_name, str(cob_file))
        result = detect_antipatterns(program_name)
        assert result["status"] == "ok", (
            f"detect_antipatterns failed for {cob_file.name}: {result.get('message', '')}"
        )
