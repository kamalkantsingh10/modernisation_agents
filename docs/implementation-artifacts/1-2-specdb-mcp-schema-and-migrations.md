# Story 1.2: specdb-mcp — Schema & Migrations

Status: done

## Story

As an **operator**,
I want to initialise the full SQLite spec layer schema with a single `init_schema` command,
So that the structured intermediate representation is ready before any COBOL analysis begins.

## Acceptance Criteria

1. **Given** `specdb-mcp` is running and `db_path` in `config.yaml` points to a valid directory **When** `init_schema` is called **Then** the SQLite database is created at `db_path` with all 9 required tables: `schema_version`, `cobol_files`, `analyses`, `metrics`, `dependencies`, `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows`.
2. **Given** `init_schema` completes **Then** the `schema_version` table records the current schema version as an integer.
3. **When** `init_schema` is called again on an existing database **Then** it completes without error and without destroying or duplicating existing data (fully idempotent — `CREATE TABLE IF NOT EXISTS` for all tables).
4. **When** the `specdb-mcp` server starts **Then** it checks the current schema version and applies any pending migrations programmatically — no manual intervention required (NFR17).
5. **Then** `init_schema` returns `{"status": "ok", "data": {"tables_created": [...], "schema_version": N}, "flags": [], "message": "Schema initialised at version N"}`.
6. **When** `db_path` directory does not exist or is not writable **Then** `init_schema` returns `{"status": "error", ...}` with an explicit message — never raises an exception.
7. **Given** each table **Then** all column names use `snake_case`; all COBOL identifier columns use `TEXT` type to preserve uppercase-with-hyphens values verbatim; all timestamp columns use `TEXT` (ISO 8601 UTC strings — never integer Unix timestamps).

## Tasks / Subtasks

- [x] Task 1: Create `src/schema.py` with all CREATE TABLE statements (AC: 1, 7)
  - [x] `schema_version` table
  - [x] `cobol_files` table
  - [x] `analyses` table
  - [x] `metrics` table
  - [x] `dependencies` table
  - [x] `spec_entities` table
  - [x] `spec_operations` table
  - [x] `spec_rules` table
  - [x] `spec_data_flows` table
  - [x] All tables use `CREATE TABLE IF NOT EXISTS` (idempotency)
  - [x] All timestamps as `TEXT NOT NULL DEFAULT ''`; program_name always `TEXT NOT NULL`
- [x] Task 2: Create `src/migrations.py` with version management (AC: 2, 4)
  - [x] `get_current_version(db)` — reads from `schema_version`
  - [x] `apply_migrations(db)` — applies all pending migrations in order
  - [x] Called on server startup via FastMCP lifespan
- [x] Task 3: Implement `init_schema` MCP tool in `src/server.py` (AC: 1, 3, 5, 6)
  - [x] Tool wrapped in try/except — returns `make_error()` on failure, never raises
  - [x] Returns `make_result(data={"tables_created": [...], "schema_version": N})`
  - [x] Idempotent — safe to call multiple times
- [x] Task 4: Write tests in `tests/test_schema.py` and `tests/test_migrations.py`
  - [x] Test all 9 tables created on fresh DB
  - [x] Test idempotency — call init_schema twice, no error
  - [x] Test `schema_version` is populated
  - [x] Test migration applies on version mismatch

## Dev Notes

### Architecture Guardrails

- **aiosqlite** — all DB operations are async.
- **Idempotency is mandatory** — every `CREATE TABLE` uses `CREATE TABLE IF NOT EXISTS`.
- **Never raise from a tool function** — catch all exceptions and return `make_error()`.
- **All timestamps: ISO 8601 UTC strings**.

### Prerequisite

Story 1.1 complete.

### References

- Schema versioning decision [Source: docs/planning-artifacts/architecture.md#Data-Architecture]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- `test_all_nine_tables_created` initially failed because SQLite auto-creates `sqlite_sequence` when AUTOINCREMENT is used. Fixed by filtering `sqlite_` prefixed tables in assertion.
- `test_apply_migrations_idempotent` confirmed only 1 row inserted in `schema_version` (version already applied not re-inserted).

### Completion Notes List

- `mcp-servers/specdb_mcp/schema.py` — all 9 CREATE TABLE IF NOT EXISTS statements
- `mcp-servers/specdb_mcp/migrations.py` — `get_current_version`, `apply_migrations`, CURRENT_VERSION=1
- `init_schema` tool added to `specdb_mcp/server.py` with lifespan startup hook
- 9 tests passing: 4 schema + 5 migrations

### File List

- `mcp-servers/specdb_mcp/schema.py`
- `mcp-servers/specdb_mcp/migrations.py`
- `mcp-servers/specdb_mcp/server.py`
- `tests/specdb_mcp/test_schema.py`
- `tests/specdb_mcp/test_migrations.py`
