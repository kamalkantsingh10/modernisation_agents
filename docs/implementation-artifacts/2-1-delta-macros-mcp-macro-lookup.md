# Story 2.1: delta-macros-mcp — Macro Lookup

Status: review

## Story

As an **analyst/agent**,
I want to look up, search, and list Delta macro definitions via `get_macro`, `search_macros`, and `list_categories`,
So that any pipeline agent can resolve client-specific macro references during COBOL analysis.

## Acceptance Criteria

1. **Given** `delta-macros-mcp` is running and `macro_library_path` in `config.yaml` points to a directory of macro `.md` files **When** `get_macro` is called with a known macro name (e.g. `DLTM-ACCT-LOCK`) **Then** the macro's purpose, parameters, and return value are returned in the structured result dict within 1 second (NFR4).
2. **When** `get_macro` is called with an unknown macro name **Then** the tool returns `{"status": "warning", "data": null, "flags": [{"code": "UNKNOWN_MACRO", "message": "...", "location": "<macro_name>"}], "message": "Macro not found"}` — never an error or exception (NFR11).
3. **When** `search_macros` is called with a keyword **Then** all matching macro definitions are returned (matched against macro name and description/purpose text, case-insensitive).
4. **When** `list_categories` is called **Then** all macro category groupings present in the library are returned as a deduplicated list.
5. **And** the macro library directory contents are never transmitted outside the local environment (NFR9) — all operations are pure local filesystem reads.

## Tasks / Subtasks

- [x] Task 1: Create test fixture macro files (AC: 1, 3, 4)
  - [x] Create `tests/delta_macros_mcp/fixtures/macros/` directory with `__init__.py`
  - [x] Create `tests/delta_macros_mcp/fixtures/macros/DLTM-ACCT-LOCK.md` — macro with category "Account Management", purpose, parameters table, returns section
  - [x] Create `tests/delta_macros_mcp/fixtures/macros/DLTM-ACCT-UNLOCK.md` — second "Account Management" macro for category dedup testing
  - [x] Create `tests/delta_macros_mcp/fixtures/macros/DLTM-AUDIT-LOG.md` — macro with category "Auditing" for multi-category listing
  - [x] Update `templates/macro-template.md` to include a `## Category` section (after `## Returns`) so macro files have a canonical location for category metadata

- [x] Task 2: Create `mcp-servers/delta_macros_mcp/macro_library.py` (AC: 1, 2, 3, 4, 5)
  - [x] Implement `_parse_macro_file(path: Path) -> dict` private helper:
    - Reads .md file, extracts sections by `## Heading` markers
    - Returns dict with keys: `name`, `purpose`, `parameters` (list of `{"name", "type", "description"}` dicts parsed from markdown table), `returns`, `category` (empty string if `## Category` section absent), `example_usage`, `notes`
    - Never raises — returns `None` on parse error
  - [x] Implement `_find_macro_file(name: str, library_path: Path) -> Path | None` — looks for `<library_path>/<name>.md` then `<library_path>/<name.upper()>.md`; returns None if not found
  - [x] Implement `get_macro(name: str, library_path: Path) -> dict`:
    - Calls `_find_macro_file`; if not found returns `make_warning(data=None, message="Macro not found", flags=[{"code": "UNKNOWN_MACRO", "message": f"No macro definition found for '{name}'", "location": name}])`
    - If found, parses and returns `make_result(data={...macro dict...})`
  - [x] Implement `search_macros(keyword: str, library_path: Path) -> dict`:
    - Scans all `.md` files in `library_path` (non-recursive)
    - For each file, calls `_parse_macro_file`; matches if keyword appears in `name` or `purpose` (case-insensitive)
    - Returns `make_result(data=[{name, purpose, category},...])` — lightweight summaries, not full parse
  - [x] Implement `list_categories(library_path: Path) -> dict`:
    - Scans all `.md` files in `library_path`
    - Collects `category` from each parsed file; deduplicates and sorts
    - Skips files with empty/missing category silently
    - Returns `make_result(data=[...sorted unique categories...])`
  - [x] All functions accept `library_path: Path` as explicit argument (not loading config internally) to enable testability without config.yaml

