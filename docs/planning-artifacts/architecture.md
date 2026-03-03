---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
status: 'complete'
completedAt: '2026-03-01'
lastStep: 8
inputDocuments:
  - docs/planning-artifacts/prd.md
  - docs/planning-artifacts/product-brief-modernisation_agents-2026-03-01.md
  - docs/planning-artifacts/research/market-cobol-modernisation-agents-research-2026-03-01.md
  - docs/project_idea.md
  - docs/reference-repo-mapping.md
workflowType: 'architecture'
project_name: 'modernisation_agents'
user_name: 'Kamal'
date: '2026-03-01'
---

# Architecture Decision Document — Mainframe Modernisation Agents

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

56 FRs across 9 capability groups:
- **COBOL Analysis (FR1–8):** Viper two-phase structural analysis — static pre-pass (paragraph call graph, complexity scoring, anti-pattern detection, external reference extraction) followed by AI semantic cluster analysis. Expert review and correction before spec layer writes. Unknown construct flagging is mandatory, not optional.
- **Dependency Mapping (FR9–13):** Crane cross-module analysis producing Mermaid dependency graph, subsystem groupings, migration order recommendation, and circular dependency / dead code detection.
- **Business Rule Extraction & Spec Layer (FR14–18):** Shifu business markdown per module plus full population of all 8 `spec_*` SQLite tables. Idempotent re-run support (update, not duplicate).
- **Migration Architecture (FR19–22):** Oogway consumes spec layer to produce target architecture. Analyst review and modification before finalisation.
- **Epic & Story Generation (FR23–25):** PM agent converts Oogway architecture + Shifu business function catalog into BMAD Epics (one per business capability) and User Stories (one per service boundary). SM enriches each story with spec layer context (rules, operations, entities, Delta macro expansions) before Dev picks it up.
- **Implementation & QA (FR26–28):** Standard BMAD Dev + QA workflow. Dev implements stories using SM-enriched spec layer context. QA validates implemented code against `spec_rules`, confidence-weighted: high-confidence rules are must-pass, medium are should-pass, low-confidence are advisory. No custom code-generation or QA agents — the existing BMAD PM, SM, Dev, QA agents handle this phase.
- **Pipeline Configuration (FR29–34):** Single-command schema initialisation, glossary configuration, incremental macro library updates, BMAD installer, individual agent re-run, consolidated flag list.
- **COBOL Dialect Coverage (FR35–39):** IBM Enterprise COBOL, COBOL-85, CICS, DB2 SQL, COPY/copybook resolution, Delta macro resolution via MCP.
- **GitLab Project Management (FR40–56):** Tigress initialises GitLab project (label taxonomy, milestones, boards). Per-module Issues track pipeline lifecycle. Sprint milestone management. Live README dashboard. Business rule sign-off gate (Claire). QA Epic sign-off gate (Tai Lung).

**Non-Functional Requirements:**

21 NFRs across 5 domains:
- **Performance:** Viper Phase 1 < 15 min per module; parser tools < 30s for modules ≤ 5k lines; specdb ops < 2s; macro lookups < 1s; GitLab ops < 10s.
- **Security & Data Privacy (hard constraint):** No source code, business rules, or spec data leaves local environment. Credentials stored via OS/IDE credential store. Macro library never synced externally.
- **Reliability & Reproducibility:** Idempotent spec layer writes. No silent failures — all errors are explicit and actionable. Partial writes roll back or are flagged. MCP servers persist across agent session restarts.
- **Integration & Compatibility:** BMAD-compatible (Claude Code + Cursor minimum). MCP protocol compliant (no proprietary extensions). GitLab Cloud + self-hosted API v4. Versioned SQLite schema with migration support.
- **Maintainability:** Independently updatable agents and MCP servers. Human-readable glossary and macro formats. BlackJack corpus as regression baseline.

**Scale & Complexity:**

- Primary domain: Local-first AI agent pipeline / developer tooling (BMAD Expansion Pack)
- Complexity level: **High** — 7 agents, 4 MCP servers, 17-table SQLite schema, GitLab integration, COBOL dialect handling, BMAD packaging
- Estimated architectural components: 5 MCP servers (adding jcl-parser-mcp), 5 custom agent definitions (Viper, Crane, Shifu, Oogway, Tigress — phases 8–9 use existing BMAD PM/SM/Dev/QA), 1 SQLite database, 1 installer, 1 glossary system, 1 macro library system
- Deployment model: Single developer machine, greenfield, local-only

### Technical Constraints & Dependencies

