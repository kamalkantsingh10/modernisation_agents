# Story 2.4: Display Module — Terminal Rendering

Status: review

## Story

As a developer,
I want `bjack-displ.cob` implemented to render the full game state in an 80-column terminal,
so that Kamal sees an authentic 1980s-era mainframe display showing both hands, card values, and round outcomes.

## Acceptance Criteria

1. **Given** WS-HANDS is populated with cards,
   **When** BJACK-DISPL is called with WS-STAT = 0,
   **Then** both player and dealer hands are displayed simultaneously, each card shown as RANK(SUIT) (e.g. `A (H)`, `10(S)`, `K (D)`).

2. **Given** BJACK-SCORE has been called and written totals to WS-GM,
   **When** BJACK-DISPL is called,
   **Then** current hand values for both player (WS-PT) and dealer (WS-DT) are displayed.

3. **Given** WS-STAT = 1 and WS-RC is set in WS-GM,
   **When** BJACK-DISPL is called,
   **Then** round outcome messages are displayed: WS-RC=1 → "PLAYER WINS", WS-RC=2 → "DEALER WINS", WS-RC=3 → "PUSH -- TIE GAME".

4. **Given** the module code is inspected,
   **When** code quality is evaluated,
   **Then** the module contains: GOTO-driven rendering logic, cryptic WS-XX variable names, hardcoded column positions using leading spaces, at least one wrong or outdated comment, zero return-code checks.

5. **Given** the module code is inspected,
   **When** language constructs are evaluated,
   **Then** the module does NOT use EVALUATE/WHEN — all conditionals use nested IF trees.

6. **Given** WS-STAT = 0,
   **When** BJACK-DISPL returns,
   **Then** no outcome message is displayed (mid-game display only).

## Tasks / Subtasks