- [x] Task 3: Add MCP tools to `server.py` (AC: 1, 2, 3, 4, 5)
  - [x] Import `macro_library` and `load_config` at top of `server.py`
  - [x] Add `@mcp.tool() def get_macro(macro_name: str) -> dict:` — resolves `library_path` from `load_config()["macro_library_path"]`, delegates to `macro_library.get_macro(macro_name, library_path)`, wraps in try/except returning `make_error()` on unexpected exceptions
  - [x] Add `@mcp.tool() def search_macros(keyword: str) -> dict:` — same pattern
  - [x] Add `@mcp.tool() def list_categories() -> dict:` — same pattern
  - [x] `macro_library_path` from config is resolved relative to project root using `_find_project_root()` from `config.py` (re-use the same discovery logic); `library_path = _find_project_root() / config["macro_library_path"]`
  - [x] Each tool validates `library_path` exists; if not: `make_error(f"Macro library not found: {library_path}")`
  - [x] Log each tool call with `logger.info("get_macro called: macro_name=%s", macro_name)`

- [x] Task 4: Write tests in `tests/delta_macros_mcp/test_macro_library.py` (AC: 1, 2, 3, 4, 5)
  - [x] Define `FIXTURES_PATH = Path(__file__).parent / "fixtures" / "macros"` at top of test file
  - [x] `test_get_macro_known_returns_structured_result` — call `get_macro("DLTM-ACCT-LOCK", FIXTURES_PATH)`; assert `status == "ok"`, `data["name"] == "DLTM-ACCT-LOCK"`, `data["purpose"]` is non-empty, `data["parameters"]` is a list, `data["returns"]` is non-empty
  - [x] `test_get_macro_unknown_returns_warning_not_error` — call `get_macro("DLTM-DOES-NOT-EXIST", FIXTURES_PATH)`; assert `status == "warning"`, `data is None`, `flags[0]["code"] == "UNKNOWN_MACRO"`, `flags[0]["location"] == "DLTM-DOES-NOT-EXIST"`
  - [x] `test_get_macro_never_raises` — wrap in try/except and assert no exception raised for any input
  - [x] `test_search_macros_matches_name` — keyword `"ACCT"` against fixtures; assert results contain both ACCT macros
  - [x] `test_search_macros_matches_purpose` — keyword present in purpose text of one fixture; assert that macro appears in results
  - [x] `test_search_macros_no_match` — keyword `"ZZZNOMATCH"` → `data == []`, `status == "ok"`
  - [x] `test_search_macros_case_insensitive` — lowercase keyword matches uppercase name
  - [x] `test_list_categories_returns_unique_sorted` — call `list_categories(FIXTURES_PATH)`; assert `status == "ok"`, result contains `"Account Management"` and `"Auditing"`, no duplicates, sorted alphabetically
  - [x] `test_list_categories_empty_dir` — call with `tmp_path` (empty dir via pytest fixture); assert `data == []`, no exception

## Dev Notes

### Architecture Guardrails

