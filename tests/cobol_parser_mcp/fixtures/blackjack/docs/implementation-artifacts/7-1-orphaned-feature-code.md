# Story 7.1: Orphaned Feature Code

Status: done

## Story

As a developer,
I want every source module to contain commented-out paragraph blocks representing
dropped features and ghost fields in the copybooks,
So that the codebase reads as a system where multiple features were planned,
partially built, and abandoned over many years.

## Acceptance Criteria

1. `copy/WS-HANDS.cpy` contains ghost split-hand fields (WS-SC card count, WS-SPLT OCCURS 11 TIMES array) — declared, included via COPY in all modules, never referenced in any PROCEDURE DIVISION
2. `copy/WS-GAME.cpy` contains ghost insurance/split status fields (WS-SP, WS-INS) — declared but never set or read by any module
3. `src/bjack-main.cob` contains a commented-out PROC-SP paragraph (split hand entry point) — syntactically valid COBOL, column 7 `*` on every line, never reachable
4. `src/bjack-deal.cob` contains a commented-out PROC-DS paragraph (deal to split hand) — column 7 `*` throughout, never reachable
5. `src/bjack-score.cob` contains a commented-out PROC-CB paragraph (five-card charlie bonus) — column 7 `*` throughout, never reachable
6. `src/bjack-dealer.cob` contains a commented-out PROC-INS paragraph (insurance offer) — column 7 `*` throughout, never reachable
7. `src/bjack-displ.cob` contains commented-out CALC-8 / CALC-8A / CALC-8X paragraphs (split hand display) — column 7 `*` throughout, never reachable
8. `src/legacy-random-gen.cob` contains a commented-out PROC-R1 paragraph (original LCG RNG) — column 7 `*` throughout, never reachable
9. `src/casino-audit-log.cob` contains a commented-out PROC-WR paragraph (full audit file write) — column 7 `*` throughout, never reachable
10. `./build.sh` exits 0 — all modules compile clean with no new errors
11. All 7 existing tests (T31–T34, T61–T63) pass without regression

## Tasks / Subtasks

