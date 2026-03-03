---
stepsCompleted: ["step-01-document-discovery", "step-02-prd-analysis", "step-03-epic-coverage-validation", "step-04-ux-alignment", "step-05-epic-quality-review", "step-06-final-assessment"]
documentsIncluded:
  prd: docs/planning-artifacts/prd.md
  architecture: docs/planning-artifacts/architecture.md
  epics: docs/planning-artifacts/epics.md
  ux: null
---

# Implementation Readiness Assessment Report

**Date:** 2026-02-26
**Project:** cobol-blackjack

---

## PRD Analysis

### Functional Requirements

**Game Engine**

- FR1: The system can shuffle and deal from a standard 52-card deck
- FR2: The system can deal an initial two-card hand to the player and the dealer
- FR3: The player can choose to hit (receive an additional card) or stand (end their turn)
- FR4: The system can execute the dealer turn according to standard casino rules
- FR5: The system can calculate hand values with Ace counted as 1 or 11
- FR6: The system can determine and display the round outcome (player win, dealer win, push)
- FR7: The player can choose to play another round without restarting the application

**Build & Deployment**

- FR8: Kamal can compile all source files with a single command on GnuCOBOL 3.1+/Ubuntu
- FR9: Kamal can launch the game immediately after compilation via the same single command
- FR10: The build process completes and the game reaches first player prompt within 5 seconds of command entry
- FR11: The build script runs without modification on a fresh Ubuntu installation with GnuCOBOL 3.1+ installed

**Terminal Display**

- FR12: The system can display playing cards as ASCII representations in an 80-column terminal
- FR13: The system can display both player and dealer hands simultaneously during a round
- FR14: The system can display current hand values for player and dealer
- FR15: The system can display round outcome messages legible to a non-COBOL audience
- FR16: The system can prompt the player for hit/stand input in a manner consistent with 1980s terminal conventions

**Legacy Code Authenticity**

- FR17: Each source file contains identifiable examples of 1980s-era code style (cryptic naming, GOTO statements, dead code, sparse/incorrect comments)
- FR18: The codebase contains a minimum of 4 distinct, pointable examples of messiness demonstrable during a live demo without COBOL expertise
- FR19: The overall project structure, file naming, and build process reflect 1980s mainframe development anti-patterns
- FR20: The running terminal output visually reads as an authentic 1980s mainframe application to a non-technical observer

**Deliberate Defects**

- FR21: The deck management module contains a biased shuffle algorithm
- FR22: The dealer logic module contains a soft 17 rule violation
- FR23: The scoring module contains an Ace value recalculation failure when two Aces are held
- FR24: The main game module contains no input validation on the hit/stand prompt
- FR25: The deal module contains an off-by-one error in the deal array
- FR26: The deck module contains a dead code paragraph that is never called
- FR27: Each of the 6 deliberate bugs is independently verifiable through targeted testing without running the full game

**Middleware Stubs**

- FR28: The system calls a CASINO-AUDIT-LOG stub that accepts parameters and performs no operation
- FR29: The system calls a LEGACY-RANDOM-GEN stub that returns a hardcoded value
- FR30: Both middleware stubs compile and link without errors as part of the standard build

**Documentation**

- FR31: Kamal can read a README that provides step-by-step compile and run instructions
- FR32: Kamal can read a README that lists and describes all 6 known bugs with enough detail to locate them in the code

**Total FRs: 32**

---

### Non-Functional Requirements

**Performance**

- NFR1: Application reaches first player prompt within 5 seconds of single launch command on standard Ubuntu machine
- NFR2: Card display and game state render immediately upon each player action — no perceptible delay between input and output
- NFR3: Play-again loop restarts a new round without recompilation or perceptible lag

**Reliability**

- NFR4: Game completes a full round (deal through play-again prompt) without abnormal termination under any normal input (H, S, or equivalent)
- NFR5: FR24 (no input validation) defines the boundary of "normal input" — undefined behavior on unexpected input is a specified defect, not a reliability gap
- NFR6: Application produces consistent, repeatable behavior across multiple consecutive runs on the same machine