- **Poetry monorepo** — not uv per server. The actual project uses a root `pyproject.toml`. Package is `delta_macros_mcp` (snake_case). Run via `poetry run python -m delta_macros_mcp.server`. Architecture doc says uv but Story 1.1 corrected this — Poetry monorepo is the actual pattern.
- **Domain logic separation** — `macro_library.py` contains all business logic. `server.py` is thin MCP tool wrappers only. Never put parsing or filesystem logic inside `@mcp.tool()` functions directly.
- **`result.py` already exists** — use `make_result()`, `make_error()`, `make_warning()` from `delta_macros_mcp.result`. Never construct result dicts inline.
- **`config.py` already exists** — use `load_config()` to get config dict; use `_find_project_root()` (or equivalent) to resolve relative paths.
- **UNKNOWN_MACRO** is a `warning`, not an `error` — the pipeline continues. Never return `status: "error"` for a missing macro. [Source: docs/planning-artifacts/epics.md#Story-2.1]
- **NFR4: macro lookup < 1 second** — this is achievable with simple filesystem reads; no indexing or caching required at this scale.
- **NFR9: data locality** — all operations must be pure local filesystem reads. No HTTP calls, no external service, no subprocess spawning.
- **Macro file naming** — macro files are `SCREAMING-SNAKE-CASE.md` e.g. `DLTM-ACCT-LOCK.md`. Case-insensitive lookup: try exact filename first, then uppercase. [Source: docs/planning-artifacts/architecture.md#Naming-Patterns]
- **`macro_library_path` is relative** to project root — resolve it via `_find_project_root() / config["macro_library_path"]`. For tests, pass `FIXTURES_PATH` directly to domain functions to avoid any config dependency.
- **`## Category` section** — the existing `templates/macro-template.md` does not have a Category section. Add `## Category\n\n<category name>` after `## Returns` in the template. Fixture files must also include this section. Existing macro files without the section should return `category: ""` without error.
- **Parameter table parsing** — the `## Parameters` section contains a standard markdown table. Skip the header row (row 0) and separator row (row 1). Each subsequent row produces `{"name": col0.strip(), "type": col1.strip(), "description": col2.strip()}`. If the section is absent or the table is malformed, return `parameters: []`.
- **Do NOT cache the macro library** — files may change (via `add_macro` in Story 2.2). Each tool call reads from disk. At this scale (dozens of .md files) this is fast enough for NFR4.
- **Fixture file structure** — use existing fixtures at `tests/delta_macros_mcp/fixtures/macros/` path (create if not present). The architecture specifies `DLTM-EXAMPLE.md` but actual fixture naming should match what tests use — use `DLTM-ACCT-LOCK.md`, `DLTM-ACCT-UNLOCK.md`, `DLTM-AUDIT-LOG.md` as test fixtures that reflect the BlackJack/COBOL domain.

### Project Structure Notes

- New file: `mcp-servers/delta_macros_mcp/macro_library.py` (domain logic)
- Modify: `mcp-servers/delta_macros_mcp/server.py` (add 3 MCP tools)
- Modify: `templates/macro-template.md` (add `## Category` section)
- New file: `tests/delta_macros_mcp/test_macro_library.py`
- New files: `tests/delta_macros_mcp/fixtures/macros/DLTM-ACCT-LOCK.md` etc.
- `result.py` and `config.py` already exist — do NOT modify them

### References

- Tool names (`get_macro`, `search_macros`, `list_categories`) [Source: docs/planning-artifacts/epics.md#Story-2.1]
- Result dict format `{"status", "data", "flags", "message"}` [Source: docs/planning-artifacts/architecture.md#API-Communication-Patterns]
- `make_result()` / `make_warning()` usage [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- `UNKNOWN_MACRO` flag code [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- NFR4 (< 1s macro lookup) [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- NFR9 (data locality) [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- Macro file location: `<macro_library_path>/<MACRO-NAME>.md` [Source: docs/planning-artifacts/architecture.md#Naming-Patterns]
- Tool naming: verb-first snake_case, exact PRD names [Source: docs/planning-artifacts/architecture.md#Naming-Patterns]
- Poetry monorepo pattern [Source: docs/implementation-artifacts/1-1-project-scaffolding-and-shared-infrastructure.md#Dev-Notes]
- Package: `delta_macros_mcp` snake_case [Source: docs/implementation-artifacts/1-1-project-scaffolding-and-shared-infrastructure.md#File-List]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- `macro_library.py` created with `_parse_macro_file`, `_find_macro_file`, `get_macro`, `search_macros`, `list_categories`
- `server.py` updated with 3 MCP tools (`get_macro`, `search_macros`, `list_categories`) using `_resolve_library_path()` helper
- `templates/macro-template.md` updated with `## Category` section after `## Returns`
- 3 fixture macro files created in `tests/delta_macros_mcp/fixtures/macros/`
- 19 tests in `test_macro_library.py` (10 for 2.1 scope); all 61 project tests passing

### File List

- `mcp-servers/delta_macros_mcp/macro_library.py` (new)
- `mcp-servers/delta_macros_mcp/server.py` (modified)
- `templates/macro-template.md` (modified)
- `tests/delta_macros_mcp/fixtures/__init__.py` (new)
- `tests/delta_macros_mcp/fixtures/macros/__init__.py` (new)
- `tests/delta_macros_mcp/fixtures/macros/DLTM-ACCT-LOCK.md` (new)
- `tests/delta_macros_mcp/fixtures/macros/DLTM-ACCT-UNLOCK.md` (new)
- `tests/delta_macros_mcp/fixtures/macros/DLTM-AUDIT-LOG.md` (new)
- `tests/delta_macros_mcp/test_macro_library.py` (new)