- [x] Task 1: Update `copy/WS-HANDS.cpy` — ghost split-hand fields (AC: #1)
  - [x] Add `05 WS-SC PIC 99` and `05 WS-SPLT OCCURS 11 TIMES` group after the last existing field in `01 WS-HND` (after WS-DFV group)
- [x] Task 2: Update `copy/WS-GAME.cpy` — ghost insurance/split flags (AC: #2)
  - [x] Add `05 WS-SP PIC X` and `05 WS-INS PIC X` inside `01 WS-GM` after `05 WS-BET`
- [x] Task 3: `src/bjack-main.cob` — orphaned PROC-SP paragraph (AC: #3)
  - [x] Append commented-out PROC-SP block after the last live line (`STOP RUN.` on line 132)
- [x] Task 4: `src/bjack-deal.cob` — orphaned PROC-DS paragraph (AC: #4)
  - [x] Append commented-out PROC-DS block after the last live line (`GOBACK.` in CHECK-X)
- [x] Task 5: `src/bjack-score.cob` — orphaned PROC-CB paragraph (AC: #5)
  - [x] Append commented-out PROC-CB block after the last live line
- [x] Task 6: `src/bjack-dealer.cob` — orphaned PROC-INS paragraph (AC: #6)
  - [x] Append commented-out PROC-INS block after the last live line
- [x] Task 7: `src/bjack-displ.cob` — orphaned CALC-8 / CALC-8A / CALC-8X block (AC: #7)
  - [x] Append commented-out three-paragraph block after the last live line
- [x] Task 8: `src/legacy-random-gen.cob` — orphaned PROC-R1 paragraph (AC: #8)
  - [x] Append commented-out PROC-R1 block after PROC-A (after `GOBACK.`)
- [x] Task 9: `src/casino-audit-log.cob` — orphaned PROC-WR paragraph (AC: #9)
  - [x] Append commented-out PROC-WR block after PROC-A (after `GOBACK.`)
- [x] Task 10: Verify build and tests (AC: #10, #11)
  - [x] Run `./build.sh` — must exit 0
  - [x] Run `bash test/run-tests.sh` — all 7 tests (T31–T34, T61–T63) must pass

## Dev Notes

### Critical Context: What This Story Is Doing

This story is purely cosmetic/structural — zero runtime behavior changes. You are:
1. Adding inert field declarations to two copybooks (never referenced by any PROCEDURE DIVISION)
2. Appending COBOL comment blocks to 7 source files (all comment lines, invisible to the compiler)

**The 9 deliberate bugs (Epics 3 and 6) must remain fully active and unchanged.**

### COBOL Comment Format — MANDATORY

GnuCOBOL fixed-format: columns 1-6 sequence area (spaces), column 7 indicator area.
`*` in column 7 = comment line. The entire line is ignored by the compiler.

**Every single line of every orphaned block must have `*` in column 7.**

Correct format (6 spaces, then `*`, then content from col 8 onwards):
```
      * THIS IS A COMMENT
      *  PROC-SP.
      *      MOVE 'Y' TO WS-SP
```

Incorrect (do NOT do this):
```
       * COMMENT   ← 7 spaces before * puts * in col 8, which is NOT a comment
      PROC-SP.     ← live code, NOT commented out
```

Max line length: 72 characters total (cols 1-72). Comment content fits in cols 8-72, i.e., max 65 chars of text after the `*`.

### Copybook Changes

#### `copy/WS-HANDS.cpy` — Current State

```cobol
      * PLAYER/DEALER HAND ARRAYS -- MAX 7 CARDS PER HAND PER RULES 1980
      * UPDATED 09/85 TO SUPPORT SPLIT HANDS -- NOT YET IMPLEMENTED
       01 WS-HND.
          05 WS-PC           PIC 99.
          05 WS-PHD OCCURS 11 TIMES.
             10 WS-PS1       PIC X.
             10 WS-PRK       PIC XX.
             10 WS-PFV       PIC 99.
          05 WS-DC           PIC 99.
          05 WS-DHD OCCURS 11 TIMES.
             10 WS-DS1       PIC X.
             10 WS-DRK       PIC XX.
             10 WS-DFV       PIC 99.
```

**Add these lines at the end of the file (inside the `01 WS-HND` group — level 05 entries):**

```cobol
      * WS-SC -- SPLIT CARD COUNT RESERVED 1987
          05 WS-SC           PIC 99.
          05 WS-SPLT OCCURS 11 TIMES.
             10 WS-SV        PIC 99.
             10 WS-SS        PIC X.
```

These fields will be compiled into every module that does `COPY WS-HANDS` (all modules except casino-audit-log and legacy-random-gen). They allocate WORKING-STORAGE space but no PROCEDURE DIVISION statement references WS-SC, WS-SPLT, WS-SV, or WS-SS.

#### `copy/WS-GAME.cpy` — Current State

```cobol
      * GAME STATE FLAGS AND TOTALS -- SINGLE PLAYER MODE ONLY 1981
      * UPDATED 02/86 FOR MULTI-PLAYER SUPPORT -- ABANDONED
       01 WS-GM.
          05 WS-FLG-A        PIC X.
          05 WS-FLG-B        PIC X.
          05 WS-RC           PIC 9.
          05 WS-PT           PIC 999.
          05 WS-DT           PIC 999.
          05 WS-STAT         PIC 9.
      * CHIP COUNTERS -- ADDED FOR TOURNAMENT MODE 1988
          05 WS-BAL          PIC 9(4).
          05 WS-BET          PIC 9(4).
```

**Add these lines at the end of the file (still inside `01 WS-GM`):**

```cobol
      * WS-SP -- SPLIT ACTIVE FLAG. WS-INS -- INSURANCE TAKEN FLAG
          05 WS-SP           PIC X.
          05 WS-INS          PIC X.
```

These fields are included in all modules that do `COPY WS-GAME` (bjack-dealer, bjack-score, bjack-displ, bjack-main). No module's PROCEDURE DIVISION reads or writes WS-SP or WS-INS.

### Source File Changes — Orphaned Paragraphs

**Placement rule for all source files:** Append the commented-out block at the end of the file, after the last live paragraph's terminating statement (GOBACK or STOP RUN). These are comment lines, so they cannot affect control flow.

---

#### `src/bjack-main.cob` — Append After Line 132 (`STOP RUN.`)

Current end of file:
```
           STOP RUN.
```

Append:
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

---

#### `src/bjack-deal.cob` — Append After `GOBACK.` in CHECK-X (last line)

Current end of file (CHECK-X paragraph, ~line 57):
```
       CHECK-X.
           GOBACK.
```

Append:
```cobol
      *  PROC-DS -- DEAL TO SPLIT HAND. REMOVED 10/87 SPLIT NOT TESTED
      *   PROC-DS.
      *       ADD 1 TO WS-SC
      *       MOVE WS-S1(WS-CT1) TO WS-SS(WS-SC)
      *       MOVE WS-RK(WS-CT1) TO WS-SV(WS-SC)
      *       ADD 1 TO WS-CT1
      *       GO TO CALC-1.
```

Note: The architecture spec references `WS-SPLT` but PROC-DS references sub-fields. Use `WS-SS` (suit) and `WS-SV` (value) from the WS-SPLT group added in WS-HANDS.cpy.

---

#### `src/bjack-score.cob` — Append After Last Live Paragraph

Check the end of bjack-score.cob — it likely ends with a `GOBACK.` or `STOP RUN.`. Append after it:

```cobol
      *  PROC-CB -- FIVE CARD CHARLIE BONUS. NEVADA RULE. DROPPED 06/88
      *   PROC-CB.
      *       IF WS-PC = 5 AND WS-PT < 22
      *           MOVE 'Y' TO WS-STAT
      *           COMPUTE WS-BAL = WS-BAL + WS-BET * 2
      *       END-IF
      *       GO TO CHECK-X.
```

Note: WS-PC (player card count), WS-PT (player total), WS-BAL, WS-BET, WS-STAT are all valid fields in this module's COPY scope (WS-HANDS + WS-GAME).

---

#### `src/bjack-dealer.cob` — Append After Last Live Paragraph

Append after the file's terminating GOBACK:

```cobol
      *  PROC-INS -- INSURANCE OFFER WHEN DEALER SHOWS ACE. DISABLED 1988
      *   PROC-INS.
      *       IF WS-DS1(1) = 'A'
      *           DISPLAY '   INSURANCE? Y/N:'
      *           ACCEPT WS-INS
      *       END-IF
      *       GO TO LOOP-A.
```

Note: WS-DS1 is the dealer's card suit field (1-indexed). WS-INS is the ghost field added to WS-GAME.cpy. LOOP-A is an existing paragraph in bjack-dealer.cob.

---

#### `src/bjack-displ.cob` — Append After Last Live Paragraph

Append a three-paragraph block (all commented out):

```cobol
      *  CALC-8 -- DISPLAY SPLIT HAND. SEE PROC-DS. REMOVED WITH SPLIT.
      *   CALC-8.
      *       DISPLAY '   SPLIT HAND:'
      *       MOVE 1 TO WS-X1
      *       GO TO CALC-8A.
      *  CALC-8A.
      *       IF WS-X1 > WS-SC GO TO CALC-8X END-IF
      *       DISPLAY '   ' WS-SS(WS-X1) WS-SV(WS-X1)
      *       ADD 1 TO WS-X1
      *       GO TO CALC-8A.
      *  CALC-8X.
      *       GO TO CALC-3.
```

Note: CALC-3 is an existing paragraph in bjack-displ.cob (find it by reading the file). WS-X1 is a live local variable already declared in bjack-displ.cob WORKING-STORAGE.

---

#### `src/legacy-random-gen.cob` — Append After PROC-A (`GOBACK.`)

Current end of file:
```
       PROC-A.
           GOBACK.
```

Append:
```cobol
      *  PROC-R1 -- ORIGINAL LCG. REPLACED WITH FIXED VALUE PER DEFECT 0042
      *   PROC-R1.
      *       COMPUTE WS-X1 = FUNCTION MOD
      *              (WS-X1 * 1103515245 + 12345, 65536)
      *       MOVE WS-X1 TO LS-R1
      *       GOBACK.
```

Note: `legacy-random-gen.cob` has `01 WS-X1 PIC 9` and `01 LS-R1 PIC 99` in LINKAGE SECTION. The formula is a standard LCG but will overflow PIC 9 — that's authentic (the original had a bug, which is why it was replaced).

---

#### `src/casino-audit-log.cob` — Append After PROC-A (`GOBACK.`)

Current end of file:
```
       PROC-A.
           GOBACK.
```

Append:
```cobol
      *  PROC-WR -- FILE WRITE. DISABLED 1989. AUDIT FILE NOT CONFIGURED.
      *   PROC-WR.
      *       MOVE LS-A1 TO WS-X1
      *       MOVE LS-A2 TO LS-A2
      *       WRITE LS-A2
      *       GOBACK.
```

Note: `casino-audit-log.cob` has `01 LS-A1 PIC X`, `01 LS-A2 PIC X(50)`, and `01 WS-X1 PIC 9`. The `WRITE LS-A2` is intentionally wrong (WRITE requires a file-attached record, not a linkage field) — it's orphaned code with a bug in it, which is authentic.

---

### What NOT To Do

- Do NOT place orphaned paragraphs inside existing live paragraphs — all orphaned blocks go after the last live paragraph in the file
- Do NOT reference orphaned paragraph names in any PERFORM or GO TO statement
- Do NOT modify any existing PROCEDURE DIVISION logic
- Do NOT modify bjack-deck.cob — it already has a dead code paragraph (FR26) and does not need an orphaned paragraph in this story
- Do NOT add `BJACK-DECK` to the orphaned paragraph list — it has 7 modules listed, not 8
- Do NOT use accented characters in any comment text (ASCII-only terminals)
- Do NOT introduce new 77-level local variables in this story (that is Story 7.2)

### Build Verification

After all changes:

```bash
# Confirm clean build
./build.sh   # Must exit 0

# Confirm all 7 tests pass
bash test/run-tests.sh
# Expected: T31, T32, T33, T34, T61, T62, T63 all pass
```

If GnuCOBOL reports any error about the copybook additions, it likely means:
- A field name conflicts with an existing field — check WS-HANDS.cpy and WS-GAME.cpy carefully
- Indentation is wrong for the OCCURS clause — keep consistent with existing 10-level field indentation

### Existing Test Coverage

The 7 tests verify the 9 deliberate bugs — none of them test anything affected by this story:
- T31: biased shuffle (bjack-deck.cob shuffle paragraph) — unaffected
- T32: off-by-one deal (bjack-deal.cob CALC-3 paragraph) — unaffected
- T33: Ace recalculation failure (bjack-score.cob) — unaffected
- T34: soft-17 rule violation (bjack-dealer.cob) — unaffected
- T61: payout rounding on natural blackjack (bjack-main.cob) — unaffected
- T62: double-down anytime violation (bjack-main.cob) — unaffected
- T63: bet-over-balance from stale variable (bjack-main.cob) — unaffected

All existing bugs must still be active after this story.

### Project Structure Notes

- Source files: `src/` directory (8 `.cob` files)
- Copybooks: `copy/` directory (3 `.cpy` files)
- Copybooks are compiled with `-I copy/` flag, resolved at compile time
- All modules use BY REFERENCE calling convention — no interfaces change here
- `bjack-deck.cob` does NOT get an orphaned paragraph in this story — it already carries FR26 dead code

### References

- [Source: docs/planning-artifacts/epics.md — Epic 7, Story 7.1]
- [Source: docs/planning-artifacts/architecture.md — Accumulated Debt Patterns (FR47-FR52)]
- [Source: docs/planning-artifacts/sprint-change-proposal-2026-02-28.md — Section 4.3]
- [Source: docs/planning-artifacts/architecture.md — Naming Patterns, Structure Patterns, Format Patterns]
- [Source: copy/WS-HANDS.cpy — current field structure]
- [Source: copy/WS-GAME.cpy — current field structure]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- All 9 file edits applied cleanly. Copybook ghost fields compile into all modules that COPY them but are never referenced in PROCEDURE DIVISION. Orphaned comment blocks appended after last live paragraph in all 7 source files. Build clean (warnings only: _FORTIFY_SOURCE redefined — pre-existing env issue). All 7 tests pass.

### File List

- copy/WS-HANDS.cpy
- copy/WS-GAME.cpy
- src/bjack-main.cob
- src/bjack-deal.cob
- src/bjack-score.cob
- src/bjack-dealer.cob
- src/bjack-displ.cob
- src/legacy-random-gen.cob
- src/casino-audit-log.cob