**Compatibility**

- NFR7: All source files compile without errors or warnings on GnuCOBOL 3.1+ on Ubuntu 20.04 or later
- NFR8: Terminal display renders correctly in any standard 80-column terminal emulator (gnome-terminal, xterm, tmux) without special configuration
- NFR9: Build script requires no additional dependencies beyond GnuCOBOL and standard GNU utilities

**Intentional Un-maintainability**

- NFR10: Codebase scores "unmaintainable" against any standard code quality heuristic — cryptic naming, no modularity, non-linear flow, absent documentation
- NFR11: Any code analysis tool (manual or automated) surfaces multiple, distinct quality issues on first inspection
- NFR12: The quality bar is explicitly inverted: a clean, well-structured implementation constitutes a failure against this requirement

**Total NFRs: 12**

---

### Additional Requirements / Constraints

- **Project scope is MVP-complete-only**: No viable partial version exists — partial delivery defeats the demo purpose
- **Multi-file structure:** 8–14 COBOL source files required (not a single-file application)
- **Two proprietary middleware stubs** (CASINO-AUDIT-LOG, LEGACY-RANDOM-GEN) must be present as named stubs
- **Single build script** (`build.sh`): compiles and launches in sequence, no manual steps
- **Target environment**: GnuCOBOL 3.1+ on Ubuntu 20.04+; 80-column terminal; no color dependency
- **Human authenticity test**: Non-technical observer must read terminal output as "old" and code as "messy" without explanation

### PRD Completeness Assessment

The PRD is thorough and well-structured. Requirements are clearly numbered, categorized, and testable. The intentional inversion of quality standards is explicitly stated, which prevents misinterpretation by implementers. The document is implementation-ready.

---

## Epic Coverage Validation

### FR Coverage Matrix

| FR | PRD Requirement (Summary) | Epic Coverage | Status |
|----|--------------------------|---------------|--------|
| FR1 | Shuffle and deal from 52-card deck | Epic 2 — BJACK-DECK | ✓ Covered |
| FR2 | Initial two-card hand to player and dealer | Epic 2 — BJACK-DEAL | ✓ Covered |
| FR3 | Player hit/stand choice | Epic 2 — BJACK-MAIN | ✓ Covered |
| FR4 | Dealer turn per standard casino rules | Epic 2 — BJACK-DEALER | ✓ Covered |
| FR5 | Hand values with Ace as 1 or 11 | Epic 2 — BJACK-SCORE | ✓ Covered |
| FR6 | Round outcome determination and display | Epic 2 — BJACK-MAIN | ✓ Covered |
| FR7 | Play-again without restart | Epic 2 — BJACK-MAIN | ✓ Covered |
| FR8 | Single-command compile on GnuCOBOL 3.1+/Ubuntu | Epic 2 — build.sh | ✓ Covered |
| FR9 | Immediate launch after compilation | Epic 2 — build.sh | ✓ Covered |
| FR10 | <5s from command to first player prompt | Epic 2 — build.sh | ✓ Covered |
| FR11 | Runs on fresh Ubuntu with GnuCOBOL 3.1+ | Epic 2 — build.sh | ✓ Covered |
| FR12 | ASCII card display in 80-column terminal | Epic 2 — BJACK-DISPL | ✓ Covered |
| FR13 | Both hands displayed simultaneously | Epic 2 — BJACK-DISPL | ✓ Covered |
| FR14 | Current hand values displayed | Epic 2 — BJACK-DISPL | ✓ Covered |
| FR15 | Round outcome messages legible to non-COBOL audience | Epic 2 — BJACK-DISPL | ✓ Covered |
| FR16 | Period-accurate hit/stand prompt | Epic 2 — BJACK-MAIN | ✓ Covered |
| FR17 | 1980s code style in every source file | Epic 1+2 — all modules | ✓ Covered |
| FR18 | 4+ pointable messiness examples without COBOL expertise | Epic 2 — Story 2.6 AC | ✓ Covered |
| FR19 | Project structure reflects 1980s mainframe anti-patterns | Epic 1 — Stories 1.1/1.2 | ✓ Covered |
| FR20 | Terminal reads as authentic 1980s mainframe | Epic 2 — BJACK-DISPL | ✓ Covered |
| FR21 | Biased shuffle algorithm (BJACK-DECK) | Epic 3 — Story 3.1 | ✓ Covered |
| FR22 | Soft 17 rule violation (BJACK-DEALER) | Epic 3 — Story 3.4 | ✓ Covered |
| FR23 | Ace recalculation failure with two Aces (BJACK-SCORE) | Epic 3 — Story 3.3 | ✓ Covered |
| FR24 | No input validation on hit/stand (BJACK-MAIN) | Epic 3 — Story 3.5 | ✓ Covered |
| FR25 | Off-by-one error in deal array (BJACK-DEAL) | Epic 3 — Story 3.2 | ✓ Covered |
| FR26 | Dead code paragraph never called (BJACK-DECK) | Epic 3 — Story 3.1 | ✓ Covered |
| FR27 | All 6 bugs independently verifiable | Epic 3 — all stories | ✓ Covered |
| FR28 | CASINO-AUDIT-LOG stub: accepts params, no-op | Epic 1 — Story 1.2 | ✓ Covered |
| FR29 | LEGACY-RANDOM-GEN stub: returns hardcoded value | Epic 1 — Story 1.2 | ✓ Covered |
| FR30 | Both stubs compile and link cleanly | Epic 1 — Story 1.2 | ✓ Covered |
| FR31 | README with compile/run instructions | Epic 4 — Story 4.1 | ✓ Covered |
| FR32 | README lists all 6 bugs with location detail | Epic 4 — Story 4.1 | ✓ Covered |