- [x] Task 1: Restructure DATA DIVISION for shared data via LINKAGE SECTION (AC: #1–3)
  - [x] Remove `COPY WS-HANDS.` and `COPY WS-DECK.` from WORKING-STORAGE SECTION
  - [x] Add LINKAGE SECTION after WORKING-STORAGE SECTION
  - [x] Place `COPY WS-HANDS.` and `COPY WS-GAME.` in LINKAGE SECTION (in that order)
  - [x] Change PROCEDURE DIVISION header to: `PROCEDURE DIVISION USING WS-HND WS-GM.`
  - [x] Declare local 77-level items in WORKING-STORAGE: WS-CT1 PIC 99, WS-X1 PIC 9
  - NOTE: Story 2-7 subsequently added WS-ESC PIC X, WS-BF1 PIC X(80), WS-POS PIC 99, WS-SYM PIC X(3) — current file has 6 WORKING-STORAGE vars total

- [x] Task 2: Implement header/display entry (AC: #4, #5)
  - [x] INIT-1 paragraph: MOVE 0 TO WS-CT1, MOVE 0 TO WS-X1, GO TO PROC-A
  - [x] PROC-A paragraph: DISPLAY header lines (separator + title + separator), GO TO CALC-1

- [x] Task 3: Implement dealer hand display loop (AC: #1, #2)
  - [x] CALC-1 paragraph: DISPLAY "   DEALER HAND:", MOVE 1 TO WS-CT1, GO TO LOOP-A
  - [x] LOOP-A paragraph: IF WS-CT1 > WS-DC GO TO CALC-2; DISPLAY card (WS-DRK + WS-DS1); ADD 1 TO WS-CT1; GO TO LOOP-A
  - [x] CALC-2 paragraph: DISPLAY dealer total (WS-DT from WS-GM), DISPLAY blank line, GO TO PROC-B

- [x] Task 4: Implement player hand display loop (AC: #1, #2)
  - [x] PROC-B paragraph: DISPLAY "   PLAYER HAND:", MOVE 1 TO WS-CT1, GO TO CALC-3
  - [x] CALC-3 paragraph: IF WS-CT1 > WS-PC GO TO CALC-4; DISPLAY card (WS-PRK + WS-PS1); ADD 1 TO WS-CT1; GO TO CALC-3
  - [x] CALC-4 paragraph: DISPLAY player total (WS-PT from WS-GM), DISPLAY blank line, GO TO CHECK-X

- [x] Task 5: Implement outcome display (AC: #3, #6)
  - [x] CHECK-X paragraph: IF WS-STAT = 0 GOBACK; GO TO CHECK-Y
  - [x] CHECK-Y paragraph: nested IF on WS-RC (1=player wins, 2=dealer wins, 3=push), DISPLAY outcome message, GOBACK

- [x] Task 6: Anti-pattern compliance (AC: #4, #5)
  - [x] All local WORKING-STORAGE names are cryptic (WS-CT1, WS-X1)
  - [x] All paragraph names are vague (INIT-1, PROC-A, CALC-1, LOOP-A, CALC-2, PROC-B, CALC-3, CALC-4, CHECK-X, CHECK-Y)
  - [x] At least 1 wrong/outdated comment
  - [x] Zero return-code checks (no CALL statements in this module)
  - [x] No EVALUATE/WHEN — only nested IF trees
  - [x] No SECTIONS in PROCEDURE DIVISION
  - [x] GOBACK (NOT STOP RUN)

- [x] Task 7: Compile validation
  - [x] Run `cobc -c -I copy/ src/bjack-displ.cob` — must produce zero COBOL errors
  - [x] Ignore `_FORTIFY_SOURCE` GCC warning (expected, exit code still 0)

## Dev Notes

### CRITICAL: Shared Data Via LINKAGE SECTION

The stub has `COPY WS-HANDS.` and `COPY WS-DECK.` in WORKING-STORAGE. Both must be removed. Replace with a LINKAGE SECTION containing `COPY WS-HANDS.` and `COPY WS-GAME.` — BJACK-DISPL does NOT need WS-DECK (card suit and rank are already in WS-HANDS as WS-PS1/WS-PRK and WS-DS1/WS-DRK). WS-GAME is needed for WS-PT, WS-DT, WS-RC, and WS-STAT.

**Correct DATA DIVISION:**
```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-CT1         PIC 99.
           77 WS-X1          PIC 9.
       LINKAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-HND WS-GM.
```

**BJACK-MAIN (Story 2.6) will call BJACK-DISPL as:**
```cobol
       CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
```

### CRITICAL: GOBACK Not STOP RUN

Subprogram — must use `GOBACK`. The stub has `STOP RUN` — replace it.

### WS-STAT and WS-RC Semantics (Shared Contract With Story 2.6)

These values are set by BJACK-MAIN and read by BJACK-DISPL. Both must agree on encoding:

**WS-STAT (PIC 9 in WS-GAME):**
- `0` — mid-game display: show hands and totals only, no outcome message
- `1` — end-of-round display: show hands, totals, AND outcome message based on WS-RC

**WS-RC (PIC 9 in WS-GAME):**
- `1` — player wins
- `2` — dealer wins
- `3` — push (tie)

BJACK-MAIN is responsible for setting these before calling BJACK-DISPL. BJACK-DISPL reads them as-is. Do NOT compute outcomes in this module.

### Copybook Field Names (Locked — From Story 1.1)

**WS-HANDS.cpy fields read by BJACK-DISPL:**
- `WS-DC` — dealer card count (PIC 99) — dealer loop upper bound
- `WS-DHD(n)` — dealer hand array (OCCURS 11 TIMES)
  - `WS-DS1(n)` — dealer card suit (PIC X): `H`, `D`, `C`, or `S`
  - `WS-DRK(n)` — dealer card rank (PIC XX): `A `, `2 `, ..., `10`, `J `, `Q `, `K `
  - `WS-DFV(n)` — dealer face value (PIC 99) — NOT used for display in this module
- `WS-PC` — player card count (PIC 99) — player loop upper bound
- `WS-PHD(n)` — player hand array (OCCURS 11 TIMES)
  - `WS-PS1(n)` — player card suit (PIC X)
  - `WS-PRK(n)` — player card rank (PIC XX)
  - `WS-PFV(n)` — player face value (PIC 99) — NOT used for display in this module

**WS-GAME.cpy fields read by BJACK-DISPL:**
- `WS-PT` — player hand total (PIC 999) — displayed as player total
- `WS-DT` — dealer hand total (PIC 999) — displayed as dealer total
- `WS-RC` — round outcome code (PIC 9) — used in CHECK-Y
- `WS-STAT` — display mode flag (PIC 9) — 0=mid-game, 1=end-game

**Local WORKING-STORAGE (77-level):**
- `WS-CT1` (PIC 99) — card loop counter (1..WS-DC or 1..WS-PC); no WS-DECK is copied so no name collision with deck's WS-CT1
- `WS-X1` (PIC 9) — unused but required for anti-pattern authenticity (dead/unused variable)

### Card Display Format

Each card is displayed as RANK(SUIT). The rank field WS-DRK / WS-PRK is PIC XX, so single-character ranks will have a trailing space (e.g., `A ` → displays as `A (H)`). This is authentic period output — no trimming:

```
     A (H)
     10(S)
     K (D)
```

Each card is on its own line with `"     "` (5 spaces) leading indent. This fits comfortably within 80 columns.

**Display format for a full game state (WS-STAT=0):**
```
   ==============================
   BLACKJACK -- CASINO SYSTEM
   ==============================
   DEALER HAND:
     Q (H)
     7 (D)
   DEALER TOTAL: 017

   PLAYER HAND:
     A (S)
     K (C)
   PLAYER TOTAL: 021

```

**Display format with outcome (WS-STAT=1):**
```
   (above, then:)
   *** PLAYER WINS ***
```

Note: WS-DT and WS-PT are PIC 999, so they display as 3-digit zero-padded numbers (e.g., `017`, `021`). This is period-authentic — no picture editing needed.

### Paragraph Structure (Full Skeleton)

```cobol
      * BJACK-DISPL -- TERMINAL DISPLAY HANDLER
      * WRITTEN 07/84 -- UPDATED 01/88 FOR VT100 TERMINAL SUPPORT
      * HANDLES SCREEN REFRESH AND CURSOR POSITIONING
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DISPL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-CT1         PIC 99.
           77 WS-X1          PIC 9.
       LINKAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-HND WS-GM.
       INIT-1.
           MOVE 0 TO WS-CT1
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           DISPLAY "   =============================="
           DISPLAY "   BLACKJACK -- CASINO SYSTEM    "
           DISPLAY "   =============================="
           GO TO CALC-1.
       CALC-1.
           DISPLAY "   DEALER HAND:"
           MOVE 1 TO WS-CT1
           GO TO LOOP-A.
       LOOP-A.
           IF WS-CT1 > WS-DC
               GO TO CALC-2
           END-IF
           DISPLAY "     " WS-DRK(WS-CT1) "(" WS-DS1(WS-CT1) ")"
           ADD 1 TO WS-CT1
           GO TO LOOP-A.
       CALC-2.
           DISPLAY "   DEALER TOTAL: " WS-DT
           DISPLAY " "
           GO TO PROC-B.
       PROC-B.
           DISPLAY "   PLAYER HAND:"
           MOVE 1 TO WS-CT1
           GO TO CALC-3.
       CALC-3.
           IF WS-CT1 > WS-PC
               GO TO CALC-4
           END-IF
           DISPLAY "     " WS-PRK(WS-CT1) "(" WS-PS1(WS-CT1) ")"
           ADD 1 TO WS-CT1
           GO TO CALC-3.
       CALC-4.
           DISPLAY "   PLAYER TOTAL: " WS-PT
           DISPLAY " "
           GO TO CHECK-X.
       CHECK-X.
           IF WS-STAT = 0
               GOBACK
           END-IF
           GO TO CHECK-Y.
       CHECK-Y.
           IF WS-RC = 1
               DISPLAY "   *** PLAYER WINS ***"
           END-IF
           IF WS-RC = 2
               DISPLAY "   *** DEALER WINS ***"
           END-IF
           IF WS-RC = 3
               DISPLAY "   *** PUSH -- TIE GAME ***"
           END-IF
           GOBACK.
```

**Paragraph names — MUST be vague:**
- `INIT-1` not `INIT-DISPLAY`
- `PROC-A` not `DISPLAY-HEADER`
- `CALC-1` not `START-DEALER-DISPLAY`
- `LOOP-A` not `DEALER-CARD-LOOP`
- `CALC-2` not `DISPLAY-DEALER-TOTAL`
- `PROC-B` not `START-PLAYER-DISPLAY`
- `CALC-3` not `PLAYER-CARD-LOOP`
- `CALC-4` not `DISPLAY-PLAYER-TOTAL`
- `CHECK-X` not `CHECK-GAME-OVER`
- `CHECK-Y` not `DISPLAY-OUTCOME`

### Wrong/Outdated Comment Requirement

The stub header already has a period-authentic wrong comment. Keep it and add one more inside:

```cobol
      * BJACK-DISPL -- TERMINAL DISPLAY HANDLER
      * WRITTEN 07/84 -- UPDATED 01/88 FOR VT100 TERMINAL SUPPORT
      * HANDLES SCREEN REFRESH AND CURSOR POSITIONING
```

"VT100 TERMINAL SUPPORT" — this module uses plain COBOL DISPLAY statements, not VT100 escape sequences. The comment is false.

"HANDLES SCREEN REFRESH AND CURSOR POSITIONING" — no cursor positioning occurs. Another false claim.

Add one more wrong comment inside:
```cobol
      * CALC-1 -- DEALER DISPLAY WITH HOLE CARD MASKING
```
(There is no hole card masking — both dealer cards are shown.)

### No CALL Statements in BJACK-DISPL

BJACK-DISPL is pure output — DISPLAY statements only. No CALL to any module. Zero return-code checks needed (no CALLs), but the zero-return-code-checks rule still applies architecturally.

### GnuCOBOL Notes (Inherited from Stories 1.1, 1.2, 2.1, 2.2, 2.3)

- **Compile:** `cobc -c -I copy/ src/bjack-displ.cob` from project root
- **`_FORTIFY_SOURCE` warning:** Expected, exit code 0, ignore
- **COPY in LINKAGE SECTION:** Valid GnuCOBOL syntax — confirmed working in previous stories
- **Subscripting in DISPLAY:** `DISPLAY WS-DRK(WS-CT1) "(" WS-DS1(WS-CT1) ")"` is valid GnuCOBOL
- **PIC 999 display:** WS-PT and WS-DT display as zero-padded 3-digit numbers (e.g., `017`) — period-authentic, no PICTURE editing needed
- **WS-CT1 local vs deck:** WS-DECK.cpy defines `05 WS-CT1` inside `01 WS-DK`. Since BJACK-DISPL does NOT COPY WS-DECK, there is no WS-CT1 in the LINKAGE — local `77 WS-CT1` has no naming conflict

### Architecture Compliance

**MUST:**
- `COPY WS-HANDS.` and `COPY WS-GAME.` in LINKAGE SECTION (NOT WS-DECK)
- `PROCEDURE DIVISION USING WS-HND WS-GM.`
- All local WORKING-STORAGE names: WS-XX pattern (WS-CT1, WS-X1)
- All paragraph names: vague (CALC-1, LOOP-A, CHECK-X pattern)
- At least 1 GOTO per module (abundant: GOTO-driven loops and branches)
- At least 1 wrong/outdated comment
- `GOBACK` (NOT `STOP RUN`)
- Zero return-code checks (no CALLs, but rule is absolute)

**MUST NOT:**
- EVALUATE/WHEN anywhere
- Descriptive variable or paragraph names
- SECTIONS in PROCEDURE DIVISION
- STOP RUN
- Call other modules (BJACK-DISPL is a display leaf — no sub-calls)

### Project Structure Notes

- **Only file changing:** `src/bjack-displ.cob` — complete rewrite of stub
- **Copybooks:** `copy/WS-HANDS.cpy` and `copy/WS-GAME.cpy` — read-only, do NOT modify
- **No new files** created in this story

### Downstream Dependencies

- **Story 2.5 (BJACK-DEALER):** No direct dependency on BJACK-DISPL.
- **Story 2.6 (BJACK-MAIN):** Calls `CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM`. Story 2.6 is responsible for setting WS-STAT and WS-RC correctly before each BJACK-DISPL call. BJACK-DISPL must be implemented and compilable before Story 2.6 can do a full build test.

### References

- Epics: Story 2.4 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 2.4]
- Architecture: BJACK-DISPL design (dedicated display module) → [Source: docs/planning-artifacts/architecture.md#Terminal Display Architecture]
- Architecture: BJACK-DISPL COPY statements (WS-HANDS, WS-DECK) → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
  - NOTE: WS-GAME is added here (not in architecture COPY list) because WS-PT, WS-DT, WS-RC, WS-STAT are needed for display
- Architecture: Display format patterns (hardcoded spaces, no dynamic columns) → [Source: docs/planning-artifacts/architecture.md#Format Patterns]
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Architecture: I/O boundary (all DISPLAY in BJACK-DISPL) → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- Architecture: Data flow sequence (steps 5, 9) → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Story 1.1: Canonical WS-HANDS field names → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 1.1: Canonical WS-GAME field names (WS-PT, WS-DT, WS-RC, WS-STAT) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 2.3: LINKAGE SECTION pattern → [Source: docs/implementation-artifacts/2-3-scoring-module-hand-value-calculation.md#CRITICAL: Shared Data Via LINKAGE SECTION]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Rewrote `src/bjack-displ.cob` from stub to initial 10-paragraph implementation.
- DATA DIVISION: removed COPY WS-HANDS/WS-DECK from WORKING-STORAGE; added LINKAGE SECTION with COPY WS-HANDS and COPY WS-GAME; added 77-level WS-CT1 (PIC 99) and WS-X1 (PIC 9) locally.
- PROCEDURE DIVISION: 10 paragraphs (INIT-1, PROC-A, CALC-1, LOOP-A, CALC-2, PROC-B, CALC-3, CALC-4, CHECK-X, CHECK-Y) — all vague names, all GOTO-driven.
- Dealer loop (LOOP-A): iterates WS-CT1 1..WS-DC displaying WS-DRK(n)(WS-DS1(n)).
- Player loop (CALC-3): iterates WS-CT1 1..WS-PC displaying WS-PRK(n)(WS-PS1(n)).
- CHECK-X: GOBACK on WS-STAT=0 (mid-game, no outcome).
- CHECK-Y: nested IF on WS-RC (1=PLAYER WINS, 2=DEALER WINS, 3=PUSH -- TIE GAME).
- Anti-patterns: 3 wrong comments, GOTO throughout, WS-XX names, no EVALUATE, no SECTIONS, GOBACK not STOP RUN, zero return-code checks.
- Compiled: `cobc -c -I copy/ src/bjack-displ.cob` — exit code 0, only expected _FORTIFY_SOURCE warning.
- **SUPERSEDED:** `src/bjack-displ.cob` was fully rewritten by Story 2-7 (visual upgrade). The current file contains 24 paragraphs and 6 WORKING-STORAGE variables (WS-CT1, WS-X1, WS-ESC, WS-BF1, WS-POS, WS-SYM) with ANSI escape codes, Unicode suit symbols, and ASCII card-box rendering. The above notes describe the Story 2-4 implementation only — see Story 2-7 Dev Agent Record for the current state of this file.

### File List

- src/bjack-displ.cob (modified — full rewrite from stub)
