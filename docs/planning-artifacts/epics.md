---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics', 'step-03-create-stories', 'step-04-final-validation']
inputDocuments:
  - docs/planning-artifacts/prd.md
  - docs/planning-artifacts/architecture.md
---

# modernisation_agents - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for modernisation_agents (Mainframe Modernisation Agents), decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**COBOL Analysis (Viper)**
- FR1: Analyst can initiate structural analysis of a COBOL module and receive a paragraph call graph
- FR2: Analyst can view a complexity score (Low/Medium/High) for any analysed COBOL module
- FR3: Analyst can view anti-patterns detected in a COBOL module (GOTOs, nested PERFORMs, REDEFINES, etc.)
- FR4: Analyst can view extracted COPY, CALL, SQL, CICS, and Delta macro references per module
- FR5: Analyst can view AI-generated semantic cluster groupings for a module's paragraphs
- FR6: Analyst can view plain-English descriptions for each semantic cluster
- FR7: Analyst can review, correct, and approve AI analysis outputs before they are written to the spec layer
- FR8: Analyst can view a warning when Viper encounters an unrecognised COBOL construct or unknown Delta macro

**Dependency Mapping (Crane)**
- FR9: Analyst can initiate cross-module dependency analysis across all COBOL modules in scope
- FR10: Architect can view a Mermaid dependency diagram showing relationships between all modules
- FR11: Architect can view detected subsystem groupings emerging from the dependency structure
- FR12: Architect can view a recommended migration order based on module dependencies
- FR13: Analyst can view detected circular dependencies and dead code across modules

**Business Rule Extraction & Spec Layer (Shifu)**
- FR14: Analyst can initiate business rule extraction for a COBOL module using Viper and Crane outputs
- FR15: Business Validator can view plain-English business markdown for any module (purpose, use cases, business rules, data entities with glossary names)
- FR16: Business Validator can validate each extracted business rule as confirmed, corrected, or rejected
- FR17: System writes approved business rules, entities, operations, and data flows to the SQLite spec layer
- FR18: Analyst can re-run Shifu on a module and have the spec layer update idempotently without duplicates

**Migration Architecture (Oogway)**
- FR19: Architect can initiate migration architecture generation from the populated spec layer
- FR20: Architect can view a target architecture document mapping COBOL subsystems to target-language services
- FR21: Architect can specify the target language as an input to Oogway
- FR22: Architect can review and modify the generated architecture before it is finalised

**Code Generation (Po)**
- FR23: Developer can initiate target-language code generation for a module from the spec layer and architecture
- FR24: Developer can view generated target-language code for each COBOL module
- FR25: Developer can regenerate code for a specific module without affecting other modules

**QA Validation (Tai Lung)**
- FR26: QA can initiate validation of generated code against spec layer business rules
- FR27: QA can view a validation report showing which business rules are confirmed, partially covered, or missing in the generated code
- FR28: QA can flag a module as requiring rework before sign-off

**Pipeline Configuration & Infrastructure**
- FR29: Operator can initialise the SQLite spec layer schema with a single command via specdb-mcp
- FR30: Analyst can configure a client-specific glossary mapping COBOL field names to business terms
- FR31: Analyst can add a new macro definition to delta-macros-mcp without restarting the pipeline
- FR32: Operator can install the full BMAD expansion pack into any BMAD-compatible IDE via a standard installer
- FR33: Analyst can re-run any individual agent on a specific module without restarting the full pipeline
- FR34: Analyst can view a consolidated list of all unresolved constructs and macros flagged across pipeline stages

**COBOL Dialect & Construct Coverage**
- FR35: System can parse and analyse IBM Enterprise COBOL and COBOL-85 modules
- FR36: System can detect and flag CICS transaction constructs within a COBOL module
- FR37: System can detect and flag DB2 embedded SQL constructs within a COBOL module
- FR38: System can parse COPY statements and resolve referenced copybooks
- FR39: All agents can resolve client-specific Delta macro references via delta-macros-mcp at analysis time

**GitLab Project Management (Tigress + All Agents)**

*Project Initialisation*
- FR40: PM can initialise a GitLab project with standard label taxonomy: pipeline stage labels (Viper-Complete, Crane-Complete, Shifu-Complete, Oogway-Complete, Po-Complete, QA-Complete), complexity labels (Complexity::Low, Complexity::Medium, Complexity::High), and status labels (In-Analysis, Awaiting-Review, In-Migration, Blocked, Done)
- FR41: PM can create a standard milestone structure per engagement phase (e.g., Phase-1-Prove, Phase-2-Complete) in GitLab
- FR42: PM can create a GitLab issue board configured with columns mapped to pipeline stages

*Module Lifecycle Tracking*
- FR43: Each COBOL module has a dedicated GitLab Issue tracking its complete pipeline lifecycle from analysis through QA sign-off
- FR44: Any agent can apply the appropriate stage completion label to a module's GitLab Issue upon completing its stage
- FR45: Any agent can transition a module Issue to Awaiting-Review status when its stage output requires analyst approval
- FR46: Analyst can close the review gate on a module Issue and transition it to the next pipeline stage

*Sprint & Iteration Planning*
- FR47: PM can create GitLab sprint milestones scoped to a specific set of modules based on Crane's migration order recommendation
- FR48: PM can assign module Issues to sprint milestones, respecting subsystem dependencies
- FR49: PM can view a milestone burndown showing open vs closed module Issues within a sprint

*Progress Reporting*
- FR50: Any agent can post a structured progress comment to a module's GitLab Issue when it completes a stage, including key outputs and any warnings or flags
- FR51: The GitLab project README is updated by any agent that changes module status — always reflects current pipeline state without manual intervention
- FR52: Client Sponsor can view a README dashboard showing total modules, modules per pipeline stage, modules blocked, and Epics signed off — at any time without requesting a status update
- FR53: PM can generate a milestone summary comment on any Epic showing sprint progress and outstanding items

*Review Gates & Sign-off*
- FR54: Business Validator can formally sign off on Shifu's business markdown by closing the Awaiting-Review gate on a module Issue
- FR55: QA can sign off on an Epic, triggering Epic completion in GitLab with a validation summary comment
- FR56: QA can formally close an Epic when all module Issues within it are QA-Complete

### NonFunctional Requirements

