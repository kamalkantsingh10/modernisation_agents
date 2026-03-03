---
stepsCompleted: ["step-01-document-discovery", "step-02-prd-analysis", "step-03-epic-coverage-validation", "step-04-ux-alignment", "step-05-epic-quality-review", "step-06-final-assessment"]
documentsIncluded:
  prd: docs/planning-artifacts/prd.md
  architecture: docs/planning-artifacts/architecture.md
  epics: docs/planning-artifacts/epics.md
  ux: null
---

# Implementation Readiness Assessment Report

**Date:** 2026-03-01
**Project:** modernisation_agents

---

## PRD Analysis

### Functional Requirements

FR1: Analyst can initiate structural analysis of a COBOL module and receive a paragraph call graph
FR2: Analyst can view a complexity score (Low/Medium/High) for any analysed COBOL module
FR3: Analyst can view anti-patterns detected in a COBOL module (GOTOs, nested PERFORMs, REDEFINES, etc.)
FR4: Analyst can view extracted COPY, CALL, SQL, CICS, and Delta macro references per module
FR5: Analyst can view AI-generated semantic cluster groupings for a module's paragraphs
FR6: Analyst can view plain-English descriptions for each semantic cluster
FR7: Analyst can review, correct, and approve AI analysis outputs before they are written to the spec layer
FR8: Analyst can view a warning when Viper encounters an unrecognised COBOL construct or unknown Delta macro
FR9: Analyst can initiate cross-module dependency analysis across all COBOL modules in scope
FR10: Architect can view a Mermaid dependency diagram showing relationships between all modules
FR11: Architect can view detected subsystem groupings emerging from the dependency structure
FR12: Architect can view a recommended migration order based on module dependencies
FR13: Analyst can view detected circular dependencies and dead code across modules
FR14: Analyst can initiate business rule extraction for a COBOL module using Viper and Crane outputs
FR15: Business Validator can view plain-English business markdown for any module (purpose, use cases, business rules, data entities with glossary names)
FR16: Business Validator can validate each extracted business rule as confirmed, corrected, or rejected
FR17: System writes approved business rules, entities, operations, and data flows to the SQLite spec layer
FR18: Analyst can re-run Shifu on a module and have the spec layer update idempotently without duplicates
FR19: Architect can initiate migration architecture generation from the populated spec layer
FR20: Architect can view a target architecture document mapping COBOL subsystems to target-language services
FR21: Architect can specify the target language as an input to Oogway
FR22: Architect can review and modify the generated architecture before it is finalised
FR23: Developer can initiate target-language code generation for a module from the spec layer and architecture
FR24: Developer can view generated target-language code for each COBOL module
FR25: Developer can regenerate code for a specific module without affecting other modules
FR26: QA can initiate validation of generated code against spec layer business rules
FR27: QA can view a validation report showing which business rules are confirmed, partially covered, or missing in the generated code
FR28: QA can flag a module as requiring rework before sign-off
FR29: Operator can initialise the SQLite spec layer schema with a single command via specdb-mcp
FR30: Analyst can configure a client-specific glossary mapping COBOL field names to business terms
FR31: Analyst can add a new macro definition to delta-macros-mcp without restarting the pipeline
FR32: Operator can install the full BMAD expansion pack into any BMAD-compatible IDE via a standard installer
FR33: Analyst can re-run any individual agent on a specific module without restarting the full pipeline
FR34: Analyst can view a consolidated list of all unresolved constructs and macros flagged across pipeline stages
FR35: System can parse and analyse IBM Enterprise COBOL and COBOL-85 modules
FR36: System can detect and flag CICS transaction constructs within a COBOL module
FR37: System can detect and flag DB2 embedded SQL constructs within a COBOL module
FR38: System can parse COPY statements and resolve referenced copybooks
FR39: All agents can resolve client-specific Delta macro references via delta-macros-mcp at analysis time
FR40: PM can initialise a GitLab project with standard label taxonomy (pipeline stage, complexity, and status labels)
FR41: PM can create a standard milestone structure per engagement phase in GitLab
FR42: PM can create a GitLab issue board configured with columns mapped to pipeline stages
FR43: Each COBOL module has a dedicated GitLab Issue tracking its complete pipeline lifecycle from analysis through QA sign-off
FR44: Any agent can apply the appropriate stage completion label to a module's GitLab Issue upon completing its stage
FR45: Any agent can transition a module Issue to Awaiting-Review status when its stage output requires analyst approval
FR46: Analyst can close the review gate on a module Issue and transition it to the next pipeline stage
FR47: PM can create GitLab sprint milestones scoped to a specific set of modules based on Crane's migration order recommendation
FR48: PM can assign module Issues to sprint milestones, respecting subsystem dependencies
FR49: PM can view a milestone burndown showing open vs closed module Issues within a sprint
FR50: Any agent can post a structured progress comment to a module's GitLab Issue when it completes a stage, including key outputs and any warnings or flags
FR51: The GitLab project README is updated by any agent that changes module status — always reflects current pipeline state without manual intervention
FR52: Client Sponsor can view a README dashboard showing total modules, modules per pipeline stage, modules blocked, and Epics signed off — at any time without requesting a status update
FR53: PM can generate a milestone summary comment on any Epic showing sprint progress and outstanding items
FR54: Business Validator can formally sign off on Shifu's business markdown by closing the Awaiting-Review gate on a module Issue
FR55: QA can sign off on an Epic, triggering Epic completion in GitLab with a validation summary comment
FR56: QA can formally close an Epic when all module Issues within it are QA-Complete

