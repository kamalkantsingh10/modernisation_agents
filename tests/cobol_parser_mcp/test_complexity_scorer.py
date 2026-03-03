from pathlib import Path

import pytest

from cobol_parser_mcp import cobol_parser
from cobol_parser_mcp.complexity_scorer import score_complexity

FIXTURES = Path(__file__).parent / "fixtures"
BLACKJACK_SRC = FIXTURES / "blackjack" / "src"


def test_score_complexity_low_rating_simple_module():
    cobol_parser.parse_module("CLEAN-TEST", str(FIXTURES / "clean.cbl"))
    result = score_complexity("CLEAN-TEST")
    assert result["status"] == "ok"
    assert result["data"]["rating"] == "Low"


def test_score_complexity_high_rating_complex_module():
    cobol_parser.parse_module("GOTO-COMPLEX", str(FIXTURES / "goto_complex.cbl"))
    result = score_complexity("GOTO-COMPLEX")
    assert result["status"] == "ok"
    assert result["data"]["rating"] == "High"


def test_score_complexity_includes_all_four_factors():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    result = score_complexity("PAYROLL-CALC")
    assert result["status"] == "ok"
    factors = result["data"]["factors"]
    for key in ("paragraph_count", "max_perform_nesting_depth", "redefines_count", "goto_count"):
        assert key in factors, f"Missing factor: {key}"
        assert isinstance(factors[key], int)


def test_score_complexity_no_cache_returns_error():
    result = score_complexity("NONEXISTENT-XYZ-99")
    assert result["status"] == "error"
    assert result["data"] is None


def test_score_complexity_never_raises():
    try:
        result = score_complexity("TOTALLY-MISSING-XYZ")
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"score_complexity raised: {e}")


@pytest.mark.skipif(not BLACKJACK_SRC.exists(), reason="BlackJack corpus not available")
def test_blackjack_corpus_score_complexity_all_ok():
    for cob_file in BLACKJACK_SRC.glob("*.cob"):
        program_name = cob_file.stem.upper()
        cobol_parser.parse_module(program_name, str(cob_file))
        result = score_complexity(program_name)
        assert result["status"] == "ok", (
            f"score_complexity failed for {cob_file.name}: {result.get('message', '')}"
        )
