# Mainframe Modernisation Agents — Project Idea

## Overview

Build a suite of AI agents on top of the BMAD method framework to drive mainframe modernisation. The primary use case is COBOL-to-X migration, where X can be Java, Python, or modernised COBOL. The agents handle the hard part — understanding legacy code — and feed into the existing BMAD agent pipeline for architecture, planning, development and QA.

**Inspiration:** [Microsoft + Bankdata Legacy Modernisation Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents)

---

## Guiding Principles

- **Understand first, convert later** — no code generation until the full program is understood
- **Target-language agnostic analysis** — analysis agents produce language-neutral outputs; Architect and Dev agents decide the target (Java / Python / COBOL)
- **Agile delivery** — proper BMAD workflow: PRD → Architecture → Epics & Stories → Sprints
- **Human-readable + machine-queryable** — every analysis produces both a markdown doc and database records
- **Spec layer as the bridge** — analysis agents populate a structured specification layer; downstream agents consume specs, not raw markdown

---

## Agent Roster — The Kung Fu Panda Cast

| Character | BMAD Role | Responsibility |
|---|---|---|
| **Viper** | COBOL Structural Analyst *(new)* | Deep structural + semantic analysis of COBOL programs |
| **Crane** | Dependency Mapper *(new)* | Cross-program dependency graph and migration order |
| **Shifu** | Business Logic Extractor *(new)* | Business rules, use cases, spec layer population |
| **Oogway** | Migration Architect *(existing)* | Target architecture and migration strategy |
| **Tigress** | PM *(existing)* | Epics, stories, GitLab management |
| **Po** | Dev *(existing)* | Code transformation (Java / Python / COBOL) |
| **Tai Lung** | QA *(existing)* | Validates transformed code — lets nothing slip through |
| **Monkey** | SM *(existing)* | Sprint management and delivery cadence |

---

## What We Build (New Agents)

Three new analysis agents + one middleware knowledge MCP server.

### Viper — COBOL Structural Analyst

The most foundational agent. Everything downstream depends on its output.

**Purpose:** Performs deep structural and semantic analysis of COBOL source files. Combines a fast static pre-pass with AI-driven per-cluster analysis.

**Inputs:**
- COBOL source files (`.cbl`, `.cob`, `.cobol`)
- Copybook files (`.cpy`)
- `glossary.md` — maps cryptic COBOL field names to business terms (optional)
- `delta-macros-mcp` — middleware knowledge server (called as needed)

**Two-Phase Approach:**

*Phase 1 — Static Pre-Pass (no AI, pure parsing):*
- IDENTIFICATION DIVISION: program name, author, date, purpose comments
- DATA DIVISION: all 01-level groups, elementary items, FILE SECTION (FD entries), WORKING-STORAGE, LINKAGE SECTION; glossary mappings applied at this stage
- PROCEDURE DIVISION: all paragraph names + line numbers, PERFORM graph (who calls whom), CALL statements (external programs), COPY statements (copybook refs), EXEC SQL blocks (tables + operations), EXEC CICS blocks, DELTA-* macro calls (resolved via MCP)
- Entry points and exit points (`STOP RUN`, `GOBACK`)
- Complexity scoring (see below)
- Semantic cluster formation from paragraph call graph

*Phase 2 — AI Analysis per Semantic Cluster:*
- Plain English description of what each cluster does
- Data transformations performed
- Business rules embedded in conditionals
- Delta macro context (looked up from MCP during analysis)
- Anti-patterns flagged (GOTO, ALTER, dead code, etc.)

**Complexity Scoring:**
- `Low` — sequential batch, flat file I/O, no SQL or CICS
- `Medium` — DB2/SQL, indexed VSAM files, moderate PERFORM nesting
- `High` — CICS transactions, REDEFINES, deep PERFORM nesting, multiple copybooks, heavy delta macro usage

**Chunking Strategy — Semantic Paragraph Clustering:**

The reference repo uses structural DIVISION → SECTION → paragraph boundaries. We go further with semantic clustering by PERFORM relationships:
1. Static pre-pass builds a paragraph call graph
2. Paragraphs that call each other are grouped into the same cluster
3. Each chunk = full DATA DIVISION summary + one cluster
4. Processing order follows the dependency graph (entry points first, parents before children)
5. Complexity score drives token budget per chunk

