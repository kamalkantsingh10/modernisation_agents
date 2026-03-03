# Story 2.2: delta-macros-mcp — Macro Ingestion

Status: review

## Story

As an **analyst**,
I want to add a new macro definition to the library via `add_macro` without restarting the pipeline,
So that I can close institutional knowledge gaps discovered during analysis in real time.

## Acceptance Criteria

1. **Given** `delta-macros-mcp` is running **When** `add_macro` is called with a macro name, purpose, parameters, return value, and optional category **Then** a new markdown file is created at `<macro_library_path>/<MACRO-NAME>.md` following the macro template format.
2. **And** the new macro is immediately retrievable via `get_macro` without any server restart (FR31).
3. **When** `add_macro` is called with a name that already exists **Then** the existing file is updated with the new content and the tool returns `{"status": "ok", ...}` — no duplicate is created.
4. **When** `add_macro` is called with an invalid or empty macro name **Then** the tool returns `{"status": "error", ...}` with a clear validation message.
5. **And** all macro files remain stored locally — no external sync (NFR9).

## Tasks / Subtasks

- [x] Task 1: Extend `mcp-servers/delta_macros_mcp/macro_library.py` with `add_macro` (AC: 1, 2, 3, 4, 5)
  - [x] Implement `_validate_macro_name(name: str) -> str | None` private helper
  - [x] Implement `_render_macro_file(name, purpose, parameters, returns, category) -> str`
  - [x] Implement `add_macro(name, purpose, parameters, returns, category, library_path) -> dict`

- [x] Task 2: Add `add_macro` MCP tool to `server.py` (AC: 1, 2, 3, 4, 5)
  - [x] Add `@mcp.tool() def add_macro(macro_name, purpose, parameters, returns, category="") -> dict`

- [x] Task 3: Extend tests in `tests/delta_macros_mcp/test_macro_library.py` (AC: 1, 2, 3, 4, 5)
  - [x] `test_add_macro_creates_new_file`
  - [x] `test_add_macro_immediately_retrievable`
  - [x] `test_add_macro_updates_existing_no_duplicate`
  - [x] `test_add_macro_invalid_name_empty`
  - [x] `test_add_macro_invalid_name_whitespace`
  - [x] `test_add_macro_with_parameters_table`
  - [x] `test_add_macro_with_empty_parameters`
  - [x] `test_add_macro_never_raises`
  - [x] `test_add_macro_category_stored_and_retrievable`

## Dev Notes

### Architecture Guardrails

- **Depends on Story 2.1** — `macro_library.py` must already exist with `get_macro`, `search_macros`, `list_categories`, `_parse_macro_file`, and `_find_macro_file`. This story extends that module. Do not rewrite from scratch; add to it.
- **Poetry monorepo** — same as Story 2.1. Package `delta_macros_mcp`, run via `poetry run python -m delta_macros_mcp.server`.
- **FR31: No server restart required** — because there is no in-memory cache in `macro_library.py` (per Story 2.1 design), `add_macro` writes to disk and `get_macro` reads from disk on every call. Immediate retrievability is guaranteed by design — no additional work needed.
- **`result.py` already exists** — use `make_result()`, `make_error()`. Never construct result dicts inline.
- **Overwrite = update, not duplicate** — `add_macro` with an existing name overwrites the file. This satisfies AC3. SQLite upsert patterns do not apply here (no DB); simple file write suffices.
- **Atomic write** — use `path.write_text(content, encoding="utf-8")`. This is atomic enough for a single-developer local tool. No temp-file-then-rename needed at this scale.
- **Filename normalisation** — always uppercase the macro name for the filename: `name.upper() + ".md"`. This ensures consistency with naming patterns. Example: `add_macro("dltm-acct-lock", ...)` → writes `DLTM-ACCT-LOCK.md`.
- **`parameters` type in tool signature** — FastMCP receives lists of dicts from agent tool calls. Declare as `list` (not `list[dict]`) in the MCP tool signature for broadest compatibility. No validation of parameter structure required — store what is given.
- **Macro template format consistency** — the written markdown file must be parseable by `_parse_macro_file` from Story 2.1 so that `get_macro` can read back what `add_macro` writes. Ensure the section headings match exactly: `## Name`, `## Purpose`, `## Parameters`, `## Returns`, `## Category`, `## Example Usage`, `## Notes`.
- **No external sync** (NFR9) — `add_macro` writes only to local `library_path`. No network calls, no external services.
- **Library path must exist** — `add_macro` should validate `library_path` is an existing directory before writing. If not, return `make_error` rather than allowing `FileNotFoundError` to propagate.
- **Test isolation** — all write tests MUST use pytest `tmp_path` fixture. Never write to `blackjack/macros/` in tests, as that directory is tracked by git and contains engagement data.

### Project Structure Notes

- Modify: `mcp-servers/delta_macros_mcp/macro_library.py` (add `_validate_macro_name`, `_render_macro_file`, `add_macro`)
- Modify: `mcp-servers/delta_macros_mcp/server.py` (add `add_macro` MCP tool)
- Modify: `tests/delta_macros_mcp/test_macro_library.py` (extend with `add_macro` tests)
- No new files required beyond what Story 2.1 established

### References

- `add_macro` tool name and behaviour [Source: docs/planning-artifacts/epics.md#Story-2.2]
- FR31: add new macro without restarting pipeline [Source: docs/planning-artifacts/epics.md#Story-2.2]
- NFR9: data locality — local only [Source: docs/planning-artifacts/architecture.md#Authentication-Security]
- Result dict format [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- `make_result()` / `make_error()` usage [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- Tool naming: verb-first snake_case, exact PRD names [Source: docs/planning-artifacts/architecture.md#Naming-Patterns]
- File naming: SCREAMING-SNAKE-CASE.md [Source: docs/planning-artifacts/architecture.md#Naming-Patterns]
- Poetry monorepo pattern [Source: docs/implementation-artifacts/1-1-project-scaffolding-and-shared-infrastructure.md#Dev-Notes]
- No in-memory cache — reads from disk each call [Source: docs/implementation-artifacts/2-1-delta-macros-mcp-macro-lookup.md#Dev-Notes]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- Extended `macro_library.py` with `_validate_macro_name`, `_render_macro_file`, `add_macro` (Story 2.2 additions co-located in same file as 2.1 domain functions)
- `add_macro` MCP tool added to `server.py` (same `_resolve_library_path()` pattern)
- 9 `add_macro` tests added to `test_macro_library.py` — all use `tmp_path`, never touch fixtures or `blackjack/macros/`
- All 61 project tests passing

### File List

- `mcp-servers/delta_macros_mcp/macro_library.py` (modified — Story 2.2 additions)
- `mcp-servers/delta_macros_mcp/server.py` (modified — `add_macro` tool)
- `tests/delta_macros_mcp/test_macro_library.py` (modified — 9 new tests)
