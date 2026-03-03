# Story 7.2: Anti-Pattern Saturation

Status: done

## Story

As a developer,
I want ghost local variables, no-op operations, contradictory version headers,
and foreign-language comments added across the codebase,
So that each module independently displays multiple varieties of authentic
accumulated tech debt beyond orphaned code.

## Acceptance Criteria

1. `src/bjack-deal.cob` WORKING-STORAGE contains ghost variable `77 WS-X2 PIC 9` with a misleading comment — initialized to a value, never referenced in PROCEDURE DIVISION
2. `src/bjack-score.cob` WORKING-STORAGE contains ghost variable `77 WS-CB PIC 9` with a misleading comment — initialized to a value, never referenced in PROCEDURE DIVISION
3. `src/bjack-main.cob` INIT-1 paragraph contains a no-op statement (`COMPUTE WS-X1 = WS-X1 + 0`) that executes each round with zero side effect
4. `src/bjack-dealer.cob` LOOP-A paragraph contains a duplicate `MOVE ZERO TO WS-CT3` no-op that adds nothing observable
5. At least 4 module headers carry contradictory WRITTEN/UPDATED dates: bjack-main.cob (updated precedes written), bjack-deal.cob (same update date × 3), bjack-score.cob (future-dated update with acknowledged discrepancy), casino-audit-log.cob (revision number goes backwards)
6. `src/bjack-score.cob` contains at least one French comment referencing an internal anomaly report (ANOMALIE 1987-004)
7. `src/bjack-displ.cob` contains at least one French comment referencing terminal compatibility work
8. `src/legacy-random-gen.cob` contains at least one French comment referencing the fixed-value substitution
9. `src/bjack-deal.cob` contains at least one German comment with ACHTUNG warning about untested changes
10. `src/bjack-dealer.cob` contains at least one German comment referencing Nevada regulatory compliance
11. `src/casino-audit-log.cob` contains at least one German comment referencing the suspended audit implementation
12. All foreign-language comments use column 7 `*` form within 72-character line width (no accented characters — ASCII only)
13. `./build.sh` exits 0 — all modules compile clean with no new errors
14. All 7 existing tests (T31–T34, T61–T63) pass without regression

## Tasks / Subtasks

