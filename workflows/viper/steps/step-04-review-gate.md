---
name: 'step-04-review-gate'
description: 'Phase 2 approval gate and spec layer write — analyst approves clusters then all analysis results are written to specdb-mcp idempotently'
---

# Step 4: Phase 2 Approval Gate & Spec Layer Write

## STEP GOAL

Confirm the analyst has approved the cluster output, then write all analysis results from the current session to the spec layer via `specdb-mcp` write tools. Display the consolidated flag list on completion. This is the only point in the Viper workflow where `specdb-mcp` is called.

## MANDATORY EXECUTION RULES (READ FIRST)

- 📖 Read the complete step file before taking any action
- 🔒 GATE CHECK: This step only runs after explicit analyst `[AP]` selection — verify `phase2_complete` is true
- 🛑 On `status: "error"` from any `specdb-mcp` write: HALT; display which write failed; offer retry / quit
- 🔄 IDEMPOTENT: All writes use `specdb-mcp`'s upsert pattern — re-running safely updates existing records without duplicates
- 📋 Write sequence is ordered — each write may depend on a prior write completing successfully
- 📣 Display the full consolidated flag list on completion regardless of flag count (FR34)

---

## Sequence of Instructions (Do not deviate, skip, or optimise)

### 1. Gate Check

Confirm `phase2_complete` is true. If false:
> "⚠ Phase 2 approval requires Phase 2 clustering to be complete. Use `[P2]` to run Phase 2 first."
HALT and return to agent menu.

Confirm `validated_clusters` is non-empty. If empty:
> "⚠ No validated clusters found. Use `[P2]` to run Phase 2 clustering first."
HALT and return to agent menu.

### 2. Display Approval Confirmation

Display:
```
── Viper: Approving Analysis for {program_name} ────────────
Writing the following to the spec layer:
  • cobol_files  — module registration
  • analyses     — structural analysis record
  • metrics      — complexity and anti-pattern metrics
  • dependencies — COPY refs and CALL targets
⏳ Writing…
────────────────────────────────────────────────────────────
```

### 3. Write `cobol_files` Record

Call tool `write_spec` via `specdb-mcp`:
- `table`: `"cobol_files"`
- `program_name`: `{program_name}`
- `fields`:
  ```json
  {
    "source_path": "{source_path}",
    "line_count": {line count from phase1_parse_result if available, else omit},
    "file_size_bytes": {file size if available, else omit}
  }
  ```

**On `status: "error"`:**
> "❌ Failed to write cobol_files record for {program_name}
> Error: {result.message}
> Options: [R] Retry | [Q] Quit to agent menu (partial write — some data may not be saved)"
HALT on retry failure after 2 attempts.

**On success:** display "  ✓ cobol_files"

### 4. Write `analyses` Record

Call tool `write_spec` via `specdb-mcp`:
- `table`: `"analyses"`
- `program_name`: `{program_name}`
- `fields`:
  ```json
  {
    "paragraph_list": "{JSON-serialised list of paragraph dicts from phase1_parse_result.paragraphs}",
    "call_graph": "{JSON-serialised list of edge dicts from phase1_callgraph_result.edges}",
    "external_refs": "{JSON-serialised object with copy_refs, call_targets, delta_macros from phase1_parse_result}"
  }
  ```

**On `status: "error"`:** halt with error display and retry/quit options. Display "  ✓ analyses" on success.

### 5. Write `metrics` Record

Call tool `write_spec` via `specdb-mcp`:
- `table`: `"metrics"`
- `program_name`: `{program_name}`
- `fields`:
  ```json
  {
    "complexity_score": "{phase1_complexity_result.rating}",
    "paragraph_count": {phase1_complexity_result.factors.paragraph_count},
    "goto_count": {phase1_complexity_result.factors.goto_count},
    "nested_perform_depth": {phase1_complexity_result.factors.max_perform_nesting_depth},
    "antipatterns": "{JSON-serialised list of antipattern dicts from phase1_antipatterns_result.antipatterns}"
  }
  ```

