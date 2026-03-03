# Story 1.3: specdb-mcp — CRUD Tools

Status: done

## Story

As an **agent**,
I want to read, write, and query the spec layer via `read_spec`, `write_spec`, and `query_spec` tools,
So that any pipeline agent can persist and retrieve structured data without direct database access.

## Acceptance Criteria

1. **Given** the schema has been initialised (Story 1.2) **When** `write_spec` is called with a valid `table`, `program_name`, and `fields` dict **Then** the record is written using the `INSERT OR IGNORE` + `UPDATE` idempotent pattern — re-calling with the same identity key updates fields, never duplicates rows (NFR10).
2. **Given** a `write_spec` call **Then** the write is wrapped in a per-tool-call SQLite transaction — if any part fails the database rolls back cleanly (NFR12).
3. **When** `read_spec` is called with `table` and `program_name` **Then** matching record(s) are returned as `{"status": "ok", "data": [{...row dict...}], ...}`.
4. **When** `query_spec` is called with a `sql_fragment` (a WHERE clause or SELECT) **Then** matching rows are returned within 2 seconds for any standard query (NFR3).
5. **When** any tool call fails (DB error, invalid table name, bad SQL) **Then** it returns `{"status": "error", ...}` with a human-readable message — never raises an exception (NFR11).
6. **Given** `write_spec` is called for a table with a `UNIQUE` constraint on `(program_name, <id_col>)` **Then** the idempotent pattern correctly identifies the row and updates it without violating the constraint.
7. **Given** `read_spec` is called for a `program_name` that does not exist **Then** it returns `{"status": "ok", "data": [], ...}` — an empty list, not an error.

## Tasks / Subtasks

- [x] Task 1: Create `src/spec_db.py` with domain logic (AC: 1, 2, 3, 4)
  - [x] `write_spec(db, table, program_name, fields)` — idempotent INSERT OR IGNORE + UPDATE
  - [x] `read_spec(db, table, program_name)` — returns list of row dicts
  - [x] `query_spec(db, sql_fragment, params)` — safe parameterised query
  - [x] All wrapped in transaction handling
- [x] Task 2: Implement MCP tools in `src/server.py` (AC: 1–7)
  - [x] `write_spec(table: str, program_name: str, fields: dict) -> dict`
  - [x] `read_spec(table: str, program_name: str) -> dict`
  - [x] `query_spec(sql_fragment: str, params: list | None) -> dict`
  - [x] Each tool fully wrapped in try/except, returns `make_error()` on failure
- [x] Task 3: Validate table names against allowed list (AC: 5)
  - [x] `ALLOWED_TABLES` constant in `spec_db.py`
  - [x] Returns `ValueError` for unknown table names — caught by server.py and returned as `make_error()`
- [x] Task 4: Write tests in `tests/test_spec_db.py` (AC: 1–7)
  - [x] Test idempotent write — second write updates, does not duplicate
  - [x] Test transaction rollback on forced failure
  - [x] Test read returns empty list for missing program_name
  - [x] Test query_spec returns correct rows
  - [x] Test error returned for invalid table name
  - [x] Use `aiosqlite` in-memory DB (`:memory:`) for test fixtures

## Dev Notes

### Architecture Guardrails

- **Idempotent write** — INSERT OR IGNORE + UPDATE. Skip UPDATE if no mutable columns (e.g. `dependencies`).
- **TABLES_WITH_PROGRAM_NAME** — `dependencies` excluded (uses `source_program`/`target_program`).
- **TABLES_WITH_UPDATED_AT** — `dependencies` excluded (no `updated_at` column).

### References

- Idempotent write pattern [Source: docs/planning-artifacts/architecture.md#Data-Architecture]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- `dependencies` table has no `program_name` or `updated_at` columns. Added `TABLES_WITH_PROGRAM_NAME` and `TABLES_WITH_UPDATED_AT` sets to handle this.
- `dependencies` identity covers ALL non-auto columns → `update_pairs` was empty → `SET WHERE` syntax error. Fixed by skipping UPDATE when `update_pairs` is empty.

### Completion Notes List

- `mcp-servers/specdb_mcp/spec_db.py` — `write_spec`, `read_spec`, `query_spec` with full idempotency and table validation
- `write_spec`, `read_spec`, `query_spec` MCP tools added to `specdb_mcp/server.py`
- 12 tests passing across all spec_db scenarios

### File List

- `mcp-servers/specdb_mcp/spec_db.py`
- `mcp-servers/specdb_mcp/server.py`
- `tests/specdb_mcp/test_spec_db.py`