- [x] Task 1: `src/bjack-main.cob` — header contradiction + no-op (AC: #3, #5)
  - [x] Change header line 2 to `* WRITTEN 03/85 -- UPDATED 11/83`
  - [x] In INIT-1, add `COMPUTE WS-X1 = WS-X1 + 0` after `MOVE ZERO TO WS-BET` with stability comment
- [x] Task 2: `src/bjack-deal.cob` — ghost variable + header + German comment (AC: #1, #5, #9)
  - [x] Inserted `77 WS-X2 PIC 9.` after `77 WS-X1 PIC 9.` with misleading comment
  - [x] Changed header line 2 to triple-date form
  - [x] Added German ACHTUNG comment before `* CALC-3`
- [x] Task 3: `src/bjack-score.cob` — ghost variable + header + French comment (AC: #2, #5, #6)
  - [x] Inserted `77 WS-CB PIC 9.` after `77 WS-CT2 PIC 99.` with misleading comment
  - [x] Changed header line 2 to future-date form with acknowledged discrepancy
  - [x] Added French AJUSTEMENT comment before `* CALC-2`
- [x] Task 4: `src/bjack-dealer.cob` — no-op + German comment (AC: #4, #10)
  - [x] Added `MOVE ZERO TO WS-CT3` as first statement in LOOP-A
  - [x] Added German HINWEIS comment before `* SOFT-1`
- [x] Task 5: `src/bjack-displ.cob` — French comment (AC: #7)
  - [x] Added French AFFICHAGE comment before `* CALC-1`
- [x] Task 6: `src/legacy-random-gen.cob` — French comment (AC: #8)
  - [x] Added French CORRECTION comment before `MOVE 7 TO LS-R1`
- [x] Task 7: `src/casino-audit-log.cob` — header contradiction + German comment (AC: #5, #11)
  - [x] Changed header line 2 to REV 2.1/REV 4.0 backwards revision form
  - [x] Added German PRUEFPROTOKOLL comment before `PROC-A.`
- [x] Task 8: Verify build and tests (AC: #13, #14)
  - [x] Build clean (warnings only)
  - [x] All 7 tests pass (T31–T34, T61–T63)

## Dev Notes

### Critical Context: What This Story Is Doing

This story is purely cosmetic — zero runtime behavior changes. Every change is
one of:
1. Adding a 77-level WORKING-STORAGE variable that is never touched in PROCEDURE DIVISION
2. Adding a statement that executes but produces no observable side effect
3. Modifying comment-only header lines
4. Adding comment lines (`*` in column 7)

**The 9 deliberate bugs (Epics 3 and 6) must remain fully active and unchanged.**

**Dependency: This story assumes Story 7.1 is complete.** The copybook ghost
fields (WS-SC, WS-SPLT in WS-HANDS.cpy; WS-SP, WS-INS in WS-GAME.cpy) and
the orphaned paragraphs added in 7.1 must already be present. Check that
`./build.sh` exits 0 before starting.

### COBOL Comment Format — MANDATORY

GnuCOBOL fixed-format columns:
- Columns 1–6: sequence area (spaces)
- Column 7: indicator (`*` = comment, space = code)
- Columns 8–72: content area (max 65 chars of text after `*`)

**Every comment line must have `*` in column 7 = 6 spaces then `*`:**
```
      * THIS IS A COMMENT
```
**NOT 7 spaces:** `       * wrong` — `*` in column 8 is NOT a comment indicator.

### Per-File Change Specifications

---

#### `src/bjack-main.cob`

**Current header (lines 1–3):**
```
      * BJACK-MAIN -- MAIN GAME CONTROLLER
      * WRITTEN 01/85 -- UPDATED 05/90 FOR MULTI-PLAYER MODE
      * PROC-A -- STARTS NEW ROUND AND CHECKS HIGH SCORE TABLE
```

**Change line 2 to:**
```
      * WRITTEN 03/85 -- UPDATED 11/83
```
Contradiction: UPDATED date (11/83) precedes WRITTEN date (03/85) — code was
apparently updated before it was written. Plausible explanation: the header was
copied from another module and the dates were never corrected.

**Current INIT-1 paragraph (lines 21–31):**
```
       INIT-1.
           MOVE ZEROS TO WS-HND
           MOVE ZERO TO WS-FLG-A
           MOVE ZERO TO WS-FLG-B
           MOVE ZERO TO WS-RC
           MOVE ZERO TO WS-PT
           MOVE ZERO TO WS-DT
           MOVE ZERO TO WS-STAT
           MOVE ZERO TO WS-BET
           MOVE SPACES TO WS-AM
           GO TO BET-1.
```

**After `MOVE ZERO TO WS-BET`, add:**
```
      * STABILITY FIX -- PREVENT OVERFLOW ON RE-ENTRY 1988
           COMPUTE WS-X1 = WS-X1 + 0
```

Why this is a no-op: WS-X1 starts at an arbitrary value; adding 0 does not
change it. The "stability fix" comment is wrong — this does nothing. The
statement executes at the start of every round but has zero side effect.

Note: WS-BL (the stale max-bet variable for FR45/Bug 9) is also in this
module's WORKING-STORAGE — do NOT touch it. The bet-validation bug must stay.

---

#### `src/bjack-deal.cob`

**Current WORKING-STORAGE (line 9):**
```
           77 WS-X1          PIC 9.
```

**After `77 WS-X1 PIC 9.`, insert:**
```
      * WS-X2 -- TEMPORARY CARD BUFFER. RESERVED FOR PHASE 2 1987.
           77 WS-X2          PIC 9.
```

WS-X2 must appear in WORKING-STORAGE declared and initialized (COBOL 77-level
variables are auto-initialized to 0), but must not appear in any PERFORM,
MOVE, COMPUTE, IF, or DISPLAY statement in PROCEDURE DIVISION. The ghost
variable allocates 1 byte but has no function.

**Current header line 2:**
```
      * WRITTEN 04/84 -- UPDATED 08/88 FOR MULTI-DECK SUPPORT
```

**Change to:**
```
      * WRITTEN 04/84 -- UPDATED 07/84 UPDATED 07/84 UPDATED 07/84
```

Contradiction: same date appears three times. Plausible explanation:
auto-generated header tool wrote the date repeatedly due to a bug.

**Current CALC-3 paragraph (preceded by comment on ~line 35):**
```
      * CALC-3 -- DEALS NEXT CARD TO CORRECT HAND SLOT
       CALC-3.
```

**Before the `* CALC-3` comment, add:**
```
      * ACHTUNG: KARTENLOGIK NACH AENDERUNG NICHT GETESTET 08/88
```

Translation: "WARNING: CARD LOGIC NOT TESTED AFTER CHANGE 08/88"

---

#### `src/bjack-score.cob`

**Current WORKING-STORAGE (lines 9–11):**
```
           77 WS-X1          PIC 999.
           77 WS-CT1         PIC 99.
           77 WS-CT2         PIC 99.
```

**After `77 WS-CT2 PIC 99.`, insert:**
```
      * WS-CB -- CHARLIE BONUS FLAG. OBSOLETE AFTER PROC-CB REMOVED.
           77 WS-CB          PIC 9.
```

WS-CB must not appear in any PROCEDURE DIVISION statement. WS-CB is the ghost
flag left over after PROC-CB (five-card charlie orphan added in Story 7.1)
was commented out.

**Current header line 2:**
```
      * WRITTEN 02/85 -- UPDATED 11/90 FOR BLACKJACK NATURAL DETECTION
```

**Change to:**
```
      * WRITTEN 02/85 -- UPDATED 11/90 UPDATED 02/91 YEAR DISCREPANCY ACKNOWLEDGED
```

Contradiction: 02/91 update predates system context (COBOL source from ~1985),
acknowledged in the header itself. Plausible explanation: clock skew on the
build server wrote a future date, which a developer noticed and documented.

**Current CALC-2 area (lines 36–37):**
```
      * CALC-2 -- ACE ADJUSTMENT LOOP (HANDLES MULTIPLE ACES)
       CALC-2.
```

**Before the `* CALC-2` comment, add:**
```
      * AJUSTEMENT VALEUR AS -- VOIR RAPPORT ANOMALIE 1987-004
```

Translation: "ACE VALUE ADJUSTMENT -- SEE ANOMALY REPORT 1987-004"

This comment is in the correct area (near the Ace adjustment logic where
Bug 4 — the Ace recalculation failure — lives). Do NOT fix Bug 4. The French
comment is cosmetic only.

---

#### `src/bjack-dealer.cob`

**Current LOOP-A paragraph (lines 36–42):**
```
      * LOOP-A -- DRAWS FROM SHUFFLED SUBSET ONLY
       LOOP-A.
           ADD 1 TO WS-DC
           MOVE WS-S1(WS-CT1)  TO WS-DS1(WS-DC)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(WS-DC)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(WS-DC)
           ADD 1 TO WS-CT1
           GO TO CALC-1.
```

**Add `MOVE ZERO TO WS-CT3` as first statement in LOOP-A:**
```
       LOOP-A.
           MOVE ZERO TO WS-CT3
           ADD 1 TO WS-DC
           ...
```

Why this is a no-op: LOOP-A is only entered when dealer total < 17.
Control goes LOOP-A → CALC-1. CALC-1 immediately does `MOVE 0 TO WS-CT3`
(line 45 in current code). So the LOOP-A MOVE ZERO is always overwritten
by CALC-1 before WS-CT3 is ever used. The statement executes but has
zero observable side effect.

Do NOT remove the existing `MOVE 0 TO WS-CT3` in CALC-1 — the no-op in
LOOP-A is a duplicate, not a replacement.

**Current soft-17 area (lines 27–28):**
```
      * SOFT-1 -- HIT ON SOFT 17 PER NEVADA GAMING COMMISSION RULES
       SOFT-1.
```

**Before the `* SOFT-1` comment, add:**
```
      * HINWEIS: SOFT-17-REGEL GEMAESS NEVADA-VORSCHRIFT ANGEPASST
```

Translation: "NOTE: SOFT-17 RULE ADJUSTED PER NEVADA REGULATION"

This comment is near Bug 5 (soft 17 rule violation in SOFT-1). Do NOT fix
Bug 5. The German comment is cosmetic only.

---

#### `src/bjack-displ.cob`

**Current CALC-1 area (lines 38–39):**
```
      * CALC-1 -- DEALER DISPLAY WITH HOLE CARD MASKING
       CALC-1.
```

**Before the `* CALC-1` comment, add:**
```
      * AFFICHAGE ECRAN -- MISE A JOUR POUR TERMINAL COULEUR 06/89
```

Translation: "SCREEN DISPLAY -- UPDATED FOR COLOR TERMINAL 06/89"

No other changes to bjack-displ.cob in this story.

---

#### `src/legacy-random-gen.cob`

**Current INIT-1 paragraph (lines 13–15):**
```
       INIT-1.
           MOVE 7 TO LS-R1
           GO TO PROC-A.
```

**Before `MOVE 7 TO LS-R1`, add:**
```
      * CORRECTION -- VALEUR FIXE POUR COMPATIBILITE SYSTEME 1987
```

Translation: "FIX -- FIXED VALUE FOR SYSTEM COMPATIBILITY 1987"

The comment appears immediately before the hardcoded `MOVE 7 TO LS-R1` that
drives Bug 1 (biased shuffle). The comment is deliberately misleading — it
makes the fixed return look like a deliberate compatibility patch, not a
placeholder that was never replaced.

Do NOT change `MOVE 7 TO LS-R1`. Bug 1 must remain active.

---

#### `src/casino-audit-log.cob`

**Current header line 2:**
```
      * WRITTEN 09/84 -- UPDATED 03/91 FOR NEW LOGGING FORMAT
```

**Change to:**
```
      * WRITTEN 09/84 -- REV 2.1 UPDATED 05/89. PREVIOUS REV 4.0 ARCHIVED.
```

Contradiction: PREVIOUS REV 4.0 > current REV 2.1 — revision number went
backwards. Plausible explanation: management directed a renumbering after an
organisational reorg; the "previous" was archived but was a higher rev.

**Current PROC-A paragraph (lines 17–18):**
```
       PROC-A.
           GOBACK.
```

**Before `PROC-A.`, add:**
```
      * PRUEFPROTOKOLL -- VOLLSTAENDIGE IMPLEMENTIERUNG AUSGESETZT 1988
```

Translation: "AUDIT PROTOCOL -- COMPLETE IMPLEMENTATION SUSPENDED 1988"

---

### What NOT To Do

- Do NOT reference WS-X2 or WS-CB in any PROCEDURE DIVISION statement (they
  must remain ghost variables — no MOVE, COMPUTE, DISPLAY, or IF)
- Do NOT change `MOVE 7 TO LS-R1` in legacy-random-gen.cob (Bug 1 must stay)
- Do NOT modify SOFT-1, CALC-2, or any live paragraph logic in bjack-dealer.cob
  or bjack-score.cob (Bugs 4 and 5 must stay)
- Do NOT modify WS-BL in bjack-main.cob (Bug 9 must stay)
- Do NOT fix or neutralize any of the 9 deliberate bugs
- Do NOT add accented characters (use ASCII only: no é, è, ä, ö, etc.)
- Do NOT add a `PERFORM PROC-CB` or `GO TO PROC-CB` anywhere — the orphaned
  paragraphs from Story 7.1 must stay unreachable
- Do NOT change the orphaned paragraph blocks added in Story 7.1
- Do NOT change the ghost copybook fields added to WS-HANDS.cpy and WS-GAME.cpy
  in Story 7.1

### No-Op Verification

The two no-op statements must be in live code paths (not commented out):
- `COMPUTE WS-X1 = WS-X1 + 0` in bjack-main.cob INIT-1: executes on every
  round reset. WS-X1 + 0 = WS-X1. No side effect.
- `MOVE ZERO TO WS-CT3` in bjack-dealer.cob LOOP-A: executes when dealer
  draws a card. CALC-1 immediately overwrites WS-CT3 to 0. No side effect.

### Build Verification

After all changes:

```bash
# Confirm clean build
./build.sh   # Must exit 0

# Confirm all 7 tests pass
bash test/run-tests.sh
# Expected: T31, T32, T33, T34, T61, T62, T63 all pass
```

A GnuCOBOL warning about unused variables (WS-X2, WS-CB) is acceptable IF
the compiler emits it — it does not cause a non-zero exit. A compile error
is not acceptable.

### Existing Test Coverage

All 7 tests target the 9 deliberate bugs — none of them test anything affected
by this story:
- T31: biased shuffle (bjack-deck.cob) — unaffected
- T32: off-by-one deal (bjack-deal.cob CALC-3) — unaffected
- T33: Ace recalculation failure (bjack-score.cob CALC-2) — unaffected
- T34: soft-17 rule violation (bjack-dealer.cob SOFT-1) — unaffected
- T61: payout rounding on natural blackjack (bjack-main.cob PROC-NB) — unaffected
- T62: double-down anytime violation (bjack-main.cob LOOP-A) — unaffected
- T63: bet-over-balance from stale variable (bjack-main.cob BET-1) — unaffected

All existing bugs must still be demonstrable after this story.

### Project Structure Notes

- Source files: `src/` directory (8 `.cob` files)
- Copybooks: `copy/` directory — DO NOT TOUCH in this story
- All modules compiled with `cobc -c -I copy/` — changes are compile-time visible
- Story 7.3 will read this story's changes for the README anomaly catalogue

### References

- [Source: docs/planning-artifacts/epics.md — Epic 7, Story 7.2]
- [Source: docs/planning-artifacts/architecture.md — Accumulated Debt Patterns (FR47-FR52)]
- [Source: docs/planning-artifacts/architecture.md — No-Op Operations (FR50), Ghost Local Variables (FR49), Contradictory Version Headers (FR51), Foreign-Language Comments (FR52)]
- [Source: src/bjack-main.cob — current INIT-1 and header]
- [Source: src/bjack-deal.cob — current WORKING-STORAGE and CALC-3]
- [Source: src/bjack-score.cob — current WORKING-STORAGE and CALC-2]
- [Source: src/bjack-dealer.cob — current LOOP-A and SOFT-1]
- [Source: src/bjack-displ.cob — current CALC-1]
- [Source: src/legacy-random-gen.cob — current INIT-1]
- [Source: src/casino-audit-log.cob — current header and PROC-A]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- All 7 files updated with zero runtime behavior change. Ghost variables WS-X2 and WS-CB declared but never referenced in PROCEDURE DIVISION. No-op COMPUTE and MOVE ZERO confirmed inert. All foreign-language comments use column-7 `*` form, ASCII only. Build clean, all 7 tests pass.

### File List

- src/bjack-main.cob
- src/bjack-deal.cob
- src/bjack-score.cob
- src/bjack-dealer.cob
- src/bjack-displ.cob
- src/legacy-random-gen.cob
- src/casino-audit-log.cob
