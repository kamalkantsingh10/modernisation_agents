# Story 3.1: cobol-parser-mcp — Core Module Parsing & Call Graph

Status: review

## Story

As an **analyst**,
I want to parse any COBOL module and receive its paragraph call graph and external references,
So that I have the structural map of the program as the foundation for all further analysis.

## Acceptance Criteria

1. **Given** `cobol-parser-mcp` is running and a `.cbl` / `.cob` source file path is provided **When** `parse_module` is called with `program_name` and `source_path` **Then** the tool returns: PROGRAM-ID verbatim, all paragraphs with line numbers, all COPY statement references, all CALL statement targets, all EXEC SQL block locations, all EXEC CICS block locations, and any Delta macro invocations found in the source (FR1, FR4).
2. **And** `program_name` is stored and returned as the COBOL PROGRAM-ID verbatim — uppercase with hyphens, e.g. `"PAYROLL-CALC"` — regardless of what was passed in the argument (FR4).
3. **And** the tool completes within 30 seconds for any module up to 5,000 lines (NFR2).
4. **And** parsed module data is stored in a server-level session cache keyed by `program_name`, available to subsequent tool calls in the same server session.
5. **When** `extract_call_graph` is called with `program_name` after `parse_module` **Then** it returns a directed graph of PERFORM relationships between paragraphs as nodes and edges (FR1).
6. **And** PERFORM THRU ranges are fully expanded: each paragraph between `thru_start` and `thru_end` (inclusive, in source order) appears as an explicit edge (FR1).
7. **When** the source file contains IBM Enterprise COBOL or COBOL-85 syntax **Then** it is parsed correctly without error (FR35).
8. **When** a COPY statement references a copybook **Then** the copybook name is recorded as an external dependency in `copy_refs` (FR38).
9. **When** any tool call fails — file not found, parse error, or program_name not in session cache — **Then** it returns `{"status": "error", "flags": [...], "data": null, "message": "..."}` — never raises (NFR11).
10. **And** no source code content is transmitted outside the local environment (NFR6).

## Tasks / Subtasks

- [x] Task 1: Create `cobol_parser_mcp` package skeleton (AC: all)
  - [x] Create `mcp-servers/cobol_parser_mcp/__init__.py` (empty)
  - [x] Create `mcp-servers/cobol_parser_mcp/result.py` — copy `make_result()`, `make_error()`, `make_warning()` pattern from `specdb_mcp/result.py` or `delta_macros_mcp/result.py` (same dict structure, same helpers)
  - [x] Create `mcp-servers/cobol_parser_mcp/config.py` — load `config.yaml` from project root via `BMAD_PROJECT_ROOT` env var or relative path; expose `get_config() -> dict`

- [x] Task 2: Implement `cobol_parser.py` — core parsing logic (AC: 1, 2, 3, 4, 7, 8, 9, 10)
  - [x] Define `_SESSION_CACHE: dict[str, dict] = {}` — module-level dict storing parse results keyed by `program_name`
  - [x] Implement `_extract_program_id(source: str) -> str` — regex on `PROGRAM-ID.` line; return verbatim COBOL value (uppercase, hyphens preserved); raise `ValueError` if not found
  - [x] Implement `_find_paragraphs(source: str) -> list[dict]` — detect paragraph labels at column 8–11 (label followed by period on its own); return `[{"name": "PARA-NAME", "line": 45}, ...]`
  - [x] Implement `_extract_copy_refs(source: str) -> list[str]` — scan for `COPY <name>` patterns; return list of copybook names (uppercase)
  - [x] Implement `_extract_call_targets(source: str) -> list[str]` — scan for `CALL '<target>'` and `CALL "<target>"` patterns; return list of target names
  - [x] Implement `_find_delta_macros(source: str) -> list[dict]` — scan for Delta macro invocations (DLTM- prefix pattern); return `[{"name": "DLTM-ACCT-LOCK", "line": 78}, ...]`
  - [x] Implement `parse_module(program_name: str, source_path: str) -> dict` — orchestrates all helpers; stores result in `_SESSION_CACHE[program_name]`; wraps in try/except; returns `make_result(data={...})`

- [x] Task 3: Implement `dialect_handler.py` — EXEC SQL, EXEC CICS, dialect detection (AC: 1, 7, 8, 9)
  - [x] Implement `find_exec_sql_blocks(source: str) -> list[dict]` — find `EXEC SQL ... END-EXEC` spans; return `[{"location": "para-name", "line_start": 123, "line_end": 128}, ...]`
  - [x] Implement `find_exec_cics_blocks(source: str) -> list[dict]` — find `EXEC CICS ... END-EXEC` spans; same return shape
  - [x] Implement `detect_dialect(source: str) -> str` — return `"IBM_ENTERPRISE"`, `"COBOL_85"`, or `"UNKNOWN"` based on source markers