### NFR Coverage Notes

The epics document inventories 10 NFRs vs. the PRD's 12 NFRs. Two gaps noted:

| NFR | PRD Text (Summary) | Epics Coverage | Status |
|-----|-------------------|----------------|--------|
| NFR1–NFR4 | Performance and reliability NFRs | Listed in epics NFR1–NFR4 | ✓ Covered |
| NFR5 (PRD) | FR24 defines boundary of "normal input" — undefined behavior on unexpected input is a specified defect | Dropped from epics NFR list | ⚠️ Minor gap — implied by FR24/Story 3.5 but not explicitly restated |
| NFR6–NFR9 (PRD) | Consistency, compatibility, dependency NFRs | Listed in epics NFR5–NFR8 | ✓ Covered |
| NFR10–NFR11 (PRD) | Unmaintainability heuristics | Listed in epics NFR9–NFR10 | ✓ Covered |
| NFR12 (PRD) | Quality bar is explicitly inverted: clean implementation = failure | Not listed in epics NFR list | ⚠️ Minor gap — principle expressed in stories but not captured as a testable NFR |

### Missing Requirements

#### Critical Missing FRs
_None._ All 32 FRs from the PRD are traceable to a specific epic and story.

#### Minor NFR Gaps

- **PRD NFR5** (input validation boundary clarification): Not restated as a standalone NFR in epics. Low risk — Story 3.5 covers the behavior explicitly.
- **PRD NFR12** (inverted quality bar as explicit NFR): Not in the epics NFR list. Medium importance for verification — without this as a testable NFR, an implementer could produce clean code and no acceptance criterion would catch it. Recommend adding to epics NFR section or confirming it is covered by the per-story anti-pattern ACs.

### Coverage Statistics

- **Total PRD FRs:** 32
- **FRs covered in epics:** 32
- **FR Coverage:** 100%
- **Total PRD NFRs:** 12
- **NFRs fully addressed in epics:** 10
- **NFR gaps (minor):** 2 (NFR5 and NFR12)

---

## UX Alignment Assessment

### UX Document Status

**Not Found** — No separate UX design document exists.

### Alignment Issues

None. A dedicated UX document is not applicable for this project type.

### Assessment

cobol-blackjack is a COBOL terminal CLI application: the entire user interface is the 80-column terminal session (text in, text out). The PRD covers all terminal presentation requirements explicitly through:

