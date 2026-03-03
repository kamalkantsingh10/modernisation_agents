# Story 1.1: Project Scaffolding & Shared Infrastructure

Status: done

## Story

As an **operator/developer**,
I want all 4 MCP server uv projects scaffolded with correct structure and shared patterns,
So that I have a consistent, runnable foundation for all subsequent implementation work.

## Acceptance Criteria

1. **Given** the repository is empty **When** scaffolding is applied **Then** four Python packages exist as a Poetry monorepo at `mcp-servers/cobol_parser_mcp`, `mcp-servers/specdb_mcp`, `mcp-servers/delta_macros_mcp`, `mcp-servers/gitlab_mcp` — each with `result.py`, `config.py`, `server.py`, and `__init__.py`. A single root `pyproject.toml` and `poetry.lock` manage all dependencies.
2. **Given** each server exists **Then** each `src/result.py` implements `make_result()`, `make_error()`, `make_warning()` returning exactly `{"status": ..., "data": ..., "flags": ..., "message": ...}` — content is identical across all 4 servers (copy, do not share as a package yet).
3. **Given** each server exists **Then** each `src/config.py` loads `config.yaml` from project root (or `BMAD_PROJECT_ROOT` env var path) and fails with an explicit, human-readable error if not found — no silent `None` returns.
4. **Given** each server exists **Then** each `server.py` is a minimal, valid FastMCP 3.0.2 app that starts without error via `poetry run python -m <package>.server` from the project root — no tools required yet, just a valid boilerplate.
5. **Given** the project exists **Then** the BlackJack COBOL corpus is present as a git submodule at `tests/cobol_parser_mcp/fixtures/blackjack/`. Source files are `.cob` under `src/` and copybooks are `.cpy` under `copy/`. These are real IBM Enterprise COBOL source files from https://github.com/kamalkantsingh10/cobol-blackjack.
6. **Given** the project root **Then** `.claude/mcp.json` and `.vscode/mcp.json` both exist registering all 4 servers using `poetry run python -m <package>.server` with no network ports.
7. **Given** the project root **Then** `config.yaml` exists with all required fields documented: `db_path`, `macro_library_path`, `gitlab_url`, `project_name`, `target_language` — with example values.
8. **Given** the project root **Then** `data/.gitkeep` and `logs/.gitkeep` exist.
9. **Given** each server **Then** `tests/` directory exists with at least a placeholder test file that imports the server module without error.

## Tasks / Subtasks

- [x] Task 1: Scaffold all 4 MCP server directories (AC: 1)
  - [x] Create `mcp-servers/cobol-parser-mcp/` with `uv init --python 3.12 cobol-parser-mcp`
  - [x] Create `mcp-servers/specdb-mcp/` with `uv init --python 3.12 specdb-mcp`
  - [x] Create `mcp-servers/delta-macros-mcp/` with `uv init --python 3.12 delta-macros-mcp`
  - [x] Create `mcp-servers/gitlab-mcp/` with `uv init --python 3.12 gitlab-mcp`
  - [x] Add dependencies per server: all get `mcp[cli] fastmcp`; specdb-mcp adds `aiosqlite`; cobol-parser-mcp adds `lark`; gitlab-mcp adds `python-gitlab==8.0.0`
- [x] Task 2: Create `src/result.py` in all 4 servers (AC: 2)
  - [x] Implement `make_result(data=None, flags=None, message="", status="ok")`
  - [x] Implement `make_error(message, flags=None)`
  - [x] Implement `make_warning(data, message, flags)`
  - [x] All return the standard 4-key dict: `{"status", "data", "flags", "message"}`
- [x] Task 3: Create `src/config.py` in all 4 servers (AC: 3)
  - [x] Load `config.yaml` from project root (walk up from CWD or use `BMAD_PROJECT_ROOT`)
  - [x] Raise `RuntimeError` with explicit message if config not found
  - [x] Expose a `load_config()` function that returns parsed YAML as dict
- [x] Task 4: Create `src/server.py` boilerplate in all 4 servers (AC: 4)
  - [x] FastMCP 3.0.2 app initialised with server name and version
  - [x] Dual logging handler: stderr + `logs/<server-name>.log`
  - [x] `if __name__ == "__main__": mcp.run()` entry point
  - [x] Verify `uv run python -m src.server` starts without error
- [x] Task 5: Create BlackJack COBOL corpus (AC: 5)
  - [x] Added https://github.com/kamalkantsingh10/cobol-blackjack as git submodule at `tests/cobol_parser_mcp/fixtures/blackjack`
  - [x] Real COBOL source corpus with src/ (.cob) and copy/ (.cpy) files