**Total FRs: 56**

---

### Non-Functional Requirements

NFR1: [Performance] Viper Phase 1 static pre-pass completes on any single COBOL module within 15 minutes on standard developer hardware
NFR2: [Performance] cobol-parser-mcp parsing tools return results within 30 seconds for any module up to 5,000 lines
NFR3: [Performance] specdb-mcp read and write operations complete within 2 seconds for any single spec layer record or query
NFR4: [Performance] delta-macros-mcp macro lookups resolve within 1 second per call
NFR5: [Performance] gitlab-mcp operations complete within 10 seconds per API call under normal network conditions
NFR6: [Security] No COBOL source code, business rules, or extracted spec data is transmitted outside the local environment by any agent or MCP server
NFR7: [Security] Where remote LLM API calls are used, source code is scoped to the minimum required context — no full-file dumps without documented justification
NFR8: [Security] GitLab credentials are stored using the host IDE's or OS credential store — never hardcoded in agent definitions or MCP server config files
NFR9: [Security] delta-macros-mcp macro library is stored locally and not synchronised to any external service
NFR10: [Reliability] Running any agent twice on the same input produces equivalent SQLite spec layer output — spec layer writes are idempotent
NFR11: [Reliability] Any agent encountering an unrecognised construct, unknown macro, or LLM error fails with an explicit, actionable error message — silent failures are not permitted
NFR12: [Reliability] A failed agent run does not corrupt existing spec layer records — partial writes roll back or are clearly flagged as incomplete
NFR13: [Reliability] All MCP servers remain operational across agent session restarts without requiring full reinitialisation
NFR14: [Compatibility] The BMAD expansion pack installs and operates correctly in any BMAD-compatible IDE (Claude Code and Cursor as minimum baseline)
NFR15: [Compatibility] All MCP servers conform to the MCP protocol specification — no proprietary extensions that break cross-IDE compatibility
NFR16: [Compatibility] gitlab-mcp supports GitLab Cloud and self-hosted GitLab instances (API v4)
NFR17: [Maintainability] The SQLite spec layer schema is versioned — schema migrations do not break existing data or require manual intervention
NFR18: [Maintainability] Each BMAD agent definition is independently updatable without requiring changes to any other agent or MCP server
NFR19: [Maintainability] Each MCP server exposes a clearly defined, versioned tool interface — adding new tools does not break existing tool calls
NFR20: [Maintainability] Glossary file format and macro library format use human-readable, plain-text markup — no binary formats or proprietary schemas
NFR21: [Maintainability] The BlackJack corpus serves as the regression test baseline — any change to an MCP server is validated against BlackJack end-to-end before release