- [x] Task 4: Implement `call_graph.py` — PERFORM graph builder (AC: 5, 6, 9)
  - [x] Implement `_find_perform_statements(source: str, paragraphs: list[dict]) -> list[dict]` — extract all `PERFORM <name>`, `PERFORM <name> THRU <name>`, `PERFORM <name> UNTIL`, `PERFORM VARYING` statements with their enclosing paragraph context
  - [x] Implement `_expand_perform_thru(paragraphs: list[dict], thru_start: str, thru_end: str) -> list[str]` — return all paragraph names between thru_start and thru_end inclusive, in source order
  - [x] Implement `build_call_graph(program_name: str) -> dict` — reads `_SESSION_CACHE[program_name]`; returns `make_result(data={"program_name": ..., "nodes": [...], "edges": [{"from": ..., "to": ...}, ...]})`; returns `make_error` if program_name not in cache

- [x] Task 5: Add MCP tools to `server.py` (AC: all)
  - [x] Create `mcp-servers/cobol_parser_mcp/server.py` with FastMCP app (`mcp = FastMCP("cobol-parser-mcp")`)
  - [x] Add `@mcp.tool() def parse_module(program_name: str, source_path: str) -> dict` — thin wrapper calling `cobol_parser.parse_module()`; docstring becomes MCP tool description
  - [x] Add `@mcp.tool() def extract_call_graph(program_name: str) -> dict` — thin wrapper calling `call_graph.build_call_graph()`
  - [x] Add `if __name__ == "__main__": mcp.run()` block

- [x] Task 6: Register server in IDE config files (AC: all)
  - [x] Add `cobol-parser-mcp` entry to `.claude/mcp.json`: `{"command": "poetry", "args": ["run", "python", "-m", "cobol_parser_mcp.server"], "env": {}}`
  - [x] Add same entry to `.vscode/mcp.json`

- [x] Task 7: Add `lark` dependency to monorepo (AC: architecture prerequisite)
  - [x] Add `lark` to root `pyproject.toml` dependencies (same section as `fastmcp`, `aiosqlite`, etc.)
  - [x] Run `poetry lock --no-update` to update lock file
  - [x] Note: Lark is not used in 3.1's regex-based pre-pass but must be available for Story 3.3

- [x] Task 8: Add BlackJack git submodule (AC: regression testing)
  - [x] Confirm BlackJack corpus repo URL with Kamal before running
  - [x] `git submodule add <blackjack-repo-url> tests/cobol_parser_mcp/fixtures/blackjack`
  - [x] Add `.gitmodules` entry; commit submodule registration

- [x] Task 9: Write tests (AC: 1–10)
  - [x] Create `tests/cobol_parser_mcp/__init__.py`
  - [x] Create `tests/cobol_parser_mcp/fixtures/` with minimal inline COBOL fixtures (5–10 lines; no real client data)
  - [x] Create `tests/cobol_parser_mcp/test_cobol_parser.py`:
    - [x] `test_parse_module_extracts_program_id_verbatim` — verify uppercase + hyphens preserved
    - [x] `test_parse_module_extracts_paragraphs_with_line_numbers`
    - [x] `test_parse_module_extracts_copy_refs`
    - [x] `test_parse_module_extracts_call_targets`
    - [x] `test_parse_module_finds_exec_sql_blocks`
    - [x] `test_parse_module_finds_exec_cics_blocks`
    - [x] `test_parse_module_finds_delta_macros`
    - [x] `test_parse_module_stores_result_in_session_cache`
    - [x] `test_parse_module_file_not_found_returns_error_not_raises`
    - [x] `test_parse_module_never_raises_on_malformed_source`
  - [x] Create `tests/cobol_parser_mcp/test_call_graph.py`:
    - [x] `test_extract_call_graph_returns_nodes_and_edges`
    - [x] `test_extract_call_graph_expands_perform_thru_range`
    - [x] `test_extract_call_graph_no_cache_returns_error`
    - [x] `test_extract_call_graph_never_raises`
  - [x] Create `tests/cobol_parser_mcp/test_server.py` (smoke: tools registered, return dicts)
  - [x] Create `tests/cobol_parser_mcp/test_dialect_handler.py`:
    - [x] `test_find_exec_sql_blocks_detects_locations`
    - [x] `test_find_exec_cics_blocks_detects_locations`
  - [x] BlackJack integration test (conditional on submodule): `test_blackjack_corpus_all_modules_parse_successfully` — if `tests/cobol_parser_mcp/fixtures/blackjack/src/` exists, parse every `.cob` file and assert `status == "ok"` for each

