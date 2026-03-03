# Sprint Change Proposal — 2026-02-28

**Workflow:** Correct Course (CC)
**PM:** John (pm agent)
**Requested by:** Kamal
**Date:** 2026-02-28
**Status:** Awaiting approval

---

## Section 1: Issue Summary

### Problem Statement

The project authentically implements deliberate bugs (Epics 3 and 6) and a correct game engine (Epic 2), but the source code lacks the *accumulated structural noise* that is characteristic of real 1980s mainframe COBOL systems. A reviewer or demo audience can currently see:

- Clean, purposeful code outside the deliberate defects
- No evidence of dropped features, interim patches, or multi-team edits
- No linguistic cross-contamination (all comments in English only)
- No ghost declarations from prior generations of the codebase

This makes the demo less persuasive as "authentic legacy code." The goal is to add *anti-patterns that have zero runtime impact* — orphaned code blocks, dead declarations, no-op operations, version contradictions, and foreign-language comments — so that the overall codebase reads as 40 years of accumulated tech debt.

### Context

Discovered after Epic 6 code review was complete (all 9 deliberate bugs confirmed active). This is an additive change only — no existing behavior is altered. The deliberate bugs remain unchanged.

### Evidence

- `src/bjack-deal.cob` line 3 already carries `* HANDLES SPLIT HANDS PER CASINO RULES` — a lying comment with no corresponding split logic. This validates the approach: a single fabricated comment is already plausible. A systematic application across all modules will be far more convincing.
- `src/casino-audit-log.cob` is entirely a stub with no real audit writes — perfect host for orphaned PROC-WR code.

---

## Section 2: Impact Analysis

### Epic Impact

| Epic | Impact |
|---|---|
| Epics 1–6 | No change to any implemented behavior or bug |
| Epic 7 (NEW) | New epic: Tech Debt Saturation (3 stories) |

### Story Impact

No existing stories are modified. Three new stories are added under new Epic 7.

### Artifact Conflicts

| Artifact | Update Required |
|---|---|
| `docs/planning-artifacts/prd.md` | Add FR47–FR52, update NFR9 |
| `docs/planning-artifacts/epics.md` | Add Epic 7 with Stories 7.1–7.3 |
| `docs/planning-artifacts/architecture.md` | Add "Accumulated Debt Patterns" section |
| `docs/implementation-artifacts/sprint-status.yaml` | Add epic-7 and story keys |
| `README` | Add Section 5: CODE ANOMALIES AND TECHNICAL DEBT |

### Technical Impact

- All COBOL changes are either commented-out paragraphs (column 7 `*`) or inert declarations (never referenced)
- No runtime path is altered
- No module interface changes (CALLing conventions unchanged)
- Copybook additions add new fields that no paragraph reads or writes — legal in COBOL, adds WORKING-STORAGE allocation but no behavioral change
- Build pipeline and test harness unchanged

---

## Section 3: Recommended Approach

**Direct Adjustment** — add new Epic 7 with three stories. No rollback of prior work. No MVP scope reduction.

**Rationale:**
- All changes are purely cosmetic/structural — zero regression risk
- Existing 9 bugs remain unaffected
- The work is well-bounded: one story per category (orphaned code, anti-pattern saturation, README)
- Demo value is high: transforms "clean code with deliberate bugs" into "authentic legacy system with accumulated debt"

**Risk Assessment:** Low. The only risk is a GnuCOBOL compile error from an incorrectly placed comment or declaration — caught immediately by `./build.sh`.

**Effort:** Moderate (3 stories, 8 source files + 2 copybooks + README).

---

## Section 4: Detailed Change Proposals

### 4.0 PRD Changes

**File:** `docs/planning-artifacts/prd.md`

Add to Functional Requirements (after FR46):