**Total NFRs: 21**

---

### Additional Requirements & Constraints

- **LLM Reliability Constraint:** Agent outputs are never treated as authoritative without analyst review; agents must explicitly flag low-confidence or unresolved analysis — uncertain outputs must not silently pass to downstream agents
- **COBOL Dialect Coverage:** Must handle or explicitly flag IBM Enterprise COBOL, VS COBOL II syntax variants, CICS transaction constructs (EXEC CICS), DB2 embedded SQL (EXEC SQL), and client-specific Delta macros
- **Pipeline Reproducibility:** LLM variance in intermediate markdown is acceptable; variance in the spec layer is not — spec layer is the authoritative, deterministic output
- **Data Locality:** Client COBOL source code and extracted business rules are confidential — no data leaves the local environment; LLM selection constrained accordingly

---

### PRD Completeness Assessment

The PRD is thorough and well-structured. Requirements are numbered, categorised by agent/capability domain, and directly traceable to user journeys. The 56 FRs span the full pipeline (Viper → Crane → Shifu → Oogway → Tigress → Po → Tai Lung) plus infrastructure and GitLab integration. The 21 NFRs cover performance, security, reliability, compatibility, and maintainability with specific, measurable targets where applicable. Domain-specific constraints (LLM reliability, COBOL dialects, data locality, pipeline reproducibility) are clearly articulated. No ambiguity was detected in requirement intent.

---

## Epic Coverage Validation

### Coverage Matrix