- FR12–FR20: ASCII card display, simultaneous hand rendering, hand values, outcome messages, 1980s-accurate prompts, authenticity requirements
- The "Terminal Application — Technical Context" section: interaction model, output method, 80-column constraint, no color dependency
- User Journeys 1–4: full demo day and setup scenarios from the presenter's perspective

These together serve the function a UX document would serve in a graphical/web project.

### Warnings

None. The absence of a UX document is justified and expected for a terminal-only CLI project of this type.

---

## Epic Quality Review

### Epic Structure Validation

#### Epic 1: Working Project Skeleton

- **User Value:** Borderline. "Working Project Skeleton" is a technical milestone framing — Kamal cannot demo anything with only the skeleton. However, this epic is architecturally mandated: the copybooks are the shared data contract and must be locked before any module work begins. The epics document explicitly calls this out as an architectural constraint. This pattern is equivalent to "set up initial project from starter template" — an accepted exception to the user-value rule.
- **Independence:** Fully standalone ✓
- **Verdict:** 🟡 Minor Concern — framing is technical, but the constraint is legitimate. Consider renaming to "Demo Foundation: Compilable Scaffold and Data Contracts" to reflect the user-visible outcome.

#### Epic 2: Playable Blackjack with Authentic Terminal Presentation

- **User Value:** Clear and strong — Kamal can run `./build.sh` and play a complete demo-ready round ✓
- **Independence:** Requires Epic 1 output only ✓ (backward dependency)
- **Verdict:** ✅ Passes

#### Epic 3: Deliberate Defects

- **User Value:** Technically named but contextually appropriate — the PRD explicitly frames bugs as demo deliverables with business value. The epic goal states all 6 bugs are embedded and independently verifiable.
- **Independence:** Requires Epics 1+2 output only ✓
- **Verdict:** 🟡 Minor Concern — naming is technical. Could be "Demo-Ready Anti-Patterns: All 6 Verifiable Defects" to reinforce user outcome framing. Functionally correct.

#### Epic 4: Demo Documentation

- **User Value:** Clear — Kamal has a README enabling setup on any machine and narration of all 6 defects ✓
- **Independence:** Depends on Epics 1–3 being complete ✓ (correct — documents the final application)
- **Verdict:** ✅ Passes

---

### Story Quality Assessment

#### Story 1.1 — Project Scaffold and Shared Data Structures
- **BDD format:** ✓ Given/When/Then throughout
- **Testable ACs:** ✓ All criteria are specific and independently verifiable
- **Independence:** ✓ No backward or forward dependencies
- **Anti-pattern coverage:** ✓ Explicitly states all copybook field names must be cryptic; readability heuristic pass = failure
- **Verdict:** ✅ Passes

#### Story 1.2 — Middleware Stubs and Build Pipeline Validation
- **BDD format:** ✓
- **Testable ACs:** ✓ Each stub behavior is explicitly defined (no-op for CASINO-AUDIT-LOG, hardcoded return for LEGACY-RANDOM-GEN)
- **Independence:** ✓ Backward dependency on 1.1 only
- **Anti-pattern enforcement:** ✓ Both stubs require GOTO, cryptic names, wrong comments, no return-code checks
- **Notable:** `set -e` prohibition in build.sh is explicitly called out — strong AC ✓
- **Verdict:** ✅ Passes

#### Story 2.1 — Deck Module
- **Testable ACs:** ✓
- **Anti-pattern ACs:** ✓ GOTO, cryptic names, wrong comment, no return-code checks, no EVALUATE
- **Dependency:** Requires copybooks from 1.1 only ✓
- **Verdict:** ✅ Passes

#### Story 2.2 — Deal Module
- **Testable ACs:** ✓ Both initial deal and hit paths specified
- **Dependency:** Requires 2.1 (WS-DECK populated) — backward only ✓
- **Verdict:** ✅ Passes

#### Story 2.3 — Scoring Module
- **Testable ACs:** ✓ Ace logic (11 unless >21 then 1) explicitly tested
- **Dependency:** Requires copybooks only ✓ — can be developed in parallel with 2.1/2.2
- **Verdict:** ✅ Passes

