# Story 3.4: Viper BMAD Agent Definition

Status: review

## Story

As an **analyst**,
I want a Viper agent I can invoke in my IDE to orchestrate COBOL structural analysis with built-in review gates,
So that I review and correct AI outputs rather than building analysis from scratch — staying in the expert seat.

## Acceptance Criteria

1. **Given** the Viper agent definition is installed in a BMAD-compatible IDE (Claude Code or Cursor) **When** the agent is invoked for a specific COBOL module **Then** it calls `parse_module` and `extract_call_graph` via `cobol-parser-mcp` (Phase 1) and displays results to the analyst.
2. **And** it calls `get_macro` from `delta-macros-mcp` for any Delta macro references encountered, surfacing `UNKNOWN_MACRO` warnings if the macro is not found in the library (FR8).
3. **When** Phase 1 is complete **Then** the analyst can review the call graph, complexity score (from `score_complexity`), anti-pattern list (from `detect_antipatterns`), and any flagged constructs before proceeding to Phase 2.
4. **And** the agent displays an explicit Phase 1 review gate — it does NOT advance to Phase 2 until the analyst confirms.
5. **When** Phase 2 (semantic clustering) completes **Then** the analyst can review each cluster's name, paragraph list, and plain-English description, correct individual cluster descriptions, and explicitly approve outputs before they are written to the spec layer (FR7).
6. **And** the write to specdb-mcp is triggered ONLY on explicit analyst approval — never automatically.
7. **When** an unrecognised COBOL construct is encountered **Then** the agent surfaces an explicit warning with the construct location — analysis continues rather than halting (FR8).
8. **When** the analyst triggers a re-run on the same module **Then** the agent re-processes only that module — other modules' spec layer data is unaffected (FR33).
9. **And** a consolidated list of all flagged constructs and macros is presented at the end of each run (FR34).
10. **And** the agent handles all `status: "error"` results from MCP tools by halting that phase, displaying an actionable error message, and prompting the analyst for next steps.

## Tasks / Subtasks

- [x] Task 1: Author `agents/viper.md` — Viper agent definition file (AC: all)
  - [x] Agent metadata block: `name: "viper"`, `title: "COBOL Structural Analyst"`, icon, capabilities list
  - [x] Activation section: load `config.yaml`, greet analyst with user_name, display menu
  - [x] Menu items:
    - `[SA]` Start Analysis — prompt for COBOL module path, begin Phase 1
    - `[V1]` View Phase 1 Results — display call graph, complexity score, anti-pattern list, flags
    - `[P2]` Proceed to Phase 2 — explicit Phase 1 approval gate → start semantic clustering
    - `[EC]` Edit Cluster — correct a specific cluster's name or description before approval
    - `[AP]` Approve & Write — explicit Phase 2 approval gate → write to spec layer via specdb-mcp
    - `[RR]` Re-run Module — re-run full analysis on the same module (overwrites session data, not other modules)
    - `[FL]` Show Flag List — consolidated list of all warnings and unresolved constructs
    - `[DA]` Dismiss Agent
  - [x] Phase 1 orchestration instructions:
    - Call `parse_module(program_name, source_path)` via `cobol-parser-mcp`
    - Call `extract_call_graph(program_name)` via `cobol-parser-mcp`
    - Call `score_complexity(program_name)` via `cobol-parser-mcp`
    - Call `detect_antipatterns(program_name)` via `cobol-parser-mcp`
    - For each Delta macro in `parse_module` result: call `get_macro(macro_name)` via `delta-macros-mcp`; collect `UNKNOWN_MACRO` flags for any not found
    - On any `status: "error"` result: halt Phase 1, display error, offer [retry / skip / quit]
    - Accumulate all `flags` from all tool calls into a session-level consolidated flag list
    - Display Phase 1 results and present `[V1]` / `[P2]` / `[DA]` options
  - [x] Phase 2 orchestration instructions (activated only after analyst selects `[P2]`):
    - Call `build_cluster_context(program_name)` via `cobol-parser-mcp`
    - Perform semantic clustering analysis using the context (paragraph names, PERFORM edges, DATA DIVISION field names) — analyst reviews AI output
    - Call `validate_cluster_output(program_name, clusters)` via `cobol-parser-mcp`
    - Present clusters for analyst review; allow `[EC]` edits
    - Do NOT call any specdb-mcp write tools until `[AP]` is explicitly selected
  - [x] Approval write instructions (activated only after analyst selects `[AP]`):
    - Call appropriate specdb-mcp write tools to persist: `cobol_files` entry, `analyses` record (complexity + anti-patterns), `dependencies` (COPY refs, CALL targets), cluster data
    - Confirm write success; display next steps
  - [x] Error handling rules: `status: "error"` = halt + display + prompt; `status: "warning"` = add to flag list + continue
  - [x] Re-run isolation rule: document in agent that re-running module X overwrites only that module's session data and spec layer records (idempotent via specdb-mcp)
  - [x] Consolidated flag list: accumulate all `flags` arrays from all tool calls; display in `[FL]` view and at end of completed run

