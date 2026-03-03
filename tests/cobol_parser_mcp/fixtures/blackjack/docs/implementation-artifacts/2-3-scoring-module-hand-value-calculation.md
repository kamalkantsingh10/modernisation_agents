# Story 2.3: Scoring Module — Hand Value Calculation

Status: review

## Story

As a developer,
I want `bjack-score.cob` implemented to calculate hand values with Ace as 1 or 11,
so that the current point total for both hands is always available for display and game logic decisions.

## Acceptance Criteria

1. **Given** WS-HANDS is populated with cards,
   **When** BJACK-SCORE is called,
   **Then** it calculates the correct point total for the player hand: Ace = 11 unless total > 21, then Ace = 1 (subtract 10 per Ace until total ≤ 21 or no Aces remain at 11).

2. **Given** WS-HANDS is populated with cards,
   **When** BJACK-SCORE is called,
   **Then** it calculates the correct point total for the dealer hand using the same Ace adjustment logic.

3. **Given** calculation is complete,
   **When** WS-GAME is inspected,
   **Then** player total is written to WS-PT and dealer total is written to WS-DT.

4. **Given** the module code is inspected,
   **When** code quality is evaluated,
   **Then** the module contains: GOTO-driven flow, cryptic WS-XX variable names, vague paragraph names (CALC-1/CHECK-X pattern), at least one wrong or outdated comment, zero return-code checks.

5. **Given** the module code is inspected,
   **When** language constructs are evaluated,
   **Then** the module does NOT use EVALUATE/WHEN — all conditionals use nested IF trees.

## Tasks / Subtasks

