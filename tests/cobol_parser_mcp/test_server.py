from cobol_parser_mcp import result, server


def test_make_result_defaults():
    r = result.make_result()
    assert r == {"status": "ok", "data": None, "flags": [], "message": ""}


def test_make_result_with_data():
    r = result.make_result(data={"key": "value"}, message="done")
    assert r["status"] == "ok"
    assert r["data"] == {"key": "value"}
    assert r["message"] == "done"


def test_make_error():
    r = result.make_error("something went wrong")
    assert r["status"] == "error"
    assert r["message"] == "something went wrong"
    assert r["data"] is None


def test_make_warning():
    r = result.make_warning(data=[1, 2], message="partial", flags=["warn"])
    assert r["status"] == "warning"
    assert r["data"] == [1, 2]
    assert r["flags"] == ["warn"]


def test_make_result_flags_default_to_empty_list():
    r = result.make_result()
    assert r["flags"] == []


def test_server_module_importable():
    assert server.mcp is not None
    assert server.mcp.name == "cobol-parser-mcp"