| FR | PRD Requirement (Summary) | Epic Coverage | Status |
|----|--------------------------|---------------|--------|
| FR1 | Structural analysis + paragraph call graph | Epic 3, Stories 3.1, 3.4 | ✓ Covered |
| FR2 | Complexity score (Low/Medium/High) | Epic 3, Stories 3.2, 3.4 | ✓ Covered |
| FR3 | Anti-pattern detection (GOTOs, REDEFINES, etc.) | Epic 3, Stories 3.2, 3.4 | ✓ Covered |
| FR4 | Extracted COPY, CALL, SQL, CICS, macro references | Epic 3, Story 3.1 | ✓ Covered |
| FR5 | AI-generated semantic cluster groupings | Epic 3, Stories 3.3, 3.4 | ✓ Covered |
| FR6 | Plain-English descriptions for semantic clusters | Epic 3, Stories 3.3, 3.4 | ✓ Covered |
| FR7 | Review/correct/approve AI outputs before spec write | Epic 3, Stories 3.4, 3.5 | ✓ Covered |
| FR8 | Warning on unrecognised construct / unknown macro | Epic 3, Stories 3.4, 3.5; Epic 2, Story 2.1 | ✓ Covered |
| FR9 | Initiate cross-module dependency analysis | Epic 4, Story 4.1 | ✓ Covered |
| FR10 | Mermaid dependency diagram | Epic 4, Story 4.1 | ✓ Covered |
| FR11 | Detected subsystem groupings | Epic 4, Story 4.1 | ✓ Covered |
| FR12 | Recommended migration order | Epic 4, Story 4.1 | ✓ Covered |
| FR13 | Circular dependencies and dead code detection | Epic 4, Story 4.1 | ✓ Covered |
| FR14 | Initiate business rule extraction | Epic 5, Story 5.1 | ✓ Covered |
| FR15 | Plain-English business markdown per module | Epic 5, Story 5.1 | ✓ Covered |
| FR16 | Validate each rule as confirmed/corrected/rejected | Epic 5, Story 5.1 | ✓ Covered |
| FR17 | Write approved rules/entities/operations/flows to spec layer | Epic 5, Story 5.1 | ✓ Covered |
| FR18 | Re-run Shifu with idempotent spec layer updates | Epic 5, Story 5.1 | ✓ Covered |
| FR19 | Initiate migration architecture generation from spec layer | Epic 7, Story 7.1 | ✓ Covered |
| FR20 | Target architecture document | Epic 7, Story 7.1 | ✓ Covered |
| FR21 | Specify target language input to Oogway | Epic 7, Story 7.1 | ✓ Covered |
| FR22 | Review and modify generated architecture | Epic 7, Stories 7.1, 7.2 | ✓ Covered |
| FR23 | Initiate target-language code generation | Epic 8, Story 8.1 | ✓ Covered |
| FR24 | View generated target-language code per module | Epic 8, Story 8.1 | ✓ Covered |
| FR25 | Regenerate code for specific module | Epic 8, Story 8.1 | ✓ Covered |
| FR26 | Validate generated code against spec layer rules | Epic 8, Story 8.2 | ✓ Covered |
| FR27 | Validation report (confirmed/partial/missing rules) | Epic 8, Story 8.2 | ✓ Covered |
| FR28 | Flag module as requiring rework | Epic 8, Story 8.2 | ✓ Covered |
| FR29 | Initialise SQLite spec layer schema via single command | Epic 1, Story 1.2 | ✓ Covered |
| FR30 | Configure client-specific glossary | Epic 1, Story 1.4 | ✓ Covered |
| FR31 | Add macro definition without restarting pipeline | Epic 2, Story 2.2 | ✓ Covered |
| FR32 | Install BMAD expansion pack via standard installer | Epic 1 (deferred — no dedicated story) | ⚠️ PARTIAL |
| FR33 | Re-run individual agent without full pipeline restart | Epic 3, Story 3.4; Epic 4, Story 4.1; Epic 5, Story 5.2 | ✓ Covered |
| FR34 | Consolidated list of unresolved constructs/macros | Epic 1, Story 1.1; Epic 3, Story 3.4 | ✓ Covered |
| FR35 | Parse IBM Enterprise COBOL and COBOL-85 | Epic 3, Story 3.1 | ✓ Covered |
| FR36 | Detect and flag CICS constructs | Epic 3, Story 3.2 | ✓ Covered |
| FR37 | Detect and flag DB2 embedded SQL | Epic 3, Story 3.2 | ✓ Covered |
| FR38 | Parse COPY statements and resolve copybooks | Epic 3, Story 3.1 | ✓ Covered |
| FR39 | Resolve Delta macro references via delta-macros-mcp | Epic 2, Story 2.1; Epic 3, Story 3.1; Epic 5, Story 5.1 | ✓ Covered |
| FR40 | Initialise GitLab project with standard label taxonomy | Epic 6, Stories 6.1, 6.4 | ✓ Covered |
| FR41 | Create standard milestone structure | Epic 6, Stories 6.1, 6.4 | ✓ Covered |
| FR42 | Create GitLab issue board with pipeline stage columns | Epic 6, Stories 6.1, 6.4 | ✓ Covered |
| FR43 | Dedicated GitLab Issue per COBOL module | Epic 6, Stories 6.2, 6.4 | ✓ Covered |
| FR44 | Apply stage completion label to module Issue | Epic 6, Story 6.2 | ✓ Covered |
| FR45 | Transition module Issue to Awaiting-Review status | Epic 6, Story 6.2 | ✓ Covered |
| FR46 | Close review gate and transition to next stage | Epic 6, Story 6.2 | ✓ Covered |
| FR47 | Create sprint milestones based on migration order | Epic 6, Stories 6.3, 6.4 | ✓ Covered |
| FR48 | Assign module Issues to sprint milestones | Epic 6, Stories 6.3, 6.4 | ✓ Covered |
| FR49 | View milestone burndown (open vs closed Issues) | Epic 6 (no dedicated story) | ⚠️ PARTIAL |
| FR50 | Post structured progress comment on module Issue | Epic 6, Story 6.2 | ✓ Covered |
| FR51 | Auto-update README to reflect current pipeline state | Epic 6, Story 6.2 | ✓ Covered |
| FR52 | Client Sponsor README dashboard | Epic 6, Stories 6.2, 6.4 | ✓ Covered |
| FR53 | PM milestone summary comment on Epic | Epic 6, Story 6.3 | ✓ Covered |
| FR54 | Business Validator formal sign-off on Shifu output | Epic 5, Story 5.2 | ✓ Covered |
| FR55 | QA sign off on Epic triggering Epic completion | Epic 8, Story 8.2 | ✓ Covered |
| FR56 | QA formally close Epic when all modules QA-Complete | Epic 8, Story 8.2 | ✓ Covered |