**Performance**
- NFR1: Viper Phase 1 static pre-pass completes on any single COBOL module within 15 minutes on standard developer hardware
- NFR2: cobol-parser-mcp parsing tools return results within 30 seconds for any module up to 5,000 lines
- NFR3: specdb-mcp read and write operations complete within 2 seconds for any single spec layer record or query
- NFR4: delta-macros-mcp macro lookups resolve within 1 second per call
- NFR5: gitlab-mcp operations complete within 10 seconds per API call under normal network conditions

**Security & Data Privacy**
- NFR6: No COBOL source code, business rules, or extracted spec data is transmitted outside the local environment by any agent or MCP server
- NFR7: Where remote LLM API calls are used, source code is scoped to the minimum required context — no full-file dumps without documented justification
- NFR8: GitLab credentials are stored using the host IDE's or OS credential store — never hardcoded in agent definitions or MCP server config files
- NFR9: delta-macros-mcp macro library is stored locally and not synchronised to any external service

**Reliability & Reproducibility**
- NFR10: Running any agent twice on the same input produces equivalent SQLite spec layer output — spec layer writes are idempotent
- NFR11: Any agent encountering an unrecognised construct, unknown macro, or LLM error fails with an explicit, actionable error message — silent failures are not permitted
- NFR12: A failed agent run does not corrupt existing spec layer records — partial writes roll back or are clearly flagged as incomplete
- NFR13: All MCP servers remain operational across agent session restarts without requiring full reinitialisation

**Integration & Compatibility**
- NFR14: The BMAD expansion pack installs and operates correctly in any BMAD-compatible IDE (Claude Code and Cursor as minimum baseline)
- NFR15: All MCP servers conform to the MCP protocol specification — no proprietary extensions that break cross-IDE compatibility
- NFR16: gitlab-mcp supports GitLab Cloud and self-hosted GitLab instances (API v4)
- NFR17: The SQLite spec layer schema is versioned — schema migrations do not break existing data or require manual intervention

**Maintainability**
- NFR18: Each BMAD agent definition is independently updatable without requiring changes to any other agent or MCP server
- NFR19: Each MCP server exposes a clearly defined, versioned tool interface — adding new tools does not break existing tool calls
- NFR20: Glossary file format and macro library format use human-readable, plain-text markup — no binary formats or proprietary schemas
- NFR21: The BlackJack corpus serves as the regression test baseline — any change to an MCP server is validated against BlackJack end-to-end before release

### Additional Requirements

**From Architecture — Starter Template & Project Initialisation**
- Architecture specifies uv as the project manager and Python 3.12 as the runtime. Each MCP server is its own uv project, initialised with: `uv init --python 3.12 <server-name>`. This pattern drives **Epic 1, Story 1** (project scaffolding).
- Four uv projects with isolated venvs and lock files: `cobol-parser-mcp`, `specdb-mcp`, `delta-macros-mcp`, `gitlab-mcp`
- MCP framework: FastMCP 3.0.2 (integrated into `mcp` package) — the authoring layer for all four servers

**From Architecture — Data & Schema**
- SQLite DB location: configurable via `db_path` in `config.yaml` (default: `<project-root>/data/specdb.sqlite`)
- Schema versioning: `schema_version` table + programmatic migrations in specdb-mcp (no Alembic)
- Idempotency pattern: `INSERT OR IGNORE` + `UPDATE` (check-then-upsert) across all spec layer writes
- SQLite transactions: one transaction per tool call; rollback on any failure

**From Architecture — Communication & Transport**
- MCP transport: STDIO for all 4 servers (IDE spawns server as subprocess)
- Structured result dict across all servers: `{"status": "ok|warning|error", "data": ..., "flags": [...], "message": "..."}`
- Shared `result.py` per server exposing `make_result()`, `make_error()`, `make_warning()`
- Flag code format: `SCREAMING_SNAKE` with category prefix (e.g., `UNKNOWN_MACRO`, `PARSE_ERROR`)

**From Architecture — Security**
- GitLab credential strategy: `GITLAB_TOKEN` environment variable — read at startup, explicit error if absent
- All other MCP servers: no authentication (local-only, STDIO)
- async/sync bridging: `asyncio.to_thread()` for all synchronous python-gitlab calls within async FastMCP tools

**From Architecture — Logging**
- Dual logging handler on all MCP servers: stderr (real-time, IDE-visible) + log file (`<project-root>/logs/<server-name>.log`)
- Standard Python `logging` module with `StreamHandler` (stderr) + `FileHandler`
- Structured log messages at DEBUG / INFO / WARNING / ERROR levels

**From Architecture — Project Structure**
- Per-server internal structure: `server.py` (thin tool wrappers) + `<domain>.py` (core logic) + `result.py` + `config.py`
- Tests: `tests/` at server root, not co-located with source
- BlackJack corpus in `mcp-servers/cobol-parser-mcp/tests/fixtures/blackjack/` (8 .cbl modules + 3 .cpy copybooks)
- IDE config files: `.claude/mcp.json` (Claude Code) + `.vscode/mcp.json` (GitHub Copilot)

**From Architecture — COBOL Parsing Approach**
- Regex-based static pre-pass (deterministic) for Phase 1 structural extraction
- Lark grammar library for deeper parsing (added to cobol-parser-mcp only: `uv add lark`)
- No full Python COBOL parser exists — custom implementation required