- [x] Task 1: Restructure DATA DIVISION for shared data via LINKAGE SECTION (AC: #1–3)
  - [x] Remove `COPY WS-HANDS.` and `COPY WS-GAME.` from WORKING-STORAGE SECTION
  - [x] Add LINKAGE SECTION after WORKING-STORAGE SECTION
  - [x] Place `COPY WS-HANDS.` and `COPY WS-GAME.` in LINKAGE SECTION (in that order)
  - [x] Change PROCEDURE DIVISION header to: `PROCEDURE DIVISION USING WS-HND WS-GM.`
  - [x] Declare local 77-level items in WORKING-STORAGE: WS-X1 PIC 999, WS-CT1 PIC 99, WS-CT2 PIC 99

- [x] Task 2: Implement player hand scoring (AC: #1, #4, #5)
  - [x] INIT-1 paragraph: MOVE 0 to locals, GOTO PROC-A
  - [x] PROC-A paragraph: MOVE 0 TO WS-X1, MOVE 0 TO WS-CT2, MOVE 1 TO WS-CT1, GOTO CALC-1
  - [x] CALC-1 paragraph (player card loop): IF WS-CT1 > WS-PC GOTO CALC-2; ADD WS-PFV(WS-CT1) TO WS-X1; IF WS-PFV(WS-CT1) = 11 ADD 1 TO WS-CT2; ADD 1 TO WS-CT1; GOTO CALC-1
  - [x] CALC-2 paragraph (player Ace adjustment): IF WS-X1 <= 21 GOTO CALC-3; IF WS-CT2 = 0 GOTO CALC-3; SUBTRACT 10 FROM WS-X1; SUBTRACT 1 FROM WS-CT2; GOTO CALC-2
  - [x] CALC-3 paragraph: MOVE WS-X1 TO WS-PT; GOTO PROC-B

- [x] Task 3: Implement dealer hand scoring (AC: #2, #3, #4, #5)
  - [x] PROC-B paragraph: MOVE 0 TO WS-X1, MOVE 0 TO WS-CT2, MOVE 1 TO WS-CT1, GOTO CALC-4
  - [x] CALC-4 paragraph (dealer card loop): IF WS-CT1 > WS-DC GOTO CALC-5; ADD WS-DFV(WS-CT1) TO WS-X1; IF WS-DFV(WS-CT1) = 11 ADD 1 TO WS-CT2; ADD 1 TO WS-CT1; GOTO CALC-4
  - [x] CALC-5 paragraph (dealer Ace adjustment): IF WS-X1 <= 21 GOTO CHECK-X; IF WS-CT2 = 0 GOTO CHECK-X; SUBTRACT 10 FROM WS-X1; SUBTRACT 1 FROM WS-CT2; GOTO CALC-5
  - [x] CHECK-X paragraph: MOVE WS-X1 TO WS-DT; GOBACK

- [x] Task 4: Anti-pattern compliance (AC: #4, #5)
  - [x] All local WORKING-STORAGE names are cryptic (WS-X1, WS-CT1, WS-CT2)
  - [x] All paragraph names are vague (INIT-1, PROC-A, CALC-1, CALC-2, CALC-3, PROC-B, CALC-4, CALC-5, CHECK-X)
  - [x] At least 1 wrong/outdated comment
  - [x] Zero return-code checks (no CALL statements in this module)
  - [x] No EVALUATE/WHEN — only nested IF trees
  - [x] No SECTIONS in PROCEDURE DIVISION

- [x] Task 5: Compile validation
  - [x] Run `cobc -c -I copy/ src/bjack-score.cob` — must produce zero COBOL errors
  - [x] Ignore `_FORTIFY_SOURCE` GCC warning (expected, exit code still 0)

## Dev Notes

### CRITICAL: Shared Data Via LINKAGE SECTION

Both `COPY WS-HANDS.` and `COPY WS-GAME.` MUST go in LINKAGE SECTION. BJACK-SCORE reads WS-PC/WS-DC (card counts), WS-PFV/WS-DFV (face values) from WS-HND, and writes WS-PT/WS-DT into WS-GM. If either COPY is in WORKING-STORAGE, BJACK-SCORE reads zeroed local copies and writes totals that BJACK-MAIN never sees.

**Correct DATA DIVISION:**
```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 999.
           77 WS-CT1         PIC 99.
           77 WS-CT2         PIC 99.
       LINKAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-HND WS-GM.
```

**BJACK-MAIN (Story 2.6) will call BJACK-SCORE as:**
```cobol
       CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
```

### CRITICAL: GOBACK Not STOP RUN

Subprogram — must use `GOBACK`. The stub has `STOP RUN` — replace it.

### Copybook Field Names (Locked — From Story 1.1)

**WS-HANDS.cpy fields read by BJACK-SCORE:**
- `WS-PC` — player card count (PIC 99) — loop upper bound for player scoring
- `WS-PFV(n)` — player face value per card (PIC 99), subscripted 1..WS-PC
- `WS-DC` — dealer card count (PIC 99) — loop upper bound for dealer scoring
- `WS-DFV(n)` — dealer face value per card (PIC 99), subscripted 1..WS-DC

**WS-GAME.cpy fields written by BJACK-SCORE:**
- `WS-PT` — player hand total (PIC 999) — written after player scoring
- `WS-DT` — dealer hand total (PIC 999) — written after dealer scoring

**Local WORKING-STORAGE (77-level):**
- `WS-X1` (PIC 999) — running total accumulator (must hold up to 4 Aces = 44 before adjustment, max value 21+ range, PIC 999 sufficient)
- `WS-CT1` (PIC 99) — card loop counter (1..WS-PC or 1..WS-DC)
- `WS-CT2` (PIC 99) — Ace counter (how many Aces are still counted as 11 in current total)

**NOTE:** WS-CT1 here is a LOCAL 77-level item in BJACK-SCORE's own WORKING-STORAGE, NOT the WS-CT1 from WS-DECK.cpy. Since BJACK-SCORE does not copy WS-DECK, there is no name conflict. This is acceptable — cryptic names intentionally create ambiguity.

### Ace Scoring Algorithm

The Ace adjustment loop is the core of this module. After summing all face values:
- If total ≤ 21: done (no adjustment needed)
- If total > 21 and Ace count > 0: subtract 10 (convert one Ace from 11 to 1), decrement Ace count, check again
- If total > 21 and Ace count = 0: total stands (hand is bust)

**Example hands:**
- A + K: sum = 11 + 10 = 21. No adjustment. WS-X1 = 21. ✓
- A + A: sum = 11 + 11 = 22 > 21, WS-CT2 = 2. Adjust: 22-10=12, WS-CT2=1. 12 ≤ 21, done. WS-X1 = 12. ✓
- A + 5 + 8: sum = 11 + 5 + 8 = 24 > 21, WS-CT2 = 1. Adjust: 24-10=14, WS-CT2=0. 14 ≤ 21, done. WS-X1 = 14. ✓
- 9 + 8 + 7: sum = 24 > 21, WS-CT2 = 0. No adjustment possible. WS-X1 = 24 (bust). ✓

**IMPORTANT:** Face values in WS-PFV and WS-DFV are set by BJACK-DEAL from WS-FV in the deck. Aces have WS-FV = 11 (set at deck initialization in Story 2.1). BJACK-SCORE detects Aces by checking if the face value = 11. This works because no non-Ace card has face value 11.

### Paragraph Structure (Full Skeleton)

```cobol
      * BJACK-SCORE -- HAND EVALUATION ROUTINE
      * WRITTEN 02/85 -- UPDATED 11/90 FOR BLACKJACK NATURAL DETECTION
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-SCORE.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 999.
           77 WS-CT1         PIC 99.
           77 WS-CT2         PIC 99.
       LINKAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-HND WS-GM.
       INIT-1.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT1
           MOVE 0 TO WS-CT2
           GO TO PROC-A.
       PROC-A.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT2
           MOVE 1 TO WS-CT1
           GO TO CALC-1.
       CALC-1.
           IF WS-CT1 > WS-PC
               GO TO CALC-2
           END-IF
           ADD WS-PFV(WS-CT1) TO WS-X1
           IF WS-PFV(WS-CT1) = 11
               ADD 1 TO WS-CT2
           END-IF
           ADD 1 TO WS-CT1
           GO TO CALC-1.
       CALC-2.
           IF WS-X1 <= 21
               GO TO CALC-3
           END-IF
           IF WS-CT2 = 0
               GO TO CALC-3
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT2
           GO TO CALC-2.
       CALC-3.
           MOVE WS-X1 TO WS-PT
           GO TO PROC-B.
       PROC-B.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT2
           MOVE 1 TO WS-CT1
           GO TO CALC-4.
       CALC-4.
           IF WS-CT1 > WS-DC
               GO TO CALC-5
           END-IF
           ADD WS-DFV(WS-CT1) TO WS-X1
           IF WS-DFV(WS-CT1) = 11
               ADD 1 TO WS-CT2
           END-IF
           ADD 1 TO WS-CT1
           GO TO CALC-4.
       CALC-5.
           IF WS-X1 <= 21
               GO TO CHECK-X
           END-IF
           IF WS-CT2 = 0
               GO TO CHECK-X
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT2
           GO TO CALC-5.
       CHECK-X.
           MOVE WS-X1 TO WS-DT
           GOBACK.
```

**Paragraph names — MUST be vague:**
- `INIT-1` not `INIT-SCORE`
- `PROC-A` not `SCORE-PLAYER`
- `CALC-1` not `SUM-PLAYER-CARDS`
- `CALC-2` not `ADJUST-PLAYER-ACES`
- `CALC-3` not `STORE-PLAYER-TOTAL`
- `PROC-B` not `SCORE-DEALER`
- `CALC-4` not `SUM-DEALER-CARDS`
- `CALC-5` not `ADJUST-DEALER-ACES`
- `CHECK-X` not `STORE-DEALER-TOTAL`

### Wrong/Outdated Comment Requirement

The existing stub header comment is already wrong — add to it:
```cobol
      * BJACK-SCORE -- HAND EVALUATION ROUTINE
      * WRITTEN 02/85 -- UPDATED 11/90 FOR BLACKJACK NATURAL DETECTION
```
"BLACKJACK NATURAL DETECTION" — there is no blackjack natural detection in this module (21 on first two cards is not specially handled here; that logic would be in BJACK-MAIN). The comment describes non-existent functionality.

Add one more inside:
```cobol
      * CALC-1 -- SUMS VALUES USING LOOKUP TABLE
```
(There is no lookup table. Pure arithmetic.)

### No CALL Statements in BJACK-SCORE

BJACK-SCORE does not call any other module. All scoring is local arithmetic. Zero CALL statements = zero return-code checks to worry about.

### Architecture Compliance

**MUST:**
- `COPY WS-HANDS.` and `COPY WS-GAME.` in LINKAGE SECTION
- `PROCEDURE DIVISION USING WS-HND WS-GM.`
- All local names: WS-XX pattern (WS-X1, WS-CT1, WS-CT2)
- All paragraph names: vague (CALC-1, PROC-A, CHECK-X pattern)
- At least 1 GOTO per module (loop structure provides many)
- At least 1 wrong/outdated comment
- `GOBACK` (NOT `STOP RUN`)

**MUST NOT:**
- EVALUATE/WHEN anywhere
- Descriptive names
- SECTIONS in PROCEDURE DIVISION
- STOP RUN

### Epic 3 Dependency — Do NOT Add the Bug Yet

Story 3.3 (Ace recalculation failure) will modify `bjack-score.cob` to introduce a bug where two-Ace hands are incorrectly scored (only the first Ace is recalculated from 11 to 1, producing 12 instead of 2). Story 2.3 must implement correct Ace adjustment — the deliberate defect is added in Epic 3. Do not introduce the bug here.

### GnuCOBOL Notes (Inherited from Stories 1.1, 1.2, 2.1, 2.2)

- **Compile:** `cobc -c -I copy/ src/bjack-score.cob` from project root
- **`_FORTIFY_SOURCE` warning:** Expected, exit code 0, ignore
- **COPY in LINKAGE SECTION:** Valid GnuCOBOL syntax
- **Subscripting:** `WS-PFV(WS-CT1)` where WS-CT1 is a 77-level PIC 99 — valid GnuCOBOL
- **PIC 999 for WS-X1:** Sufficient for all possible hand totals (max theoretical pre-adjustment: 11×11=121 for 11 Aces, but in practice with 4 suits max 4 Aces=44, plus remaining cards max ~4×10+3×9=67, total can't exceed ~120 with all face cards; PIC 999 covers 0–999)

### Project Structure Notes

- **Only file changing:** `src/bjack-score.cob` — complete rewrite
- **Copybooks:** `copy/WS-HANDS.cpy` and `copy/WS-GAME.cpy` — read-only, do NOT modify
- **No new files** created in this story

### Downstream Dependencies

- **Story 2.4 (BJACK-DISPL):** Reads WS-PT and WS-DT from WS-GM for display. Depends on correct values written here after each BJACK-SCORE call.
- **Story 2.5 (BJACK-DEALER):** Reads WS-DT to determine if dealer should draw. If scoring is wrong, dealer logic breaks.
- **Story 2.6 (BJACK-MAIN):** Reads WS-PT to check player bust (WS-PT > 21) and WS-RC outcome. BJACK-SCORE is called after every card deal and after the dealer turn.
- **Story 3.3 (Epic 3):** Adds Ace recalculation failure bug to THIS file. Story 2.3 must be correct first.

### References

- Epics: Story 2.3 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 2.3]
- Architecture: BY REFERENCE calling convention → [Source: docs/planning-artifacts/architecture.md#Inter-Module Communication]
- Architecture: BJACK-SCORE COPY statements (WS-HANDS, WS-GAME) → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
- Architecture: Naming patterns (CALC-1/CHECK-X) → [Source: docs/planning-artifacts/architecture.md#Naming Patterns]
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Architecture: Data flow sequence (steps 4, 7) → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Story 1.1: Canonical WS-GAME field names (WS-PT, WS-DT, WS-STAT, WS-RC) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 1.1: Canonical WS-HANDS field names (WS-PC, WS-PFV, WS-DC, WS-DFV) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 2.1: Ace face value = 11 set at deck initialization → [Source: docs/implementation-artifacts/2-1-deck-module-initialization-and-shuffle.md#Deck Initialization — Full Card Table]
- Story 2.2: LINKAGE SECTION pattern (same applies here) → [Source: docs/implementation-artifacts/2-2-deal-module-initial-hand-distribution.md#CRITICAL: Shared Data Via LINKAGE SECTION]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Rewrote `src/bjack-score.cob`: COPY WS-HANDS and WS-GAME moved to LINKAGE SECTION; PROCEDURE DIVISION USING WS-HND WS-GM; local 77-level vars WS-X1 (PIC 999), WS-CT1 (PIC 99), WS-CT2 (PIC 99) in WORKING-STORAGE. Note: WS-CT1 here is local — no conflict with WS-DECK's WS-CT1 since WS-DECK is not copied in this module.
- Player scoring: PROC-A resets accumulators → CALC-1 sums WS-PFV(1..WS-PC) into WS-X1, counts Aces (FV=11) in WS-CT2 → CALC-2 Ace adjustment loop (subtract 10 per Ace while total > 21 and Aces remain) → CALC-3 writes WS-X1 to WS-PT.
- Dealer scoring: PROC-B resets accumulators → CALC-4/CALC-5 mirrors player logic using WS-DC/WS-DFV → CHECK-X writes WS-X1 to WS-DT; GOBACK.
- Ace logic verified: A+K=21 (no adjust), A+A=12 (one adjust), A+5+8=14 (one adjust), 9+8+7=24 (bust, no Aces).
- Anti-patterns: 11 GOTOs, 0 EVALUATE, 0 STOP RUN, 0 return-code checks, 0 PROCEDURE SECTIONs, 2 wrong comments.
- Full build: `bash build.sh` exit 0 ✓

### File List

- src/bjack-score.cob
