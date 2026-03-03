# Story 3.2: cobol-parser-mcp — Complexity Scoring & Anti-Pattern Detection

Status: review

## Story

As an **analyst**,
I want to see a complexity score and a list of detected anti-patterns for any parsed COBOL module,
So that I can prioritise review effort and flag structural risks before analysis begins.

## Acceptance Criteria

1. **Given** a module has been parsed via `parse_module` (Story 3.1) **When** `score_complexity` is called with `program_name` **Then** it returns a `rating` of `"Low"`, `"Medium"`, or `"High"` with a `factors` dict containing: `paragraph_count`, `max_perform_nesting_depth`, `redefines_count`, `goto_count` (FR2).
2. **When** `detect_antipatterns` is called with `program_name` **Then** it returns a list of flagged anti-patterns, each with `type`, `location` (paragraph name + line number), and `description` (FR3).
3. **And** the anti-pattern `type` values detected include: `"GOTO"`, `"ALTER"`, `"NESTED_PERFORM_THRU"`, `"REDEFINES_NON_FILLER"`, `"FALLTHROUGH_PARAGRAPH"` (FR3).
4. **When** `detect_antipatterns` encounters an EXEC CICS block **Then** it is included in the `flags` array as `{"code": "CICS_CONSTRUCT", "message": "...", "location": "..."}` (FR36).
5. **When** `detect_antipatterns` encounters an EXEC SQL block **Then** it is included in the `flags` array as `{"code": "DB2_SQL_CONSTRUCT", "message": "...", "location": "..."}` (FR37).
6. **When** the module has no anti-patterns **Then** `detect_antipatterns` returns `{"status": "ok", "data": {"antipatterns": []}, "flags": [], "message": "No anti-patterns detected"}`.
7. **When** `score_complexity` or `detect_antipatterns` is called for a `program_name` not in session cache **Then** the tool returns `{"status": "error", ...}` — never raises.
8. **And** both tools read from the session cache populated by `parse_module` — they do NOT re-read the source file.

## Tasks / Subtasks

- [x] Task 1: Implement `complexity_scorer.py` (AC: 1, 7, 8)
  - [x] Implement `_calculate_perform_nesting_depth(call_graph_edges: list[dict]) -> int` — compute maximum PERFORM nesting depth from the call graph built in Story 3.1
  - [x] Implement `_count_redefines(source: str) -> int` — count `REDEFINES` clauses in DATA DIVISION that are NOT applied to `FILLER` items
  - [x] Implement `_count_gotos(source: str) -> int` — count `GO TO` statements in PROCEDURE DIVISION
  - [x] Implement `_compute_rating(paragraph_count: int, nesting_depth: int, redefines_count: int, goto_count: int) -> str` — return `"Low"`, `"Medium"`, or `"High"` based on thresholds (suggested starting thresholds: Low = ≤20 paragraphs AND ≤3 nesting AND ≤3 REDEFINES AND 0 GOTOs; High = >50 paragraphs OR >5 nesting OR >10 REDEFINES OR ≥5 GOTOs; Medium = all other cases — developer should document chosen thresholds in a module-level comment)
  - [x] Implement `score_complexity(program_name: str) -> dict` — reads `_SESSION_CACHE[program_name]`; computes all factors; returns `make_result(data={"program_name": ..., "rating": "Medium", "factors": {...}})`

- [x] Task 2: Implement `antipattern_detector.py` (AC: 2, 3, 4, 5, 6, 7, 8)
  - [x] Implement `_detect_gotos(source: str, paragraphs: list[dict]) -> list[dict]` — find `GO TO` statements; each result: `{"type": "GOTO", "location": "PARA-NAME:45", "description": "Unconditional GO TO at line 45"}`
  - [x] Implement `_detect_alters(source: str) -> list[dict]` — find `ALTER` statements (deprecated COBOL construct)
  - [x] Implement `_detect_nested_perform_thru(source: str, paragraphs: list[dict]) -> list[dict]` — detect `PERFORM THRU` inside another paragraph that is itself within a `PERFORM THRU` range
  - [x] Implement `_detect_redefines_non_filler(source: str) -> list[dict]` — find `REDEFINES` clauses applied to non-FILLER data items in DATA DIVISION
  - [x] Implement `_detect_fallthrough_paragraphs(paragraphs: list[dict], perform_targets: list[str]) -> list[dict]` — identify paragraphs reachable only by fall-through (not explicitly PERFORMed and not the first paragraph)
  - [x] Implement `detect_antipatterns(program_name: str) -> dict` — reads `_SESSION_CACHE[program_name]`; runs all detectors; merges CICS and SQL blocks from session cache into `flags` array with codes `"CICS_CONSTRUCT"` and `"DB2_SQL_CONSTRUCT"`; returns `make_result(data={"antipatterns": [...]}, flags=[...])`