## Dev Notes

### Architecture Guardrails

- **This is the first story for `cobol_parser_mcp`** — create the full package from scratch. Follow the same structural pattern as `specdb_mcp` and `delta_macros_mcp` established in Stories 1.2, 1.3, 2.1.
- **Poetry monorepo** — no separate `pyproject.toml` in `mcp-servers/cobol_parser_mcp/`. All deps managed at root. Add `lark` to root `pyproject.toml`. Run server via `poetry run python -m cobol_parser_mcp.server`.
- **`result.py` is COPIED into this package** — architecture explicitly states "shared result.py as published package deferred for post-MVP; copy per server is acceptable". Do not import from another server's package.
- **Thin `server.py`** — tool functions must be one-line wrappers calling into `cobol_parser.py`, `call_graph.py`, or `dialect_handler.py`. No business logic in `server.py`.
- **Session cache pattern** — `_SESSION_CACHE: dict[str, dict] = {}` at module level in `cobol_parser.py`. This dict persists for the lifetime of the server process (a single IDE session). `parse_module` writes to it; `extract_call_graph`, `score_complexity`, `detect_antipatterns` (Stories 3.1–3.2) and `build_cluster_context` (Story 3.3) read from it. Re-calling `parse_module` for the same `program_name` overwrites the cache entry.
- **PROGRAM-ID verbatim** — `program_name` stored and returned as COBOL PROGRAM-ID value exactly as it appears in the source (uppercase with hyphens): `"PAYROLL-CALC"`, `"ACCT-BATCH"`. Never lowercase, never underscore. The architecture mandates this as the canonical module identity key across all tables and all tool calls.
- **Regex-based pre-pass for 3.1** — COBOL structure detection uses Python `re` module. Lark grammar-level parsing is added for complex constructs in later stories if needed. Keep the regex approach simple and deterministic for Story 3.1.
- **COBOL column layout** — standard fixed-format COBOL: columns 1–6 sequence numbers, column 7 indicator (`*` = comment, `-` = continuation), columns 8–11 Area A (divisions, sections, paragraphs), columns 12–72 Area B (statements). Paragraph detection must account for this layout.
- **`.cbl` and `.cob` both valid** — `source_path` can point to either extension. No validation of extension required.
- **Error handling mandatory** — every tool function must have its own `try/except Exception` wrapping ALL internal calls. Never let exceptions propagate to FastMCP's default handler. Return `make_error(...)` instead.
- **IDE config files already exist** — Stories 1.1 established `.claude/mcp.json` and `.vscode/mcp.json`. **EXTEND** these files by adding the `cobol-parser-mcp` entry. Do not recreate them from scratch.
- **MCP tool names exact** — `parse_module` and `extract_call_graph` are the PRD-specified names. Do not rename, abbreviate, or suffix them.
- **No source code leaves the environment** — `parse_module` reads source from local disk only. No content of the COBOL source file is transmitted anywhere. The tool returns structural metadata only (paragraph names, line numbers, reference names).
- **Performance** — `parse_module` must complete within 30 seconds for a 5,000-line module (NFR2). Avoid reading the file multiple times; parse in a single pass.

### Project Structure Notes

Create (new files):
- `mcp-servers/cobol_parser_mcp/__init__.py`
- `mcp-servers/cobol_parser_mcp/server.py`
- `mcp-servers/cobol_parser_mcp/cobol_parser.py` (contains `_SESSION_CACHE`, `parse_module`)
- `mcp-servers/cobol_parser_mcp/call_graph.py` (contains `build_call_graph`)
- `mcp-servers/cobol_parser_mcp/dialect_handler.py` (contains EXEC SQL/CICS detection)
- `mcp-servers/cobol_parser_mcp/result.py`
- `mcp-servers/cobol_parser_mcp/config.py`
- `tests/cobol_parser_mcp/__init__.py`
- `tests/cobol_parser_mcp/test_cobol_parser.py`
- `tests/cobol_parser_mcp/test_call_graph.py`
- `tests/cobol_parser_mcp/test_server.py`
- `tests/cobol_parser_mcp/test_dialect_handler.py`
- `tests/cobol_parser_mcp/fixtures/` (directory with minimal inline COBOL snippets)
- `tests/cobol_parser_mcp/fixtures/blackjack/` (git submodule — confirm URL before adding)

