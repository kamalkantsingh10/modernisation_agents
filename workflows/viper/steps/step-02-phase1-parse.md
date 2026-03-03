---
name: 'step-02-phase1-parse'
description: 'Phase 1 static pre-pass — parse COBOL module, extract call graph, score complexity, detect anti-patterns, and look up Delta macros'
---

# Step 2: Phase 1 — Static Pre-Pass

## STEP GOAL

Execute all Phase 1 MCP tool calls to extract structural metadata from the COBOL module. Accumulate all flags. Display a structured Phase 1 summary to the analyst. Present the Phase 1 review gate — analyst must explicitly confirm before Phase 2 can begin.

## MANDATORY EXECUTION RULES (READ FIRST)

- 📖 Read the complete step file before taking any action
- 🛑 On any `status: "error"` result: HALT immediately; display error; offer retry / skip / quit to agent menu
- ⚠ On any `status: "warning"` result: append ALL flag objects from `result["flags"]` to `consolidated_flag_list`; display brief warning; CONTINUE
- ⏸ Phase 1 review gate at the end of this step REQUIRES explicit analyst confirmation — do NOT auto-proceed
- 🔄 Append flags from EVERY tool call to `consolidated_flag_list` regardless of status
- ⏱ NFR1 SLA: Phase 1 must complete within 15 minutes per module. If this step appears to be taking longer than expected, notify the analyst and provide the log path

## NFR1 SLA NOTICE

> **Phase 1 should complete within 15 minutes on standard developer hardware.**
> If parsing appears stuck, check: `logs/cobol-parser-mcp.log` for details.
> The log is written by the `cobol-parser-mcp` server to the project root `logs/` directory.

---

## Sequence of Instructions (Do not deviate, skip, or optimise)

### 1. Call `parse_module`

Call tool `parse_module` via `cobol-parser-mcp`:
- `program_name`: use `""` (empty string) — the server extracts PROGRAM-ID from the source file
- `source_path`: use `{source_path}` from session state

**On `status: "error"`:**
> "❌ parse_module failed for `{source_path}`
> Error: {result.message}
> Suggested action: Verify the file path is correct and the file is readable. Check `logs/cobol-parser-mcp.log` for details.
> Options: [R] Retry with corrected path | [Q] Quit to agent menu"

Wait for analyst choice; act accordingly. If retry, prompt for a new `source_path` and retry.

**On success:**
- Set `program_name` = `result["data"]["program_name"]` (verbatim, uppercase with hyphens — never modify)
- Store `phase1_parse_result` = `result["data"]`
- Append `result["flags"]` to `consolidated_flag_list`

### 2. Call `extract_call_graph`

Call tool `extract_call_graph` via `cobol-parser-mcp`:
- `program_name`: `{program_name}` (from step 1)

**On `status: "error"`:**
> "❌ extract_call_graph failed for `{program_name}`
> Error: {result.message}
> Options: [R] Retry | [S] Skip call graph (continue with limited data) | [Q] Quit to agent menu"

**On success:**
- Store `phase1_callgraph_result` = `result["data"]`
- Append `result["flags"]` to `consolidated_flag_list`

### 3. Call `score_complexity`

Call tool `score_complexity` via `cobol-parser-mcp`:
- `program_name`: `{program_name}`

**On `status: "error"`:**
> "❌ score_complexity failed for `{program_name}`
> Error: {result.message}
> Options: [R] Retry | [S] Skip complexity score (continue without it) | [Q] Quit to agent menu"

**On success:**
- Store `phase1_complexity_result` = `result["data"]`
- Append `result["flags"]` to `consolidated_flag_list`

### 4. Call `detect_antipatterns`

Call tool `detect_antipatterns` via `cobol-parser-mcp`:
- `program_name`: `{program_name}`

**On `status: "error"`:**
> "❌ detect_antipatterns failed for `{program_name}`
> Error: {result.message}
> Options: [R] Retry | [S] Skip anti-pattern detection (continue without it) | [Q] Quit to agent menu"

**On `status: "warning"` or success:**
- Store `phase1_antipatterns_result` = `result["data"]`
- Append `result["flags"]` to `consolidated_flag_list` (CICS and SQL construct flags appear here)

### 5. Look Up Delta Macros

For each entry in `phase1_parse_result["delta_macros"]` (may be empty):