This ensures every chunk has the data context it needs and logically related code stays together.

**Output:**
- Analysis markdown file (see schema below)
- SQLite records (program metadata, data items, paragraphs, middleware calls)

**Analysis Markdown Schema:**
```
# COBOL Analysis: [PROGRAM-NAME]

## Program Summary
  - Type: Batch | Online (CICS) | Called Subroutine
  - Complexity: Low | Medium | High
  - Reasons for complexity score

## Data Dictionary
  - Data items grouped by 01-level structure
  - Business term (from glossary) alongside COBOL name
  - Type, length, initial value

## File & Database Interactions
  - Input/output files (FD entries)
  - DB2 tables + operations (from EXEC SQL)
  - CICS resources (from EXEC CICS)

## External Dependencies
  - COPY books used
  - External PROGRAMs CALLed
  - Delta macros called (with description from MCP)
  - Entry / exit points

## Paragraph Call Graph  [mermaid diagram]
  - Full PERFORM relationship tree
  - Entry points highlighted

## Paragraph Analysis (per cluster)
  For each cluster:
  - Paragraph names in cluster
  - Called by / calls
  - Plain English: what it does
  - Data items it reads / writes
  - Business rules identified
  - SQL / CICS / Delta macro operations (if any)

## JCL Context (if provided)
  - Job steps, DD names, datasets, scheduling dependencies

## Migration Risk Notes
  - Patterns that complicate migration
  - Recommended chunk order for migration
```

---

### Crane — Dependency Mapper

**Purpose:** Builds a complete cross-program dependency graph across the entire codebase — not just a single program. Runs against all programs after Agent 1 has analysed each file individually.

**Key insight from reference repo:** Dependency extraction is primarily regex-based (no AI needed). AI is only used for the architectural analysis layer on top of the extracted graph.

**How it works:**

*Step 1 — Regex Extraction (no AI):*
- Scans all COBOL files for: `COPY` statements (copybook deps), `CALL` statements (inter-program deps), `EXEC SQL` blocks (table deps), `EXEC CICS LINK` (CICS program deps), `DELTA-*` macro calls (middleware deps), file `OPEN/READ/WRITE/CLOSE` operations
- Deduplicates on source + target + type + line number
- Builds in-memory dependency map across all programs

*Step 2 — AI Analysis:*
- Identifies circular dependencies
- Flags dead code (programs/paragraphs with no callers)
- Groups programs into logical subsystems
- Recommends migration order (least-coupled first)
- Produces Mermaid diagram of the full dependency graph

**Output:**
- Mermaid dependency graph (program-to-program, program-to-copybook)
- Dependency markdown report (circular deps, orphans, subsystem groupings, recommended migration order)
- SQLite records (dependencies table: source, target, type, line number)

---

### Shifu — Business Logic Extractor

**Purpose:** Consumes the structural analysis (Agent 1) and dependency map (Agent 2) to produce both a business-readable document and a structured **spec layer** — the machine-readable intermediate representation that bridges analysis and code generation.

**Key insight from reference repo:** "Identify WHAT the business does, not HOW the code works." The glossary is injected as context to make technical logic accessible to non-technical stakeholders and to name things correctly in the spec.

**Inputs:**
- Agent 1 analysis markdown (per program)
- Agent 2 dependency report
- `glossary.md`
- `delta-macros-mcp`

**Output — Business Markdown:**
```
# Business Analysis: [PROGRAM-NAME]

## Business Purpose
  One or two sentence plain-English description.

## Use Cases
  For each identified use case:
  - Trigger (what starts this process)
  - Description
  - Step sequence
  - Actors involved

## Business Rules
  - Validation rules (field-level constraints)
  - Logic rules (conditional business constraints)
  - Each rule linked to the paragraph/cluster it came from

## Data Entities
  - Business entities managed by this program
  - Fields with business names (from glossary)
  - Relationships between entities
```

**Output — Spec Layer (SQLite tables populated):**

| Table | What gets written |
|---|---|
| `spec_rosetta_dictionary` | COBOL field name ↔ business term (from glossary + AI inference) |
| `spec_data_entities` | Business entities this program manages |
| `spec_data_fields` | Fields on each entity with types and constraints |
| `spec_business_rules` | Extracted rules with source paragraph reference |
| `spec_service_definitions` | The service/API this program will become |
| `spec_service_operations` | Individual operations the service exposes |
| `spec_operation_inputs` | Parameters per operation |
| `spec_operation_rules` | Which business rules apply to which operation |

