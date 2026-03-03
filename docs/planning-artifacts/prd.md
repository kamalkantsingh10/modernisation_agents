---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
inputDocuments:
  - docs/planning-artifacts/product-brief-modernisation_agents-2026-03-01.md
  - docs/planning-artifacts/research/market-cobol-modernisation-agents-research-2026-03-01.md
  - docs/project_idea.md
workflowType: 'prd'
classification:
  projectType: developer_tool
  domain: scientific
  complexity: medium
  projectContext: greenfield
---

# Product Requirements Document — Mainframe Modernisation Agents

**Author:** Kamal
**Date:** 2026-03-01
**Type:** Developer Tool / BMAD Expansion Pack — locally deployed, greenfield

---

## Executive Summary

Mainframe Modernisation Agents reinvents the SDLC for mainframe modernisation. Traditional agile assumes you understand what you're building. COBOL estates break that assumption entirely: no documentation, no living institutional knowledge, systems that have accreted business rules over decades that nobody fully understands. Applying standard agile to mainframe modernisation is why the industry has a 70% project failure rate.

This project creates a suite of specialised AI agents — packaged as a **BMAD Expansion Pack** — that together implement a re-envisioned agile process built specifically for the realities of COBOL modernisation. Each agent owns a discrete, sequenced stage of a reimagined SDLC. Each stage is a hard prerequisite for the next. "Understand first, convert later" is not a team norm — it is the architecture of the pipeline itself.

The agents created by this project are:
- **Viper** — structural COBOL analysis per module
- **Crane** — cross-module dependency mapping
- **Shifu** — business rule extraction and spec layer population
- **Oogway** — migration architecture
- **Tigress** — GitLab project management and delivery structuring
- **Po** — target-language code generation
- **Tai Lung** — QA validation and sign-off

All agents run locally in any BMAD-compatible IDE (Claude Code, Cursor, and equivalents). A shared SQLite intermediate representation (spec layer) carries structured understanding forward through every agent stage, eliminating the context loss that causes traditional approaches to fail at handoff points. Four local MCP servers provide agents with the computational tools they call: COBOL parsing, spec layer CRUD, macro/middleware knowledge, and GitLab integration.

### What Makes This Special

**A new SDLC, not a better tool** — Every existing tool (IBM watsonx, AWS Transform, Micro Focus) automates the *conversion* step of the old SDLC. This project replaces the entire process model: structured discovery → validated understanding → architecture → delivery → verification. Each agent gates the next. No shortcutting.

**SQLite spec layer as the SDLC backbone** — `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows` — the first open-source formalisation of COBOL program semantics as a relational schema. Every downstream agent consumes structured data, not unstructured markdown. This eliminates the interpretation gap that causes handoff failures in every existing tool.

**Agile delivery built in** — Tigress maps the analysed estate into a fully managed GitLab project: Epics per subsystem, Issues per module, sprint milestones, label taxonomy, and a live README dashboard. The reimagined SDLC produces a sprint-ready delivery backlog grounded in verified understanding.

---

## Success Criteria

### User Success

**Alex (COBOL Factory Analyst — primary pipeline operator):**
- Viper Phase 1 static pre-pass on any COBOL module: **< 15 minutes**
- AI analysis accuracy on first pass validated by COBOL expert: **> 90%** — no critical structural misidentifications requiring rework
- Programs tractably analysable per sprint: **10–20** (vs 1–2 manually)
- Alex stays in the expert/reviewer seat — every agent output is something he refines, not builds from scratch

**Priya (Enterprise Architect — primary output consumer):**
- Crane dependency graph surfaces subsystem boundaries and migration order without manual cross-referencing
- Spec layer is directly consumable by Oogway — no manual translation step between analysis and architecture
- Full estate structural picture available before any migration commitment is made

**Claire (Business Validator — Shifu output consumer):**
- Business rules correctly extracted on first Shifu pass: **> 85%** — Claire confirms without major corrections
- Every business rule traceable: Shifu markdown → spec layer → Po output → Tai Lung validation

### Business Success

| Horizon | Objective |
|---|---|
| **3 months** | BlackJack pipeline runs end-to-end: Viper → Crane → Shifu → Oogway → Tigress → Po → Tai Lung. Full demo in a single session. |
| **6 months** | Pipeline configurable for a real client estate — glossary loaded, `delta-macros-mcp` populated, first real COBOL program analysed |
| **12 months** | At least one complete application (all modules) processed through to verified GitLab Epics closed |