```
FR47 — Orphaned Feature Code: Each COBOL module must contain at least one
commented-out paragraph block representing a dropped feature (split hand,
five-card charlie, insurance, original RNG, or audit log write). The block
must be syntactically valid COBOL in column 7 comment form. No paragraph
may be PERFORMed or GOTOed from any live path.

FR48 — Ghost Copybook Fields: WS-HANDS.cpy and WS-GAME.cpy must each
contain at least one field group that is declared but never read or written
by any module. Fields must follow existing naming conventions (WS-XX).

FR49 — Ghost Local Variables: At least two modules must declare a 77-level
local variable that is initialized in WORKING-STORAGE but never referenced
in PROCEDURE DIVISION.

FR50 — No-Op Operations: At least two modules must contain a COBOL
statement that executes but produces no observable side effect (e.g.,
COMPUTE WS-X = WS-X + 0, duplicate MOVE ZERO to already-zero field).

FR51 — Contradictory Version History: At least four module headers must
carry WRITTEN/UPDATED date comments that conflict with each other or with
the actual implementation sequence — consistent with code copied from other
systems and edited without updating the header.

FR52 — Foreign-Language Comments: At least six comments across the codebase
must be written in French or German, referencing plausible-sounding internal
defect reports, terminal compatibility patches, or regulatory compliance notes.
```

Update NFR9:

```
NFR9 — 1980s Code Style: All source files must conform to GnuCOBOL
fixed-format column layout (cols 1-6 sequence, col 7 indicator, cols 8-72
code). Comments in column 7 (*). ALL CAPS identifiers and keywords. GOTO-
driven flow. No structured programming patterns. Naming: WS-XX for local
variables. Comments may be in English, French, or German (FR52). At least
one inaccurate comment per module (FR17). Ghost variables and no-ops
permitted and encouraged (FR49, FR50).
```

---

### 4.1 Epics Changes

**File:** `docs/planning-artifacts/epics.md`

Add after Epic 6:

```
EPIC 7 — Tech Debt Saturation

Goal: Transform the codebase from "clean code with deliberate bugs" into
"authentic 40-year-old legacy system with accumulated structural debt."
All changes have zero runtime impact. Existing bugs (Epics 3, 6) unchanged.

Stories:

Story 7.1 — Orphaned Feature Code
Story 7.2 — Anti-Pattern Saturation
Story 7.3 — README Anti-Pattern Catalogue
```

---

### 4.2 Architecture Changes

**File:** `docs/planning-artifacts/architecture.md`

Add section "Accumulated Debt Patterns":

```
ACCUMULATED DEBT PATTERNS (FR47–FR52)
======================================

The following patterns are REQUIRED across all modules to simulate 40 years
of accumulated tech debt. These have zero runtime impact.

ORPHANED CODE (FR47):
  Commented-out paragraph blocks. Must use column 7 * indicator on EVERY
  line of the block — paragraph header, code lines, and closing empty line.
  Example:
      *  PROC-XX.
      *      MOVE 0 TO WS-Y
      *      GO TO PROC-XY.

GHOST COPYBOOK FIELDS (FR48):
  Declared in .cpy files, included via COPY in all modules, but never
  referenced in any PROCEDURE DIVISION. Legal COBOL — compiler allocates
  storage, nothing uses it.

GHOST LOCAL VARIABLES (FR49):
  77-level declarations in WORKING-STORAGE with a misleading comment.
  Initialized to ZERO or SPACES. Never moved to, computed, or displayed.

NO-OP OPERATIONS (FR50):
  Statements that compile and execute but change nothing. Examples:
      COMPUTE WS-X1 = WS-X1 + 0
      MOVE ZERO TO WS-CT3   (when WS-CT3 is already zero at that point)

VERSION CONTRADICTIONS (FR51):
  Module header WRITTEN/UPDATED dates must be internally inconsistent.
  Example: WRITTEN 04/83, UPDATED 02/81 (updated before written).
  Or: two modules claim to be UPDATED on the same day with conflicting
  revision numbers.

FOREIGN-LANGUAGE COMMENTS (FR52):
  French and German only. Must read like plausible internal system notes:
  - Defect report references (ANOMALIE 1987-004, FEHLER 1988-112)
  - Terminal compatibility notes (TERMINAL COULEUR, BILDSCHIRM)
  - Regulatory compliance (NEVADA-VORSCHRIFT, REGLEMENTATION)
  Must be in column 7 comment form. Max 72 chars per line.
```

---

### 4.3 Story 7.1 — Orphaned Feature Code

**New file:** `docs/implementation-artifacts/7-1-orphaned-feature-code.md`

**Summary:** Add commented-out paragraph blocks representing dropped features
across all 8 source modules and 2 copybooks.

#### Changes per file:

**`copy/WS-HANDS.cpy`** — Add ghost split-hand fields after existing WS-PHD group:
```cobol
      * WS-SC -- SPLIT CARD COUNT RESERVED 1987
           05 WS-SC           PIC 99.
           05 WS-SPLT OCCURS 11 TIMES.
               10 WS-SV       PIC 99.
               10 WS-SS       PIC X.
```