This spec layer is what the **Migration Architect** and **Dev agent** consume to design and generate the target system — not raw COBOL analysis markdown.

---

## Supporting Infrastructure

### delta-macros-mcp (Middleware Knowledge Server)

**Purpose:** A dedicated MCP server that acts as a queryable knowledge base for all Delta middleware macros. Any agent in the pipeline can call it to understand what a macro does without that knowledge being hardcoded into any agent.

**Input:** A folder of Delta macro markdown files (one file per macro).

**Delta Macro Markdown Format** (one file per macro):
```markdown
# DELTA-MACRO-NAME

## Category
[Messaging | File I/O | Transaction | Database | System | ...]

## Purpose
One paragraph describing what this macro does.

## COBOL Call Signature
```cobol
CALL 'DELTA-MACRO-NAME' USING PARAM-1
                               PARAM-2
                               RETURN-CODE
```

## Parameters
| Parameter | Direction | Type | Description |
|---|---|---|---|
| PARAM-1 | IN | PIC X(8) | ... |
| RETURN-CODE | OUT | PIC 9(4) | Completion code |

## Return Codes
| Code | Meaning |
|---|---|
| 0000 | Success |
| 0001 | ... |

## Behaviour
Detailed description of runtime behaviour.

## Side Effects
- Any state changes, audit writes, counter increments, etc.

## Transaction Awareness
Behaviour within DELTA-BEGIN-TRANS / DELTA-END-TRANS / DELTA-ROLLBACK blocks.

## Notes
Any caveats, limitations, or usage guidance.
```

**Tools exposed:**
- `get_macro(name)` — returns full markdown content for a named macro
- `search_macros(keyword)` — returns matching macro names and purpose lines
- `list_categories()` — returns all categories with macro names grouped

**Consumers:** COBOL Structural Analyst, Business Logic Extractor, Migration Architect

---

## Storage Layer

**SQLite only** (no Neo4j — the reference repo mentions Neo4j in docs but the actual implementation is SQLite throughout).

### Core Tables

| Table | Purpose |
|---|---|
| `runs` | Migration execution records (started, completed, status, source, output) |
| `cobol_files` | Source files per run (name, path, is_copybook, content) |
| `analyses` | Agent 1 output per file (raw analysis, divisions, variables, paragraphs as JSON) |
| `dependencies` | Agent 2 output — file-to-file relationships (source, target, type, line number) |
| `metrics` | Aggregated stats (total programs, copybooks, circular deps, Mermaid diagram) |

### Chunking Support Tables

| Table | Purpose |
|---|---|
| `chunk_metadata` | Processing status per chunk (start/end line, tokens used, status, converted code) |
| `signatures` | COBOL paragraph → target method name + signature |
| `type_mappings` | COBOL variable type → target language type |
| `forward_references` | Unresolved method calls across chunk boundaries |

### Spec Layer Tables (populated by Agent 3)

| Table | Purpose |
|---|---|
| `spec_rosetta_dictionary` | Legacy field name ↔ modern business term |
| `spec_data_entities` | Business data structures |
| `spec_data_fields` | Fields per entity |
| `spec_business_rules` | Operational constraints and validation rules |
| `spec_service_definitions` | Services/APIs that replace COBOL programs |
| `spec_service_operations` | Individual service operations |
| `spec_operation_inputs` | Parameters per operation |
| `spec_operation_rules` | Rule-to-operation bindings |

Enables cross-program queries such as:
- *"Which programs call DELTA-SEND-MSG?"*
- *"What programs write to table ACCT-MASTER?"*
- *"Show all High complexity programs not yet migrated"*
- *"Which services depend on the same data entity?"*

---

## Overall Agent Pipeline