#### Story 2.4 — Display Module
- **Testable ACs:** ✓ 80-column, ASCII suits, simultaneous display, non-COBOL legibility
- **Dependency:** "Given WS-HANDS and WS-DECK are populated" — correctly specified as data precondition, not a story dependency. Can be built with stub data ✓
- **Anti-pattern ACs:** ✓ Hardcoded column positions, GOTO, wrong comments, no EVALUATE
- **Verdict:** ✅ Passes

#### Story 2.5 — Dealer Module
- **Testable ACs:** ✓ Draw-to-17 loop clearly specified
- **Dependency:** "BJACK-SCORE is available" — backward dependency on 2.3 ✓
- **Verdict:** ✅ Passes

#### Story 2.6 — Main Game Loop
- **Testable ACs:** ✓ Full call sequence specified (BJACK-DECK → BJACK-DEAL → ... → CASINO-AUDIT-LOG → play-again)
- **Dependency:** "Given all 5 game modules from Stories 2.1–2.5 are implemented" — correct integration story pattern; large dependency cluster is expected for an orchestrator ✓
- **FR18 coverage:** ✓ "minimum of 4 distinct, pointable examples of messiness" as holistic AC — appropriate here as the integration validation point
- **Notable gap:** 🟡 BJACK-MAIN anti-pattern requirements (GOTO, cryptic names, wrong comments) are implicit through the general additional requirements section but not restated as explicit ACs in Story 2.6. Other module stories each call these out explicitly.
- **Verdict:** 🟡 Minor Concern — recommend explicitly adding anti-pattern ACs to Story 2.6 to match the pattern of all other module stories

#### Stories 3.1–3.5 — Deliberate Defects
- **BDD format:** ✓ All use Given/When/Then
- **Independence:** ✓ Each modifies a specific module from Epic 2; backward dependencies only
- **Verifiability:** ✓ Each bug AC requires it to be verifiable in isolation without full game run — strong AC
- **Normal-input non-regression:** ✓ Every story requires game still completes without ABEND on H/S input
- **Verdict:** ✅ All pass

#### Story 4.1 — README
- **Testable ACs:** ✓ Bug entries require: name, module/file, paragraph/line, plain-English description
- **Authenticity AC:** ✓ README must contain at least one outdated/incorrect statement — unusual but consistent with the inverted quality model
- **Notable:** 🟡 ACs specify "plain text format, no markdown rendering" — this is an implicit NFR on the README format itself, not something the AC enforcement steps will automatically verify.
- **Verdict:** ✅ Passes with minor note

---

### Dependency Analysis

**Cross-epic dependency chain:**
- Epic 1 → Epic 2 ✓ (copybooks + stubs + build pipeline are foundational)
- Epic 2 → Epic 3 ✓ (defects modify Epic 2 modules)
- Epics 1–3 → Epic 4 ✓ (documentation of complete system)
- No forward dependencies found ✓
- No circular dependencies ✓

**Within-epic story sequencing:**
- Epic 1: 1.1 → 1.2 ✓ (scaffold before pipeline validation)
- Epic 2: 2.1/2.2/2.3 can proceed in parallel or any order (only depend on copybooks); 2.4 can proceed with stubs; 2.5 requires 2.3; 2.6 requires all ✓
- Epic 3: All stories are independent modifications; can proceed in any order ✓
- Epic 4: Single story; requires all prior epics complete ✓

---

### Best Practices Compliance Checklist

| Epic | Delivers User Value | Independent | Stories Sized Right | No Forward Deps | Clear ACs | FR Traceability |
|------|--------------------|-----------  |---------------------|-----------------|-----------|-----------------|
| Epic 1 | 🟡 Technical milestone (justified) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Epic 2 | ✅ | ✅ | ✅ | ✅ | 🟡 Story 2.6 missing explicit anti-pattern ACs | ✅ |
| Epic 3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Epic 4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### Quality Findings Summary

#### 🔴 Critical Violations
_None._

#### 🟠 Major Issues
_None._

