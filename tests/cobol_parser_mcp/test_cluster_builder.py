from pathlib import Path

import pytest

from cobol_parser_mcp import cobol_parser
from cobol_parser_mcp.cluster_builder import build_cluster_context, validate_cluster_output

FIXTURES = Path(__file__).parent / "fixtures"
BLACKJACK_SRC = FIXTURES / "blackjack" / "src"

_VALID_CLUSTERS = [
    {"name": "Calculation", "paragraphs": ["MAIN-PARA", "CALC-PARA"], "description": "Core calc logic"},
    {"name": "Termination", "paragraphs": ["FINAL-PARA"], "description": "Program exit"},
]


def test_build_cluster_context_returns_paragraphs_not_source():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    result = build_cluster_context("PAYROLL-CALC")
    assert result["status"] == "ok"
    data = result["data"]
    # Only expected keys — no raw source
    assert set(data.keys()) == {"program_name", "paragraph_names", "perform_edges", "data_division_fields"}
    # Raw COBOL statement text must not appear
    data_str = str(data)
    assert "COMPUTE WS-AMT = WS-AMT * 2" not in data_str
    assert "STOP RUN" not in data_str


def test_build_cluster_context_returns_perform_edges():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    result = build_cluster_context("PAYROLL-CALC")
    edges = result["data"]["perform_edges"]
    assert any(e["from"] == "MAIN-PARA" and e["to"] == "CALC-PARA" for e in edges)


def test_build_cluster_context_returns_data_division_fields():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    result = build_cluster_context("PAYROLL-CALC")
    fields = result["data"]["data_division_fields"]
    assert "WS-AMT" in fields


def test_build_cluster_context_no_cache_returns_error():
    result = build_cluster_context("NONEXISTENT-XYZ-99")
    assert result["status"] == "error"
    assert result["data"] is None


def test_validate_cluster_output_accepts_valid_clusters():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    result = validate_cluster_output("PAYROLL-CALC", _VALID_CLUSTERS)
    assert result["status"] == "ok"
    assert result["data"]["program_name"] == "PAYROLL-CALC"
    assert len(result["data"]["clusters"]) == 2


def test_validate_cluster_output_flags_unknown_paragraph_reference():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    bad_clusters = [
        {"name": "Bad Cluster", "paragraphs": ["NONEXISTENT-PARA"], "description": "..."}
    ]
    result = validate_cluster_output("PAYROLL-CALC", bad_clusters)
    assert result["status"] == "warning"
    codes = [f["code"] for f in result["flags"]]
    assert "INVALID_CLUSTER_DATA" in codes


def test_validate_cluster_output_flags_empty_cluster_name():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    bad_clusters = [
        {"name": "", "paragraphs": ["MAIN-PARA"], "description": "..."}
    ]
    result = validate_cluster_output("PAYROLL-CALC", bad_clusters)
    assert result["status"] == "warning"
    codes = [f["code"] for f in result["flags"]]
    assert "INVALID_CLUSTER_DATA" in codes


def test_validate_cluster_output_stores_in_session_cache():
    from cobol_parser_mcp.cobol_parser import _SESSION_CACHE
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    validate_cluster_output("PAYROLL-CALC", _VALID_CLUSTERS)
    assert "clusters" in _SESSION_CACHE["PAYROLL-CALC"]
    assert _SESSION_CACHE["PAYROLL-CALC"]["clusters"] == _VALID_CLUSTERS


def test_build_cluster_context_never_raises():
    try:
        result = build_cluster_context("TOTALLY-MISSING-XYZ")
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"build_cluster_context raised: {e}")


def test_validate_cluster_output_never_raises():
    try:
        result = validate_cluster_output("TOTALLY-MISSING-XYZ", [])
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"validate_cluster_output raised: {e}")


@pytest.mark.skipif(not BLACKJACK_SRC.exists(), reason="BlackJack corpus not available")
def test_blackjack_corpus_build_cluster_context_all_ok():
    for cob_file in BLACKJACK_SRC.glob("*.cob"):
        program_name = cob_file.stem.upper()
        cobol_parser.parse_module(program_name, str(cob_file))
        result = build_cluster_context(program_name)
        assert result["status"] == "ok", (
            f"build_cluster_context failed for {cob_file.name}: {result.get('message', '')}"
        )
        assert len(result["data"]["paragraph_names"]) > 0, (
            f"No paragraphs in {cob_file.name}"
        )
