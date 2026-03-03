# Story 3.5: Viper Workflow & Step Files

Status: review

## Story

As an **analyst**,
I want the Viper agent to follow a structured, step-by-step workflow with enforced phase gates,
So that Phase 2 AI analysis cannot run until Phase 1 structural parsing is complete and the spec layer is never written without analyst approval.

## Acceptance Criteria

1. **Given** the Viper workflow is loaded in the IDE **When** the analyst initiates analysis on a module **Then** the workflow executes in sequence: Phase 1 static pre-pass → Phase 1 review gate → Phase 2 AI clustering → Phase 2 review/correction gate → spec layer write.
2. **And** the workflow cannot advance past the Phase 1 review gate without explicit analyst confirmation.
3. **And** Phase 1 completes within 15 minutes for any single COBOL module on standard developer hardware (NFR1) — the step file for Phase 1 must document this SLA and surface a warning to the analyst if progress seems slow.
4. **When** Phase 2 review is complete and the analyst approves **Then** the workflow writes approved outputs to the spec layer via `specdb-mcp` write tools.
5. **And** the write is idempotent — re-running the full workflow on the same module updates spec layer records rather than creating duplicates (NFR10). This is guaranteed by the specdb-mcp idempotent write pattern (INSERT OR IGNORE + UPDATE) — the workflow does not need to implement extra deduplication logic.
6. **When** any workflow step encounters an error (`status: "error"` from any MCP tool) **Then** it surfaces an explicit, actionable error message — the workflow halts that phase rather than proceeding with corrupted state (NFR11).
7. **And** `status: "warning"` results (unknown macros, CICS/SQL constructs, unknown constructs) are added to the consolidated flag list — the workflow continues.

## Tasks / Subtasks

- [x] Task 1: Create `workflows/viper/workflow.md` — top-level workflow definition (AC: 1–7)
  - [x] Workflow header: name, description, prerequisites (MCP servers must be running), analyst entry point
  - [x] Phase overview: describe the 4 phases and their sequence dependencies
  - [x] Reference to each step file in order: `step-01-init.md` → `step-02-phase1-parse.md` → `step-03-phase2-analyse.md` → `step-04-review-gate.md`
  - [x] Session state description: what data accumulates in session (parse results, call graph, complexity score, anti-patterns, cluster context, validated clusters, consolidated flags)
  - [x] Idempotency note: document that re-running this workflow on any module safely updates its spec layer data without affecting other modules
  - [x] Error policy: `status: "error"` = halt phase + display actionable message; `status: "warning"` = log to flag list + continue

- [x] Task 2: Create `workflows/viper/steps/step-01-init.md` — initialisation step (AC: 1, 2, 6, 7)
  - [x] Prompt analyst for COBOL module path (program_name auto-detected from parse_module result in step-02)
  - [x] Acknowledge that STDIO MCP servers are started by the IDE; note log path for troubleshooting
  - [x] Initialise consolidated flag list (empty list for this session)
  - [x] Output: `source_path` ready for Phase 1; auto-proceed to step-02

- [x] Task 3: Create `workflows/viper/steps/step-02-phase1-parse.md` — Phase 1 static pre-pass (AC: 1, 2, 3, 6, 7)
  - [x] Call `parse_module(program_name, source_path)` via `cobol-parser-mcp`; handle error result
  - [x] Call `extract_call_graph(program_name)` via `cobol-parser-mcp`; handle error result
  - [x] Call `score_complexity(program_name)` via `cobol-parser-mcp`; handle error result
  - [x] Call `detect_antipatterns(program_name)` via `cobol-parser-mcp`; handle error result
  - [x] For each Delta macro in `parse_module.data.delta_macros`: call `get_macro(macro_name)` via `delta-macros-mcp`; collect `UNKNOWN_MACRO` flags for not-found macros
  - [x] Accumulate all `flags` from all tool calls into session consolidated flag list
  - [x] Display Phase 1 results to analyst: summary table, anti-pattern list with locations, CICS/SQL flags, unknown macro warnings, call graph edges, external references
  - [x] Document NFR1 SLA: "Phase 1 should complete within 15 minutes. If this step appears hung, check `logs/cobol-parser-mcp.log`."
  - [x] Present Phase 1 review gate: set `phase1_complete=true`; HALT; return to agent menu (analyst must select [P2])