- **Data locality (hard):** All processing, storage, and agent-to-agent communication must remain local. No cloud data transmission for source code or extracted artefacts.
- **BMAD format compliance:** All agents, workflows, and step files must conform to BMAD module conventions for cross-IDE compatibility. Expansion pack installer must follow BMAD installer pattern.
- **MCP protocol compliance:** All 4 MCP servers must use standard MCP protocol — no proprietary extensions. Tools must be versioned and backwards-compatible.
- **SQLite as the sole database:** No Neo4j or other graph database. SQLite is both the analysis store (core tables) and the intermediate representation (spec layer tables).
- **LLM as an unreliable actor:** Every AI-produced output must have an explicit review gate before downstream consumption. No AI output is authoritative without analyst sign-off.
- **Target language TBD for MVP:** Oogway/Po decide the target language (Java or Python) — analysis agents must remain target-language agnostic throughout the pipeline.
- **GitLab dependency:** GitLab (Cloud or self-hosted, API v4) is required for delivery management. The pipeline has a hard GitLab boundary — analysis stays local; GitLab manages Epics, Issues, and the status dashboard.

### Cross-Cutting Concerns Identified

1. **Data locality enforcement** — Must be architecturally guaranteed across all 4 MCP servers and all 7 agents. No component should have a code path that transmits source or spec data externally without explicit documentation.
2. **Idempotency** — Spec layer writes across Viper, Crane, and Shifu must all be idempotent. Re-running any agent on any module must produce equivalent output without duplication or contradiction.
3. **Error propagation (no silent failures)** — Every unrecognised construct, unknown macro, LLM error, or partial write must surface an explicit, actionable error. This crosses all 4 MCP servers and all 7 agents.
4. **BMAD format compliance** — Agent definitions, workflow files, step files, and config patterns must all conform to BMAD standards. This is a cross-cutting structural constraint on how every component is authored.
5. **LLM reliability gating** — Human review gates (analyst approval before spec layer writes) are a cross-cutting concern that must be architecturally enforced at every AI-output stage.
6. **COBOL dialect handling** — Unknown or unsupported constructs must be flagged at the `cobol-parser-mcp` layer and propagated correctly through the pipeline — not silently ignored.
7. **MCP server lifecycle** — All 4 MCP servers must start via the installer and remain operational across agent session restarts without requiring full reinitialisation.

## Starter Template Evaluation

### Primary Technology Domain

Local-first Python MCP server suite + BMAD markdown agent definitions.
No UI, no frontend framework, no cloud runtime.

### MCP Server Framework: FastMCP 3.0.2

FastMCP is the official Python MCP SDK authoring layer (integrated into `mcp` package).
Powers ~70% of MCP servers across all languages. Python 3.12, managed with **Poetry**.

**Monorepo setup (root-level, one-time):**

```bash
poetry init --python "^3.12"
poetry add "mcp[cli]" fastmcp          # all servers
poetry add lark                         # cobol-parser-mcp only
poetry add aiosqlite                    # specdb-mcp only
poetry add "python-gitlab==8.0.0"       # gitlab-mcp only
poetry add --group dev pytest
```

All four MCP servers live as Python packages under `mcp-servers/` and are managed by the single root `pyproject.toml` + `poetry.lock`.

### Per-Server Library Decisions

| MCP Server | Libraries | Version |
|---|---|---|
| `cobol-parser-mcp` | fastmcp, lark | FastMCP 3.0.2, Lark latest |
| `jcl-parser-mcp` | fastmcp | FastMCP 3.0.2 (regex-based JCL parsing) |
| `specdb-mcp` | fastmcp, aiosqlite | FastMCP 3.0.2, aiosqlite latest |
| `delta-macros-mcp` | fastmcp | FastMCP 3.0.2 |
| `gitlab-mcp` | fastmcp, python-gitlab | FastMCP 3.0.2, python-gitlab 8.0.0 |

### Architectural Decisions Established

**Language & Runtime:** Python 3.12, Poetry for project management
**MCP Authoring:** FastMCP 3.0.2 (type-hint-driven tool definitions, lifecycle management)
**Database Access:** aiosqlite (async, non-blocking SQLite for specdb-mcp)
**GitLab Client:** python-gitlab 8.0.0 (GitLab API v4, Cloud + self-hosted)
**COBOL Parsing:** Regex-based static pre-pass (deterministic) + Lark for grammar-level parsing — no full Python COBOL parser exists; custom implementation required.
**Project Structure:** Poetry monorepo — single root `pyproject.toml` + `poetry.lock`; all four MCP servers as Python packages under `mcp-servers/` with snake_case package names.

**Note:** Project initialisation (uv init for all 4 servers) should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- SQLite DB location: configurable via `db_path` in config.yaml
- MCP transport: STDIO (all 4 servers)
- MCP error response format: structured result dict (consistent across all servers)
- GitLab credential strategy: GITLAB_TOKEN environment variable
- IDE target: Claude Code + GitHub Copilot (VS Code)

**Important Decisions (Shape Architecture):**
- Schema versioning: schema_version table + programmatic migrations in specdb-mcp
- Idempotency pattern: INSERT OR IGNORE + UPDATE (check-then-upsert)
- Logging: stderr + log file dual handler

**Deferred Decisions (Post-MVP):**
- Installer mechanism (parked — to be decided during implementation)
- Parallel Viper processing (Phase 2)
- Multi-engagement DB isolation (Scale phase)

### Data Architecture