---

### Missing or Partial Requirements

#### ⚠️ FR32 — BMAD Expansion Pack Installer (Partial)
- **PRD Requirement:** Operator can install the full BMAD expansion pack into any BMAD-compatible IDE via a standard installer
- **Current State:** Marked as deferred in the epics document — Epic 1 references it but no story exists with acceptance criteria, tasks, or definition of done
- **Impact:** Without an installer story, delivery of the expansion pack as a self-contained, installable product is unplanned. This is a Must-Have per the PRD MVP feature set.
- **Recommendation:** Add Story 1.5 — "BMAD Expansion Pack Installer" with acceptance criteria covering installer script, MCP server startup, and IDE deployment validation

#### ⚠️ FR49 — Milestone Burndown View (Partial)
- **PRD Requirement:** PM can view a milestone burndown showing open vs closed module Issues within a sprint
- **Current State:** Referenced at the Epic 6 level in the coverage map but no story in Story 6.3 or elsewhere explicitly implements a burndown view tool or display mechanism
- **Impact:** Lower priority — GitLab natively provides burndown charts on milestones; the question is whether `gitlab-mcp` needs a dedicated tool or if native GitLab UI suffices
- **Recommendation:** Clarify in Epic 6 whether this is satisfied by native GitLab milestone burndown (in which case mark as deferred/out-of-scope) or requires an explicit `gitlab-mcp` tool

---

### Coverage Statistics

- **Total PRD FRs:** 56
- **FRs with full story-level coverage:** 54 (96.4%)
- **FRs with partial/deferred coverage:** 2 (FR32, FR49)
- **FRs with no coverage:** 0
- **Overall coverage:** 96.4% — **Near-complete, two gaps require resolution before implementation**

---

## UX Alignment Assessment

### UX Document Status

Not found — and **not required** for this project type.

### Rationale

Mainframe Modernisation Agents is a developer tool / BMAD Expansion Pack operating entirely within an IDE (Claude Code, Cursor). There is no web UI, mobile interface, or end-user-facing application. The interaction model is:
- Analyst/Architect invokes agents in their IDE
- Agents present menus, review gates, and structured outputs via the BMAD workflow engine
- Human review/correction happens within the IDE conversation

The "UX" of this system is fully defined by the BMAD agent definitions, step files, and workflow structure — all of which are specified in the epics and stories document.

### Alignment Issues

None — no UX/PRD or UX/Architecture misalignment possible given the product type.

### Warnings

None — UX documentation is explicitly not applicable for a CLI/agent-based developer tool.

---

## Epic Quality Review

### Evaluation Against Best Practices

All 8 epics and 24 stories were read completely and assessed against create-epics-and-stories standards.

---

### Epic Structure Validation — User Value