#### 🟡 Minor Concerns

1. **Epic 1 naming** — "Working Project Skeleton" is technical milestone language. Rename to reflect user outcome (e.g., "Demo Foundation: Compilable Scaffold and Data Contracts").
2. **Epic 3 naming** — "Deliberate Defects" is technical. Consider "Demo-Verifiable Anti-Patterns" or similar to reinforce user-value framing.
3. **Story 2.6 missing anti-pattern ACs** — BJACK-MAIN is the only module story that does not explicitly restate GOTO/cryptic-naming/wrong-comment/no-EVALUATE ACs in its acceptance criteria. All other module stories (2.1–2.5) do. Recommend adding these to Story 2.6 for consistency and to prevent an implementer from inadvertently producing clean orchestrator code.
4. **NFR2 (immediate render) and NFR6 (consistent runs) not explicitly in any story AC** — These NFRs are implied by Story 2.6 and the general build requirements but not tested by a specific AC. Low risk given project simplicity; document as a known coverage gap.
5. **PRD NFR12 not in epics NFR list** (identified in Step 3) — The inverted quality bar principle ("clean = failure") is embedded in per-story ACs but not listed as a standalone testable NFR. Recommend adding to epics NFR section for completeness.

---

## Summary and Recommendations

### Overall Readiness Status

**✅ READY**

The project is implementation-ready. All 32 functional requirements have full, traceable coverage in the epics and stories. No critical or major issues were found. The planning artifacts are coherent, consistent, and well-structured. The 5 minor concerns identified are optional refinements — none of them constitute blockers.

---

### Critical Issues Requiring Immediate Action

_None._ No blockers to implementation.

---

### Minor Concerns (Optional — Address or Accept Risk)

| # | Concern | Risk if Unaddressed | Recommendation |
|---|---------|---------------------|----------------|
| 1 | Epic 1 named "Working Project Skeleton" (technical framing) | Low — implementer may not appreciate the user-visible outcome | Rename to reflect user outcome, e.g. "Demo Foundation: Compilable Scaffold and Data Contracts" |
| 2 | Epic 3 named "Deliberate Defects" (technical framing) | Low | Rename to "Demo-Verifiable Anti-Patterns" or similar |
| 3 | Story 2.6 missing explicit anti-pattern ACs for BJACK-MAIN | Medium — risk of implementer writing clean orchestrator code | Add GOTO / cryptic-naming / wrong-comment / no-EVALUATE ACs to Story 2.6, consistent with Stories 2.1–2.5 |
| 4 | NFR2 (immediate render) and NFR6 (consistent behavior across runs) not in any story AC | Low — implied by overall build quality | Optionally add to Story 2.6 as verifiable ACs or accept as implicit |
| 5 | PRD NFR12 (inverted quality bar as explicit NFR) not listed in epics NFR section | Low — principle is enforced per-story | Add NFR12 to epics NFR list for completeness of traceability |

---

### Recommended Next Steps

1. **Proceed to implementation.** The epics are sequenced correctly. Begin with Epic 1, Story 1.1 (Project Scaffold and Shared Data Structures).
2. **Address Concern #3 before Story 2.6 begins.** Add explicit anti-pattern ACs to Story 2.6 to close the single meaningful gap before the BJACK-MAIN implementation story runs.
3. **Optionally address Concerns #1 and #2** (epic renaming) during sprint planning or story creation — low-effort and improves clarity for future readers of the planning artifacts.
4. **Concerns #4 and #5** can be addressed as a quick edit to epics.md or accepted as-is given the low risk.

---

### Final Note

This assessment identified **5 minor concerns** across **2 categories** (epic naming and acceptance criteria completeness). No critical or major issues were found. The planning artifacts — PRD, Architecture, and Epics — are well-aligned and implementation-ready. The most actionable item before implementation starts is adding anti-pattern ACs to Story 2.6 (Concern #3).

**Assessed by:** Winston (Architect Agent)
**Assessment Date:** 2026-02-26
**Report:** docs/planning-artifacts/implementation-readiness-report-2026-02-26.md