Modify (existing files):
- `pyproject.toml` — add `lark` dependency
- `.claude/mcp.json` — add `cobol-parser-mcp` entry
- `.vscode/mcp.json` — add `cobol-parser-mcp` entry

### References

- `parse_module` and `extract_call_graph` tool names and behaviour [Source: docs/planning-artifacts/epics.md#Story-3.1]
- FR1: paragraph call graph [Source: docs/planning-artifacts/epics.md#Story-3.1]
- FR4: COPY, CALL, SQL, CICS, Delta macro references [Source: docs/planning-artifacts/epics.md#Story-3.1]
- FR35: IBM Enterprise COBOL + COBOL-85 support [Source: docs/planning-artifacts/epics.md#Story-3.1]
- FR38: copybook dependency recording [Source: docs/planning-artifacts/epics.md#Story-3.1]
- NFR2: parser < 30s for modules ≤ 5k lines [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- NFR6: no source code transmitted externally [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- NFR11: no silent failures [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- `result.py` pattern: `make_result()`, `make_error()`, `make_warning()` [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- MCP tool naming: verb-first snake_case, exact PRD names [Source: docs/planning-artifacts/architecture.md#Naming-Patterns]
- `program_name` = COBOL PROGRAM-ID verbatim [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- Poetry monorepo, thin server.py, domain modules [Source: docs/planning-artifacts/architecture.md#Structure-Patterns]
- Session cache: design decision for STDIO server — state persists within IDE session
- MCP server IDE config format [Source: docs/planning-artifacts/architecture.md#Infrastructure-Deployment]
- BlackJack corpus as regression baseline: NFR21 [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- Error handling pattern (per-tool try/except) [Source: docs/planning-artifacts/architecture.md#Process-Patterns]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

_none_

### Completion Notes List

- All 9 tasks completed. 37 tests pass, 0 failures, 0 regressions.
- Tasks 1, 6, 7, 8 were pre-completed before this session (package skeleton, IDE configs, lark dep, BlackJack submodule already present).
- `cobol_parser.py`: regex-based single-pass parser. Paragraphs detected only within PROCEDURE DIVISION (post `PROCEDURE DIVISION.` line). Avoids false-positives from PROGRAM-ID, IDENTIFICATION DIVISION, etc.
- `dialect_handler.py`: `re.DOTALL` multiline regex for EXEC SQL/CICS blocks; line numbers computed via `\n` count before match offset.
- `call_graph.py`: imports `_SESSION_CACHE` by reference from `cobol_parser` module; mutations visible across both modules without reassignment. PERFORM VARYING/UNTIL/TIMES filtered via `_PERFORM_KEYWORDS`.
- `server.py`: thin wrappers, no business logic. Both tools importable as module-level callables for testing.
- `conftest.py` added with `autouse` fixture to clear `_SESSION_CACHE` between tests for isolation.
- BlackJack integration test (`test_blackjack_corpus_all_modules_parse_successfully`) passes against all 8 `.cob` corpus files.

### File List

- `mcp-servers/cobol_parser_mcp/__init__.py` (pre-existing)
- `mcp-servers/cobol_parser_mcp/result.py` (pre-existing)
- `mcp-servers/cobol_parser_mcp/config.py` (pre-existing)
- `mcp-servers/cobol_parser_mcp/cobol_parser.py` (new)
- `mcp-servers/cobol_parser_mcp/dialect_handler.py` (new)
- `mcp-servers/cobol_parser_mcp/call_graph.py` (new)
- `mcp-servers/cobol_parser_mcp/server.py` (modified — added tool wrappers)
- `tests/cobol_parser_mcp/__init__.py` (pre-existing)
- `tests/cobol_parser_mcp/conftest.py` (new)
- `tests/cobol_parser_mcp/test_cobol_parser.py` (new)
- `tests/cobol_parser_mcp/test_call_graph.py` (new)
- `tests/cobol_parser_mcp/test_dialect_handler.py` (new)
- `tests/cobol_parser_mcp/test_server.py` (modified — added tool smoke tests)
- `tests/cobol_parser_mcp/fixtures/minimal.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/exec_blocks.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/delta_macros.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/perform_thru.cbl` (new)

## Change Log

- 2026-03-03: Story 3.1 implemented. Created cobol_parser_mcp domain modules (cobol_parser, dialect_handler, call_graph), MCP tool wrappers in server.py, and full test suite (37 tests). All ACs satisfied. Status → review.