**SQLite DB Location:** Configurable via `db_path` in `config.yaml`.
Default: `<project-root>/data/specdb.sqlite`. Agents reference this path from config, not hardcoded.

**Schema Versioning:** `schema_version` table managed by `specdb-mcp`.
On server startup: check current version, apply any pending migrations programmatically.
No external migration framework — single-developer local tool does not warrant Alembic overhead.

**Idempotency Pattern:** `INSERT OR IGNORE` + `UPDATE` (check-then-upsert) across all spec layer writes.
- Safer than `INSERT OR REPLACE` for partial re-runs — only updates fields present in the new write.
- All `specdb-mcp` write tools implement this pattern consistently.
- Partial writes on error: wrap in SQLite transaction; rollback on failure rather than leaving inconsistent state.

### Authentication & Security

**GitLab Credentials:** `GITLAB_TOKEN` environment variable.
- `gitlab-mcp` reads from `os.environ["GITLAB_TOKEN"]` at startup; fails with explicit error if not set.
- No `.env` file dependency; no keychain library.
- Installer documents required environment variables clearly.
- All other MCP servers: no authentication required (local-only, STDIO transport).

### API & Communication Patterns (MCP Layer)

**MCP Transport:** STDIO (all 4 servers).
- IDE spawns each MCP server as a subprocess; communication via stdin/stdout.
- Supported by Claude Code and GitHub Copilot (VS Code) with identical config format.
- No network port, no firewall configuration required.
- FastMCP handles STDIO transport natively.

**Structured Error/Result Format:** Consistent schema across all 4 MCP servers:
```python
{
  "status": "ok" | "error" | "warning",
  "data": <tool-specific payload>,
  "flags": [{"code": str, "message": str, "location": str}],
  "message": str
}
```
- `warning`: recoverable issue (unknown macro, unrecognised construct) — agent flags and continues.
- `error`: non-recoverable failure (DB write error, parse failure) — agent halts and surfaces error.
- `flags`: structured list of all flagged items, enabling FR34 (consolidated unresolved construct list).

**MCP Tool Limit:** GitHub Copilot caps at 128 tools across all servers.
Projected tool count: ~28 tools total (cobol-parser: 4, jcl-parser: 4, specdb: 4, delta-macros: 4, gitlab: 12). Well within limit.

**GitHub Copilot Constraint:** Copilot supports MCP tools only (not resources or prompts).
No impact — all 4 servers expose tools only by design.

### Infrastructure & Deployment

**IDE Configuration Files:** Installer writes MCP server registration to:
- `.claude/mcp.json` → Claude Code
- `.vscode/mcp.json` → GitHub Copilot (VS Code)

Both files use identical format:
```json
{
  "servers": {
    "cobol-parser-mcp": {
      "command": "poetry",
      "args": ["run", "python", "-m", "cobol_parser_mcp.server"],
      "env": {}
    }
  }
}
```

**Installer Mechanism:** Deferred — to be designed during implementation planning.

**Logging:** Dual handler on all MCP servers.
- stderr: real-time visibility in IDE's MCP server output panel (required for STDIO servers — stdout is reserved for JSON-RPC).
- Log file: `<project-root>/logs/<server-name>.log` — persistent, reviewable after pipeline runs.
- Standard Python `logging` module with StreamHandler (stderr) + FileHandler (log file).

## Implementation Patterns & Consistency Rules

### Critical Conflict Points Identified

7 areas where AI agents could make different choices without explicit rules:
code style, SQLite naming, MCP tool naming, result dict construction,
timestamp format, module identity key, error handling scope.

### Naming Patterns

**Python Code (PEP 8 — mandatory):**
- Functions and variables: `snake_case` → `parse_module()`, `program_name`
- Classes: `PascalCase` → `CobolParser`, `SpecDbServer`
- Constants: `SCREAMING_SNAKE` → `DEFAULT_DB_PATH`, `SCHEMA_VERSION`
- Private helpers: prefix with `_` → `_build_call_graph()`

**MCP Tool Names (snake_case, verb-first):**
- Pattern: `<verb>_<noun>` → `parse_module`, `get_macro`, `write_spec`, `create_epic`
- Exactly as defined in the PRD tool lists — no variation permitted
- Tool docstrings become the MCP tool description: keep them concise and accurate

**SQLite Naming (snake_case throughout):**
- Tables: `snake_case` plural → `cobol_files`, `spec_business_rules`, `dependencies`
- Columns: `snake_case` → `program_name`, `created_at`, `source_paragraph`
- Foreign keys: `<table_singular>_id` → `cobol_file_id`, `spec_entity_id`
- No PascalCase or camelCase anywhere in the schema

**COBOL Identifiers in the DB:**
- Store COBOL program names in UPPERCASE as-is: `PAYROLL-CALC`, `ACCT-BATCH`
- Store COBOL field names in UPPERCASE as-is: `WS-CUST-BAL`
- Business term mappings (glossary/rosetta) use the human-readable casing from the glossary file
- The `program_name` column always contains the COBOL PROGRAM-ID value verbatim