**From Architecture — Implementation Order (mandated)**
1. `specdb-mcp` — schema, migrations, CRUD tools (all downstream depends on this)
2. `delta-macros-mcp` — macro library, get/search/add tools (Viper depends on this)
3. `cobol-parser-mcp` — parsing, call graph, clustering, complexity (Viper's engine)
4. `gitlab-mcp` — GitLab integration (Tigress onwards)
5. `agents/` — Viper, Crane, Shifu (new); Oogway, Tigress (customise existing BMAD) — no Po or Tai Lung agents
6. `workflows/` — per-agent workflow and step files

**From Architecture — Config Schema**
- `config.yaml` fields: `db_path`, `macro_library_path`, `gitlab_url`, `project_name`, `target_language`
- Glossary file format: markdown table (`| COBOL Name | Business Term |`) — human-editable, parseable

### FR Coverage Map

| FR Range | Epic | Summary |
|---|---|---|
| FR29, FR30, FR32, FR34 | Epic 1 | Pipeline setup infrastructure |
| FR31, FR39, FR8 (partial) | Epic 2 | Delta macro integration |
| FR1–FR8, FR33, FR35–FR39 | Epic 3 | Viper COBOL analysis |
| FR9–FR13 | Epic 4 | JCL parsing (jcl-parser-mcp) + Crane dependency mapping |
| FR14–FR18, FR54 | Epic 5 | Shifu business rules |
| FR40–FR56 | Epic 6 | Tigress GitLab management |
| FR19–FR22 | Epic 7 | Oogway architecture |
| FR23–FR28, FR55–FR56 | Epic 8 | PM epic/story generation + SM context enrichment (BMAD Dev + QA) |
| FR32 | Epic 9 | Expansion pack installer & setup guide |

## Epic List

### Epic 1: Pipeline Foundation & Configuration
Operators can set up the complete pipeline for a new COBOL engagement — uv project structure scaffolded for all 4 MCP servers, the spec layer initialised with a single command, config and glossary template ready, and the BlackJack regression corpus in place. After this epic, any agent can be pointed at an engagement and start running.
**FRs covered:** FR29, FR30, FR32 (installer structure — deferred impl), FR34 (flags infrastructure via shared result.py)
**NFRs addressed:** NFR3, NFR10, NFR12, NFR13, NFR17, NFR20
**Architecture items:** uv project scaffolding for all 4 servers, specdb-mcp full implementation, config.yaml schema, glossary template, BlackJack corpus fixtures, `.claude/mcp.json` + `.vscode/mcp.json`

### Epic 2: Client Macro Knowledge Integration
Analysts can configure the pipeline with client-specific Delta macro knowledge. Unknown macros are gracefully flagged rather than causing silent failures. Analysts can add new macro definitions without restarting the pipeline.
**FRs covered:** FR31, FR39, FR8 (partial — unknown macro flagging)
**NFRs addressed:** NFR4, NFR9, NFR11
**Architecture items:** delta-macros-mcp full implementation (get_macro, search_macros, list_categories, add_macro), macro library file format

### Epic 3: COBOL Structural Analysis — Viper
Analysts can run a complete structural analysis of any COBOL module: paragraph call graph, complexity scoring, anti-pattern detection, CICS/DB2/COPY dialect handling, and AI semantic clustering. All agent outputs pass through an analyst review gate before touching the spec layer.
**FRs covered:** FR1–FR8, FR33, FR35–FR39
**NFRs addressed:** NFR1, NFR2, NFR6, NFR7, NFR11
**Architecture items:** cobol-parser-mcp full implementation, Viper BMAD agent definition, Viper workflow + step files

### Epic 4: JCL Analysis & Cross-Module Dependency Mapping — jcl-parser-mcp + Crane
Architects and analysts can map the full dependency landscape of a COBOL estate — JCL job boundaries parsed into specdb, static CALL/COPY dependencies combined with JCL runtime execution order, Mermaid dependency diagram, subsystem groupings, migration order, and circular dependency / dead code detection.
**FRs covered:** FR9–FR13, FR33
**NFRs addressed:** NFR2, NFR6
**Architecture items:** jcl-parser-mcp full implementation (parse_jcl, list_job_steps, get_dataset_allocations, build_job_graph) + specdb-mcp schema migration for jcl_jobs/jcl_steps/dataset_allocations; Crane BMAD agent definition; Crane workflow + step files (uses cobol-parser-mcp + jcl-parser-mcp + specdb-mcp)

### Epic 5: Business Rule Extraction & Validation — Shifu
Analysts and business validators can extract business rules from COBOL modules in plain English, validate and correct each rule, and persist approved rules to the spec layer as the verified source of truth. Business validator formally signs off.
**FRs covered:** FR14–FR18, FR54
**NFRs addressed:** NFR6, NFR10, NFR11
**Architecture items:** Shifu BMAD agent definition, Shifu workflow + step files (uses specdb-mcp + delta-macros-mcp)

### Epic 6: GitLab Delivery Management — Tigress
PMs can set up and manage a fully structured modernisation project in GitLab — label taxonomy, milestone structure, per-module issue lifecycle, sprint planning, live README dashboard, and formal review gates.
**FRs covered:** FR40–FR56
**NFRs addressed:** NFR5, NFR8, NFR11, NFR16
**Architecture items:** gitlab-mcp full implementation, Tigress BMAD agent definition + workflow

### Epic 7: Migration Architecture — Oogway
Architects can generate a target migration architecture from the validated spec layer — subsystem-to-service mapping, target language specification, analyst review and finalisation.
**FRs covered:** FR19–FR22
**NFRs addressed:** NFR6
**Architecture items:** Oogway BMAD agent customisation + Oogway workflow (reads spec layer via specdb-mcp)

### Epic 8: BMAD Delivery Pipeline — PM Epic Generation + SM Context Enrichment
PM agent converts Oogway architecture and Shifu business function catalog into BMAD Epics and User Stories (one Epic per business capability, one Story per service boundary). SM agent enriches each story with full spec layer context (business rules as acceptance criteria, confidence scores, Delta macro expansions). Dev and QA use standard BMAD agents to implement and validate — no custom code-generation or QA agents are needed.
**FRs covered:** FR23–FR28, FR55–FR56
**NFRs addressed:** NFR6, NFR11
**Architecture items:** PM workflow step file for epic/story generation from business_functions + architecture; SM workflow step file for spec layer context enrichment (queries spec_rules, spec_operations, spec_entities, spec_data_flows per story); confidence-weighted QA acceptance criteria embedded in stories

### Epic 9: Expansion Pack Release — Installer & Setup
Operators can install the complete expansion pack with a single command. All agents, workflows, MCP servers, and IDE configuration are deployed automatically. Depends on Epics 1–8 complete.
**FRs covered:** FR32
**NFRs addressed:** NFR14
**Architecture items:** npx-compatible installer script, expansion pack folder structure, `.claude/mcp.json` + `.vscode/mcp.json` templates, `SETUP.md`

---

## Epic 1: Pipeline Foundation & Configuration

Operators can set up the complete pipeline for a new COBOL engagement — uv project structure scaffolded for all 4 MCP servers, the spec layer initialised with a single command, config and glossary template ready, and the BlackJack regression corpus in place. After this epic, any agent can be pointed at an engagement and start running.

### Story 1.1: Project Scaffolding & Shared Infrastructure

As an **operator/developer**,
I want all 4 MCP server uv projects scaffolded with correct structure and shared patterns,
So that I have a consistent, runnable foundation for all subsequent implementation work.

**Acceptance Criteria:**

**Given** the repository is empty
**When** the scaffolding is applied
**Then** four uv projects exist: `cobol-parser-mcp`, `specdb-mcp`, `delta-macros-mcp`, `gitlab-mcp` — each with `pyproject.toml`, `uv.lock`, `src/server.py`, `src/result.py`, `src/config.py`, and a `tests/` directory
**And** each `result.py` implements `make_result()`, `make_error()`, `make_warning()` returning `{"status", "data", "flags", "message"}`
**And** each `src/config.py` loads `config.yaml` from project root (or `BMAD_PROJECT_ROOT` env var) — fails with explicit error if not found
**And** each `server.py` is a valid FastMCP 3.0.2 app that starts without error (`uv run python -m src.server`)
**And** the BlackJack corpus is present at `cobol-parser-mcp/tests/fixtures/blackjack/` (8 `.cbl` + 3 `.cpy` files)
**And** `.claude/mcp.json` and `.vscode/mcp.json` exist at project root, registering all 4 servers with correct `uv run` commands
**And** `config.yaml` exists at project root with all required fields: `db_path`, `macro_library_path`, `gitlab_url`, `project_name`, `target_language`

### Story 1.2: specdb-mcp — Schema & Migrations

As an **operator**,
I want to initialise the full SQLite spec layer schema with a single `init_schema` command,
So that the structured intermediate representation is ready before any COBOL analysis begins.

**Acceptance Criteria:**

**Given** `specdb-mcp` is running and `db_path` in `config.yaml` points to a valid directory
**When** `init_schema` is called
**Then** the SQLite database is created at `db_path` with all required tables: `schema_version`, `cobol_files`, `analyses`, `metrics`, `dependencies`, `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows`
**And** the `schema_version` table records the current schema version
**When** `init_schema` is called again on an existing database
**Then** the operation completes without error and without destroying existing data (idempotent)
**When** a schema migration is pending
**Then** it is applied programmatically at server startup without manual intervention (NFR17)
**And** the tool returns `{"status": "ok", "data": {"tables_created": [...], "schema_version": N}, "flags": [], "message": "..."}`

### Story 1.3: specdb-mcp — CRUD Tools

As an **agent**,
I want to read, write, and query the spec layer via `read_spec`, `write_spec`, and `query_spec` tools,
So that any pipeline agent can persist and retrieve structured data without direct database access.

**Acceptance Criteria:**

**Given** the schema has been initialised (Story 1.2)
**When** `write_spec` is called with a valid table name, program name, and field data
**Then** the record is written using the INSERT OR IGNORE + UPDATE idempotent pattern
**And** the write is wrapped in a transaction — if it fails, the database rolls back cleanly (NFR12)
**And** re-calling `write_spec` with the same identity key updates fields rather than duplicating rows (NFR10)
**When** `read_spec` is called with a table name and program name
**Then** the matching record(s) are returned in the structured result dict
**When** `query_spec` is called with a SQL fragment
**Then** matching rows are returned within 2 seconds for any standard spec layer query (NFR3)
**When** any tool call fails (DB error, bad table name)
**Then** it returns `{"status": "error", ...}` with an explicit message — never raises an exception (NFR11)

### Story 1.4: Engagement Configuration & Templates

As an **operator**,
I want a glossary template, macro library template, and clear config schema,
So that I can configure any new client engagement in under an hour with no code changes.

**Acceptance Criteria:**

**Given** the project is scaffolded (Story 1.1)
**When** an operator opens `config.yaml`
**Then** all required fields are documented with examples: `db_path`, `macro_library_path`, `gitlab_url`, `project_name`, `target_language`
**When** an operator opens `templates/glossary-template.md`
**Then** it contains a markdown table with header `| COBOL Name | Business Term |` and example rows, ready to populate (NFR20)
**When** an operator opens `templates/macro-template.md`
**Then** it is a human-readable markdown template describing purpose, parameters, and return for a Delta macro (NFR20)
**When** an operator opens `blackjack/glossary.md`
**Then** it contains the BlackJack field-name-to-business-term mappings (populated — not empty) serving as a working example
**And** `data/.gitkeep` and `logs/.gitkeep` exist, ensuring runtime directories are tracked in git but their contents are not

---

## Epic 2: Client Macro Knowledge Integration

Analysts can configure the pipeline with client-specific Delta macro knowledge. Unknown macros are gracefully flagged rather than causing silent failures. Analysts can add new macro definitions without restarting the pipeline.

### Story 2.1: delta-macros-mcp — Macro Lookup

As an **analyst/agent**,
I want to look up, search, and list Delta macro definitions via `get_macro`, `search_macros`, and `list_categories`,
So that any pipeline agent can resolve client-specific macro references during COBOL analysis.

**Acceptance Criteria:**

**Given** `delta-macros-mcp` is running and `macro_library_path` in `config.yaml` points to a directory of macro `.md` files
**When** `get_macro` is called with a known macro name (e.g. `DLTM-ACCT-LOCK`)
**Then** the macro's purpose, parameters, and return value are returned in the structured result dict within 1 second (NFR4)
**When** `get_macro` is called with an unknown macro name
**Then** the tool returns `{"status": "warning", "data": null, "flags": [{"code": "UNKNOWN_MACRO", "message": "...", "location": "<macro_name>"}], "message": "Macro not found"}` — never an error or exception (NFR11)
**When** `search_macros` is called with a keyword
**Then** all matching macro definitions are returned (matched against macro name and description)
**When** `list_categories` is called
**Then** all macro category groupings present in the library are returned
**And** the macro library directory contents are never transmitted outside the local environment (NFR9)

### Story 2.2: delta-macros-mcp — Macro Ingestion

As an **analyst**,
I want to add a new macro definition to the library via `add_macro` without restarting the pipeline,
So that I can close institutional knowledge gaps discovered during analysis in real time.

**Acceptance Criteria:**

**Given** `delta-macros-mcp` is running
**When** `add_macro` is called with a macro name, purpose, parameters, return value, and optional category
**Then** a new markdown file is created at `<macro_library_path>/<MACRO-NAME>.md` following the macro template format
**And** the new macro is immediately retrievable via `get_macro` without any server restart (FR31)
**When** `add_macro` is called with a name that already exists
**Then** the existing file is updated with the new content and the tool returns `{"status": "ok", ...}` — no duplicate is created
**When** `add_macro` is called with an invalid or empty macro name
**Then** the tool returns `{"status": "error", ...}` with a clear validation message
**And** all macro files remain stored locally — no external sync (NFR9)

---

## Epic 3: COBOL Structural Analysis — Viper

Analysts can run a complete structural analysis of any COBOL module: paragraph call graph, complexity scoring, anti-pattern detection, CICS/DB2/COPY dialect handling, and AI semantic clustering. All agent outputs pass through an analyst review gate before touching the spec layer.

### Story 3.1: cobol-parser-mcp — Core Module Parsing & Call Graph

As an **analyst**,
I want to parse any COBOL module and receive its paragraph call graph and external references,
So that I have the structural map of the program as the foundation for all further analysis.

**Acceptance Criteria:**

**Given** `cobol-parser-mcp` is running and a `.cbl` source file path is provided
**When** `parse_module` is called with `program_name` and `source_path`
**Then** the tool returns: PROGRAM-ID, all paragraphs with line numbers, all COPY statement references, all CALL statement targets, all EXEC SQL and EXEC CICS block locations, and any Delta macro invocations found in the source (FR1, FR4)
**And** `program_name` is stored and returned as the COBOL PROGRAM-ID verbatim (uppercase with hyphens: e.g. `"PAYROLL-CALC"`)
**And** the tool completes within 30 seconds for any module up to 5,000 lines (NFR2)
**When** `extract_call_graph` is called with the parsed module data
**Then** it returns a directed graph of PERFORM relationships between paragraphs (FR1)
**And** PERFORM THRU ranges are fully expanded in the graph
**When** the source file contains IBM Enterprise COBOL or COBOL-85 syntax
**Then** it is parsed correctly without error (FR35)
**When** a COPY statement references a copybook
**Then** the copybook name is recorded as an external dependency in the result (FR38)
**When** any tool call fails (file not found, parse error)
**Then** it returns `{"status": "error", "flags": [{"code": "PARSE_ERROR", ...}], ...}` — never raises (NFR11)
**And** no source code is transmitted outside the local environment (NFR6)

### Story 3.2: cobol-parser-mcp — Complexity Scoring & Anti-Pattern Detection

As an **analyst**,
I want to see a complexity score and a list of detected anti-patterns for any parsed COBOL module,
So that I can prioritise review effort and flag structural risks before analysis begins.

**Acceptance Criteria:**

**Given** a module has been parsed (Story 3.1)
**When** `score_complexity` is called with `program_name`
**Then** it returns a score of `Low`, `Medium`, or `High` with the contributing factors (paragraph count, PERFORM nesting depth, REDEFINES count, GOTO count) (FR2)
**When** `detect_antipatterns` is called with `program_name`
**Then** it returns a list of flagged anti-patterns, each with type, location (paragraph name + line number), and description (FR3)
**And** the anti-pattern types detected include: `GOTO`, `ALTER`, nested `PERFORM THRU`, `REDEFINES` on non-filler items, and fall-through paragraph logic
**When** `detect_antipatterns` encounters an EXEC CICS block
**Then** it is flagged as `{"code": "CICS_CONSTRUCT", "message": "...", "location": "..."}` in the flags array (FR36)
**When** `detect_antipatterns` encounters an EXEC SQL block
**Then** it is flagged as `{"code": "DB2_SQL_CONSTRUCT", "message": "...", "location": "..."}` in the flags array (FR37)
**When** the module has no anti-patterns
**Then** the tool returns `{"status": "ok", "data": {"antipatterns": []}, "flags": [], ...}`

### Story 3.3: cobol-parser-mcp — Semantic Paragraph Clustering

As an **analyst**,
I want AI-generated semantic cluster groupings and plain-English descriptions for a module's paragraphs,
So that I can review the AI's understanding of program structure and correct it before it reaches the spec layer.

**Acceptance Criteria:**

**Given** `parse_module` and `extract_call_graph` have been run for a program
**When** the cluster builder is invoked (as part of the Viper Phase 2 workflow)
**Then** paragraphs are grouped into semantic clusters based on naming patterns, call relationships, and data access patterns (FR5)
**And** each cluster has a plain-English description of its functional role (FR6)
**And** only paragraph names, call graph structure, and DATA DIVISION field names are sent to the LLM — never raw COBOL source (NFR7)
**And** the cluster output is returned to the Viper agent for analyst review — it is NOT written to the spec layer until explicitly approved (FR7)
**When** the LLM call fails or times out
**Then** the tool returns `{"status": "warning", "flags": [{"code": "LLM_UNAVAILABLE", ...}], ...}` — never a silent failure (NFR11)

### Story 3.4: Viper BMAD Agent Definition

As an **analyst**,
I want a Viper agent I can invoke in my IDE to orchestrate COBOL structural analysis with built-in review gates,
So that I review and correct AI outputs rather than building analysis from scratch — staying in the expert seat.

**Acceptance Criteria:**

**Given** the Viper agent definition is installed in a BMAD-compatible IDE (Claude Code or Cursor)
**When** the agent is invoked for a specific COBOL module
**Then** it calls `parse_module` and `extract_call_graph` via `cobol-parser-mcp` (Phase 1) and displays results to the analyst
**And** it calls `get_macro` for any Delta macro references encountered, surfacing `UNKNOWN_MACRO` warnings if not found (FR8)
**When** Phase 1 is complete
**Then** the analyst can review the call graph, complexity score, anti-pattern list, and any flagged constructs before proceeding to Phase 2
**When** Phase 2 (semantic clustering) completes
**Then** the analyst can review, correct individual cluster descriptions, and explicitly approve outputs before they are written to the spec layer (FR7)
**When** an unrecognised COBOL construct is encountered
**Then** the agent surfaces an explicit warning with the construct location — analysis continues rather than halting (FR8)
**When** the analyst triggers a re-run on the same module
**Then** the agent re-processes only that module — other modules' spec layer data is unaffected (FR33)
**And** a consolidated list of all flagged constructs and macros is presented at the end of the run (FR34)

### Story 3.5: Viper Workflow & Step Files

As an **analyst**,
I want the Viper agent to follow a structured, step-by-step workflow with enforced phase gates,
So that Phase 2 AI analysis cannot run until Phase 1 structural parsing is complete and the spec layer is never written without analyst approval.

**Acceptance Criteria:**

**Given** the Viper workflow is loaded in the IDE
**When** the analyst initiates analysis on a module
**Then** the workflow executes in sequence: Phase 1 static pre-pass → Phase 1 review gate → Phase 2 AI clustering → Phase 2 review/correction gate → spec layer write
**And** the workflow cannot advance past the Phase 1 review gate without explicit analyst confirmation
**And** Phase 1 completes within 15 minutes for any single COBOL module on standard developer hardware (NFR1)
**When** Phase 2 review is complete and the analyst approves
**Then** the workflow writes approved outputs to the spec layer via `specdb-mcp` write tools
**And** the write is idempotent — re-running the full workflow on the same module updates spec layer records rather than creating duplicates (NFR10)
**When** any workflow step encounters an error
**Then** it surfaces an explicit, actionable error message — the workflow halts rather than proceeding with corrupted state (NFR11)

---

## Epic 4: Cross-Module Dependency Mapping — Crane

Architects and analysts can map the full dependency landscape of a COBOL estate — Mermaid dependency diagram, detected subsystem groupings, recommended migration order, and circular dependency / dead code detection.

### Story 4.1: Crane BMAD Agent Definition

As an **architect/analyst**,
I want a Crane agent that reads all analysed module data from the spec layer and produces a cross-module dependency picture,
So that subsystem boundaries and migration order emerge from verified structural data rather than manual cross-referencing.

**Acceptance Criteria:**

**Given** Viper has been run on all modules in scope and their data is in the spec layer
**When** Crane is invoked for an estate (set of modules)
**Then** it reads all `cobol_files`, `dependencies`, and `analyses` records from the spec layer via `specdb-mcp` (FR9)
**And** it produces a Mermaid dependency diagram showing directed relationships between all modules (FR10)
**And** it identifies subsystem groupings — clusters of modules with high internal cohesion and clear external boundaries (FR11)
**And** it produces a recommended migration order: modules with no inbound dependencies first; modules with the most dependents last (FR12)
**And** it identifies any circular dependencies between modules and flags them explicitly (FR13)
**And** it identifies dead code — modules present in scope but not referenced by any other module — and flags them (FR13)
**When** Crane is re-invoked after additional modules have been analysed by Viper
**Then** it re-runs on the full updated module set — prior dependency data in the spec layer is updated idempotently (FR33, NFR10)
**And** no spec layer data is transmitted outside the local environment (NFR6)

### Story 4.2: Crane Workflow & Step Files

As an **architect/analyst**,
I want a structured Crane workflow that guides me through estate scoping, dependency review, and analyst sign-off,
So that the dependency map is confirmed as accurate before it informs any migration architecture decisions.

**Acceptance Criteria:**

**Given** the Crane workflow is loaded in the IDE
**When** the analyst initiates a Crane run
**Then** the workflow prompts for the set of modules in scope (or reads all analysed modules from the spec layer)
**And** the workflow executes in sequence: spec layer read → dependency graph construction → subsystem detection → migration order calculation → analyst review gate → spec layer write
**When** Crane presents the dependency map and subsystem groupings
**Then** the analyst can review and annotate (e.g. confirm or override subsystem boundaries) before the results are finalised
**When** the analyst approves the dependency output
**Then** the workflow writes the dependency graph and migration order to the `dependencies` table in the spec layer via `specdb-mcp`
**And** the Mermaid diagram is saved as a markdown artefact alongside the spec layer output
**When** any step fails (e.g. spec layer read error, module not in spec layer)
**Then** the workflow surfaces an explicit error identifying the missing module — it does not silently skip it (NFR11)

---

## Epic 5: Business Rule Extraction & Validation — Shifu

Analysts and business validators can extract business rules from COBOL modules in plain English, validate and correct each rule, and persist approved rules to the spec layer as the verified source of truth. The business validator formally signs off, creating a compliance-grade artefact as a byproduct of analysis.

### Story 5.1: Shifu BMAD Agent Definition

As an **analyst/business validator**,
I want a Shifu agent that generates plain-English business markdown per module and presents each extracted rule for validation,
So that business rules are confirmed accurate by a domain expert before they flow into architecture and code generation.

**Acceptance Criteria:**

**Given** Viper and Crane have been run and their outputs are in the spec layer
**When** Shifu is invoked for a specific module
**Then** it reads the module's Viper analysis and Crane dependency data from `specdb-mcp` (FR14)
**And** it generates a plain-English business markdown document covering: module purpose, use cases, extracted business rules, and data entities using glossary business terms rather than COBOL identifiers (FR15)
**And** each business rule is presented individually to the business validator for a decision: confirmed, corrected, or rejected (FR16)
**When** the business validator corrects a rule
**Then** the corrected version is stored — the original AI-generated version is not written to the spec layer (FR16)
**When** all rules are validated and approved
**Then** Shifu writes the approved business rules, entities, operations, and data flows to the spec layer tables: `spec_rules`, `spec_entities`, `spec_operations`, `spec_data_flows` (FR17)
**When** Shifu is re-run on the same module
**Then** the spec layer tables are updated idempotently — no duplicate rules or entities are created (FR18, NFR10)
**And** `delta-macros-mcp` is called to resolve any Delta macro references found in the module's data, with `UNKNOWN_MACRO` warnings surfaced to the analyst if not found (FR39)
**And** no source code or business rules are transmitted outside the local environment (NFR6)

### Story 5.2: Shifu Workflow & Step Files

As an **analyst/business validator**,
I want a structured Shifu workflow with an explicit sign-off gate,
So that business rule extraction follows a consistent, auditable process with a formal validator approval step before spec layer writes.

**Acceptance Criteria:**

**Given** the Shifu workflow is loaded in the IDE
**When** the analyst initiates Shifu for a module
**Then** the workflow executes in sequence: spec layer read → business markdown generation → rule-by-rule validation gate → spec layer write → business validator sign-off gate
**And** the workflow cannot advance past the validation gate without the business validator confirming each rule
**When** all rules are validated and the business validator confirms sign-off
**Then** the workflow records formal sign-off on the module — this closes the review gate for this module (FR54)
**And** the approved business markdown is saved as a human-readable artefact alongside the spec layer data
**When** the analyst triggers a re-run on a specific module
**Then** only that module is re-processed — other modules' spec layer data is unaffected (FR33)
**When** any workflow step encounters an error (e.g. spec layer write failure)
**Then** it surfaces an explicit, actionable error and halts — no partial or inconsistent spec layer state is left (NFR11, NFR12)

---

## Epic 6: GitLab Delivery Management — Tigress

PMs can set up and manage a fully structured modernisation project in GitLab — label taxonomy, milestone structure, per-module issue lifecycle, sprint planning, live README dashboard, and formal review gates.

### Story 6.1: gitlab-mcp — Project Initialisation Tools

As a **PM**,
I want to initialise a GitLab project with the full label taxonomy, milestone structure, and issue board via `gitlab-mcp` tools,
So that the modernisation delivery framework is ready for the team before the first module analysis begins.

**Acceptance Criteria:**

**Given** `gitlab-mcp` is running, `GITLAB_TOKEN` is set in the environment, and `gitlab_url` is configured in `config.yaml`
**When** `create_epic` is called
**Then** a new GitLab Epic is created in the configured project (FR40)
**When** `apply_label` is called with a pipeline stage label (Viper-Complete, Crane-Complete, Shifu-Complete, Oogway-Complete, Po-Complete, QA-Complete), a complexity label (Complexity::Low/Medium/High), or a status label (In-Analysis, Awaiting-Review, In-Migration, Blocked, Done)
**Then** the label is applied to the specified Issue or Epic (FR40)
**When** `create_milestone` is called with a name and optional due date
**Then** a new milestone is created in the GitLab project (FR41)
**When** `create_board` is called
**Then** a GitLab issue board is created with columns mapped to the pipeline stage labels (FR42)
**When** `GITLAB_TOKEN` is not set
**Then** the server fails at startup with an explicit error message — never silently proceeds with no auth (NFR8, NFR11)
**And** all `gitlab-mcp` tools complete within 10 seconds per call under normal network conditions (NFR5)
**And** the server works against both GitLab Cloud and self-hosted instances using API v4 (NFR16)
**And** `asyncio.to_thread()` is used for all synchronous `python-gitlab` calls to avoid blocking the async FastMCP event loop

### Story 6.2: gitlab-mcp — Module Lifecycle & Progress Reporting Tools

As an **agent/analyst**,
I want to track each module's pipeline lifecycle in GitLab and post structured progress updates via `gitlab-mcp` tools,
So that the entire team and client sponsor have real-time visibility into pipeline progress without manual status updates.

**Acceptance Criteria:**

**Given** `gitlab-mcp` is running and a GitLab project is initialised (Story 6.1)
**When** `create_issue` is called with a module name and description
**Then** a new GitLab Issue is created representing that module's pipeline lifecycle (FR43)
**When** `apply_label` is called on a module Issue after a pipeline stage completes
**Then** the appropriate completion label is applied (e.g. `Viper-Complete`) (FR44)
**When** `update_issue_status` is called to transition a module to `Awaiting-Review`
**Then** the Issue status is updated and the analyst is flagged for review (FR45, FR46)
**When** `add_comment` is called with structured progress data
**Then** a formatted comment is posted to the module Issue containing stage outputs and any warnings or flags (FR50)
**When** `update_readme` is called
**Then** the GitLab project README is updated to reflect current pipeline state: total modules, modules per stage, blocked modules, Epics signed off (FR51, FR52)
**When** any `gitlab-mcp` tool call fails (network error, auth failure, rate limit)
**Then** it returns `{"status": "error", "flags": [{"code": "GITLAB_API_ERROR", ...}], ...}` — never raises (NFR11)

### Story 6.3: gitlab-mcp — Sprint & Sign-off Tools

As a **PM/QA**,
I want sprint milestone management and formal Epic sign-off tools via `gitlab-mcp`,
So that sprint planning is grounded in Crane's migration order and QA sign-off formally closes each Epic in GitLab.

**Acceptance Criteria:**

**Given** Crane has produced a migration order recommendation
**When** `create_milestone` is called with a sprint scope (set of module Issues)
**Then** a sprint milestone is created in GitLab and the specified module Issues are assigned to it (FR47, FR48)
**When** `assign_to_milestone` is called
**Then** the specified Issue is assigned to the specified milestone, respecting the dependency order from Crane (FR48)
**When** `add_comment` is called on an Epic
**Then** a milestone summary comment is posted showing sprint progress and outstanding items (FR53)
**When** `close_epic` is called by Tai Lung after all module Issues within it are QA-Complete
**Then** the Epic is formally closed in GitLab with a validation summary comment (FR55, FR56)
**And** `remove_label` correctly removes outdated status labels when a new status is applied — no label accumulation

### Story 6.4: Tigress BMAD Agent & Workflow

As a **PM**,
I want a Tigress agent that orchestrates full GitLab project setup and ongoing delivery management,
So that the modernisation project is structured, tracked, and visible from day one with no manual GitLab configuration.

**Acceptance Criteria:**

**Given** the Tigress agent is installed and `gitlab-mcp` is running
**When** Tigress is invoked to initialise a new engagement
**Then** it creates the full GitLab project structure: label taxonomy, milestone structure, issue board, one Issue per COBOL module in scope (FR40–FR43)
**When** Tigress is invoked for sprint planning
**Then** it reads Crane's migration order from the spec layer and proposes sprint milestone groupings respecting subsystem dependencies (FR47, FR48)
**When** Tigress is invoked to check progress
**Then** it reads module Issue statuses from GitLab and posts an updated README dashboard reflecting the current pipeline state (FR51, FR52)
**When** the Tigress workflow runs
**Then** it executes in sequence: spec layer read (module list + migration order) → GitLab project init → milestone structure → analyst review gate → sprint assignment
**And** all GitLab credentials are read from `GITLAB_TOKEN` environment variable — never hardcoded (NFR8)

---

## Epic 7: Migration Architecture — Oogway

Architects can generate a target migration architecture from the validated spec layer — subsystem-to-service mapping, target language specification, analyst review and finalisation — ready to guide code generation.

### Story 7.1: Oogway BMAD Agent Definition

As an **architect**,
I want an Oogway agent that generates a target migration architecture from the validated spec layer,
So that the architecture is grounded in verified COBOL structure and business rules rather than assumptions.

**Acceptance Criteria:**

**Given** Shifu has been run and all `spec_*` tables are populated for all modules in scope
**When** Oogway is invoked with a target language specified (e.g. Java or Python) (FR21)
**Then** it reads `spec_entities`, `spec_operations`, `spec_rules`, and `spec_data_flows` from `specdb-mcp` (FR19)
**And** it produces a target architecture document mapping COBOL subsystems (from Crane's analysis) to target-language services (FR20)
**And** the architecture identifies shared services (entities used across multiple modules), module-specific services, and data ownership boundaries
**And** the Crane migration order is reflected in the architecture — subsystems with no inbound dependencies are architectured as extraction candidates first
**When** the architect reviews the generated architecture
**Then** they can modify service boundaries, rename services, or adjust ownership before the architecture is finalised (FR22)
**When** the architect approves the architecture
**Then** the finalised architecture document is saved as a markdown artefact for use by Po and Tai Lung
**And** no spec layer data is transmitted outside the local environment (NFR6)

### Story 7.2: Oogway Workflow & Step Files

As an **architect**,
I want a structured Oogway workflow with a mandatory review and modification gate,
So that the architecture cannot be consumed by downstream agents until an architect has explicitly approved it.

**Acceptance Criteria:**

**Given** the Oogway workflow is loaded in the IDE
**When** the architect initiates Oogway
**Then** the workflow prompts for the target language and executes in sequence: spec layer read → architecture generation → architect review and modification gate → architecture finalisation and save
**And** the workflow cannot advance past the review gate without explicit architect approval
**When** the architect requests modifications (e.g. merge two proposed services, rename a service)
**Then** the agent updates the architecture document and re-presents it for review — changes are reflected immediately
**When** the architect finalises the architecture
**Then** the workflow saves the architecture document and signals readiness for Po to begin code generation
**When** any workflow step encounters an error (e.g. spec layer incomplete — Shifu not run on all modules)
**Then** it surfaces an explicit error identifying which modules are missing from the spec layer — it does not proceed with incomplete data (NFR11)

---

## Epic 8: Code Generation & QA Sign-off — Po + Tai Lung

Developers can generate target-language code per COBOL module from the spec layer and architecture. QA can validate generated code against spec layer business rules and formally sign off each Epic when all modules pass — completing the pipeline end-to-end.

### Story 8.1: Po BMAD Agent & Workflow

As a **developer**,
I want a Po agent that generates target-language code for each COBOL module from the spec layer and Oogway architecture,
So that I have a structured, traceable starting point for each module rather than writing from scratch.

**Acceptance Criteria:**

**Given** Oogway has produced a finalised architecture document and the spec layer is fully populated
**When** Po is invoked for a specific module with the target language and architecture as inputs
**Then** it reads that module's `spec_entities`, `spec_operations`, `spec_rules`, and `spec_data_flows` from `specdb-mcp` (FR23)
**And** it generates target-language code implementing the business rules and data flows for that module (FR24)
**And** the generated code follows the service structure defined in the Oogway architecture
**When** Po is invoked for a different module
**Then** only that module's code is generated — other modules are not affected (FR25)
**When** Po is re-invoked for the same module (e.g. after a spec layer correction)
**Then** new code is generated for that module only — the previous output is replaced, not accumulated
**And** no spec layer data or generated code is transmitted outside the local environment (NFR6)

### Story 8.2: Tai Lung BMAD Agent & Workflow

As a **QA engineer**,
I want a Tai Lung agent that validates generated code against the spec layer business rules and formally signs off completed Epics,
So that every migrated module has a documented, traceable quality gate before the Epic closes.

**Acceptance Criteria:**

**Given** Po has generated code for a module and the spec layer contains approved business rules for that module
**When** Tai Lung is invoked for a module
**Then** it reads the module's `spec_rules` from `specdb-mcp` and compares them against the generated code (FR26)
**And** it produces a validation report showing each business rule as: confirmed (present in generated code), partially covered (present but incomplete), or missing (FR27)
**When** the validation report shows missing or partially covered rules
**Then** Tai Lung flags the module as requiring rework — it cannot sign off until all rules are confirmed (FR28)
**When** all business rules for a module are confirmed
**Then** Tai Lung posts a QA-Complete comment to the module's GitLab Issue via `gitlab-mcp` and applies the `QA-Complete` label
**When** all module Issues within a GitLab Epic are QA-Complete
**Then** Tai Lung calls `close_epic` via `gitlab-mcp` to formally close the Epic with a validation summary (FR55, FR56)
**And** no source code, spec data, or generated code is transmitted outside the local environment (NFR6)

---

## Epic 9: Expansion Pack Release — Installer & Setup

Operators can install the complete Mainframe Modernisation Agents expansion pack into any BMAD-compatible IDE with a single command. All agents, workflows, MCP servers, and IDE configuration are deployed automatically. A setup guide covers the remaining human steps to configure a new engagement.

**Depends on:** Epics 1–8 complete (all agents, workflows, and MCP servers must exist before packaging)
**FRs covered:** FR32
**NFRs addressed:** NFR14
**Architecture items:** npx-compatible installer script, expansion pack folder structure, `.claude/mcp.json` + `.vscode/mcp.json` templates, `SETUP.md`

### Story 9.1: Expansion Pack Installer Script

As an **operator/developer**,
I want to run a single install command that deploys the full expansion pack into my BMAD setup,
So that all agents, workflows, and MCP servers are in place and my IDE recognises them without manual file copying.

**Acceptance Criteria:**

**Given** the expansion pack installer is available (e.g. via `npx` or a shell script)
**When** the installer is run in the target project directory
**Then** all 7 agent definition files are copied into the correct BMAD agents folder
**And** all agent workflow and step files are copied into the correct BMAD workflows folder
**And** all 4 MCP server source directories (`cobol-parser-mcp`, `specdb-mcp`, `delta-macros-mcp`, `gitlab-mcp`) are present at `mcp-servers/` in the project root
**And** `.claude/mcp.json` is written at project root, registering all 4 MCP servers with correct `uv run` startup commands (FR32, NFR14)
**And** `.vscode/mcp.json` is written at project root with equivalent configuration for Cursor / GitHub Copilot (NFR14)
**And** `templates/glossary-template.md` and `templates/macro-template.md` are present
**And** the installer is idempotent — re-running it on an existing installation does not overwrite user-modified config files (e.g. `config.yaml`, populated glossary)
**When** the installer completes
**Then** it prints a confirmation listing what was installed and directs the operator to `SETUP.md` for next steps

### Story 9.2: Operator Setup Guide

As an **operator**,
I want a clear, step-by-step setup guide that walks me through all post-install configuration steps,
So that I can have a new client engagement fully configured and ready for first analysis within one hour.

**Acceptance Criteria:**

**Given** the installer has been run (Story 9.1)
**When** the operator opens `SETUP.md`
**Then** it contains numbered steps covering: populate `config.yaml` (all required fields with examples), run `specdb-mcp init_schema` to initialise the spec layer, populate `glossary.md` from the template, point `delta-macros-mcp` at a macro library directory, set `GITLAB_TOKEN` environment variable
**And** each step includes the exact command or action required — no ambiguity
**And** a "Verify your setup" section lists how to confirm each component is working (e.g. invoke Viper on `blackjack/HELLO-WORLD.cbl` and confirm output)
**And** the BlackJack corpus is referenced as the first test case, giving the operator a concrete end-to-end validation path