- [x] Task 3: Extend `server.py` with two new tools (AC: 1–8)
  - [x] Add `@mcp.tool() def score_complexity(program_name: str) -> dict` — thin wrapper calling `complexity_scorer.score_complexity()`
  - [x] Add `@mcp.tool() def detect_antipatterns(program_name: str) -> dict` — thin wrapper calling `antipattern_detector.detect_antipatterns()`

- [x] Task 4: Write tests (AC: 1–8)
  - [x] Create `tests/cobol_parser_mcp/test_complexity_scorer.py`:
    - [x] `test_score_complexity_low_rating_simple_module`
    - [x] `test_score_complexity_high_rating_complex_module`
    - [x] `test_score_complexity_includes_all_four_factors`
    - [x] `test_score_complexity_no_cache_returns_error`
    - [x] `test_score_complexity_never_raises`
  - [x] Create `tests/cobol_parser_mcp/test_antipattern_detector.py`:
    - [x] `test_detect_antipatterns_finds_goto`
    - [x] `test_detect_antipatterns_finds_alter`
    - [x] `test_detect_antipatterns_finds_nested_perform_thru`
    - [x] `test_detect_antipatterns_finds_redefines_non_filler`
    - [x] `test_detect_antipatterns_flags_cics_construct`
    - [x] `test_detect_antipatterns_flags_db2_sql_construct`
    - [x] `test_detect_antipatterns_empty_result_when_no_antipatterns`
    - [x] `test_detect_antipatterns_no_cache_returns_error`
    - [x] `test_detect_antipatterns_never_raises`
  - [x] Extend BlackJack integration test: all BJ-* modules must return `status == "ok"` for both `score_complexity` and `detect_antipatterns`

## Dev Notes

### Architecture Guardrails

- **DEPENDS ON STORY 3.1** — this story extends the `cobol_parser_mcp` package. `server.py`, `result.py`, `config.py`, `cobol_parser.py`, `call_graph.py`, `dialect_handler.py`, and the session cache (`_SESSION_CACHE`) are all pre-existing from Story 3.1. **EXTEND** `server.py` by adding two new tools. Do NOT rewrite from scratch.
- **Session cache is the only data source** — `complexity_scorer.py` and `antipattern_detector.py` MUST read exclusively from `_SESSION_CACHE` in `cobol_parser.py`. They must NOT open the source file. If session cache entry is missing, return `make_error("program_name not parsed in this session: ...")`.
- **CICS and SQL flags come from session cache** — the EXEC CICS and EXEC SQL block locations are already stored in the session cache from `parse_module`. `detect_antipatterns` should read these from the cache and add them as flag entries in the result's `flags` array using codes `"CICS_CONSTRUCT"` and `"DB2_SQL_CONSTRUCT"`. Do not re-scan the source file.
- **Anti-pattern `type` values are fixed** — use exactly: `"GOTO"`, `"ALTER"`, `"NESTED_PERFORM_THRU"`, `"REDEFINES_NON_FILLER"`, `"FALLTHROUGH_PARAGRAPH"`. These are the authoritative type strings. Do not invent new type codes without an architecture update.
- **Flag codes for CICS/SQL** — use exactly: `"CICS_CONSTRUCT"` (not `"CICS"` or `"EXEC_CICS"`) and `"DB2_SQL_CONSTRUCT"` (not `"SQL"` or `"EXEC_SQL"`). These match the flag code format defined in the architecture.
- **Complexity thresholds are implementation decisions** — the story specifies contributing factors, not specific threshold values. Developer must choose sensible thresholds, document them in a module-level comment in `complexity_scorer.py`, and ensure the BlackJack corpus produces plausible ratings (BlackJack is a card game — expect Low to Medium complexity).
- **`detect_antipatterns` when no antipatterns** — return `make_result(data={"antipatterns": []}, flags=flags)` — `flags` may still contain CICS/SQL construct flags even when `antipatterns` is empty. Never return an error for "no antipatterns found".
- **Location format** — consistently use `"PARAGRAPH-NAME:line_number"` format for the `location` field, e.g. `"2000-PROCESS:123"`. This enables the Viper agent (Story 3.4) to show analysts precise locations.
- **`result.py` already exists** — use `make_result()`, `make_error()` from the existing `cobol_parser_mcp/result.py`. Do not construct result dicts inline.
- **Tool names are fixed** — `score_complexity` and `detect_antipatterns` are the PRD-specified names. Do not rename.
- **Error handling pattern** — wrap each function body in `try/except Exception`. Return `make_error(...)`, never raise.