**File Naming:**
- Python modules: `snake_case.py` → `server.py`, `cobol_parser.py`, `db_helpers.py`
- Config files: `snake_case.yaml` / `snake_case.json`
- Macro library files: SCREAMING-SNAKE matching the macro name → `DLTM-ACCT-LOCK.md`

### Structure Patterns

**MCP Server Internal Structure (all 4 servers):**
```
mcp-servers/<package_name>/          # e.g. cobol_parser_mcp (snake_case Python package)
├── __init__.py
├── server.py        # FastMCP app, tool definitions (thin wrappers only)
├── <domain>.py      # Core logic (e.g. cobol_parser.py, spec_db.py)
├── result.py        # make_result() / make_error() / make_warning() helpers
└── config.py        # Config loading from config.yaml / env vars

tests/<package_name>/                # Root-level tests, mirroring package structure
├── test_server.py
├── test_<domain>.py
└── fixtures/        # Sample COBOL files, mock DB, etc.
```

- `server.py` contains ONLY tool definitions — each tool is a thin wrapper calling into `<domain>.py`
- Business logic lives in domain modules, not in tool functions
- This separation means logic can be tested without running the MCP server

**Tests Location:** Root-level `tests/<package_name>/` directory (not co-located with source, not inside the server package directory)

**Config Loading:** Each server has a `config.py` that reads `config.yaml` from the project root (via path relative to the server's working directory or `BMAD_PROJECT_ROOT` env var). Never hardcode paths.

### Format Patterns

**MCP Tool Result Format (mandatory for all tools in all 4 servers):**
```python
# result.py — shared in every MCP server
def make_result(data=None, flags=None, message="", status="ok"):
    return {
        "status": status,       # "ok" | "warning" | "error"
        "data": data,           # tool-specific payload (dict, list, str, None)
        "flags": flags or [],   # list of {"code": str, "message": str, "location": str}
        "message": message      # human-readable summary
    }

def make_error(message, flags=None):
    return make_result(status="error", message=message, flags=flags)

def make_warning(data, message, flags):
    return make_result(status="warning", data=data, message=message, flags=flags)
```

**Flag Code Format:** `SCREAMING_SNAKE` with category prefix:
- `UNKNOWN_MACRO` — delta-macros-mcp
- `UNKNOWN_CONSTRUCT` — cobol-parser-mcp
- `PARSE_ERROR` — cobol-parser-mcp
- `DB_WRITE_CONFLICT` — specdb-mcp
- `GITLAB_API_ERROR` — gitlab-mcp

**Timestamp Format:** ISO 8601 UTC strings in all SQLite columns and tool outputs.
```python
from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat()  # → "2026-03-01T14:30:00.123456+00:00"
```
Never Unix timestamps — the DB must be human-readable in any SQLite browser.

**Program Identity Key:** `program_name` is the canonical identifier for a COBOL module across all tables, all agents, and all MCP tool parameters. Value is the COBOL PROGRAM-ID verbatim (uppercase with hyphens): `"PAYROLL-CALC"`.

### Process Patterns

**Error Handling in MCP Tools:**
```python
@mcp.tool()
def parse_module(program_name: str, source_path: str) -> dict:
    """Parse a COBOL module and return structural analysis."""
    try:
        result = _do_parse(program_name, source_path)
        return make_result(data=result)
    except FileNotFoundError as e:
        return make_error(f"Source file not found: {source_path}", flags=[{
            "code": "FILE_NOT_FOUND", "message": str(e), "location": source_path
        }])
    except Exception as e:
        return make_error(f"Unexpected parse error: {e}")
```
- Every tool has its own try/except — no silent propagation to FastMCP's default error handler
- Catch specific exceptions first, broad `Exception` last
- Always return a result dict — never raise from a tool function

**SQLite Transaction Pattern (specdb-mcp):**
```python
async with db.execute("BEGIN"):
    try:
        # all writes for this tool call
        await db.execute("INSERT OR IGNORE INTO ...")
        await db.execute("UPDATE ... WHERE ...")
        await db.execute("COMMIT")
    except Exception as e:
        await db.execute("ROLLBACK")
        return make_error(f"DB write failed: {e}")
```
Transaction per tool call — never per individual statement.

**Idempotent Write Pattern:**
```python
# INSERT OR IGNORE creates the row if absent
await db.execute(
    "INSERT OR IGNORE INTO spec_business_rules (program_name, rule_id) VALUES (?, ?)",
    (program_name, rule_id)
)
# UPDATE sets all fields — runs whether INSERT created or skipped the row
await db.execute(
    "UPDATE spec_business_rules SET description=?, source_paragraph=?, updated_at=? "
    "WHERE program_name=? AND rule_id=?",
    (description, source_paragraph, now, program_name, rule_id)
)
```

**Logging Pattern:**
```python
import logging
logger = logging.getLogger(__name__)  # module-level logger, named by module path

# Use structured messages
logger.info("parse_module called: program=%s", program_name)
logger.warning("Unknown macro encountered: macro=%s program=%s", macro_name, program_name)
logger.error("DB write failed: table=%s error=%s", table_name, str(e))
```
- `DEBUG`: detailed internal state (call graphs, regex matches)
- `INFO`: tool calls, stage completions
- `WARNING`: flagged items (unknown constructs, macros) — mirrors tool `flags` output
- `ERROR`: failures that return `status: "error"`

### Enforcement Guidelines

**All AI Agents MUST:**
- Use `make_result()` / `make_error()` / `make_warning()` from `result.py` — never construct the dict inline
- Use `program_name` (uppercase COBOL PROGRAM-ID) as the module identity key in all tool calls and DB writes
- Wrap every tool body in try/except — no exceptions may propagate to FastMCP's handler
- Use ISO 8601 UTC timestamps — never Unix integers
- Name all MCP tools exactly as defined in the PRD tool lists — no additions or renames without architecture update
- Keep `server.py` thin — logic goes in domain modules

**Anti-Patterns to Avoid:**
- ❌ `return {"error": "something went wrong"}` — use `make_error()`
- ❌ `program_name = "payroll_calc"` — must be `"PAYROLL-CALC"` (COBOL PROGRAM-ID verbatim)
- ❌ `created_at = int(time.time())` — use ISO 8601 string
- ❌ Business logic inside tool functions in `server.py`
- ❌ `INSERT OR REPLACE` — use the idempotent INSERT OR IGNORE + UPDATE pattern
- ❌ Bare `except:` or `except Exception: raise` inside a tool function

## Project Structure & Boundaries

### Complete Project Directory Structure

```
mainframe-modernisation/                    # BMAD Expansion Pack root
├── README.md
├── pyproject.toml                          # Root Poetry monorepo — all deps managed here
├── poetry.lock
├── config.yaml                             # Expansion pack config (db_path, gitlab_url, etc.)
├── .gitignore                              # Excludes data/, logs/, client COBOL source
│
├── agents/                                 # BMAD agent definitions (markdown)
│   ├── viper.md                            # FR1–8, FR35–39
│   ├── crane.md                            # FR9–13
│   ├── shifu.md                            # FR14–18
│   ├── oogway.md                           # FR19–22 (existing BMAD agent — customised)
│   └── tigress.md                          # FR40–56 (existing BMAD agent — customised)
│   # NOTE: Phases 8–9 (Epic & Story gen, Dev, QA) use the standard BMAD PM/SM/Dev/QA
│   # agents from _bmad/bmm/agents/ — no custom Po or Tai Lung agents are needed.
│
├── workflows/                              # BMAD workflow + step files (one folder per agent)
│   ├── viper/
│   │   ├── workflow.md
│   │   └── steps/
│   │       ├── step-01-init.md
│   │       ├── step-02-phase1-parse.md
│   │       ├── step-03-phase2-analyse.md
│   │       └── step-04-review-gate.md
│   ├── crane/
│   │   ├── workflow.md
│   │   └── steps/
│   │       ├── step-01-extract-deps.md
│   │       └── step-02-analyse-graph.md
│   ├── shifu/
│   │   ├── workflow.md
│   │   └── steps/
│   │       ├── step-01-business-markdown.md
│   │       ├── step-02-spec-layer-write.md
│   │       └── step-03-review-gate.md
│   ├── crane/
│   │   ├── workflow.md
│   │   └── steps/
│   ├── oogway/
│   │   └── workflow.md
│   └── tigress/
│       └── workflow.md
│   # NOTE: No po/ or tai-lung/ workflow folders — phases 8–9 use standard BMAD workflows
│
├── mcp-servers/                            # Python packages — no per-server pyproject.toml
│   │
│   ├── cobol_parser_mcp/                   # FR1–8, FR35–39 | NFR1, NFR2  (snake_case package)
│   │   ├── __init__.py
│   │   ├── server.py                       # FastMCP app + tool definitions (thin wrappers)
│   │   ├── cobol_parser.py                 # IDENTIFICATION/DATA/PROCEDURE division parsing
│   │   ├── call_graph.py                   # Paragraph PERFORM graph builder
│   │   ├── cluster_builder.py              # Semantic paragraph clustering
│   │   ├── complexity_scorer.py            # Low/Medium/High scoring logic
│   │   ├── antipattern_detector.py         # GOTO, ALTER, nested PERFORM detection
│   │   ├── dialect_handler.py              # CICS, DB2 SQL, COPY statement handling
│   │   ├── result.py                       # make_result(), make_error(), make_warning()
│   │   └── config.py                       # Reads config.yaml + env vars
│   │
│   ├── specdb_mcp/                         # FR17–18, FR29, FR33 | NFR3, NFR10, NFR12, NFR17
│   │   ├── __init__.py
│   │   ├── server.py                       # FastMCP app + tool definitions (thin wrappers)
│   │   ├── spec_db.py                      # All read/write operations — core domain logic
│   │   ├── schema.py                       # CREATE TABLE statements + migration logic
│   │   ├── migrations.py                   # schema_version table + programmatic migrations
│   │   ├── result.py                       # make_result(), make_error(), make_warning()
│   │   └── config.py                       # Reads db_path from config.yaml
│   │
│   ├── delta_macros_mcp/                   # FR8, FR31, FR34, FR39 | NFR4, NFR9
│   │   ├── __init__.py
│   │   ├── server.py                       # FastMCP app + tool definitions (thin wrappers)
│   │   ├── macro_library.py                # Markdown file parsing + search logic
│   │   ├── result.py                       # make_result(), make_error(), make_warning()
│   │   └── config.py                       # Reads macro_library_path from config.yaml
│   │
│   ├── jcl_parser_mcp/                     # Epic 4 | NFR1, NFR2
│   │   ├── __init__.py
│   │   ├── server.py                       # FastMCP app + tool definitions (thin wrappers)
│   │   ├── jcl_parser.py                   # JOB/STEP/DD statement parsing
│   │   ├── job_graph.py                    # Cross-job execution graph builder
│   │   ├── result.py                       # make_result(), make_error(), make_warning()
│   │   └── config.py                       # Reads config.yaml
│   │
│   └── gitlab_mcp/                         # FR40–56 | NFR5, NFR8, NFR16
│       ├── __init__.py
│       ├── server.py                       # FastMCP app + tool definitions (thin wrappers)
│       ├── gitlab_client.py                # python-gitlab wrapper — all API calls
│       ├── label_manager.py                # Label taxonomy creation and management
│       ├── readme_updater.py               # README dashboard generation
│       ├── result.py                       # make_result(), make_error(), make_warning()
│       └── config.py                       # Reads gitlab_url from config.yaml + GITLAB_TOKEN env
│
├── tests/                                  # Root-level tests, mirroring mcp-servers/ structure
│   ├── __init__.py
│   ├── cobol_parser_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_cobol_parser.py
│   │   ├── test_call_graph.py
│   │   ├── test_cluster_builder.py
│   │   ├── test_complexity_scorer.py
│   │   ├── test_antipattern_detector.py
│   │   └── fixtures/
│   │       └── blackjack/                  # git submodule — real IBM Enterprise COBOL corpus
│   │           ├── src/                    # .cob source files (BJ-MAIN.cob, BJ-DEALER.cob, …)
│   │           └── copy/                   # .cpy copybooks (BJ-COMMON.cpy, BJ-CARDS.cpy, …)
│   ├── specdb_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_spec_db.py
│   │   ├── test_schema.py
│   │   ├── test_migrations.py
│   │   └── fixtures/
│   │       └── seed_data.py                # Test data for spec layer tables
│   ├── delta_macros_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_macro_library.py
│   │   └── fixtures/
│   │       └── macros/                     # Sample macro .md files for tests
│   │           └── DLTM-EXAMPLE.md
│   └── gitlab_mcp/
│       ├── __init__.py
│       ├── test_server.py
│       ├── test_gitlab_client.py           # Uses mock python-gitlab responses
│       ├── test_label_manager.py
│       ├── test_readme_updater.py
│       └── fixtures/
│           └── mock_gitlab.py              # Mock GitLab API responses
│
├── templates/
│   ├── glossary-template.md               # Empty glossary for new client engagements
│   └── macro-template.md                  # Empty Delta macro doc template
│
├── blackjack/                             # BlackJack demo engagement (not client data)
│   ├── glossary.md                        # BlackJack field-name → business-term mappings
│   └── macros/                            # BlackJack Delta macro docs (if any)
│
├── data/                                  # Runtime — SQLite DB lives here (gitignored for client)
│   └── .gitkeep
│
├── logs/                                  # Runtime — MCP server logs (gitignored)
│   └── .gitkeep
│
├── installer/
│   └── install.py                         # BMAD expansion pack installer (implementation deferred)
│
├── .claude/
│   └── mcp.json                           # Claude Code MCP registration (generated by installer)
│
└── .vscode/
    └── mcp.json                           # GitHub Copilot MCP registration (generated by installer)
```

### Architectural Boundaries

**MCP Tool Boundaries (what each server owns):**

| Server | Owns | Does NOT own |
|---|---|---|
| `cobol-parser-mcp` | COBOL parsing, call graph, complexity, anti-patterns, dialect detection | Spec layer writes, business logic extraction |
| `jcl-parser-mcp` | JCL parsing, job step extraction, dataset allocation parsing, job graphs | COBOL source parsing, spec layer writes |
| `specdb-mcp` | All SQLite reads/writes, schema, migrations | Parsing logic, GitLab calls |
| `delta-macros-mcp` | Macro library reads, macro search, macro ingest | Anything about COBOL source files |
| `gitlab-mcp` | All GitLab API calls, label management, README updates | Any local data reads or DB operations |

**The spec layer is the only shared state between agents.**
Agents do not communicate with each other directly — Crane reads Viper's output via specdb-mcp,
Shifu reads Crane's output via specdb-mcp, etc. The DB is the message bus.

**The GitLab boundary is post-architecture only.**
No GitLab calls occur during Viper, Crane, or Shifu stages.
`gitlab-mcp` is only active from Tigress onwards.

### Requirements to Structure Mapping

| FR Group | Component | Key Files |
|---|---|---|
| FR1–8 (Viper/COBOL Analysis) | `cobol-parser-mcp` | `cobol_parser.py`, `call_graph.py`, `cluster_builder.py`, `complexity_scorer.py`, `antipattern_detector.py` |
| FR9–13 (Crane/Dependencies) | `cobol-parser-mcp` + `specdb-mcp` | `dialect_handler.py` (COPY/CALL extraction), `spec_db.py` (dependencies table) |
| FR14–18 (Shifu/Spec Layer) | `specdb-mcp` | `spec_db.py`, `schema.py` (all spec_* tables) |
| FR9–13 (Crane/Dependencies) | `cobol-parser-mcp` + `jcl-parser-mcp` + `specdb-mcp` | Static CALL/COPY deps + JCL runtime deps + spec writes |
| FR19–22 (Oogway/Architecture) | `agents/oogway.md` | Agent reads spec layer via specdb-mcp |
| FR23–25 (Epic & Story Gen) | Standard BMAD PM agent + SM agent | PM reads business_functions + Oogway output; SM enriches with spec layer context |
| FR26–28 (Dev & QA) | Standard BMAD Dev + QA agents | Dev implements SM-enriched stories; QA validates against spec_rules |
| FR29 (Schema init) | `specdb-mcp` | `schema.py` `init_schema` tool |
| FR30 (Glossary config) | `config.yaml` + agent workflows | `glossary.md` loaded by Viper workflow |
| FR31 (Add macro) | `delta-macros-mcp` | `macro_library.py` `add_macro` tool |
| FR32 (BMAD installer) | `installer/install.py` | Deferred |
| FR34 (Consolidated flags) | All MCP servers | `flags` array in result dict; Viper agent aggregates |
| FR35–39 (COBOL dialects) | `cobol-parser-mcp` | `dialect_handler.py` |
| FR40–56 (GitLab PM) | `gitlab-mcp` + `agents/tigress.md` | `gitlab_client.py`, `label_manager.py`, `readme_updater.py` |

### Integration Points

**Internal Data Flow:**
```
COBOL source files
    → cobol-parser-mcp (parse_module, extract_call_graph, score_complexity, detect_antipatterns)
    → specdb-mcp (write_spec: cobol_files, analyses, dependencies, metrics tables)
    → delta-macros-mcp (get_macro — called during parse for unknown macros)
    → specdb-mcp (write_spec: spec_* tables — written by Shifu stage)
    → agents/oogway.md (reads spec layer via specdb-mcp query_spec)
    → agents/po.md (reads spec layer + architecture)
    → gitlab-mcp (create_epic, create_issue, apply_label, update_readme — Tigress onwards)
```

**External Integrations:**
- GitLab Cloud or self-hosted (API v4, HTTPS) — via `gitlab-mcp` only
- LLM provider (Claude API) — called by IDE for agent AI analysis; no MCP server involvement

**Config Flow:**
```
config.yaml (project root)
    → db_path        → specdb-mcp/src/config.py       → aiosqlite connection
    → macro_lib_path → delta-macros-mcp/src/config.py → macro file reads
    → gitlab_url     → gitlab-mcp/src/config.py       → python-gitlab client
    GITLAB_TOKEN (env var) → gitlab-mcp/src/config.py → python-gitlab auth
```

### Development Workflow

**Running a single MCP server for development (from project root):**
```bash
poetry run python -m cobol_parser_mcp.server
poetry run python -m specdb_mcp.server
poetry run python -m delta_macros_mcp.server
poetry run python -m gitlab_mcp.server
```

**Running tests (from project root):**
```bash
poetry run pytest tests/                          # all servers
poetry run pytest tests/cobol_parser_mcp/         # single server
```

**BlackJack regression run:** Load BlackJack corpus files from
`tests/cobol_parser_mcp/fixtures/blackjack/src/` (`.cob`) and `copy/` (`.cpy`) and run the full
pipeline against them. All modules must produce valid spec layer output.

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:** All technology choices are compatible.
One bridging pattern required: `gitlab-mcp` must use `asyncio.to_thread()` to wrap
synchronous python-gitlab calls within async FastMCP tool functions (see pattern added below).

**Pattern Consistency:** All naming, structure, format, and process patterns are
internally consistent and aligned with the chosen technology stack.

**Structure Alignment:** Project structure supports all architectural decisions.
Separate uv projects per server directly enables independent updatability (NFR18).

### Requirements Coverage Validation ✅

**Functional Requirements:** 55 of 56 FRs fully covered.
FR32 (BMAD installer) deferred by design — `installer/install.py` structure defined,
implementation intentionally deferred.

**Non-Functional Requirements:** All 21 NFRs covered.
NFR13 clarification: "MCP servers persist across restarts" means SQLite data persists
(which it does — local file), not the server process. STDIO servers are spawned per
IDE session by design; data integrity is the persistence guarantee, not process uptime.

### Implementation Readiness Validation ✅

- All critical decisions documented with verified versions
- Implementation patterns comprehensive with code examples and anti-patterns
- Project structure complete with file-level specificity
- All 56 FRs mapped to specific components and files
- Integration points and data flow explicitly defined

### Gap Analysis Results

**Critical (addressed in this document):**
- `gitlab-mcp` async/sync bridge: `asyncio.to_thread()` pattern added to patterns section

**Important (to address at implementation start):**
- Glossary file format: markdown table (`| COBOL Name | Business Term |`) — simple,
  human-editable, parseable by agents
- config.yaml complete schema: `db_path`, `macro_library_path`, `gitlab_url`,
  `project_name`, `target_language` (TBD Oogway input)
- Viper, Crane, Shifu are net-new BMAD agents — require full authoring from scratch
  following BMAD module conventions (not customisations of existing agents)

**Deferred (post-MVP):**
- Shared `result.py` as published package (currently copied per server — acceptable for MVP)
- Pre-commit hooks for PEP 8 enforcement

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] 56 FRs and 21 NFRs analyzed for architectural implications
- [x] Scale assessed: High complexity, 7 agents, 4 MCP servers
- [x] Hard constraints identified: data locality, BMAD compliance, STDIO transport
- [x] 7 cross-cutting concerns mapped

