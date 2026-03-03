from pathlib import Path

import pytest

from delta_macros_mcp import macro_library

FIXTURES_PATH = Path(__file__).parent / "fixtures" / "macros"


# ── Story 2.1: get_macro ──────────────────────────────────────────────────────

def test_get_macro_known_returns_structured_result():
    r = macro_library.get_macro("DLTM-ACCT-LOCK", FIXTURES_PATH)
    assert r["status"] == "ok"
    assert r["data"]["name"] == "DLTM-ACCT-LOCK"
    assert r["data"]["purpose"]
    assert isinstance(r["data"]["parameters"], list)
    assert r["data"]["returns"]


def test_get_macro_unknown_returns_warning_not_error():
    r = macro_library.get_macro("DLTM-DOES-NOT-EXIST", FIXTURES_PATH)
    assert r["status"] == "warning"
    assert r["data"] is None
    assert r["flags"][0]["code"] == "UNKNOWN_MACRO"
    assert r["flags"][0]["location"] == "DLTM-DOES-NOT-EXIST"


def test_get_macro_never_raises():
    try:
        macro_library.get_macro("", FIXTURES_PATH)
        macro_library.get_macro("../../../etc/passwd", FIXTURES_PATH)
        macro_library.get_macro("DLTM-DOES-NOT-EXIST", FIXTURES_PATH)
    except Exception as e:
        pytest.fail(f"get_macro raised: {e}")


def test_get_macro_case_insensitive_filename(tmp_path):
    # Write a file in uppercase; look it up by lowercase name
    (tmp_path / "DLTM-TEST.md").write_text(
        "## Name\n\n`DLTM-TEST`\n\n## Purpose\n\nTest macro\n\n## Parameters\n\n"
        "| Parameter | Type | Description |\n|---|---|---|\n\n## Returns\n\nNothing\n\n"
        "## Category\n\nTesting\n\n## Example Usage\n\n```cobol\n```\n\n## Notes\n\n",
        encoding="utf-8",
    )
    r = macro_library.get_macro("dltm-test", tmp_path)
    assert r["status"] == "ok"
    assert r["data"]["name"] == "DLTM-TEST"


# ── Story 2.1: search_macros ──────────────────────────────────────────────────

def test_search_macros_matches_name():
    r = macro_library.search_macros("ACCT", FIXTURES_PATH)
    assert r["status"] == "ok"
    names = [m["name"] for m in r["data"]]
    assert "DLTM-ACCT-LOCK" in names
    assert "DLTM-ACCT-UNLOCK" in names


def test_search_macros_matches_purpose():
    # "audit entry" appears in DLTM-AUDIT-LOG purpose
    r = macro_library.search_macros("audit entry", FIXTURES_PATH)
    assert r["status"] == "ok"
    names = [m["name"] for m in r["data"]]
    assert "DLTM-AUDIT-LOG" in names


def test_search_macros_no_match():
    r = macro_library.search_macros("ZZZNOMATCH", FIXTURES_PATH)
    assert r["status"] == "ok"
    assert r["data"] == []


def test_search_macros_case_insensitive():
    r = macro_library.search_macros("acct", FIXTURES_PATH)
    assert r["status"] == "ok"
    names = [m["name"] for m in r["data"]]
    assert "DLTM-ACCT-LOCK" in names


# ── Story 2.1: list_categories ────────────────────────────────────────────────

def test_list_categories_returns_unique_sorted():
    r = macro_library.list_categories(FIXTURES_PATH)
    assert r["status"] == "ok"
    data = r["data"]
    assert "Account Management" in data
    assert "Auditing" in data
    assert data == sorted(set(data)), "categories should be sorted and unique"


def test_list_categories_empty_dir(tmp_path):
    r = macro_library.list_categories(tmp_path)
    assert r["status"] == "ok"
    assert r["data"] == []


# ── Story 2.2: add_macro ──────────────────────────────────────────────────────

def test_add_macro_creates_new_file(tmp_path):
    r = macro_library.add_macro("DLTM-NEW-MACRO", "Does X", [], "Sets Y", "Testing", tmp_path)
    assert r["status"] == "ok"
    assert (tmp_path / "DLTM-NEW-MACRO.md").exists()


def test_add_macro_immediately_retrievable(tmp_path):
    macro_library.add_macro("DLTM-NEW-MACRO", "Does X", [], "Sets Y", "Testing", tmp_path)
    r = macro_library.get_macro("DLTM-NEW-MACRO", tmp_path)
    assert r["status"] == "ok"
    assert r["data"]["purpose"] == "Does X"


def test_add_macro_updates_existing_no_duplicate(tmp_path):
    macro_library.add_macro("DLTM-DUP", "Purpose 1", [], "Returns 1", "", tmp_path)
    macro_library.add_macro("DLTM-DUP", "Purpose 2", [], "Returns 2", "", tmp_path)
    md_files = list(tmp_path.glob("*.md"))
    assert len(md_files) == 1
    r = macro_library.get_macro("DLTM-DUP", tmp_path)
    assert r["status"] == "ok"
    assert r["data"]["purpose"] == "Purpose 2"


def test_add_macro_invalid_name_empty(tmp_path):
    r = macro_library.add_macro("", "Purpose", [], "Returns", "", tmp_path)
    assert r["status"] == "error"
    assert "invalid" in r["message"].lower() or "name" in r["message"].lower()


def test_add_macro_invalid_name_whitespace(tmp_path):
    r = macro_library.add_macro("   ", "Purpose", [], "Returns", "", tmp_path)
    assert r["status"] == "error"


def test_add_macro_with_parameters_table(tmp_path):
    params = [{"name": "ACCT-ID", "type": "TEXT", "description": "Account ID"}]
    macro_library.add_macro("DLTM-WITH-PARAMS", "Does Z", params, "Returns Z", "", tmp_path)
    content = (tmp_path / "DLTM-WITH-PARAMS.md").read_text(encoding="utf-8")
    assert "ACCT-ID" in content
    assert "TEXT" in content


def test_add_macro_with_empty_parameters(tmp_path):
    r = macro_library.add_macro("DLTM-NO-PARAMS", "Minimal", [], "Nothing", "", tmp_path)
    assert r["status"] == "ok"
    content = (tmp_path / "DLTM-NO-PARAMS.md").read_text(encoding="utf-8")
    assert "| Parameter | Type | Description |" in content


def test_add_macro_never_raises(tmp_path):
    try:
        macro_library.add_macro("", "p", [], "r", "", tmp_path)
        macro_library.add_macro("DLTM-OK", "p", [], "r", "", tmp_path)
        macro_library.add_macro("DLTM-OK", "", [], "", "", tmp_path)
    except Exception as e:
        pytest.fail(f"add_macro raised: {e}")


def test_add_macro_category_stored_and_retrievable(tmp_path):
    macro_library.add_macro("DLTM-CATTEST", "Cat test", [], "None", "Foo", tmp_path)
    r = macro_library.list_categories(tmp_path)
    assert r["status"] == "ok"
    assert "Foo" in r["data"]
