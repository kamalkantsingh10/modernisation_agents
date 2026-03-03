---
name: 'step-03-phase2-analyse'
description: 'Phase 2 AI semantic clustering — build cluster context, perform LLM-based paragraph grouping, validate clusters, and present for analyst review'
---

# Step 3: Phase 2 — Semantic Paragraph Clustering

## STEP GOAL

Retrieve the privacy-safe cluster context for the module, perform AI semantic clustering analysis to group paragraphs into meaningful functional clusters, validate the proposed clusters, and present them for analyst review and correction before any spec layer write.

## MANDATORY EXECUTION RULES (READ FIRST)

- 📖 Read the complete step file before taking any action
- 🔒 GATE CHECK: This step only runs after explicit analyst `[P2]` selection — verify `phase1_complete` is true before proceeding
- 🛑 On `status: "error"` from any MCP tool: HALT; display error; offer retry / quit to agent menu
- ⚠ On `status: "warning"` from `validate_cluster_output`: append flags to `consolidated_flag_list`; display validation issues; allow analyst to correct via `[EC]` before `[AP]`
- 🚫 ZERO `specdb-mcp` calls in this step — Phase 2 analysis NEVER touches the spec layer
- 📋 Cluster proposals are AI suggestions — always present them as "PROPOSED — awaiting your review" and never as authoritative
- 🔒 NFR7: The context passed to the LLM must contain ONLY paragraph names, PERFORM edges, and DATA DIVISION field names — never raw COBOL source

---

## Sequence of Instructions (Do not deviate, skip, or optimise)

### 1. Gate Check

Confirm `phase1_complete` is true. If false:
> "⚠ Phase 2 cannot begin — Phase 1 analysis is not complete. Please use `[SA]` to run Phase 1 first."
HALT and return to agent menu.

### 2. Call `build_cluster_context`

Call tool `build_cluster_context` via `cobol-parser-mcp`:
- `program_name`: `{program_name}` (verbatim from session state)

**On `status: "error"`:**
> "❌ build_cluster_context failed for `{program_name}`
> Error: {result.message}
> This likely means parse_module was not called in this session. Try [RR] to re-run from Phase 1.
> Options: [R] Retry | [Q] Quit to agent menu"

**On success:**
- Store cluster context: `paragraph_names`, `perform_edges`, `data_division_fields` from `result["data"]`
- Append `result["flags"]` to `consolidated_flag_list`

> **Privacy check:** The context returned by `build_cluster_context` contains ONLY structured metadata — paragraph names, PERFORM edges, and DATA DIVISION field names. Raw COBOL source is never included. This is enforced by the MCP tool (NFR7).

### 3. Perform Semantic Clustering Analysis

Using the cluster context (paragraph names, PERFORM edges, DATA DIVISION field names), reason about functional groupings and produce proposed clusters.

**Clustering guidance:**
- Group paragraphs by inferred functional role (e.g. "Initialisation", "Payment Processing", "Validation", "Error Handling", "Finalisation")
- Use PERFORM edges to identify which paragraphs are called together — clusters should reflect call cohesion
- Use DATA DIVISION field names as semantic hints (e.g. `WS-CUST-BAL` suggests a balance/customer cluster)
- Prefer cohesive meaningful groups over many singleton clusters
- Aim for 3–8 clusters for a typical module; very small modules may have fewer
- Each cluster must have:
  - `name`: short plain-English label (3–5 words max, e.g. "Payment Calculation")
  - `paragraphs`: non-empty list of paragraph names from `paragraph_names` (verbatim)
  - `description`: one sentence plain-English description of the cluster's functional role

**Important:** Every paragraph in `paragraph_names` must appear in exactly one cluster. Do not leave paragraphs unassigned.

### 4. Call `validate_cluster_output`

Call tool `validate_cluster_output` via `cobol-parser-mcp`:
- `program_name`: `{program_name}`
- `clusters`: the proposed cluster list from step 3

**On `status: "error"`:**
> "❌ validate_cluster_output failed: {result.message}
> Options: [R] Retry | [Q] Quit to agent menu"

**On `status: "warning"`:**
- Append flags to `consolidated_flag_list`
- Display validation issues:
  > "⚠ Cluster validation found issues:
  > {for each flag: "  • [{flag.code}] {flag.message} (cluster: {flag.location})"}
  >
  > You can use `[EC]` from the agent menu to correct cluster names or reassign paragraphs,
  > then select `[AP]` to approve."

**On `status: "ok"`:**
- Store `validated_clusters` = `result["data"]["clusters"]`
- Append any `result["flags"]` to `consolidated_flag_list`

### 5. Display Proposed Clusters for Analyst Review

Display proposed clusters in a clear, reviewable format:

```
╔═══════════════════════════════════════════════════════════╗
║  VIPER — Phase 2 Proposed Clusters: {program_name}       ║
╚═══════════════════════════════════════════════════════════╝

PROPOSED — Please review these AI-generated cluster groupings.
You can edit any cluster with [EC] before approving with [AP].

{for each cluster, numbered:}
┌─ Cluster {n}: {name} ─────────────────────────────────────
│  Paragraphs ({count}): {paragraph list}
│  Description: {description}
└───────────────────────────────────────────────────────────

Total clusters: {cluster count}
Total paragraphs assigned: {total count}

────────────────────────────────────────────────────────────
  ⏸ PHASE 2 REVIEW GATE

  Review the proposed clusters above. The analyst is in the expert seat —
  correct any groupings that do not reflect the module's actual structure.

  Options:
    [EC] Edit a cluster (name or description)
    [AP] Approve clusters and write to spec layer
    [FL] View full consolidated flag list
    [DA] Dismiss agent
────────────────────────────────────────────────────────────
```

Set `phase2_complete` = true.

**HALT here.** Return control to the Viper agent menu.

---

## CRITICAL STEP COMPLETION NOTE

This step is complete when proposed clusters are displayed and the Phase 2 review gate is shown. `phase2_complete` must be set to `true`. Control returns to the agent menu — spec layer writes happen ONLY when the analyst selects `[AP]`.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- Gate check confirmed Phase 1 complete before proceeding
- `build_cluster_context` called successfully; context contains no raw source
- All paragraphs assigned to at least one cluster
- `validate_cluster_output` called and result stored
- Proposed clusters displayed clearly as "PROPOSED"
- Review gate displayed; `phase2_complete` = true; control returned to agent menu
- Zero `specdb-mcp` calls made

### ❌ SYSTEM FAILURE

- Proceeding without `phase1_complete` = true
- Making any `specdb-mcp` write call in this step
- Including raw COBOL source text anywhere in the cluster context passed to LLM reasoning
- Auto-proceeding to step-04 without analyst `[AP]` selection
- Leaving any paragraph unassigned across all clusters