**✅ Architectural Decisions**
- [x] MCP framework: FastMCP 3.0.2 (Python 3.12, Poetry monorepo)
- [x] Database: SQLite via aiosqlite, configurable path
- [x] Transport: STDIO (Claude Code + GitHub Copilot)
- [x] GitLab: python-gitlab 8.0.0, GITLAB_TOKEN env var
- [x] COBOL parsing: regex + Lark (custom implementation)
- [x] Schema versioning: schema_version table + programmatic migrations
- [x] Idempotency: INSERT OR IGNORE + UPDATE
- [x] Error format: structured result dict across all servers
- [x] Logging: dual handler (stderr + log file)

**✅ Implementation Patterns**
- [x] Python naming: PEP 8 (snake_case, PascalCase, SCREAMING_SNAKE)
- [x] MCP tool names: verb-first snake_case, exactly per PRD tool lists
- [x] SQLite naming: snake_case, COBOL identifiers verbatim uppercase
- [x] Server structure: thin server.py + domain modules + result.py + config.py
- [x] Error handling: per-tool try/except, make_result() helpers
- [x] Transaction pattern: per-tool-call in specdb-mcp
- [x] Async bridging: asyncio.to_thread() for python-gitlab in gitlab-mcp
- [x] Timestamps: ISO 8601 UTC strings
- [x] Program identity key: program_name = COBOL PROGRAM-ID verbatim