Call tool `get_macro` via `delta-macros-mcp`:
- `macro_name`: the macro name (verbatim)

**On `status: "error"` OR when result contains a flag with `code: "UNKNOWN_MACRO"`:**
- Append an `UNKNOWN_MACRO` flag to `consolidated_flag_list`:
  `{"code": "UNKNOWN_MACRO", "message": "Macro '{macro_name}' not found in Delta macro library", "location": ""}`
- Do NOT halt — continue with the next macro

**On success:** append any `result["flags"]` to `consolidated_flag_list`; continue

### 6. Display Phase 1 Summary

Display the following structured summary to the analyst:

```
╔═══════════════════════════════════════════════════════════╗
║  VIPER — Phase 1 Results: {program_name}                 ║
╚═══════════════════════════════════════════════════════════╝

── MODULE OVERVIEW ─────────────────────────────────────────
  Source:       {source_path}
  Program ID:   {program_name}
  Paragraphs:   {paragraph_count}
  COPY refs:    {count of copy_refs}
  CALL targets: {count of call_targets}
  Delta macros: {count of delta_macros}

── CALL GRAPH ──────────────────────────────────────────────
  Nodes: {node count}  Edges: {edge count}

  PERFORM relationships:
  {for each edge: "  {edge.from} → {edge.to}"}
  (THRU ranges shown as: FROM → TO [THRU END])

── COMPLEXITY ──────────────────────────────────────────────
  Rating:           {rating}  (Low / Medium / High)
  Paragraphs:       {paragraph_count}
  Max PERFORM depth:{max_perform_nesting_depth}
  REDEFINES:        {redefines_count}
  GO TO statements: {goto_count}

── ANTI-PATTERNS ───────────────────────────────────────────
  {if no antipatterns: "None detected ✓"}
  {if antipatterns exist, display as table:}
  Type                  | Location              | Description
  ─────────────────────────────────────────────────────────
  {for each: type | location | description}

── FLAGGED CONSTRUCTS ──────────────────────────────────────
  {if no flags: "No flagged constructs ✓"}
  {if flags exist:}
  Code              | Message                     | Location
  ─────────────────────────────────────────────────────────
  {for each flag in consolidated_flag_list so far}

── EXTERNAL REFERENCES ─────────────────────────────────────
  COPY copybooks:  {list of copy_refs or "none"}
  CALL targets:    {list of call_targets or "none"}
  Delta macros:    {list of delta_macros or "none"}
  {for each UNKNOWN_MACRO flag: "  ⚠ {macro_name}: NOT FOUND in macro library"}
```

### 7. Phase 1 Review Gate

Display the Phase 1 gate prompt:

```
────────────────────────────────────────────────────────────
  ⏸ PHASE 1 REVIEW GATE

  Please review the Phase 1 results above.
  You may correct any misidentified paragraphs or flag additional concerns.

  When you are satisfied with the Phase 1 results, select [P2] from
  the agent menu to proceed to Phase 2 semantic clustering.

  Other options:
    [RR] Re-run this analysis with the same or a different module
    [FL] View the full consolidated flag list
    [DA] Dismiss the agent

  Phase 2 will NOT begin until you select [P2].
────────────────────────────────────────────────────────────
```

Set `phase1_complete` = true.

**HALT here.** Return control to the Viper agent menu. Do NOT auto-proceed to step-03.

---

## CRITICAL STEP COMPLETION NOTE

This step is complete when the Phase 1 summary is displayed and the review gate prompt is shown. `phase1_complete` must be set to `true`. Control returns to the agent menu — step-03 is executed ONLY when the analyst selects `[P2]`.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- All 4 cobol-parser-mcp tools called (or skipped with analyst consent)
- All Delta macros looked up via delta-macros-mcp
- All flags from all tool calls appended to `consolidated_flag_list`
- `program_name` set verbatim from `parse_module` result
- Phase 1 summary displayed in structured format
- Review gate displayed; `phase1_complete` = true; control returned to agent menu

### ❌ SYSTEM FAILURE

- Continuing after `status: "error"` without analyst consent
- Not appending flags from a tool call to `consolidated_flag_list`
- Auto-proceeding to step-03 without analyst `[P2]` selection
- Modifying `program_name` (lowercasing, trimming, etc.)
- Making any `specdb-mcp` calls in this step