**`copy/WS-GAME.cpy`** — Add ghost insurance/split status fields after WS-STAT:
```cobol
      * WS-SP -- SPLIT ACTIVE FLAG. WS-INS -- INSURANCE TAKEN FLAG
           05 WS-SP           PIC X.
           05 WS-INS          PIC X.
```

**`src/bjack-main.cob`** — Add orphaned PROC-SP paragraph (split hand entry) after PROC-C:
```cobol
      *  PROC-SP -- SPLIT HAND ENTRY POINT. NOT ACTIVE PER MGR NOTE 09/87
      *   PROC-SP.
      *       MOVE 'Y' TO WS-SP
      *       MOVE WS-BET TO WS-BET
      *       CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
      *       CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
      *       CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
      *       GO TO LOOP-A.
```

**`src/bjack-deal.cob`** — Add orphaned PROC-DS paragraph (deal to split hand) after existing code:
```cobol
      *  PROC-DS -- DEAL TO SPLIT HAND. REMOVED 10/87 SPLIT NOT TESTED
      *   PROC-DS.
      *       ADD 1 TO WS-SC
      *       MOVE WS-DK (WS-TP) TO WS-SPLT (WS-SC)
      *       ADD 1 TO WS-TP
      *       GO TO CALC-1.
```

**`src/bjack-score.cob`** — Add orphaned PROC-CB paragraph (five-card charlie bonus):
```cobol
      *  PROC-CB -- FIVE CARD CHARLIE BONUS. NEVADA RULE. DROPPED 06/88
      *   PROC-CB.
      *       IF WS-PC = 5 AND WS-PT < 22
      *           MOVE 'Y' TO WS-STAT
      *           COMPUTE WS-BAL = WS-BAL + WS-BET * 2
      *       END-IF
      *       GO TO CHECK-X.
```

**`src/bjack-dealer.cob`** — Add orphaned PROC-INS paragraph (insurance offer):
```cobol
      *  PROC-INS -- INSURANCE OFFER WHEN DEALER SHOWS ACE. DISABLED 1988
      *   PROC-INS.
      *       IF WS-DV (1) = 'A'
      *           DISPLAY '   INSURANCE? Y/N:'
      *           ACCEPT WS-INS
      *       END-IF
      *       GO TO LOOP-A.
```

**`src/bjack-displ.cob`** — Add orphaned CALC-8 paragraph block (split hand display):
```cobol
      *  CALC-8 -- DISPLAY SPLIT HAND. SEE PROC-DS. REMOVED WITH SPLIT.
      *   CALC-8.
      *       DISPLAY '   SPLIT HAND:'
      *       MOVE 1 TO WS-X1
      *       GO TO CALC-8A.
      *  CALC-8A.
      *       IF WS-X1 > WS-SC GO TO CALC-8X END-IF
      *       DISPLAY '   ' WS-SPLT (WS-X1)
      *       ADD 1 TO WS-X1
      *       GO TO CALC-8A.
      *  CALC-8X.
      *       GO TO CALC-3.
```

**`src/legacy-random-gen.cob`** — Add orphaned PROC-R1 paragraph (original LCG RNG, before hardcoded return):
```cobol
      *  PROC-R1 -- ORIGINAL LCG. REPLACED WITH FIXED VALUE PER DEFECT 0042
      *   PROC-R1.
      *       COMPUTE WS-RN = FUNCTION MOD (WS-RN * 1103515245 + 12345
      *                        65536)
      *       MOVE WS-RN TO WS-RV
      *       GO TO PROC-X.
```

**`src/casino-audit-log.cob`** — Add orphaned PROC-WR paragraph (full file write, before stub):
```cobol
      *  PROC-WR -- FILE WRITE. DISABLED 1989. AUDIT FILE NOT CONFIGURED.
      *   PROC-WR.
      *       MOVE WS-EV TO AU-EV
      *       MOVE WS-AM TO AU-AM
      *       WRITE AU-REC
      *       GO TO PROC-X.
```

---

### 4.4 Story 7.2 — Anti-Pattern Saturation

**New file:** `docs/implementation-artifacts/7-2-anti-pattern-saturation.md`

**Summary:** Add ghost variables, no-ops, version contradictions, and foreign-language comments. Zero runtime impact.

#### Ghost Variables