### Project Structure Notes

Create (new files):
- `mcp-servers/cobol_parser_mcp/complexity_scorer.py`
- `mcp-servers/cobol_parser_mcp/antipattern_detector.py`
- `tests/cobol_parser_mcp/test_complexity_scorer.py`
- `tests/cobol_parser_mcp/test_antipattern_detector.py`

Modify (existing files):
- `mcp-servers/cobol_parser_mcp/server.py` — add `score_complexity` and `detect_antipatterns` tool definitions

Do NOT modify:
- `cobol_parser.py`, `call_graph.py`, `dialect_handler.py`, `result.py`, `config.py` — these are Story 3.1 files. Read from them, do not change their interfaces.

### References

- `score_complexity` and `detect_antipatterns` behaviour (AC, FR2, FR3) [Source: docs/planning-artifacts/epics.md#Story-3.2]
- FR36: CICS construct flag [Source: docs/planning-artifacts/epics.md#Story-3.2]
- FR37: DB2 SQL construct flag [Source: docs/planning-artifacts/epics.md#Story-3.2]
- Flag code format: SCREAMING_SNAKE with category prefix [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- `make_result()` / `make_error()` helpers [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- Thin `server.py` rule [Source: docs/planning-artifacts/architecture.md#Structure-Patterns]
- Error handling per-tool try/except [Source: docs/planning-artifacts/architecture.md#Process-Patterns]
- Session cache pattern — design established in Story 3.1 [Source: docs/implementation-artifacts/3-1-cobol-parser-mcp-core-module-parsing-and-call-graph.md#Dev-Notes]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

_none_

### Completion Notes List

- All 4 tasks completed. 53 total tests pass (16 new), 0 failures, 0 regressions.
- `complexity_scorer.py`: DFS-based nesting depth calculation with cycle guard; source read from `_source` in session cache; thresholds documented in module-level docstring.
- `antipattern_detector.py`: Five detectors implemented. NESTED_PERFORM_THRU uses `_expand_perform_thru` from `call_graph.py` and scans paragraph line ranges for inner PERFORM THRU; deduplication via seen-set. FALLTHROUGH_PARAGRAPH checks all non-first paragraphs not in the PERFORM targets set.
- CICS/SQL flags read directly from cached `exec_cics_blocks`/`exec_sql_blocks` — no source file re-read.
- BlackJack corpus integration test passes for both `score_complexity` and `detect_antipatterns` across all 8 modules.
- Added COBOL fixtures: `goto_complex.cbl`, `redefines.cbl`, `alter.cbl`, `nested_thru.cbl`, `clean.cbl`.

### File List

- `mcp-servers/cobol_parser_mcp/complexity_scorer.py` (new)
- `mcp-servers/cobol_parser_mcp/antipattern_detector.py` (new)
- `mcp-servers/cobol_parser_mcp/server.py` (modified — added score_complexity, detect_antipatterns tools)
- `tests/cobol_parser_mcp/test_complexity_scorer.py` (new)
- `tests/cobol_parser_mcp/test_antipattern_detector.py` (new)
- `tests/cobol_parser_mcp/fixtures/goto_complex.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/redefines.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/alter.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/nested_thru.cbl` (new)
- `tests/cobol_parser_mcp/fixtures/clean.cbl` (new)

## Change Log

- 2026-03-03: Story 3.2 implemented. Added complexity_scorer.py and antipattern_detector.py; extended server.py with score_complexity and detect_antipatterns tools; added 10 new test fixtures and 16 new tests. All ACs satisfied. Status → review.