- [x] Task 4: Create `workflows/viper/steps/step-03-phase2-analyse.md` — Phase 2 AI clustering (AC: 1, 4, 6, 7)
  - [x] Gate check: verify `phase1_complete=true` before proceeding
  - [x] Call `build_cluster_context(program_name)` via `cobol-parser-mcp`; handle error result; confirm context contains no raw source (NFR7)
  - [x] Perform semantic clustering analysis: using paragraph names, PERFORM edges, DATA DIVISION field names; produce proposed clusters with `name`, `paragraphs`, `description`
  - [x] Call `validate_cluster_output(program_name, clusters)` via `cobol-parser-mcp`; handle warning/error result
  - [x] Display proposed clusters clearly as "PROPOSED — awaiting your review"; set `phase2_complete=true`; HALT; return to agent menu

- [x] Task 5: Create `workflows/viper/steps/step-04-review-gate.md` — Phase 2 approval gate and spec layer write (AC: 1, 4, 5, 6, 7)
  - [x] Gate checks: verify `phase2_complete=true` and `validated_clusters` non-empty
  - [x] Spec layer write sequence (all via `specdb-mcp` `write_spec` tool):
    - Write `cobol_files` record: `program_name`, `source_path`, line_count, file_size_bytes
    - Write `analyses` record: paragraph_list (JSON), call_graph (JSON), external_refs (JSON)
    - Write `metrics` record: complexity_score, paragraph_count, goto_count, nested_perform_depth, antipatterns (JSON)
    - Write `dependencies` records: COPY refs (dependency_type="COPY") and CALL targets (dependency_type="CALL"), one row per entry
  - [x] Each primary write (cobol_files, analyses, metrics) halts with error/retry on failure; dependency write errors log and continue
  - [x] Display consolidated flag list in full (FR34)
  - [x] Display completion summary: tables written, records created/updated, next steps

## Dev Notes

### Architecture Guardrails

- **DEPENDS ON STORIES 3.1–3.4** — this story creates the workflow files that orchestrate the MCP tools from Stories 3.1–3.3 and reference the Viper agent from Story 3.4. All 4 `cobol-parser-mcp` tool pairs must be available.
- **Workflow file format** — these are BMAD workflow and step files (markdown). Follow the exact BMAD step file conventions. Study the existing step files under `_bmad/bmm/workflows/` for structural reference, but Viper's files live in `workflows/viper/` (the expansion pack's `workflows/` folder, not `_bmad/`).
- **Phase gate enforcement** — the step files use BMAD workflow conventions to enforce sequential phases. Step 3 (`phase2-analyse`) must include a documented gate check that it only runs after Phase 1 is confirmed. In BMAD markdown workflows, this is enforced by the workflow structure and the agent's execution of steps in order. Make the gate explicit in the step file text.
- **Idempotency is free (NFR10)** — the step-04 write sequence does NOT need special logic to check for existing records. The specdb-mcp tools use INSERT OR IGNORE + UPDATE pattern (established in Stories 1.2–1.3). Re-running the workflow on the same module will update existing records. Document this in the workflow header so the analyst understands re-runs are safe.
- **`status: "warning"` accumulation** — every step file must handle warnings by logging to the session flag list and continuing. Never halt on a warning. Only `status: "error"` halts the current phase.
- **Error message must be actionable** — when halting on error, the step file must display BOTH the error message AND a suggested next action (e.g., "Check that the source file path is correct and the file is readable" for a file-not-found error, or "Check `logs/cobol-parser-mcp.log` for details" for a parse failure).
- **Spec layer write tool names** — the exact tool names for specdb-mcp writes are defined in Stories 1.2–1.3. Check the implementation of `specdb-mcp` (files `mcp-servers/specdb_mcp/server.py` and `spec_db.py`) for the exact tool names. Common patterns from the architecture suggest tool names like `write_cobol_file`, `write_analysis`, `write_dependency`. Use whatever was actually implemented, not guessed names.
- **Step 02 flag accumulation pattern** — each tool call in step-02 appends any `result["flags"]` to the session's consolidated flag list. By the end of Phase 1, the consolidated list contains ALL flags from ALL tools. This enables FR34 (consolidated unresolved construct list).
- **Re-run isolation (FR33)** — document in `workflow.md` that re-running this workflow on module X ONLY affects module X's records in the spec layer. The specdb-mcp write tools use `program_name` as the key; they never touch other modules' data.
- **NFR1: 15-min SLA** — `step-02-phase1-parse.md` must include the SLA text and the log path to check if parsing is slow. The workflow cannot enforce this programmatically but must surface it to the analyst.
- **Phase 1 clustering does NOT touch specdb** — step 02 and step 03 make zero calls to specdb-mcp. All specdb writes happen exclusively in step 04 after analyst approval.