- [x] Task 6: Create IDE MCP registration files (AC: 6)
  - [x] `.claude/mcp.json` with all 4 servers using `poetry run` commands
  - [x] `.vscode/mcp.json` with identical format
- [x] Task 7: Create `config.yaml` at project root (AC: 7)
  - [x] Include `db_path: data/specdb.sqlite`
  - [x] Include `macro_library_path: blackjack/macros/`
  - [x] Include `gitlab_url: https://gitlab.com`
  - [x] Include `project_name: mainframe-modernisation`
  - [x] Include `target_language: ""  # TBD — set before Oogway stage`
- [x] Task 8: Create runtime directories and test stubs (AC: 8, 9)
  - [x] `data/.gitkeep`, `logs/.gitkeep`
  - [x] Placeholder `tests/<package>/test_server.py` in each server importing result module

## Dev Notes

### Architecture Guardrails

- **Python 3.12 + Poetry** — switched from uv to Poetry per project preference. Root `pyproject.toml` manages all deps.
- **FastMCP 3.0.2** — installed via Poetry. Confirmed version.
- **Monorepo layout** — single root `pyproject.toml`; packages named `cobol_parser_mcp`, `specdb_mcp`, `delta_macros_mcp`, `gitlab_mcp` under `mcp-servers/`.
- **Run via** `poetry run python -m <package>.server` from project root.
- **BlackJack corpus** — real COBOL project at https://github.com/kamalkantsingh10/cobol-blackjack added as git submodule. Files use `.cob` extension, located at `tests/cobol_parser_mcp/fixtures/blackjack/src/` and `.../copy/`.

### References

- Architecture decision: FastMCP 3.0.2, Python 3.12 [Source: docs/planning-artifacts/architecture.md#MCP-Server-Framework]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- Switched from per-server uv projects to root Poetry monorepo per operator preference
- BlackJack corpus replaced with real COBOL project (git submodule) instead of synthetic files
- Package names use snake_case (`cobol_parser_mcp`) to match Python conventions; server IDs remain hyphenated in mcp.json

### Completion Notes List

- All 4 packages scaffolded under `mcp-servers/`
- `result.py`, `config.py`, `server.py` created in all 4 packages (identical result.py/config.py)
- FastMCP 3.0.2 installed and confirmed via `poetry install`
- BlackJack git submodule added at `tests/cobol_parser_mcp/fixtures/blackjack`
- `.claude/mcp.json` and `.vscode/mcp.json` created with Poetry run commands
- `config.yaml`, `data/.gitkeep`, `logs/.gitkeep` created at project root
- 11 tests passing for result.py across all 4 packages

### File List

- `pyproject.toml`
- `config.yaml`
- `data/.gitkeep`
- `logs/.gitkeep`
- `.claude/mcp.json`
- `.vscode/mcp.json`
- `mcp-servers/cobol_parser_mcp/__init__.py`
- `mcp-servers/cobol_parser_mcp/result.py`
- `mcp-servers/cobol_parser_mcp/config.py`
- `mcp-servers/cobol_parser_mcp/server.py`
- `mcp-servers/specdb_mcp/__init__.py`
- `mcp-servers/specdb_mcp/result.py`
- `mcp-servers/specdb_mcp/config.py`
- `mcp-servers/specdb_mcp/server.py`
- `mcp-servers/delta_macros_mcp/__init__.py`
- `mcp-servers/delta_macros_mcp/result.py`
- `mcp-servers/delta_macros_mcp/config.py`
- `mcp-servers/delta_macros_mcp/server.py`
- `mcp-servers/gitlab_mcp/__init__.py`
- `mcp-servers/gitlab_mcp/result.py`
- `mcp-servers/gitlab_mcp/config.py`
- `mcp-servers/gitlab_mcp/server.py`
- `tests/__init__.py`
- `tests/cobol_parser_mcp/__init__.py`
- `tests/cobol_parser_mcp/test_server.py`
- `tests/cobol_parser_mcp/fixtures/blackjack` (git submodule)
- `tests/specdb_mcp/__init__.py`
- `tests/specdb_mcp/test_server.py`
- `tests/delta_macros_mcp/__init__.py`
- `tests/delta_macros_mcp/test_server.py`
- `tests/gitlab_mcp/__init__.py`
- `tests/gitlab_mcp/test_server.py`