| Epic | Title | User Value Assessment | Verdict |
|------|-------|-----------------------|---------|
| Epic 1 | Pipeline Foundation & Configuration | Operator can set up complete pipeline for new engagement — operators are a valid user class | ✅ Acceptable |
| Epic 2 | Client Macro Knowledge Integration | Analyst can look up and add Delta macros in real time | ✅ |
| Epic 3 | COBOL Structural Analysis — Viper | Analyst can run complete structural analysis per module | ✅ |
| Epic 4 | Cross-Module Dependency Mapping — Crane | Architect can map full dependency landscape of COBOL estate | ✅ |
| Epic 5 | Business Rule Extraction & Validation — Shifu | Analyst and Business Validator can extract, validate, and persist business rules | ✅ |
| Epic 6 | GitLab Delivery Management — Tigress | PM can set up and manage modernisation project in GitLab | ✅ |
| Epic 7 | Migration Architecture — Oogway | Architect can generate target migration architecture | ✅ |
| Epic 8 | Code Generation & QA Sign-off — Po + Tai Lung | Developer generates code; QA validates and signs off Epics | ✅ |

**Note on Epic 1:** Infrastructure-focused but appropriate for a developer tool product. The MCP servers and spec layer ARE the product — this is not the same anti-pattern as a web app "Setup Database" epic. Epic 1 delivers an operational pipeline foundation with tangible operator value. Acceptable.

---

### Epic Independence Validation

| Epic | Forward Dependencies | Assessment |
|------|---------------------|------------|
| Epic 1 | None — standalone | ✅ |
| Epic 2 | Depends on Epic 1 (shared infra) | ✅ Correct ordering |
| Epic 3 | Depends on Epic 1 (specdb-mcp) + Epic 2 (delta-macros-mcp) | ✅ Correct ordering |
| Epic 4 | Depends on Epic 1 + Epic 3 (Viper output in spec layer) | ✅ Correct ordering |
| Epic 5 | Depends on Epic 3 + Epic 4 (Viper + Crane output) | ✅ Correct ordering |
| Epic 6 | Stories 6.1–6.3 are independent; Story 6.4 reads Crane output (Epic 4) | ✅ Acceptable — MCP stories independently deliverable |
| Epic 7 | Depends on Epic 5 (spec layer fully populated by Shifu) | ✅ Correct ordering |
| Epic 8 | Depends on Epic 7 (Oogway architecture finalised) | ✅ Correct ordering |

**No circular dependencies. No forward dependencies (Epic N requiring Epic N+1). Dependency chain follows the pipeline order and is architecturally correct.**

---

### Story Quality Assessment

**Acceptance Criteria Format:** All stories use proper "As a [role], I want [capability], So that [value]" structure. ACs are written in Given/When/Then BDD format throughout. NFR and FR references are embedded directly in ACs. Error conditions are explicitly covered in every story. This is high-quality story writing. ✅

**Story Sizing:** All stories are appropriately scoped — each delivers a discrete, independently completable capability.

**Intra-Epic Dependencies (acceptable):**
- Story 1.3 references Story 1.2 ("Given schema has been initialised") — correct sequential ordering within Epic
- Story 1.4 references Story 1.1 ("Given project is scaffolded") — correct
- Story 6.2 references Story 6.1 ("Given GitLab project is initialised") — correct

These are within-epic sequential dependencies, not forward dependencies. All are correctly ordered.

---

### 🔴 Critical Violations

**None detected.**

---

### 🟠 Major Issues

**Issue M1 — FR32 ✅ RESOLVED**
- **Epic 9 added** — Expansion Pack Release. Correctly placed after Epics 1–8 as the installer can only package artefacts that have been built.
- Story 9.1: `npx`-style installer script (copies agents, workflows, MCP servers, writes IDE config files)
- Story 9.2: `SETUP.md` operator setup guide (config.yaml, init_schema, glossary, GITLAB_TOKEN, verification steps)
- FR32 coverage map updated accordingly.

**Issue M2 — NFR21 ✅ RESOLVED**
- Regression validation is manual: the developer manually re-runs the full BlackJack pipeline end-to-end after any MCP server change and verifies outputs by inspection. No automated test suite is required for MVP.
- Story 1.1 places the BlackJack corpus in the correct location — this is sufficient.
- NFR21 language ("validated against BlackJack end-to-end") is satisfied by this manual process.

---

### 🟡 Minor Concerns