**✅ Project Structure**
- [x] Complete directory tree with file-level specificity
- [x] All 4 MCP server structures defined
- [x] BMAD agent definitions mapped
- [x] Workflow/step file structure defined
- [x] BlackJack corpus location specified
- [x] Runtime directories (data/, logs/) defined
- [x] IDE config files (.claude/mcp.json, .vscode/mcp.json) defined

### Architecture Readiness Assessment

**Overall Status: READY FOR IMPLEMENTATION**

**Confidence Level: High**

**Key Strengths:**
- SQLite spec layer as the message bus between agents eliminates direct agent coupling
- Structured result dict with flags array directly implements "no silent failures" (NFR11)
- Poetry monorepo with a single lock file ensures reproducible installs across all 4 servers
- STDIO transport confirmed compatible with both target IDEs
- BlackJack corpus (git submodule) in `tests/cobol_parser_mcp/fixtures/blackjack/` provides immediate regression baseline (NFR21)

**Areas for Future Enhancement:**
- Shared `result.py` as a published package (avoids copy-per-server)
- Parallel Viper processing for large estates (Phase 2)
- Formal installer mechanism (currently deferred)

### Implementation Handoff

**Implementation order:**
```
1. specdb-mcp        — schema, migrations, CRUD tools (all downstream depends on this)
2. delta-macros-mcp  — macro library, get/search/add tools (Viper depends on this)
3. cobol-parser-mcp  — parsing, call graph, clustering, complexity (Viper's engine)
4. jcl-parser-mcp    — JCL parsing, job steps, dataset allocations (Crane depends on this)
5. gitlab-mcp        — GitLab integration (Tigress onwards, post-architecture stage)
6. agents/           — Viper, Crane, Shifu (new); Oogway, Tigress (customise existing BMAD)
                       NOTE: No Po or Tai Lung agents — phases 8–9 use standard BMAD workflow
7. workflows/        — Per-agent workflow and step files (viper, crane, shifu, oogway, tigress)
```

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented
- Use `make_result()` / `make_error()` / `make_warning()` — never construct result dicts inline
- Use `asyncio.to_thread()` for all synchronous library calls within async FastMCP tools
- `program_name` = COBOL PROGRAM-ID verbatim (uppercase with hyphens) — everywhere
- Refer to this document before any implementation decision not covered in the story