- [x] Task 2: Register Viper agent in IDE (AC: 1)
  - [x] Add Viper agent entry to `.claude/commands/viper.md` — thin shim following same format as existing BMAD agent commands (e.g. `.claude/commands/bmad-agent-bmm-architect.md`), loading the full agent definition from `agents/viper.md`

## Dev Notes

### Architecture Guardrails

- **NET-NEW BMAD AGENT** — Viper is not a customisation of an existing BMAD agent. It must be authored from scratch following BMAD module conventions. Study the BMAD agent format by examining agents in `_bmad/bmm/agents/` for structure reference, but Viper lives in `agents/viper.md` (the expansion pack's own `agents/` folder).
- **BMAD compliance is mandatory** — the agent definition must be cross-IDE compatible (Claude Code + Cursor minimum). Follow exactly the BMAD agent authoring conventions for agent ID, persona, menu, activation steps.
- **MCP tools Viper uses** (all must be declared/referenced in agent):
  - `cobol-parser-mcp`: `parse_module`, `extract_call_graph`, `score_complexity`, `detect_antipatterns`, `build_cluster_context`, `validate_cluster_output`
  - `delta-macros-mcp`: `get_macro`
  - `specdb-mcp`: appropriate write tools for `cobol_files`, `analyses`, `dependencies` tables (check Story 1.3 for exact tool names)
- **Phase gate is enforced in the agent** — the agent's menu/activation logic must make it impossible to call `build_cluster_context` (Phase 2) without analyst first selecting `[P2]` after reviewing Phase 1 results. Similarly, `[AP]` is the only path to specdb writes.
- **Analyst is always in the expert seat** — every AI output (call graph display, complexity score, cluster groupings) is presented as information for analyst review, not as authoritative truth. The agent's persona should reinforce this.
- **Phase 1 time limit (NFR1: < 15 min)** — document this SLA in the agent's Phase 1 section. The agent cannot enforce it programmatically but should note to the analyst if Phase 1 seems slow.
- **Re-run isolation (FR33)** — when re-running, the agent re-calls the same Phase 1 tools. The idempotent write pattern in specdb-mcp (INSERT OR IGNORE + UPDATE) ensures re-runs update existing records without creating duplicates or touching other modules.
- **`status: "warning"` does NOT halt** — unrecognised constructs, unknown macros, and CICS/SQL flags produce warnings. The agent must add these to its consolidated flag list and continue analysis. Only `status: "error"` halts a phase.
- **Consolidated flag list (FR34)** — the agent must maintain a running list of all flag objects from all tool calls throughout the session. `[FL]` menu item displays this. At the end of a completed run, display the full list automatically.
- **Separation of concerns** — the Viper workflow files (Story 3.5) define the step-by-step execution logic. The agent definition (this story) defines persona, menu, and orchestration rules. Avoid duplicating detailed step logic between `agents/viper.md` and `workflows/viper/workflow.md`.
- **`program_name` discipline** — always pass the COBOL PROGRAM-ID verbatim (uppercase with hyphens) to MCP tools. Never normalise or lowercase it. The agent should display it as-is from the `parse_module` result.

### Project Structure Notes

Create (new files):
- `agents/viper.md` — primary deliverable of this story

Possibly create (confirm from Story 1.1 implementation):
- Agent registration entry in `.claude/agents.json` or equivalent IDE config

Do NOT modify:
- MCP server code
- `workflows/viper/` (that is Story 3.5)
- Any existing agent definitions

### References

- FR1–FR8: Viper functional requirements [Source: docs/planning-artifacts/epics.md#Story-3.4]
- FR7: analyst review gate before spec layer write [Source: docs/planning-artifacts/epics.md#Story-3.4]
- FR8: unknown construct and macro warnings [Source: docs/planning-artifacts/epics.md#Story-3.4]
- FR33: re-run isolation [Source: docs/planning-artifacts/epics.md#Story-3.4]
- FR34: consolidated flag list [Source: docs/planning-artifacts/epics.md#Story-3.4]
- NFR1: Phase 1 < 15 min [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- NFR11: no silent failures [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- BMAD agent format reference: `_bmad/bmm/agents/*.md` (structure reference only; do not import)
- Viper agent location: `agents/viper.md` [Source: docs/planning-artifacts/architecture.md#Project-Structure]
- MCP tools available from Stories 3.1–3.3 (cobol-parser-mcp), Story 2.1 (delta-macros-mcp), Stories 1.2–1.3 (specdb-mcp)
- Net-new agent requirement [Source: docs/planning-artifacts/architecture.md#Gap-Analysis-Results]
- BMAD format compliance cross-cutting concern [Source: docs/planning-artifacts/architecture.md#Cross-Cutting-Concerns]
- `status: "warning"` = continue; `status: "error"` = halt [Source: docs/planning-artifacts/architecture.md#API-Communication-Patterns]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

_none_

### Completion Notes List

- Both tasks completed. `agents/viper.md` authored following BMAD agent format aligned with `_bmad/bmm/agents/architect.md` and `dev.md` — same activation steps 1–8, `menu-handlers` with typed handlers, `rules`, `persona`, `menu` structure.
- Agent uses `workflow=` handler type for SA, P2, AP (referencing `workflows/viper/workflow.yaml` created in Story 3.5); V1, EC, RR, FL have no exec/workflow and are handled by the LLM persona naturally per rules.
- Gate enforcement implemented via `gate="phase1-required"` on `[P2]` and `gate="phase2-required"` on `[EC]` and `[AP]` menu items, with a `<handler type="gate">` in menu-handlers.
- All 10 ACs covered: Phase 1 orchestration (parse_module, extract_call_graph, score_complexity, detect_antipatterns, get_macro per delta macro), Phase 2 (build_cluster_context → AI clustering → validate_cluster_output), AP write (write_spec to cobol_files, analyses, metrics, dependencies tables), error/warning handling rules, FR33 re-run isolation, FR34 consolidated flag list.
- Phase Orchestration Reference section added OUTSIDE the XML agent block — serves as authoritative sequencing guide for the Story 3.5 workflow author.
- IDE registration: `.claude/commands/viper.md` created as thin shim (matching existing BMAD command format). `/viper` skill appeared immediately in the IDE skills list.

### File List

- `agents/viper.md` (new)
- `.claude/commands/viper.md` (new)

## Change Log

- 2026-03-03: Story 3.4 implemented. Authored agents/viper.md BMAD agent definition and registered via .claude/commands/viper.md. All ACs satisfied. Status → review.
