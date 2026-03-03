# Story 3.3: cobol-parser-mcp — Semantic Paragraph Clustering

Status: review

## Story

As an **analyst**,
I want AI-generated semantic cluster groupings and plain-English descriptions for a module's paragraphs,
So that I can review the AI's understanding of program structure and correct it before it reaches the spec layer.

## Acceptance Criteria

1. **Given** `parse_module` and `extract_call_graph` have been run for a program **When** `build_cluster_context` is called with `program_name` **Then** it returns a structured context object containing ONLY: paragraph names, PERFORM edges from the call graph, and DATA DIVISION field names — never raw COBOL source (NFR7).
2. **And** this context object is what the Viper agent (Story 3.4) uses for its own LLM-based semantic clustering analysis — the MCP tool itself makes NO LLM API calls.
3. **When** the Viper agent has completed its clustering analysis and produced cluster groupings **When** `validate_cluster_output(program_name, clusters)` is called **Then** it validates cluster structure (non-empty names, paragraph references exist in parse result), stores validated clusters in session cache, and returns `make_result(data={"clusters": [...], "program_name": ...})`.
4. **And** each cluster in the returned data has: `name` (plain English label), `paragraphs` (list of paragraph names), `description` (plain English functional role).
5. **And** the cluster output is NOT written to the spec layer by this tool — that write happens in the Viper workflow (Story 3.5) after explicit analyst approval (FR7).
6. **When** `build_cluster_context` is called for a `program_name` not in session cache (i.e. `parse_module` and `extract_call_graph` not yet run) **Then** it returns `{"status": "error", "message": "Module not parsed in this session: run parse_module and extract_call_graph first", ...}`.
7. **When** `validate_cluster_output` receives malformed cluster data (missing `name`, `paragraphs` references to non-existent paragraphs) **Then** it returns `{"status": "warning", "flags": [{"code": "INVALID_CLUSTER_DATA", ...}], ...}` with the specific validation failure described.
8. **And** the tool never raises — all errors are returned as structured result dicts (NFR11).

## Tasks / Subtasks

- [x] Task 1: Implement `cluster_builder.py` — cluster context preparation and validation (AC: 1–8)
  - [x] Implement `_extract_data_division_fields(source: str) -> list[str]` — scan DATA DIVISION for field names (WORKING-STORAGE, LINKAGE SECTION items); return uppercase field names only (e.g. `["WS-CUST-BAL", "WS-TRANS-AMT"]`); exclude `FILLER` entries
  - [x] Implement `build_cluster_context(program_name: str) -> dict` — reads `_SESSION_CACHE[program_name]`; assembles and returns ONLY: paragraph names list, PERFORM edges list, DATA DIVISION field names list; no raw source included; wraps in `make_result(data={...})`
  - [x] Implement `_validate_single_cluster(cluster: dict, valid_paragraphs: set[str]) -> list[dict]` — check: `name` is non-empty string, `paragraphs` is non-empty list, every paragraph in `paragraphs` exists in `valid_paragraphs`; return list of flag dicts for violations
  - [x] Implement `validate_cluster_output(program_name: str, clusters: list[dict]) -> dict` — reads `_SESSION_CACHE[program_name]`; validates each cluster; stores validated clusters back into `_SESSION_CACHE[program_name]["clusters"]`; returns `make_result(data={"program_name": ..., "clusters": clusters})` or `make_warning(...)` if validation flags found

- [x] Task 2: Add MCP tools to `server.py` (AC: 1–8)
  - [x] Add `@mcp.tool() def build_cluster_context(program_name: str) -> dict` — thin wrapper calling `cluster_builder.build_cluster_context()`
  - [x] Add `@mcp.tool() def validate_cluster_output(program_name: str, clusters: list) -> dict` — thin wrapper calling `cluster_builder.validate_cluster_output()`

- [x] Task 3: Write tests (AC: 1–8)
  - [x] Create `tests/cobol_parser_mcp/test_cluster_builder.py`:
    - [x] `test_build_cluster_context_returns_paragraphs_not_source` — assert raw source text does NOT appear anywhere in the result
    - [x] `test_build_cluster_context_returns_perform_edges`
    - [x] `test_build_cluster_context_returns_data_division_fields`
    - [x] `test_build_cluster_context_no_cache_returns_error`
    - [x] `test_validate_cluster_output_accepts_valid_clusters`
    - [x] `test_validate_cluster_output_flags_unknown_paragraph_reference`
    - [x] `test_validate_cluster_output_flags_empty_cluster_name`
    - [x] `test_validate_cluster_output_stores_in_session_cache`
    - [x] `test_build_cluster_context_never_raises`
    - [x] `test_validate_cluster_output_never_raises`
  - [x] Extend BlackJack integration test: for each BJ-* module, `build_cluster_context` must return `status == "ok"` with non-empty paragraph list

## Dev Notes

### Architecture Guardrails