### Technical Success

- All 7 agents produce correct, well-formed outputs at their stage
- SQLite spec layer fully populated after Shifu — all `spec_*` tables have data, queryable by downstream agents
- `delta-macros-mcp` resolves macro lookups correctly for all agents
- No agent requires manual intervention to pass output to the next — pipeline handoffs are automated
- Pipeline is re-runnable: re-processing a module updates the spec layer without requiring a full reset

### Measurable Outcomes

- **Pipeline completeness:** BlackJack corpus (8 modules, 3 copybooks) processed end-to-end with all agent outputs present
- **Spec layer integrity:** All `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows` tables populated for all 8 modules
- **Migration readiness:** Oogway architecture produced; Tigress GitLab Epics created; Po code generated; Tai Lung sign-off on each Epic
- **Zero gaps between stages:** No manual file manipulation or prompt engineering required to move output between agents

---

## Product Scope & Phased Development

### MVP Strategy

**Approach:** Problem-solving MVP — prove the complete pipeline works end-to-end on the BlackJack COBOL corpus before any client engagement. Validates COBOL parsing accuracy, spec layer integrity, agent-to-agent handoffs, and LLM reliability in a controlled environment.

**Resource requirements:** Small core team — 1 COBOL expert (Alex profile), 1 architect/engineer. Agents are configuration; MCP servers are the primary engineering effort (4 servers).

### MVP Feature Set — BlackJack End-to-End

**Must-Have: 7 BMAD Agent Definitions**

| Agent | MVP Scope |
|---|---|
| Viper | Phase 1 static pre-pass + Phase 2 AI analysis; anti-pattern flagging; complexity scoring |
| Crane | Cross-module dependency map; Mermaid diagram; subsystem detection; migration order |
| Shifu | Business markdown per module; spec layer population (all `spec_*` tables) |
| Oogway | Target architecture from spec layer; one target language (Java or Python — TBD) |
| Tigress | GitLab project setup; Epics + Issues; milestone structure; README dashboard |
| Po | Target-language code per module from spec layer |
| Tai Lung | QA validation per module against spec layer; Epic sign-off |

**Must-Have: 4 MCP Servers**

| MCP Server | MVP Scope |
|---|---|
| `cobol-parser-mcp` | Parse COBOL-85 / IBM Enterprise COBOL; call graph; complexity scoring; anti-pattern detection; unknown construct flagging |
| `specdb-mcp` | Full CRUD on all `spec_*` SQLite tables; `init_schema`; idempotent writes |
| `delta-macros-mcp` | `get_macro`, `search_macros`, `list_categories`, `add_macro`; graceful not-found handling |
| `gitlab-mcp` | Full GitLab integration: Epics, Issues, labels, milestones, boards, comments, README, sign-off |

**Must-Have: Supporting Infrastructure**

- BMAD expansion pack installer (deploys agents + starts MCP servers)
- Glossary file format + loading mechanism (field-name resolution in agent outputs)
- SQLite schema definition (all `spec_*` tables)
- BlackJack corpus (8 `.cbl` modules, 3 `.cpy` copybooks) as reference test case

### Phase 2 — Expansion Pack Maturity

- Second target language support in Oogway/Po
- JCL context analysis for clients with job stream dependencies
- Parallel Viper processing for large estates (MVP runs sequentially)
- Automated complexity-based sprint sizing in Tigress
- AI-assisted glossary suggestion (Viper proposes, Alex confirms)
- Client engagement playbook template (onboarding guide, glossary template, macro doc template)

### Phase 3 — BMAD Ecosystem Contribution

- RPG and PL/I language support alongside COBOL
- Behavioural equivalence testing framework in Tai Lung (formal compliance differentiator)
- Contribution to BMAD open-source ecosystem as official expansion pack
- Factory metrics dashboard across engagements
- JIRA / Azure DevOps integration (post-GitLab)

### Risk Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| **LLM reliability** — inaccurate COBOL analysis | Corrupt spec layer → wrong architecture | Alex expert review gate before spec layer writes; agents flag low-confidence outputs explicitly |
| **COBOL dialect gaps** — `cobol-parser-mcp` misparses variant syntax | Silent errors propagate downstream | Unrecognised constructs flagged, not ignored; BlackJack corpus tests known dialect patterns |
| **Scope creep on MCP servers** | MVP delayed | Hard boundary: 4 MCP servers, defined tool lists; no new tools without explicit scope change |
| **BMAD compatibility** — expansion pack breaks across IDE versions | Adoption blocked | Follow BMAD module conventions exactly; test against Claude Code + Cursor as minimum baseline |