### Project Structure Notes

Create (new files — all new):
- `workflows/viper/workflow.md`
- `workflows/viper/steps/step-01-init.md`
- `workflows/viper/steps/step-02-phase1-parse.md`
- `workflows/viper/steps/step-03-phase2-analyse.md`
- `workflows/viper/steps/step-04-review-gate.md`

Do NOT modify:
- Any MCP server code
- `agents/viper.md` (Story 3.4)
- Any specdb-mcp, cobol-parser-mcp, or delta-macros-mcp source

### References

- Viper two-phase workflow requirement (FR1–FR8, FR33, FR34) [Source: docs/planning-artifacts/epics.md#Story-3.5]
- NFR1: Phase 1 < 15 min [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- NFR10: idempotent spec layer writes [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- NFR11: no silent failures — halt on error, accumulate warnings [Source: docs/planning-artifacts/architecture.md#Requirements-Overview]
- Idempotent write pattern (INSERT OR IGNORE + UPDATE) [Source: docs/planning-artifacts/architecture.md#Data-Architecture]
- Workflow step file structure: `workflows/viper/` [Source: docs/planning-artifacts/architecture.md#Project-Structure]
- BMAD workflow file conventions: `_bmad/bmm/workflows/` (reference only)
- `status: "warning"` = continue; `status: "error"` = halt [Source: docs/planning-artifacts/architecture.md#API-Communication-Patterns]
- Spec layer write tools — check Story 1.3 implementation [Source: docs/implementation-artifacts/1-3-specdb-mcp-crud-tools.md]
- Phase gate pattern — reference Viper agent menu in Story 3.4 [Source: docs/implementation-artifacts/3-4-viper-bmad-agent-definition.md]
- Consolidated flag list (FR34) [Source: docs/planning-artifacts/epics.md#Story-3.4]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

_none_

### Completion Notes List

- All 5 tasks completed. 5 workflow/step markdown files created following BMAD step-file architecture (same pattern as `_bmad/bmm/workflows/1-analysis/create-product-brief/`).
- `workflow.md`: top-level exec-based workflow. Defines phase table, session state variables, error/warning policies, idempotency note, and kicks off step-01. Uses `exec=` handler type (matching architect.md format) — NOT the YAML-based workflow handler type from dev.md.
- `step-01-init.md`: prompts analyst for `source_path`; initialises `consolidated_flag_list=[]` and phase flags to false; auto-proceeds to step-02.
- `step-02-phase1-parse.md`: runs 4 cobol-parser-mcp calls + per-macro `get_macro` calls; accumulates all flags; displays structured Phase 1 summary; includes NFR1 15-min SLA text and `logs/cobol-parser-mcp.log` reference; sets `phase1_complete=true`; HALTS (analyst must select [P2]).
- `step-03-phase2-analyse.md`: gate-checks `phase1_complete`; calls `build_cluster_context`; performs LLM semantic clustering on privacy-safe context (NFR7); calls `validate_cluster_output`; displays clusters as "PROPOSED"; sets `phase2_complete=true`; HALTS (analyst must select [AP]).
- `step-04-review-gate.md`: gate-checks `phase2_complete`; writes `cobol_files`, `analyses`, `metrics`, `dependencies` (COPY + CALL) via `specdb-mcp` `write_spec` tool; primary writes halt on error; dependency writes log-and-continue on error; displays full `consolidated_flag_list` (FR34); displays next steps.
- Agent `agents/viper.md` updated: menu handler changed from `workflow=` (YAML) to `exec=` (markdown) to match the step-file format; SA uses `exec=workflow.md`, P2 uses `exec=step-03-phase2-analyse.md`, AP uses `exec=step-04-review-gate.md`.
- Spec layer write uses `write_spec` tool (the actual tool name from `specdb-mcp/server.py` Story 1.3 implementation) — not guessed names.

### File List

- `workflows/viper/workflow.md` (new)
- `workflows/viper/steps/step-01-init.md` (new)
- `workflows/viper/steps/step-02-phase1-parse.md` (new)
- `workflows/viper/steps/step-03-phase2-analyse.md` (new)
- `workflows/viper/steps/step-04-review-gate.md` (new)
- `agents/viper.md` (modified — handler type corrected from `workflow=` to `exec=` for SA, P2, AP menu items)

## Change Log

- 2026-03-03: Story 3.5 implemented. Created Viper workflow.md and 4 step files following BMAD step-file architecture. Updated agents/viper.md handler type. All ACs satisfied. Status → review.
