---
name: viper-workflow
description: 'Viper two-phase COBOL structural analysis workflow — Phase 1 static pre-pass then Phase 2 AI semantic clustering, with enforced analyst review gates before spec layer writes'
---

# Viper Analysis Workflow

**Goal:** Orchestrate two-phase COBOL structural analysis — static pre-pass followed by AI semantic clustering — with enforced analyst review gates at every AI-output stage before writing to the spec layer.

**Prerequisites:**
- `cobol-parser-mcp` server must be running (registered in `.claude/mcp.json`)
- `delta-macros-mcp` server must be running (registered in `.claude/mcp.json`)
- `specdb-mcp` server must be running and schema initialised (required for `[AP]` writes)

**Entry Point:** Analyst selects `[SA]` from the Viper agent menu.

---

## WORKFLOW ARCHITECTURE

This workflow uses **step-file architecture** for disciplined execution:

### Core Principles

- **Just-In-Time Loading**: Only the current step file is active — never load future step files until directed
- **Sequential Enforcement**: Steps within each file must be completed in order; no skipping or optimisation
- **Phase Gates**: Phase 2 (step-03) only runs after explicit analyst confirmation at the end of step-02. Spec layer writes (step-04) only run after explicit analyst approval.
- **Error Policy**: `status: "error"` from any MCP tool = HALT the current phase; display actionable error message; prompt analyst for next steps. NEVER continue with corrupted state.
- **Warning Policy**: `status: "warning"` from any MCP tool = append all flag objects from the result's `flags` array to the session consolidated flag list; display a brief warning summary; CONTINUE analysis.

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order; never deviate
3. **WAIT AT GATES**: Phase gates require explicit analyst confirmation — HALT and wait
4. **FLAG ACCUMULATION**: Every tool call's `flags` array is appended to the session flag list, regardless of status
5. **PROGRAM-ID DISCIPLINE**: Always pass `program_name` verbatim as returned by `parse_module` — never normalise or lowercase

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** advance past a phase gate without explicit analyst confirmation
- 🛑 **NEVER** call any `specdb-mcp` write tool before analyst selects `[AP]`
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimise the sequence
- ⏸️ **ALWAYS** halt at gates and wait for analyst input
- 🔄 **IDEMPOTENT**: Re-running on module X updates only module X's spec records — never touches other modules

---

## WORKFLOW PHASES

| Phase | Step File | Trigger | Gate Before Next |
|-------|-----------|---------|-----------------|
| Initialisation | `step-01-init.md` | `[SA]` auto | None (auto-proceeds to Phase 1) |
| Phase 1 — Static Pre-pass | `step-02-phase1-parse.md` | Auto from step-01 | **Phase 1 review gate** — analyst confirms before `[P2]` |
| Phase 2 — AI Clustering | `step-03-phase2-analyse.md` | `[P2]` agent menu | **Phase 2 approval gate** — analyst approves before `[AP]` |
| Approval & Spec Write | `step-04-review-gate.md` | `[AP]` agent menu | None (completion) |

---

## SESSION STATE

The following data accumulates across steps within a session:

- `program_name` — COBOL PROGRAM-ID verbatim (set by `parse_module` result)
- `source_path` — absolute path to the .cob/.cbl source file (set in step-01)
- `phase1_parse_result` — full result from `parse_module`
- `phase1_callgraph_result` — full result from `extract_call_graph`
- `phase1_complexity_result` — full result from `score_complexity`
- `phase1_antipatterns_result` — full result from `detect_antipatterns`
- `consolidated_flag_list` — all flag objects from all tool calls this session (accumulated incrementally)
- `proposed_clusters` — cluster groupings produced by Phase 2 AI analysis
- `validated_clusters` — clusters after `validate_cluster_output` confirms them

---

## IDEMPOTENCY NOTE

Re-running this workflow on any module safely updates that module's spec layer records without creating duplicates. The `specdb-mcp` write tool uses an idempotent upsert pattern (INSERT OR IGNORE + UPDATE keyed by `program_name`). Other modules' records are never touched.

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from `{project-root}/_bmad/bmm/config.yaml` and resolve:
- `user_name`, `communication_language`

### 2. First Step Execution

Read fully and follow: `{project-root}/workflows/viper/steps/step-01-init.md`