**On `status: "error"`:** halt with error display and retry/quit options. Display "  ✓ metrics" on success.

### 6. Write `dependencies` Records — COPY References

For each entry in `phase1_parse_result["copy_refs"]`:

Call tool `write_spec` via `specdb-mcp`:
- `table`: `"dependencies"`
- `program_name`: `{program_name}`
- `fields`:
  ```json
  {
    "source_program": "{program_name}",
    "target_program": "{copybook_name}",
    "dependency_type": "COPY",
    "location": "{location if available, else empty string}"
  }
  ```

**On `status: "error"`:** display warning for this specific entry; continue with remaining COPY refs (do not halt).

On all COPY writes complete: display "  ✓ dependencies (COPY: {count} records)"

### 7. Write `dependencies` Records — CALL Targets

For each entry in `phase1_parse_result["call_targets"]`:

Call tool `write_spec` via `specdb-mcp`:
- `table`: `"dependencies"`
- `program_name`: `{program_name}`
- `fields`:
  ```json
  {
    "source_program": "{program_name}",
    "target_program": "{call_target_name}",
    "dependency_type": "CALL",
    "location": "{location if available, else empty string}"
  }
  ```

**On `status: "error"`:** display warning for this specific entry; continue with remaining CALL targets.

On all CALL writes complete: display "  ✓ dependencies (CALL: {count} records)"

### 8. Display Completion Summary

Display:
```
╔═══════════════════════════════════════════════════════════╗
║  VIPER — Analysis Complete: {program_name}               ║
╚═══════════════════════════════════════════════════════════╝

✅ Spec layer updated:
  • cobol_files    — 1 record written/updated
  • analyses       — 1 record written/updated
  • metrics        — 1 record written/updated
  • dependencies   — {copy_count + call_count} records written/updated

Clusters approved: {cluster count}
```

### 9. Display Consolidated Flag List (FR34)

Display the full consolidated flag list regardless of whether it is empty:

```
── Consolidated Flag List ───────────────────────────────────
{if empty: "  No flags raised during this analysis ✓"}
{if non-empty, display as table:}
  # | Code              | Message                      | Location
  ──┼───────────────────┼──────────────────────────────┼─────────
  {for each flag in consolidated_flag_list, numbered}

Total flags: {count}
  {breakdown by code: "  {code}: {count}"}
────────────────────────────────────────────────────────────
```

### 10. Display Next Steps

Display:
```
── Next Steps ──────────────────────────────────────────────
  This module's structural analysis is recorded in the spec layer.

  Suggested next actions:
  • Run Viper on another COBOL module: use [SA]
  • Re-run this module if corrections needed: use [RR]
  • Proceed to Crane for cross-module dependency mapping
  • Proceed to Shifu for business rule extraction

  [DA] Dismiss agent when done
────────────────────────────────────────────────────────────
```

Return control to the Viper agent menu.

---

## CRITICAL STEP COMPLETION NOTE

This step is complete when all `specdb-mcp` writes have succeeded (or error-handled), the consolidated flag list has been displayed, and the next steps message has been shown. Control returns to the agent menu.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Gate checks passed (phase2_complete = true, validated_clusters non-empty)
- All 3 primary writes completed: cobol_files, analyses, metrics
- All dependency records written for COPY refs and CALL targets
- Consolidated flag list displayed in full (FR34)
- Completion summary and next steps displayed
- `phase1_complete` and `phase2_complete` remain true for potential `[RR]` context

### ❌ SYSTEM FAILURE

- Halting on individual dependency write errors (these should log and continue)
- Not displaying the consolidated flag list (FR34 violation)
- Proceeding without gate checks passing
- Making additional MCP calls beyond the `write_spec` sequence defined above
- Calling `specdb-mcp` without analyst `[AP]` selection (this step is triggered by `[AP]`)