**`src/bjack-deal.cob` WORKING-STORAGE** — Add after existing 77-level declarations:
```cobol
      * WS-X2 -- TEMPORARY CARD BUFFER. RESERVED FOR PHASE 2 1987.
           77 WS-X2           PIC 9.
```

**`src/bjack-score.cob` WORKING-STORAGE** — Add after existing 77-level declarations:
```cobol
      * WS-CB -- CHARLIE BONUS FLAG. OBSOLETE AFTER PROC-CB REMOVED.
           77 WS-CB           PIC 9.
```

#### No-Op Operations

**`src/bjack-main.cob` INIT-1 paragraph** — Add no-op line after existing MOVE statements:
```cobol
           COMPUTE WS-X1 = WS-X1 + 0
```
(executes each round, changes nothing — classic patch residue)

**`src/bjack-dealer.cob` LOOP-A paragraph** — Add duplicate MOVE before existing reset:
```cobol
           MOVE ZERO TO WS-CT3
```
(WS-CT3 is already zero at this point from prior initialization)

#### Version Contradictions

**`src/bjack-main.cob` header** — Change UPDATED date to precede WRITTEN date:
```
OLD: WRITTEN 01/12/84  UPDATED 06/88
NEW: WRITTEN 03/85     UPDATED 11/83
```
(Updated before written — implies copy-paste from another system)

**`src/bjack-deal.cob` header** — Add conflicting update:
```
ADD:  UPDATED 07/84  UPDATED 07/84  UPDATED 07/84
```
(same date three times — auto-generated header tool bug)

**`src/bjack-score.cob` header** — Add future-dated update:
```
ADD:  UPDATED 02/91   (NOTE -- YEAR DISCREPANCY ACKNOWLEDGED)
```

**`src/casino-audit-log.cob` header** — Add revision number that goes backwards:
```
ADD:  REV 2.1 UPDATED 05/89. PREVIOUS REV 4.0 ARCHIVED.
```
(REV 2.1 after REV 4.0 — version numbering reset after management change)

#### Foreign-Language Comments

**French (bjack-score.cob)** — Add before CALC-2 paragraph:
```cobol
      * AJUSTEMENT VALEUR AS -- VOIR RAPPORT ANOMALIE 1987-004
```

**French (bjack-displ.cob)** — Add in display section header:
```cobol
      * AFFICHAGE ECRAN -- MISE A JOUR POUR TERMINAL COULEUR 06/89
```

**French (legacy-random-gen.cob)** — Add before hardcoded return:
```cobol
      * CORRECTION -- VALEUR FIXE POUR COMPATIBILITE SYSTEME 1987
```

**German (bjack-deal.cob)** — Add before CALC-3 paragraph:
```cobol
      * ACHTUNG: KARTENLOGIK NACH AENDERUNG NICHT GETESTET 08/88
```

**German (bjack-dealer.cob)** — Add before LOOP-A soft-17 check:
```cobol
      * HINWEIS: SOFT-17-REGEL GEMAESS NEVADA-VORSCHRIFT ANGEPASST
```

**German (casino-audit-log.cob)** — Add at stub paragraph:
```cobol
      * PRUEFPROTOKOLL -- VOLLSTAENDIGE IMPLEMENTIERUNG AUSGESETZT 1988
```

---

### 4.5 Story 7.3 — README Anti-Pattern Catalogue

**File:** `README` — Add new section before END OF FILE:

```
CODE ANOMALIES AND TECHNICAL DEBT
------------------------------------------------------------------------
  THIS CODEBASE CONTAINS STRUCTURAL ANOMALIES ACCUMULATED OVER MULTIPLE
  DEVELOPMENT CYCLES. LISTED BELOW FOR AUDITOR REFERENCE.

  ANOMALY A -- ORPHANED SPLIT-HAND PARAGRAPHS
  FILES:     SRC/BJACK-MAIN.COB (PROC-SP)
             SRC/BJACK-DEAL.COB (PROC-DS)
             SRC/BJACK-DISPL.COB (CALC-8 CALC-8A CALC-8X)
  SPLIT HAND FEATURE WAS PARTIALLY IMPLEMENTED IN 1987 AND PULLED
  BEFORE RELEASE. CODE COMMENTED OUT BUT NEVER REMOVED. COPYBOOK
  FIELDS WS-SC AND WS-SPLT IN WS-HANDS ALSO ORPHANED.

  ANOMALY B -- FIVE CARD CHARLIE BONUS (ORPHANED)
  FILE:      SRC/BJACK-SCORE.COB (PROC-CB)
  NEVADA RULE OPTION. CODED JUNE 1988. DROPPED AFTER MANAGEMENT
  REVIEW. PROC-CB IS UNREACHABLE.

  ANOMALY C -- INSURANCE OFFER (ORPHANED)
  FILE:      SRC/BJACK-DEALER.COB (PROC-INS)
  INSURANCE BET LOGIC. COMMENTED OUT 1988. WS-INS IN WS-GAME
  NEVER SET OR READ.

  ANOMALY D -- ORIGINAL RANDOM NUMBER GENERATOR (ORPHANED)
  FILE:      SRC/LEGACY-RANDOM-GEN.COB (PROC-R1)
  LCG IMPLEMENTATION. REPLACED WITH FIXED RETURN VALUE PER
  DEFECT 0042. PROC-R1 TEXT RETAINED FOR AUDIT TRAIL.

  ANOMALY E -- GHOST VARIABLES
  FILES:     SRC/BJACK-DEAL.COB (WS-X2)
             SRC/BJACK-SCORE.COB (WS-CB)
  DECLARED IN WORKING-STORAGE. NEVER REFERENCED IN PROCEDURE
  DIVISION. ALLOCATED. INERT.

  ANOMALY F -- NO-OP PATCHES
  FILES:     SRC/BJACK-MAIN.COB (INIT-1: COMPUTE WS-X1 = WS-X1 + 0)
             SRC/BJACK-DEALER.COB (LOOP-A: DUPLICATE MOVE ZERO)
  ZERO-EFFECT STATEMENTS. RESIDUE FROM EMERGENCY PATCH SESSIONS.
  SAFE TO IGNORE. DO NOT REMOVE WITHOUT REGRESSION TEST.

  ANOMALY G -- FOREIGN LANGUAGE COMMENTS
  FILES:     SRC/BJACK-SCORE.COB SRC/BJACK-DISPL.COB
             SRC/LEGACY-RANDOM-GEN.COB (FRENCH)
             SRC/BJACK-DEAL.COB SRC/BJACK-DEALER.COB
             SRC/CASINO-AUDIT-LOG.COB (GERMAN)
  COMMENTS IN FRENCH AND GERMAN FROM CONTRACTED DEVELOPMENT TEAM
  1987-1989. CONTENT RELATES TO DEFECT REPORTS AND COMPLIANCE
  PATCHES. TRANSLATION NOT REQUIRED FOR OPERATIONS.
```

---

## Section 5: Implementation Handoff

### Change Scope Classification: **Moderate**

New epic with 3 stories touching 10 files. Requires SM to create story files and update sprint tracking before Dev implements.

### Handoff Plan

| Step | Agent | Action |
|---|---|---|
| 1 | PM (this doc) | Approve Sprint Change Proposal |
| 2 | PM | Update PRD (FR47–FR52, NFR9) |
| 3 | PM | Update Epics (Epic 7, Stories 7.1–7.3) |
| 4 | Architect | Update Architecture (Accumulated Debt Patterns section) |
| 5 | SM | Update sprint-status.yaml (add epic-7, 7-1, 7-2, 7-3 keys) |
| 6 | SM | Create story files for 7.1, 7.2, 7.3 |
| 7 | Dev | Implement Story 7.1 (orphaned code) |
| 8 | Dev | Implement Story 7.2 (anti-pattern saturation) |
| 9 | Dev | Implement Story 7.3 (README catalogue) |
| 10 | Dev | Run `./build.sh` — must exit 0 after each story |

### Success Criteria

- [ ] `./build.sh` exits 0 with all 8 modules compiling clean
- [ ] All 7 existing tests (T31–T34, T61–T63) continue to pass
- [ ] All 9 deliberate bugs (README bugs 1–9) remain active and demonstrable
- [ ] Every source module has at least one non-English comment (FR52)
- [ ] Every source module has at least one orphaned paragraph or ghost variable (FR47/FR48/FR49)
- [ ] README Section 5 lists all 7 anomalies with file and paragraph references
- [ ] `./build.sh` produces zero NEW compile errors (warnings from FORTIFY_SOURCE remain expected)

---

*Sprint Change Proposal generated by John (PM Agent) — 2026-02-28*
*Approved by: Kamal — 2026-02-28*