- **DEPENDS ON STORIES 3.1 AND 3.2** — `cluster_builder.py` reads from `_SESSION_CACHE` in `cobol_parser.py` (established Story 3.1). The session cache should contain parse results (paragraphs, call graph, EXEC SQL/CICS locations, DATA DIVISION fields) when these tools are called. Extend `_SESSION_CACHE` structure in `cobol_parser.py` to include a `"data_division_fields"` key if not already present — OR implement `_extract_data_division_fields` in `cluster_builder.py` and call it during `build_cluster_context` using the raw source from cache (the cache may store the raw source for this purpose; check the Story 3.1 session cache structure and align).
- **CRITICAL PRIVACY CONSTRAINT (NFR7)** — `build_cluster_context` is the data privacy enforcement point. It MUST strip all raw COBOL source before returning. The `data` dict returned must contain ONLY: `paragraph_names: list[str]`, `perform_edges: list[dict]`, `data_division_fields: list[str]`. If the developer is uncertain whether something constitutes "raw source", exclude it. Test explicitly: `test_build_cluster_context_returns_paragraphs_not_source` should assert that no multi-word COBOL statement text appears in the result.
- **NO LLM CALLS IN THIS MODULE** — `cluster_builder.py` makes zero external API calls. The semantic clustering analysis is performed by the Viper agent itself (Claude, the LLM executing the workflow). This module only prepares input data for the agent and validates the output the agent produces. Any LLM timeout/unavailability is handled by the Viper workflow (Story 3.5), not here.
- **`validate_cluster_output` is called after agent analysis** — the flow is: agent calls `build_cluster_context` → agent does LLM reasoning → agent calls `validate_cluster_output` with its proposed clusters → tool validates structure → analyst reviews → Viper workflow writes to specdb-mcp. The `validate_cluster_output` tool does NOT write to specdb — that is strictly Story 3.5's responsibility.
- **`clusters` parameter type in MCP tool** — declare as `list` (not `list[dict]`) in the tool signature for FastMCP compatibility, same pattern as Story 2.2 `add_macro`'s `parameters` argument.
- **Session cache extended** — after `validate_cluster_output` succeeds, store clusters in `_SESSION_CACHE[program_name]["clusters"]` so the Viper workflow (Story 3.5) can read them when writing to specdb-mcp.
- **Warning vs error for validation** — invalid clusters return `make_warning` (not `make_error`) because the agent can correct them and retry. An error is only appropriate for system failures (cache miss, unexpected exception).
- **`result.py` already exists** — use `make_result()`, `make_error()`, `make_warning()` from the existing `cobol_parser_mcp/result.py`.
- **Tool names are fixed** — `build_cluster_context` and `validate_cluster_output`.

### Project Structure Notes

Create (new files):
- `mcp-servers/cobol_parser_mcp/cluster_builder.py`
- `tests/cobol_parser_mcp/test_cluster_builder.py`

Modify (existing files):
- `mcp-servers/cobol_parser_mcp/server.py` — add `build_cluster_context` and `validate_cluster_output` tool definitions
- `mcp-servers/cobol_parser_mcp/cobol_parser.py` — extend session cache structure to include `data_division_fields` if not already populated in `parse_module` (coordinate with Story 3.1 implementation; if Story 3.1 already scans DATA DIVISION fields, use that; if not, add it here via `_extract_data_division_fields`)

Do NOT modify:
- `call_graph.py`, `complexity_scorer.py`, `antipattern_detector.py`, `dialect_handler.py`, `result.py`, `config.py`

### References

- FR5: AI semantic cluster groupings [Source: docs/planning-artifacts/epics.md#Story-3.3]
- FR6: plain-English cluster descriptions [Source: docs/planning-artifacts/epics.md#Story-3.3]
- FR7: analyst review gate — clusters not written until explicitly approved [Source: docs/planning-artifacts/epics.md#Story-3.3]
- NFR7: only paragraph names, call graph, DATA DIVISION field names sent to LLM — never raw source [Source: docs/planning-artifacts/epics.md#Story-3.3]
- NFR11: no silent failures [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- `make_result()`, `make_warning()`, `make_error()` helpers [Source: docs/planning-artifacts/architecture.md#Format-Patterns]
- Session cache pattern [Source: docs/implementation-artifacts/3-1-cobol-parser-mcp-core-module-parsing-and-call-graph.md#Dev-Notes]
- `list` (not `list[dict]`) for MCP tool signature [Source: docs/implementation-artifacts/2-2-delta-macros-mcp-macro-ingestion.md#Dev-Notes]
- Spec layer writes belong to Viper workflow, not this MCP tool [Source: docs/planning-artifacts/epics.md#Story-3.5]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

_none_

### Completion Notes List

- All 3 tasks completed. 64 total tests pass (11 new for cluster_builder, plus BlackJack integration), 0 failures, 0 regressions.
- `cluster_builder.py`: `_extract_data_division_fields` uses regex `^\s*\d{1,2}\s+([A-Z][A-Z0-9\-]*)` to scan only between DATA DIVISION and PROCEDURE DIVISION; excludes FILLER with deduplication via seen-set.
- `build_cluster_context` is the NFR7 privacy enforcement point — result dict contains ONLY `{program_name, paragraph_names, perform_edges, data_division_fields}`, raw `_source` is never included.
- `validate_cluster_output` returns `make_warning` (not `make_error`) for structural issues so the Viper agent can correct and retry; stores clusters in `_SESSION_CACHE[program_name]["clusters"]` (best-effort, even on warning) for Story 3.5 workflow to read.
- Call graph edges fetched via `build_call_graph(program_name)` internal call rather than duplicating edge-extraction logic.
- BlackJack corpus integration test passes for all 8 modules.

### File List

- `mcp-servers/cobol_parser_mcp/cluster_builder.py` (new)
- `mcp-servers/cobol_parser_mcp/server.py` (modified — added build_cluster_context, validate_cluster_output tools)
- `tests/cobol_parser_mcp/test_cluster_builder.py` (new)

## Change Log

- 2026-03-03: Story 3.3 implemented. Added cluster_builder.py; extended server.py with build_cluster_context and validate_cluster_output tools; added 11 new tests. All ACs satisfied. Status → review.
