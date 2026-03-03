---
name: 'step-01-init'
description: 'Initialise Viper analysis session — prompt analyst for COBOL module path and verify MCP servers are available'
nextStepFile: '{project-root}/workflows/viper/steps/step-02-phase1-parse.md'
---

# Step 1: Viper Initialisation

## STEP GOAL

Collect the COBOL module source path from the analyst, initialise the session flag list, and hand off to Phase 1.

## MANDATORY EXECUTION RULES (READ FIRST)

- 📖 CRITICAL: Read the complete step file before taking any action
- 🛑 NEVER proceed to Phase 1 without a valid `source_path` from the analyst
- ✅ Communicate in `{communication_language}` throughout
- 🔄 Initialise the consolidated flag list as an empty list at the start of every new analysis

## EXECUTION PROTOCOLS

- Prompt analyst for exactly the information needed — no unnecessary questions
- Confirm inputs before proceeding
- Initialise session state variables before loading next step

---

## Sequence of Instructions (Do not deviate, skip, or optimise)

### 1. Initialise Session State

Set the following session variables to empty/false values:
- `program_name` = "" (will be populated from `parse_module` result in step-02)
- `source_path` = "" (to be set below)
- `consolidated_flag_list` = [] (empty — accumulates flags from every tool call)
- `phase1_complete` = false
- `phase2_complete` = false

### 2. Prompt for Module Details

Display to analyst:

```
── Viper: New Analysis ─────────────────────────────────────
Please provide the following details for the COBOL module to analyse:

  Source file path (absolute path to .cob or .cbl file):
  ▶
```

Accept the source path. If the analyst provides a relative path, note that MCP tools require an absolute path and ask them to confirm or convert it.

### 3. Acknowledge MCP Server Availability

The `cobol-parser-mcp`, `delta-macros-mcp`, and `specdb-mcp` servers are started by the IDE when configured in `.claude/mcp.json`. No explicit health-check call is needed.

Display a brief note:
```
MCP servers: cobol-parser-mcp, delta-macros-mcp, specdb-mcp
(Started automatically by the IDE. If any tool call returns status:"error" due to server
unavailability, you will be prompted with recovery options at that step.)
```

### 4. Confirm Inputs and Proceed

Display:
```
── Analysis Target ─────────────────────────────────────────
  Source path: {source_path}

⏳ Starting Phase 1 static pre-pass…
────────────────────────────────────────────────────────────
```

Set `source_path` to the value provided.

### 5. Auto-Proceed to Phase 1

This is an initialisation step — auto-proceed without waiting for user input after confirmation.

Read fully and follow: `{nextStepFile}`

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the analyst has provided a valid `source_path` AND session state is initialised, proceed to load `{nextStepFile}` to begin Phase 1.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS

- `source_path` collected and non-empty
- Session `consolidated_flag_list` initialised as empty list
- Phase 1 handed off to step-02 automatically

### ❌ SYSTEM FAILURE

- Proceeding to step-02 without a `source_path`
- Failing to initialise `consolidated_flag_list` before step-02
- Asking the analyst for information not required by this step