**Concern m1 — FR46 AC Coverage Gap in Story 6.2**
- FR46: "Analyst can close the review gate on a module Issue and transition it to the next pipeline stage"
- Story 6.2 AC explicitly covers transitioning a module TO `Awaiting-Review` (FR45) but doesn't explicitly cover transitioning it OUT of `Awaiting-Review` (FR46)
- The `update_issue_status` tool likely handles both, but the AC should make FR46 explicit
- **Recommendation:** Add a "When update_issue_status is called to close the review gate / transition to In-Migration, Then..." AC to Story 6.2

**Concern m2 — Story 3.4 ↔ Story 3.5 Soft Interdependency**
- Story 3.4 (Viper Agent Definition) references the workflow in its ACs ("the workflow executes in sequence") — but the workflow is Story 3.5
- Story 3.4 is not independently demonstrable end-to-end without Story 3.5
- **Recommendation:** Acknowledge this dependency explicitly in Story 3.4's notes, or combine 3.4 and 3.5 (consistent with Epics 7 and 8 where agent + workflow are combined in one story)

**Concern m3 — Epic 8 Combines Two Distinct Pipeline Agents**
- Po (code generation) and Tai Lung (QA validation) are separate agents serving different users (developer vs. QA engineer)
- Epics 3/4/5 each give a single agent its own epic; Epic 8 combines two
- While Po and Tai Lung are tightly coupled (Tai Lung validates Po's output), combining them means the Epic cannot close until both are complete
- **Recommendation:** Acceptable as-is for MVP scope, but note this for future epic planning if Po or Tai Lung need independent development velocity

**Concern m4 — NFR13 Not Explicitly Tested in Any Story AC**
- NFR13: "All MCP servers remain operational across agent session restarts without requiring full reinitialisation"
- No story has an AC covering server restart behaviour
- **Recommendation:** Add an AC to one of the MCP implementation stories (e.g., Story 1.2) confirming that server restart does not require `init_schema` to be re-called

**Concern m5 — NFR14 Cross-IDE Compatibility Not Verified**
- NFR14: "BMAD expansion pack installs and operates correctly in any BMAD-compatible IDE (Claude Code and Cursor as minimum baseline)"
- Story 1.1 creates `.claude/mcp.json` and `.vscode/mcp.json` but no AC explicitly tests cross-IDE startup
- **Recommendation:** Add an AC to Story 1.1 or Story 1.5 (installer) explicitly testing that all 4 MCP servers start correctly in both Claude Code and Cursor

---

### Best Practices Compliance Checklist

| Check | Result |
|-------|--------|
| All epics deliver user value | ✅ Yes (with noted caveat on Epic 1) |
| All epics can function independently | ✅ Yes |
| Stories appropriately sized | ✅ Yes |
| No forward dependencies | ✅ None found |
| Schema/tables created appropriately | ✅ Yes (init_schema pattern is correct for this product type) |
| Clear, testable acceptance criteria in BDD format | ✅ Yes — strong quality throughout |
| FR traceability maintained | ✅ Yes — FR references embedded in story ACs |
| NFR traceability maintained | ⚠️ Mostly — NFR13 and NFR14 gaps noted |
| Greenfield setup story present | ✅ Story 1.1 |

---

### Epic Quality Summary

The epic and story quality is **high**. BDD acceptance criteria are well-written, requirements are traceable, and the dependency ordering is architecturally sound. No critical violations were found. Two major issues (FR32 installer story missing; NFR21 regression test story missing) and five minor concerns were identified, all with clear remediation paths.

---

## Summary and Recommendations

### Overall Readiness Status

## ✅ READY — With One Remaining Action

The planning artifacts are of high quality. The PRD is comprehensive, the architecture is referenced throughout, and the epic/story breakdown shows strong discipline: BDD acceptance criteria, explicit FR/NFR traceability, and correct dependency ordering. Two previously flagged major issues have been resolved through clarification. One story gap remains before implementation is fully planned.

---

### Issue Summary

| # | Severity | Issue | Affects |
|---|----------|-------|---------|
| 1 | ✅ Resolved | FR32: Epic 9 added — Expansion Pack Release (Stories 9.1 installer script + 9.2 setup guide). Correctly placed after Epics 1–8 as it packages all built artefacts. | Epic 9 / FR32 |
| 2 | ✅ Resolved | NFR21: BlackJack regression baseline is manual — developer manually runs the BlackJack pipeline to validate changes. No automated test story required. | NFR21 |
| 3 | ✅ Resolved | FR49: Milestone burndown is satisfied by native GitLab milestone burndown UI. No gitlab-mcp tool required. | Epic 6 / FR49 |
| 4 | 🟡 Minor | FR46 AC gap: Story 6.2 covers entering Awaiting-Review (FR45) but not exiting it (FR46) | Story 6.2 |
| 5 | 🟡 Minor | Story 3.4 ↔ 3.5 soft dependency — Viper agent not independently demonstrable without its workflow | Stories 3.4, 3.5 |
| 6 | 🟡 Minor | Epic 8 combines Po + Tai Lung — different users, different pipeline stages | Epic 8 |
| 7 | 🟡 Minor | NFR13 (server session restart behaviour) has no explicit AC in any story | NFR13 |
| 8 | 🟡 Minor | NFR14 (cross-IDE compatibility) has no verification AC or test story | NFR14 |

---

### Recommended Next Steps

**Before starting implementation:**

1. ~~Add final installer story~~ — **RESOLVED.** Epic 9 (Expansion Pack Release) added to `epics.md` with Stories 9.1 (installer script) and 9.2 (operator setup guide). Depends on Epics 1–8 complete. FR32 fully covered.

2. ~~Add a regression test story~~ — **RESOLVED.** Manual BlackJack pipeline run confirmed as the validation approach for NFR21.

3. ~~Resolve FR49 scope decision~~ — **RESOLVED.** Native GitLab milestone burndown satisfies FR49. No `gitlab-mcp` tool required.

**Before Sprint 1 execution:**

4. **Fix Story 6.2 AC for FR46.** Add explicit AC covering `update_issue_status` transitioning a module Issue from `Awaiting-Review` to the next pipeline stage. One line addition.

5. **Address NFR13 in Story 1.2 or 1.3.** Add an AC confirming that `specdb-mcp` (and by extension other servers) do not require `init_schema` to be re-called after a server restart — existing data is preserved.

6. **Address NFR14 in Story 1.1 or installer story.** Add an explicit AC testing MCP server startup in both Claude Code and Cursor.

---

### Strengths Worth Noting

- **PRD is production-quality.** 56 FRs and 21 NFRs with clear categorisation, measurable targets, and domain-specific constraints. Zero ambiguity found.
- **BDD acceptance criteria throughout.** Every story follows Given/When/Then format with error conditions covered. Rare in planning documents at this stage.
- **FR traceability is end-to-end.** Every FR is traceable from PRD → epic → story → AC. The FR Coverage Map in the epics document is explicit and accurate.
- **Architecture drives stories correctly.** Architecture decisions (uv, FastMCP, STDIO transport, result dict format, idempotency pattern) are embedded directly in story ACs — not left for implementation to figure out.
- **No forward dependencies or circular dependencies found.** Epic ordering follows the pipeline dependency chain precisely.

---

### Final Note

This assessment identified **9 issues** across 3 categories (2 major, 1 coverage gap, 5 minor). The major issues — specifically the missing installer story and missing regression test story — represent planning gaps that could cause delivery uncertainty late in the project. The minor issues are low-risk and can be resolved with small AC additions. No fundamental rework of the planning artifacts is required.

**Recommended action:** Address Issues 1–3 (stories 1.5, regression test, FR49 decision) before Sprint 1 kick-off. Address Issues 4–8 as part of story refinement before each relevant story is picked up.

---

**Assessment completed by:** John (PM Agent)
**Date:** 2026-03-01
**Report file:** `docs/planning-artifacts/implementation-readiness-report-2026-03-01.md`
