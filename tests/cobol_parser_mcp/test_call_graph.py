from pathlib import Path

import pytest

from cobol_parser_mcp import cobol_parser
from cobol_parser_mcp.call_graph import build_call_graph, _expand_perform_thru

FIXTURES = Path(__file__).parent / "fixtures"


def test_extract_call_graph_returns_nodes_and_edges():
    cobol_parser.parse_module("PAYROLL-CALC", str(FIXTURES / "minimal.cbl"))
    result = build_call_graph("PAYROLL-CALC")
    assert result["status"] == "ok"
    data = result["data"]
    assert data["program_name"] == "PAYROLL-CALC"
    assert "nodes" in data
    assert "edges" in data
    assert "MAIN-PARA" in data["nodes"]
    assert "CALC-PARA" in data["nodes"]
    edges = data["edges"]
    assert any(e["from"] == "MAIN-PARA" and e["to"] == "CALC-PARA" for e in edges)


def test_extract_call_graph_expands_perform_thru_range():
    cobol_parser.parse_module("THRU-TEST", str(FIXTURES / "perform_thru.cbl"))
    result = build_call_graph("THRU-TEST")
    assert result["status"] == "ok"
    edges = result["data"]["edges"]
    targets_from_main = [e["to"] for e in edges if e["from"] == "MAIN-PARA"]
    assert "STEP-A" in targets_from_main
    assert "STEP-B" in targets_from_main
    assert "STEP-C" in targets_from_main


def test_extract_call_graph_no_cache_returns_error():
    result = build_call_graph("NONEXISTENT-MODULE-XYZ")
    assert result["status"] == "error"
    assert result["data"] is None


def test_extract_call_graph_never_raises():
    try:
        result = build_call_graph("TOTALLY-FAKE-XYZ")
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"build_call_graph raised an exception: {e}")


def test_expand_perform_thru_returns_inclusive_range():
    paragraphs = [
        {"name": "PARA-A", "line": 10},
        {"name": "PARA-B", "line": 20},
        {"name": "PARA-C", "line": 30},
        {"name": "PARA-D", "line": 40},
    ]
    result = _expand_perform_thru(paragraphs, "PARA-A", "PARA-C")
    assert result == ["PARA-A", "PARA-B", "PARA-C"]


def test_expand_perform_thru_single_paragraph():
    paragraphs = [{"name": "PARA-A", "line": 10}, {"name": "PARA-B", "line": 20}]
    result = _expand_perform_thru(paragraphs, "PARA-A", "PARA-A")
    assert result == ["PARA-A"]


def test_expand_perform_thru_unknown_paragraph_returns_empty():
    paragraphs = [{"name": "PARA-A", "line": 10}]
    result = _expand_perform_thru(paragraphs, "UNKNOWN", "PARA-A")
    assert result == []
