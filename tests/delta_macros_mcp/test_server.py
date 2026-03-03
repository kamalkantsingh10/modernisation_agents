from delta_macros_mcp import result, server


def test_make_result_defaults():
    r = result.make_result()
    assert r == {"status": "ok", "data": None, "flags": [], "message": ""}


def test_make_error():
    r = result.make_error("something went wrong")
    assert r["status"] == "error"
    assert r["message"] == "something went wrong"


def test_make_warning():
    r = result.make_warning(data=[1], message="warn", flags=["f"])
    assert r["status"] == "warning"


def test_server_module_importable():
    assert server.mcp is not None
    assert server.mcp.name == "delta-macros-mcp"
