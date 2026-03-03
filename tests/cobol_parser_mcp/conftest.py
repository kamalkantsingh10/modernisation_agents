import pytest


@pytest.fixture(autouse=True)
def clear_session_cache():
    from cobol_parser_mcp import cobol_parser
    cobol_parser._SESSION_CACHE.clear()
    yield
    cobol_parser._SESSION_CACHE.clear()