---

## User Journeys

### Journey 1 — Alex Runs the Pipeline on a New COBOL Module (Success Path)

Alex has received the source files for a new client's payroll processing system. It's a 4,200-line COBOL program called `PAYROLL-CALC.cbl` with a comment at the top that says "DO NOT TOUCH — last modified 1994."

He runs Viper against it. Phase 1 completes in 11 minutes: a call graph of 47 paragraphs, 3 REDEFINES, 12 PERFORM THRU blocks, and a complexity score of High. He spots two GOTOs that Viper has flagged as anti-patterns — he already knew they'd be there. The fact that Viper caught them means he doesn't have to hunt.

Phase 2 runs. The AI clusters paragraphs by semantic function and produces plain-English descriptions. Alex reads through, corrects one misidentification (the AI called a tax-band lookup a "validation routine" — it's a calculation), and marks the rest as reviewed.

Shifu runs next. The spec layer populates: `PAYROLL-CALC` appears in `spec_entities`, seven business rules in `spec_rules`, three data flows in `spec_data_flows`. The business markdown reads: "This program calculates gross pay by applying hourly rate × hours worked, applies NI band deductions using a stepped lookup table, and writes net pay to `PAYROLL-OUT`." Accurate. He approves it. Viper posts a structured completion comment on the module's GitLab Issue and applies the `Viper-Complete` label.

**The moment that matters:** Alex fully documented a 4,200-line program in under two hours. He reviewed and corrected a model, not built one from scratch.

*Requirements revealed: FR1–FR8, FR14–FR18, FR50, FR56.*

---

### Journey 2 — Alex Hits an Unknown Delta Macro (Edge Case)

Midway through Viper's Phase 1 pass on `ACCOUNTS-BATCH.cbl`, the agent calls `delta-macros-mcp` to look up `DLTM-ACCT-LOCK`. The MCP server returns: not found.

Viper flags the unknown macro, marks the affected paragraph with an unresolved dependency warning, and continues rather than halting. Alex sees the warning. He knows what `DLTM-ACCT-LOCK` does — he learned it in the first week on this engagement.

He writes a short markdown file describing the macro: purpose, parameters, return. He adds it to the MCP server's macro library via `add_macro`. He re-runs Viper on just the affected paragraph cluster. The macro resolves. Analysis completes cleanly.

**The moment that matters:** The pipeline flagged what it didn't know, let Alex fill the gap, and let him re-run only what was affected. No full restart, no lost work.

*Requirements revealed: FR8, FR36, FR38.*

---

### Journey 3 — Priya Designs the Migration Architecture from the Spec Layer

Priya receives the Crane dependency map for a 14-module payroll application. She opens the Mermaid diagram. Three subsystems emerge immediately: payment calculation, tax processing, and file I/O. Migration order puts file I/O first — no inbound dependencies, extractable cleanly.

She queries the spec layer directly: `spec_entities` and `spec_operations` reveal `EMPLOYEE-RECORD`, `PAY-PERIOD`, and `TAX-BAND` as core entities. `TAX-BAND` is read-only in six modules and written in one: `TAX-SETUP.cbl`. Candidate for a shared service.

She opens Oogway and feeds it the spec layer. Oogway produces a target Java architecture — one service per subsystem, a shared `TaxBandService` extracted from the monolith. The architecture follows the seam lines Crane surfaced.

**The moment that matters:** Priya designed an architecture grounded in the actual system structure. The seam lines follow real module boundaries, not guesses.

*Requirements revealed: FR9–FR13, FR19–FR22.*

---

### Journey 4 — New Engagement Setup (Pipeline Configuration)

A new client engagement starts. Alex needs to configure the pipeline for an estate he's never seen.

He runs the BMAD expansion pack installer — agents deploy, MCP servers start. He initialises the SQLite database with a single `init_schema` call. He creates the glossary file: `WS-CUST-BAL` → `Customer Account Balance`, `PROC-DT` → `Processing Date`. Forty entries. He points `delta-macros-mcp` at an empty macro library directory.

He runs Viper on the first program. Glossary resolves field names correctly in the output — business terms appear, not COBOL identifiers. Tigress initialises the GitLab project: label taxonomy created, milestone structure set up, issue board configured. The pipeline is ready. It took 45 minutes.

**The moment that matters:** Two inputs — glossary + macro library — contextualise the entire pipeline for any COBOL estate. No code changes.

*Requirements revealed: FR34–FR37, FR46–FR48.*

---

### Journey Requirements Summary

| Capability | Revealed By |
|---|---|
| Viper Phase 1 static pre-pass (call graph, anti-pattern detection, complexity scoring) | Journey 1 |
| Viper Phase 2 AI analysis with cluster-based semantic grouping | Journey 1 |
| Shifu business rule extraction and spec layer population | Journey 1 |
| Analyst review/correction workflow for agent outputs | Journey 1 |
| Graceful unknown-macro handling with partial re-run | Journey 2 |
| `delta-macros-mcp` macro write/ingest path | Journey 2 |
| Crane cross-module dependency map with Mermaid output and subsystem detection | Journey 3 |
| Spec layer SQL queryability by external tools | Journey 3 |
| Oogway architecture generation from spec layer | Journey 3 |
| BMAD expansion pack installer | Journey 4 |
| SQLite schema initialisation | Journey 4 |
| Glossary file format, loading, and field-name resolution | Journey 4 |
| GitLab project initialisation (labels, milestones, board) | Journey 4 |

---

## Domain-Specific Requirements

### LLM Reliability

Agent outputs depend on probabilistic LLM responses. The pipeline must surface confidence and flag uncertainty explicitly — AI output is never treated as authoritative without analyst review. Agents must indicate unresolved or low-confidence analysis in their output; the pipeline must not silently pass uncertain outputs to downstream agents as validated.

### COBOL Dialect Coverage

COBOL is not a single language. Viper must handle or explicitly flag:
- IBM Enterprise COBOL and VS COBOL II syntax variants
- CICS transaction constructs (`EXEC CICS ... END-EXEC`)
- DB2 embedded SQL (`EXEC SQL ... END-EXEC`)
- Client-specific Delta macros (resolved via `delta-macros-mcp`)

Silent misparsing of a dialect variant produces a corrupt spec layer and a wrong architecture. Unrecognised constructs must be flagged, not ignored.

### Pipeline Reproducibility

Running the pipeline twice on the same input must produce equivalent SQLite spec layer output. LLM variance in intermediate markdown is acceptable; variance in the spec layer is not. Spec layer writes must be idempotent — re-running a module updates records rather than creating duplicates or contradictions.

### Data Locality

Client COBOL source code and extracted business rules are confidential. No source code, business rules, or extracted spec data may leave the local environment. LLM selection is constrained: local models preferred; if remote API calls are used, data handling boundaries must be documented and enforced at the agent level.

---

## Innovation & Novel Patterns

### Detected Innovation Areas

**1. The SDLC as an executable agent pipeline**

Traditional modernisation methodologies are documents. This project turns the SDLC into machine-enforced software. Each stage is a discrete agent with defined inputs, outputs, and a hard dependency on the previous stage. The process cannot be shortcut because the process *is* the software. This is a new paradigm for how delivery methodology is implemented.

**2. SQLite as a structured intermediate representation for COBOL**

No existing commercial or open-source COBOL tool implements a queryable, structured IR between analysis and implementation. `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows` — the first open-source formalisation of COBOL program semantics as a relational schema. Every downstream agent consumes structured data, not unstructured markdown, eliminating the interpretation gap that causes handoff failures.

**3. Structural enforcement of "understand first"**

Every existing tool treats understanding as a phase that can be compressed or skipped. This pipeline makes skipping structurally impossible: Oogway cannot run until Shifu has populated the spec layer; Po cannot run until Oogway has produced an architecture. The constraint is in the dependency graph, not in team discipline.

**4. Local MCP server as domain knowledge injection**

`delta-macros-mcp` is a novel pattern: a locally-running MCP server that gives every agent on-demand access to client-specific institutional knowledge (proprietary macros, middleware patterns) without model fine-tuning or prompt stuffing. Knowledge is maintained as human-readable markdown files, updated incrementally.

### Market Context & Competitive Landscape

| Tool | What They Do | What's Missing |
|---|---|---|
| IBM watsonx Code Assistant | AI-assisted COBOL → Java conversion | No structured IR; skips understanding; cloud-locked |
| AWS Mainframe Modernisation | Automated refactoring and replatforming | No business rule extraction; no compliance artefacts |
| Micro Focus / OpenText | Modernisation tooling + services | Tool-centric, not process-enforcing; no open IR |
| Microsoft/Bankdata (open-source) | COBOL parsing and analysis | No business rule extraction; no delivery integration; no IR |

None implement a structured intermediate representation. None enforce understanding as a pipeline constraint. None produce compliance-grade business rule artefacts as a byproduct of analysis. None integrate analysis through to sprint delivery.

### Validation Approach

- **BlackJack corpus** — 8 COBOL modules with realistic technical debt patterns serve as the proof-of-concept and regression baseline
- **Expert validation gate** — Alex reviews every agent output as the human quality gate; > 90% accuracy on first pass is the validation criterion
- **Spec layer integrity check** — completeness and internal consistency validated before Oogway is permitted to run

---

## BMAD Expansion Pack Requirements

Mainframe Modernisation Agents is a **BMAD Expansion Pack** — a self-contained, installable extension to the BMAD framework adding a complete mainframe modernisation capability to any BMAD-compatible IDE. Agent definitions, workflow files, step files, and config patterns all conform to BMAD standards.

This is the first domain-specific BMAD expansion pack — establishing the pattern for how BMAD can be extended into specialised technical domains.

### Agent Artefacts

Each agent is a complete BMAD agent definition, installable via the expansion pack, usable in any BMAD-compatible IDE:

| Agent | Role | Primary MCP Tools |
|---|---|---|
| **Viper** | COBOL structural analyst — per module | `cobol-parser-mcp`, `delta-macros-mcp`, `specdb-mcp`, `gitlab-mcp` |
| **Crane** | Cross-module dependency mapper | `cobol-parser-mcp`, `specdb-mcp`, `gitlab-mcp` |
| **Shifu** | Business rule extractor | `specdb-mcp`, `delta-macros-mcp`, `gitlab-mcp` |
| **Oogway** | Migration architect | `specdb-mcp`, `gitlab-mcp` |
| **Tigress** | GitLab PM and delivery structurer | `gitlab-mcp`, `specdb-mcp` |
| **Po** | Target-language code generator | `specdb-mcp`, `gitlab-mcp` |
| **Tai Lung** | QA validator and sign-off | `specdb-mcp`, `gitlab-mcp` |

### MCP Server Artefacts

| MCP Server | Purpose | Tools Exposed |
|---|---|---|
| **`delta-macros-mcp`** | Client-specific macro and middleware knowledge | `get_macro`, `search_macros`, `list_categories`, `add_macro` |
| **`cobol-parser-mcp`** | COBOL static pre-pass: parsing, call graph, complexity scoring | `parse_module`, `extract_call_graph`, `score_complexity`, `detect_antipatterns` |
| **`specdb-mcp`** | SQLite spec layer CRUD — shared IR across all agents | `read_spec`, `write_spec`, `query_spec`, `init_schema` |
| **`gitlab-mcp`** | Full GitLab integration for all agents | `create_epic`, `create_issue`, `apply_label`, `remove_label`, `create_milestone`, `assign_to_milestone`, `create_board`, `add_comment`, `update_readme`, `close_epic`, `update_issue_status` |

### Expansion Pack Structure

```
mainframe-modernisation/
├── agents/          # Viper, Crane, Shifu, Oogway, Tigress, Po, Tai Lung
├── workflows/       # Per-agent workflow files and step files
├── mcp-servers/     # cobol-parser-mcp, specdb-mcp, delta-macros-mcp, gitlab-mcp
├── templates/       # Glossary template, macro library template
├── config.yaml      # Expansion pack configuration
└── installer/       # BMAD-compatible installation script
```

### Installation & Setup

- Installed via BMAD installer into any BMAD-compatible IDE
- MCP servers start locally as part of setup
- SQLite database initialised via `specdb-mcp init_schema` — one call, schema ready
- Glossary file: structured template provided, populated per engagement
- `delta-macros-mcp` pointed at a macro library directory, populated incrementally

### Extensibility

- New agents: add a BMAD agent definition — immediately available in any connected IDE
- New MCP tools: extend existing servers or create new ones — agents call via standard MCP protocol
- Expansion pack pattern itself becomes reusable for other domain-specific BMAD packs

---

## Functional Requirements

### COBOL Analysis (Viper)

- **FR1:** Analyst can initiate structural analysis of a COBOL module and receive a paragraph call graph
- **FR2:** Analyst can view a complexity score (Low/Medium/High) for any analysed COBOL module
- **FR3:** Analyst can view anti-patterns detected in a COBOL module (GOTOs, nested PERFORMs, REDEFINES, etc.)
- **FR4:** Analyst can view extracted COPY, CALL, SQL, CICS, and Delta macro references per module
- **FR5:** Analyst can view AI-generated semantic cluster groupings for a module's paragraphs
- **FR6:** Analyst can view plain-English descriptions for each semantic cluster
- **FR7:** Analyst can review, correct, and approve AI analysis outputs before they are written to the spec layer
- **FR8:** Analyst can view a warning when Viper encounters an unrecognised COBOL construct or unknown Delta macro

### Dependency Mapping (Crane)

- **FR9:** Analyst can initiate cross-module dependency analysis across all COBOL modules in scope
- **FR10:** Architect can view a Mermaid dependency diagram showing relationships between all modules
- **FR11:** Architect can view detected subsystem groupings emerging from the dependency structure
- **FR12:** Architect can view a recommended migration order based on module dependencies
- **FR13:** Analyst can view detected circular dependencies and dead code across modules

### Business Rule Extraction & Spec Layer (Shifu)

- **FR14:** Analyst can initiate business rule extraction for a COBOL module using Viper and Crane outputs
- **FR15:** Business Validator can view plain-English business markdown for any module (purpose, use cases, business rules, data entities with glossary names)
- **FR16:** Business Validator can validate each extracted business rule as confirmed, corrected, or rejected
- **FR17:** System writes approved business rules, entities, operations, and data flows to the SQLite spec layer
- **FR18:** Analyst can re-run Shifu on a module and have the spec layer update idempotently without duplicates

### Migration Architecture (Oogway)

- **FR19:** Architect can initiate migration architecture generation from the populated spec layer
- **FR20:** Architect can view a target architecture document mapping COBOL subsystems to target-language services
- **FR21:** Architect can specify the target language as an input to Oogway
- **FR22:** Architect can review and modify the generated architecture before it is finalised

### Code Generation (Po)

- **FR23:** Developer can initiate target-language code generation for a module from the spec layer and architecture
- **FR24:** Developer can view generated target-language code for each COBOL module
- **FR25:** Developer can regenerate code for a specific module without affecting other modules

### QA Validation (Tai Lung)

- **FR26:** QA can initiate validation of generated code against spec layer business rules
- **FR27:** QA can view a validation report showing which business rules are confirmed, partially covered, or missing in the generated code
- **FR28:** QA can flag a module as requiring rework before sign-off

### Pipeline Configuration & Infrastructure

- **FR29:** Operator can initialise the SQLite spec layer schema with a single command via `specdb-mcp`
- **FR30:** Analyst can configure a client-specific glossary mapping COBOL field names to business terms
- **FR31:** Analyst can add a new macro definition to `delta-macros-mcp` without restarting the pipeline
- **FR32:** Operator can install the full BMAD expansion pack into any BMAD-compatible IDE via a standard installer
- **FR33:** Analyst can re-run any individual agent on a specific module without restarting the full pipeline
- **FR34:** Analyst can view a consolidated list of all unresolved constructs and macros flagged across pipeline stages

### COBOL Dialect & Construct Coverage

- **FR35:** System can parse and analyse IBM Enterprise COBOL and COBOL-85 modules
- **FR36:** System can detect and flag CICS transaction constructs within a COBOL module
- **FR37:** System can detect and flag DB2 embedded SQL constructs within a COBOL module
- **FR38:** System can parse COPY statements and resolve referenced copybooks
- **FR39:** All agents can resolve client-specific Delta macro references via `delta-macros-mcp` at analysis time

### GitLab Project Management (Tigress + All Agents)

**Project Initialisation**

- **FR40:** PM can initialise a GitLab project with standard label taxonomy: pipeline stage labels (`Viper-Complete`, `Crane-Complete`, `Shifu-Complete`, `Oogway-Complete`, `Po-Complete`, `QA-Complete`), complexity labels (`Complexity::Low`, `Complexity::Medium`, `Complexity::High`), and status labels (`In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`)
- **FR41:** PM can create a standard milestone structure per engagement phase (e.g., `Phase-1-Prove`, `Phase-2-Complete`) in GitLab
- **FR42:** PM can create a GitLab issue board configured with columns mapped to pipeline stages

**Module Lifecycle Tracking**

- **FR43:** Each COBOL module has a dedicated GitLab Issue tracking its complete pipeline lifecycle from analysis through QA sign-off
- **FR44:** Any agent can apply the appropriate stage completion label to a module's GitLab Issue upon completing its stage
- **FR45:** Any agent can transition a module Issue to `Awaiting-Review` status when its stage output requires analyst approval
- **FR46:** Analyst can close the review gate on a module Issue and transition it to the next pipeline stage

**Sprint & Iteration Planning**

- **FR47:** PM can create GitLab sprint milestones scoped to a specific set of modules based on Crane's migration order recommendation
- **FR48:** PM can assign module Issues to sprint milestones, respecting subsystem dependencies
- **FR49:** PM can view a milestone burndown showing open vs closed module Issues within a sprint

**Progress Reporting**

- **FR50:** Any agent can post a structured progress comment to a module's GitLab Issue when it completes a stage, including key outputs and any warnings or flags
- **FR51:** The GitLab project README is updated by any agent that changes module status — always reflects current pipeline state without manual intervention
- **FR52:** Client Sponsor can view a README dashboard showing total modules, modules per pipeline stage, modules blocked, and Epics signed off — at any time without requesting a status update
- **FR53:** PM can generate a milestone summary comment on any Epic showing sprint progress and outstanding items

**Review Gates & Sign-off**

- **FR54:** Business Validator can formally sign off on Shifu's business markdown by closing the `Awaiting-Review` gate on a module Issue
- **FR55:** QA can sign off on an Epic, triggering Epic completion in GitLab with a validation summary comment
- **FR56:** QA can formally close an Epic when all module Issues within it are `QA-Complete`

---

## Non-Functional Requirements

### Performance

- **NFR1:** Viper Phase 1 static pre-pass completes on any single COBOL module within **15 minutes** on standard developer hardware
- **NFR2:** `cobol-parser-mcp` parsing tools return results within **30 seconds** for any module up to 5,000 lines
- **NFR3:** `specdb-mcp` read and write operations complete within **2 seconds** for any single spec layer record or query
- **NFR4:** `delta-macros-mcp` macro lookups resolve within **1 second** per call
- **NFR5:** `gitlab-mcp` operations complete within **10 seconds** per API call under normal network conditions

### Security & Data Privacy

- **NFR6:** No COBOL source code, business rules, or extracted spec data is transmitted outside the local environment by any agent or MCP server
- **NFR7:** Where remote LLM API calls are used, source code is scoped to the minimum required context — no full-file dumps without documented justification
- **NFR8:** GitLab credentials are stored using the host IDE's or OS credential store — never hardcoded in agent definitions or MCP server config files
- **NFR9:** `delta-macros-mcp` macro library is stored locally and not synchronised to any external service

### Reliability & Reproducibility

- **NFR10:** Running any agent twice on the same input produces equivalent SQLite spec layer output — spec layer writes are idempotent
- **NFR11:** Any agent encountering an unrecognised construct, unknown macro, or LLM error fails with an explicit, actionable error message — silent failures are not permitted
- **NFR12:** A failed agent run does not corrupt existing spec layer records — partial writes roll back or are clearly flagged as incomplete
- **NFR13:** All MCP servers remain operational across agent session restarts without requiring full reinitialisation

### Integration & Compatibility

- **NFR14:** The BMAD expansion pack installs and operates correctly in any BMAD-compatible IDE (Claude Code and Cursor as minimum baseline)
- **NFR15:** All MCP servers conform to the MCP protocol specification — no proprietary extensions that break cross-IDE compatibility
- **NFR16:** `gitlab-mcp` supports GitLab Cloud and self-hosted GitLab instances (API v4)
- **NFR17:** The SQLite spec layer schema is versioned — schema migrations do not break existing data or require manual intervention

### Maintainability

- **NFR18:** Each BMAD agent definition is independently updatable without requiring changes to any other agent or MCP server
- **NFR19:** Each MCP server exposes a clearly defined, versioned tool interface — adding new tools does not break existing tool calls
- **NFR20:** Glossary file format and macro library format use human-readable, plain-text markup — no binary formats or proprietary schemas
- **NFR21:** The BlackJack corpus serves as the regression test baseline — any change to an MCP server is validated against BlackJack end-to-end before release