```
COBOL Source Files + Copybooks
Delta Macro Docs (markdown)
Glossary (markdown)
        ↓
┌─────────────────────────────────────────────┐
│         delta-macros-mcp (always on)        │
│  Queryable by any agent at any time         │
└─────────────────────────────────────────────┘
        ↓
[Viper — COBOL Structural Analyst]         ← per file, parallelisable
  Phase 1: static parse → clusters + complexity
  Phase 2: AI analysis per cluster → markdown + SQLite
        ↓
[Crane — Dependency Mapper]                ← across all files
  Step 1: regex extraction → dependency map
  Step 2: AI analysis → subsystems, migration order → markdown + SQLite
        ↓
[Shifu — Business Logic Extractor]         ← per file, consumes Viper + Crane
  Business rules + use cases → markdown
  Spec layer population → SQLite spec tables
        ↓
[Oogway — Migration Architect]             ← reads spec layer
  Target architecture + migration strategy
        ↓
─ ─ ─ ─ ─ ─ GitLab boundary ─ ─ ─ ─ ─ ─ ─ ─
[Tigress — PM]                             ← creates Epics + Stories in GitLab
  Epics and stories per program/module
  GitLab README updated with migration status
        ↓
[Po — Dev]                                 ← reads spec layer
  Code transformation (Java / Python / COBOL)
        ↓
[Tai Lung — QA]                            ← lets nothing slip through
  Validates transformed code vs original behaviour
  Epic completion triggers review in GitLab
        ↓
[Monkey — SM]
  Sprint management and delivery cadence
```

---

## GitLab Integration

GitLab is the delivery management layer. It is **not** used during the analysis phase — Viper, Crane and Shifu outputs stay in SQLite and markdown only.

GitLab becomes active **after Oogway (Architect) completes the migration architecture.**

### What lives in GitLab

| GitLab Artefact | Created by | Content |
|---|---|---|
| **Epics** | Tigress (PM) | One Epic per logical subsystem (from Crane's dependency groupings) |
| **User Stories / Issues** | Tigress (PM) | One Issue per COBOL program to be migrated; labelled with complexity and type |
| **Milestones** | Monkey (SM) | One Milestone per sprint |
| **README.md** | Updated by pipeline | Current migration status — programs done, in progress, not started |

### Labels

```
complexity::low | complexity::medium | complexity::high
type::batch | type::online | type::subroutine
status::not-started | status::in-progress | status::migrated | status::verified
```

### Epic completion review

When all stories under an Epic are closed (migrated + verified by Tai Lung), the Epic triggers a **review gate** — a manual review before the subsystem is signed off as complete.

### README status format

```markdown
## Migration Status — [Project Name]

Last updated: [date]

| Program | Type | Complexity | Status |
|---|---|---|---|
| CUST-INQ | Online | High | In Progress |
| ACCT-BAT | Batch | Low | Migrated ✓ |
| ...

**Summary:** X of Y programs complete | Z in progress
```

### What is NOT in GitLab
- Analysis outputs (Viper, Crane, Shifu) — these live in SQLite + markdown only
- Raw COBOL or generated code — managed in the code repository
- Agent-to-agent communication — internal to the pipeline

---

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Target language selection | Oogway + Po decide | Analysis agents stay target-agnostic |
| Chunking strategy | Semantic paragraph clustering | Preserves logical coherence better than structural DIVISION/SECTION boundaries used in reference repo |
| Output format | Markdown (human) + SQLite (machine) | Both needed for different consumers |
| Intermediate representation | Spec layer in SQLite | Dev agent consumes structured specs, not raw analysis markdown |
| Middleware knowledge | Separate MCP server | Decoupled, reusable, updateable without changing agents |
| Delta macro migration equivalents | Migration Architect figures out | Not pre-mapped; architect reasons from macro behaviour docs |
| Glossary | Shared input to Viper, Crane, Shifu | Applied at Phase 1 before any AI analysis; also drives spec_rosetta_dictionary |
| Graph database | SQLite only (no Neo4j) | Reference repo documents Neo4j but implements SQLite; avoids unnecessary infrastructure |
| Dependency extraction | Regex-based (no AI) | Fast, deterministic, no token cost for structural facts |
| GitLab scope | Delivery only (post-architecture) | Analysis stays internal; GitLab manages Epics, Stories, status README |
| Agent names | Kung Fu Panda characters | Viper, Crane, Shifu (new); Oogway, Tigress, Po, Tai Lung, Monkey (existing BMAD) |

---

## Reference

- [Microsoft + Bankdata Legacy Modernisation Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents)
- [Bankdata announcement](https://www.bankdata.dk/about/news/microsoft-and-bankdata-launch-open-source-ai-framework-for-modernizing-legacy-systems)
- See `reference-repo-mapping.md` for which reference repo files to consult when designing each component
