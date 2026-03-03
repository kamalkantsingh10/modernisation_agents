# Story 2.5: Dealer Module — Dealer Turn Logic

Status: review

## Story

As a developer,
I want `bjack-dealer.cob` implemented to execute the dealer's turn according to standard casino rules,
so that the dealer draws to 17 or higher and stands, enabling round outcome determination.

## Acceptance Criteria

1. **Given** WS-HANDS contains the dealer's initial two-card hand and WS-DT is set (via a preceding BJACK-SCORE call),
   **When** BJACK-DEALER is called,
   **Then** the dealer draws cards from WS-CDS until the dealer hand total reaches 17 or higher.

2. **Given** WS-DT >= 17,
   **When** BJACK-DEALER evaluates the stand condition,
   **Then** the dealer stands (does not draw another card) and GOBACK is executed.

3. **Given** a card is drawn,
   **When** WS-HANDS is inspected,
   **Then** WS-DC has incremented by 1 and WS-DHD(WS-DC) contains the drawn card (suit, rank, face value).

4. **Given** a card is drawn,
   **When** WS-DT is inspected,
   **Then** WS-DT reflects the dealer's recalculated total with correct Ace adjustment (Ace = 11 unless total > 21, then Ace = 1).

5. **Given** the module code is inspected,
   **When** code quality is evaluated,
   **Then** the module contains: GOTO-driven loop logic, cryptic WS-XX variable names, vague paragraph names, at least one wrong or outdated comment, zero return-code checks after any CALL.

6. **Given** the module code is inspected,
   **When** language constructs are evaluated,
   **Then** the module does NOT use EVALUATE/WHEN — all conditionals use nested IF trees.

## Tasks / Subtasks

- [x] Task 1: Restructure DATA DIVISION for shared data via LINKAGE SECTION (AC: #1–4)
  - [x] Remove `COPY WS-HANDS.` and `COPY WS-GAME.` from WORKING-STORAGE SECTION
  - [x] Add LINKAGE SECTION after WORKING-STORAGE SECTION
  - [x] Place `COPY WS-DECK.`, `COPY WS-HANDS.`, `COPY WS-GAME.` in LINKAGE SECTION (in that order)
  - [x] Change PROCEDURE DIVISION header to: `PROCEDURE DIVISION USING WS-DK WS-HND WS-GM.`
  - [x] Declare local 77-level items in WORKING-STORAGE: WS-X1 PIC 999, WS-CT2 PIC 99, WS-CT3 PIC 99

- [x] Task 2: Implement draw-or-stand decision (AC: #1, #2)
  - [x] INIT-1 paragraph: MOVE 0 TO WS-X1, WS-CT2, WS-CT3; GO TO PROC-A
  - [x] PROC-A paragraph: IF WS-DT >= 17 GO TO CHECK-X (stand); GO TO LOOP-A (draw)

- [x] Task 3: Implement card draw from deck (AC: #3)
  - [x] LOOP-A paragraph: ADD 1 TO WS-DC; MOVE WS-S1(WS-CT1) TO WS-DS1(WS-DC); MOVE WS-RK(WS-CT1) TO WS-DRK(WS-DC); MOVE WS-FV(WS-CT1) TO WS-DFV(WS-DC); ADD 1 TO WS-CT1; GO TO CALC-1

- [x] Task 4: Implement inline dealer scoring (AC: #4)
  - [x] CALC-1 paragraph: MOVE 0 TO WS-X1; MOVE 0 TO WS-CT3; MOVE 1 TO WS-CT2; GO TO CALC-2
  - [x] CALC-2 paragraph (sum loop): IF WS-CT2 > WS-DC GO TO CALC-3; ADD WS-DFV(WS-CT2) TO WS-X1; IF WS-DFV(WS-CT2) = 11 ADD 1 TO WS-CT3; ADD 1 TO WS-CT2; GO TO CALC-2
  - [x] CALC-3 paragraph (Ace adjustment): IF WS-X1 <= 21 GO TO CALC-4; IF WS-CT3 = 0 GO TO CALC-4; SUBTRACT 10 FROM WS-X1; SUBTRACT 1 FROM WS-CT3; GO TO CALC-3
  - [x] CALC-4 paragraph: MOVE WS-X1 TO WS-DT; GO TO PROC-A (re-check stand condition)

- [x] Task 5: Exit (AC: #2, #5)
  - [x] CHECK-X paragraph: GOBACK (NOT STOP RUN)

- [x] Task 6: Anti-pattern compliance (AC: #5, #6)
  - [x] All local WORKING-STORAGE names are cryptic (WS-X1, WS-CT2, WS-CT3)
  - [x] All paragraph names are vague (INIT-1, PROC-A, LOOP-A, CALC-1, CALC-2, CALC-3, CALC-4, CHECK-X)
  - [x] At least 1 wrong/outdated comment
  - [x] Zero return-code checks after the CALL 'LEGACY-RANDOM-GEN' in BJACK-DECK (no CALLs in this module, but rule is absolute)
  - [x] No EVALUATE/WHEN — only nested IF trees
  - [x] No SECTIONS in PROCEDURE DIVISION
  - [x] GOBACK (NOT STOP RUN)

- [x] Task 7: Compile validation
  - [x] Run `cobc -c -I copy/ src/bjack-dealer.cob` — must produce zero COBOL errors
  - [x] Ignore `_FORTIFY_SOURCE` GCC warning (expected, exit code still 0)

## Dev Notes

### CRITICAL: Shared Data Via LINKAGE SECTION

The stub has `COPY WS-HANDS.` and `COPY WS-GAME.` in WORKING-STORAGE. Both must be removed. BJACK-DEALER also needs `COPY WS-DECK.` to draw cards from the deck array using WS-CT1 (deck pointer) and WS-CDS(WS-CT1) (card data).

**Correct DATA DIVISION:**
```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 999.
           77 WS-CT2         PIC 99.
           77 WS-CT3         PIC 99.
       LINKAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-DK WS-HND WS-GM.
```

**BJACK-MAIN (Story 2.6) will call BJACK-DEALER as:**
```cobol
       CALL 'BJACK-DEALER' USING BY REFERENCE WS-DK WS-HND WS-GM
```

### CRITICAL: GOBACK Not STOP RUN

Subprogram — must use `GOBACK`. The stub has `STOP RUN` — replace it.

### CRITICAL: WS-CT1 Name Conflict Avoidance

WS-DECK.cpy defines `05 WS-CT1 PIC 99` inside the `01 WS-DK` group. When BJACK-DEALER copies WS-DECK into LINKAGE SECTION, `WS-CT1` is the deck pointer (the current position in the 52-card array). BJACK-DEALER uses WS-CT1 directly to advance the deck pointer when drawing cards.

Because WS-CT1 is already defined by the COPY, BJACK-DEALER MUST NOT declare a local `77 WS-CT1`. Instead, use:
- `WS-CT2` (local 77-level) — hand scoring loop counter (1..WS-DC)
- `WS-CT3` (local 77-level) — Ace counter for adjustment loop

There is NO naming conflict between local `77 WS-CT2`/`77 WS-CT3` and the group structure of WS-DK or WS-HND.

### Dealer Logic: Why Inline Scoring (Not a BJACK-SCORE Call)

Per architecture: "BJACK-MAIN is the sole orchestrator — modules do not call each other directly." BJACK-DEALER cannot call BJACK-SCORE to recalculate the dealer total after each draw. Instead, BJACK-DEALER performs inline hand scoring using the same algorithm as BJACK-SCORE.

After each drawn card, BJACK-DEALER:
1. Sums all WS-DFV values from 1..WS-DC into WS-X1 (local accumulator)
2. Applies Ace adjustment (subtract 10 per Ace counted as 11 until total ≤ 21 or no Aces remain)
3. Writes result to WS-DT (in WS-GM)
4. Loops back to PROC-A to check if WS-DT >= 17

This intentional code duplication is period-authentic. 1980s COBOL shops routinely duplicated logic across modules rather than calling shared subroutines.

When BJACK-MAIN calls BJACK-SCORE after BJACK-DEALER returns, BJACK-SCORE will recalculate and overwrite WS-DT. The results should match since both use the same algorithm.

### Pre-Condition: WS-DT Already Set

Before BJACK-MAIN calls BJACK-DEALER, it calls BJACK-SCORE to compute the initial dealer total. So when BJACK-DEALER's PROC-A checks `WS-DT >= 17`, the first check uses the correctly pre-computed dealer total from BJACK-SCORE. After each card draw, BJACK-DEALER's inline scoring updates WS-DT before the next check.

### Correct Dealer Stand Rule (Standard Casino Rules)

Standard casino rules (implemented correctly here; Epic 3 will introduce the bug):
- Dealer draws on 16 or less (WS-DT < 17 → draw)
- Dealer stands on 17 or more (WS-DT >= 17 → stand)
- This applies to BOTH hard 17 (e.g., 10+7=17) AND soft 17 (e.g., A+6=17 counted as 11+6)

**Epic 3 Note:** Story 3.4 (Soft 17 Rule Violation) will modify `bjack-dealer.cob` to make the dealer incorrectly handle a soft 17. Story 2.5 MUST implement the CORRECT rule. Do NOT introduce the soft 17 bug here.

### Copybook Field Names (Locked — From Story 1.1)

**WS-DECK.cpy fields used by BJACK-DEALER:**
- `WS-CT1` — deck pointer (PIC 99) inside `01 WS-DK`; used to index into WS-CDS, incremented after each draw
- `WS-CDS(n)` — card array (OCCURS 52 TIMES)
  - `WS-S1(WS-CT1)` — suit (PIC X) of card at deck position WS-CT1
  - `WS-RK(WS-CT1)` — rank (PIC XX) of card at deck position WS-CT1
  - `WS-FV(WS-CT1)` — face value (PIC 99) of card at deck position WS-CT1

**WS-HANDS.cpy fields used by BJACK-DEALER:**
- `WS-DC` — dealer card count (PIC 99) — incremented before each draw
- `WS-DHD(n)` — dealer hand array (OCCURS 11 TIMES)
  - `WS-DS1(n)` — dealer card suit (PIC X)
  - `WS-DRK(n)` — dealer card rank (PIC XX)
  - `WS-DFV(n)` — dealer card face value (PIC 99) — also used in inline scoring

**WS-GAME.cpy fields used by BJACK-DEALER:**
- `WS-DT` — dealer hand total (PIC 999) — read (for stand check) and written (inline scoring)

**Local WORKING-STORAGE (77-level):**
- `WS-X1` (PIC 999) — running total accumulator during inline scoring
- `WS-CT2` (PIC 99) — hand loop counter (1..WS-DC) during inline scoring
- `WS-CT3` (PIC 99) — Ace counter during inline scoring (tracks Aces counted as 11)

### Inline Scoring Algorithm

The inline scoring after each card draw mirrors BJACK-SCORE's dealer scoring logic exactly:

1. Reset: MOVE 0 TO WS-X1; MOVE 0 TO WS-CT3; MOVE 1 TO WS-CT2
2. Sum loop (CALC-2): for WS-CT2 from 1 to WS-DC:
   - ADD WS-DFV(WS-CT2) TO WS-X1
   - IF WS-DFV(WS-CT2) = 11: ADD 1 TO WS-CT3 (count Aces at 11)
   - ADD 1 TO WS-CT2; GOTO CALC-2
3. Ace adjustment loop (CALC-3): while WS-X1 > 21 AND WS-CT3 > 0:
   - SUBTRACT 10 FROM WS-X1; SUBTRACT 1 FROM WS-CT3; GOTO CALC-3
4. Store (CALC-4): MOVE WS-X1 TO WS-DT

**Key:** Aces are identified by face value = 11 (set by BJACK-DECK at initialization). This is the same detection method as BJACK-SCORE.

### Paragraph Structure (Full Skeleton)

```cobol
      * BJACK-DEALER -- DEALER TURN AUTOMATION
      * WRITTEN 05/84 -- UPDATED 08/89 FOR SOFT 17 RULE CHANGE
      * SOFT 17 LOGIC ADDED PER NEVADA GAMING COMMISSION
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DEALER.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 999.
           77 WS-CT2         PIC 99.
           77 WS-CT3         PIC 99.
       LINKAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-DK WS-HND WS-GM.
       INIT-1.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT2
           MOVE 0 TO WS-CT3
           GO TO PROC-A.
       PROC-A.
           IF WS-DT >= 17
               GO TO CHECK-X
           END-IF
           GO TO LOOP-A.
       LOOP-A.
           ADD 1 TO WS-DC
           MOVE WS-S1(WS-CT1)  TO WS-DS1(WS-DC)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(WS-DC)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(WS-DC)
           ADD 1 TO WS-CT1
           GO TO CALC-1.
       CALC-1.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT3
           MOVE 1 TO WS-CT2
           GO TO CALC-2.
       CALC-2.
           IF WS-CT2 > WS-DC
               GO TO CALC-3
           END-IF
           ADD WS-DFV(WS-CT2) TO WS-X1
           IF WS-DFV(WS-CT2) = 11
               ADD 1 TO WS-CT3
           END-IF
           ADD 1 TO WS-CT2
           GO TO CALC-2.
       CALC-3.
           IF WS-X1 <= 21
               GO TO CALC-4
           END-IF
           IF WS-CT3 = 0
               GO TO CALC-4
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT3
           GO TO CALC-3.
       CALC-4.
           MOVE WS-X1 TO WS-DT
           GO TO PROC-A.
       CHECK-X.
           GOBACK.
```

**Paragraph names — MUST be vague:**
- `INIT-1` not `INIT-DEALER`
- `PROC-A` not `CHECK-STAND`
- `LOOP-A` not `DRAW-CARD`
- `CALC-1` not `INIT-SCORING`
- `CALC-2` not `SUM-DEALER-CARDS`
- `CALC-3` not `ADJUST-ACES`
- `CALC-4` not `STORE-DEALER-TOTAL`
- `CHECK-X` not `DEALER-DONE`

### Wrong/Outdated Comment Requirement

The existing stub header has a period-authentic wrong comment. Expand it:

```cobol
      * BJACK-DEALER -- DEALER TURN AUTOMATION
      * WRITTEN 05/84 -- UPDATED 08/89 FOR SOFT 17 RULE CHANGE
      * SOFT 17 LOGIC ADDED PER NEVADA GAMING COMMISSION
```

"SOFT 17 LOGIC ADDED" — this module implements the standard hard-17 stand rule (no special soft 17 logic). The comment implies functionality that doesn't exist (the soft 17 violation gets added in Epic 3, but even then it's not the "Nevada Gaming Commission" rule). The comment is historically and functionally wrong. Perfect.

Add one more wrong comment inside:
```cobol
      * LOOP-A -- DRAWS FROM SHUFFLED SUBSET ONLY
```
(There is no "subset" — LOOP-A draws from the full deck in order from WS-CT1.)

### No External CALL Statements

BJACK-DEALER does not call any other module. No CALL 'BJACK-SCORE', no CALL 'LEGACY-RANDOM-GEN'. All scoring is inline. Zero CALL statements = zero return-code checks to worry about (but the rule remains absolute).

### Architecture Compliance

**MUST:**
- `COPY WS-DECK.`, `COPY WS-HANDS.`, `COPY WS-GAME.` in LINKAGE SECTION (in that order)
- `PROCEDURE DIVISION USING WS-DK WS-HND WS-GM.`
- Use `WS-CT1` (from WS-DECK LINKAGE) as the deck pointer — do NOT redeclare as local
- Local vars: WS-X1 (PIC 999), WS-CT2 (PIC 99), WS-CT3 (PIC 99) — all cryptic
- All paragraph names: vague (PROC-A, LOOP-A, CALC-1 pattern)
- At least 1 GOTO per module (abundant: loop + Ace adjustment loop)
- At least 1 wrong/outdated comment
- `GOBACK` (NOT `STOP RUN`)

**MUST NOT:**
- Declare a local `77 WS-CT1` — this conflicts with WS-DECK's WS-CT1
- EVALUATE/WHEN — use nested IF trees
- Call BJACK-SCORE or any other module (orchestrator boundary)
- Descriptive variable or paragraph names
- SECTIONS in PROCEDURE DIVISION
- STOP RUN

### Epic 3 Dependency

Story 3.4 (Soft 17 Rule Violation) will modify `bjack-dealer.cob` to introduce a bug in the dealer hit/stand decision paragraph. Story 2.5 must produce CORRECT behavior first. Do not introduce any soft 17 special case — implement the clean "stand at 17 or higher" rule. The bug will be retrofitted in Epic 3.

### GnuCOBOL Notes (Inherited from Stories 1.1, 1.2, 2.1, 2.2, 2.3)

- **Compile:** `cobc -c -I copy/ src/bjack-dealer.cob` from project root
- **`_FORTIFY_SOURCE` warning:** Expected, exit code 0, ignore
- **COPY in LINKAGE SECTION:** Valid GnuCOBOL syntax — confirmed working in all previous subprogram stories
- **Subscripting with WS-CT1:** `WS-S1(WS-CT1)` where WS-CT1 is `05 WS-CT1 PIC 99` inside the LINKAGE group — valid GnuCOBOL subscripting
- **WS-DC as subscript:** `WS-DS1(WS-DC)` where WS-DC is `05 WS-DC PIC 99` inside WS-HND LINKAGE — valid
- **OCCURS 11 TIMES boundary:** WS-DHD is declared with OCCURS 11 TIMES. Do not draw more than 11 cards (impossible in a valid 52-card game anyway — max dealer draw is ~7-8 cards)

### Project Structure Notes

- **Only file changing:** `src/bjack-dealer.cob` — complete rewrite of stub
- **Copybooks:** `copy/WS-DECK.cpy`, `copy/WS-HANDS.cpy`, `copy/WS-GAME.cpy` — read-only, do NOT modify
- **No new files** created in this story

### Downstream Dependencies

- **Story 2.6 (BJACK-MAIN):** Calls BJACK-DEALER in the dealer turn sequence. Depends on correct inline scoring writing WS-DT before GOBACK. After BJACK-DEALER returns, BJACK-MAIN calls BJACK-SCORE to get the final authoritative totals for outcome determination.
- **Story 3.4 (Epic 3):** Adds soft 17 rule violation to THIS file. Story 2.5 must be correct first.

### References

- Epics: Story 2.5 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 2.5]
- Architecture: Orchestration boundary (no module-to-module calls) → [Source: docs/planning-artifacts/architecture.md#Communication Patterns]
- Architecture: BY REFERENCE calling convention → [Source: docs/planning-artifacts/architecture.md#Inter-Module Communication]
- Architecture: Data flow sequence (step 8) → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Architecture: BJACK-DEALER COPY statements (WS-HANDS, WS-GAME) → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
  - NOTE: WS-DECK added here (not in architecture COPY list) — required for card drawing
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Story 1.1: Canonical WS-DECK field names (WS-DK, WS-CT1, WS-CDS, WS-S1, WS-RK, WS-FV) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 1.1: Canonical WS-HANDS field names (WS-DC, WS-DHD, WS-DS1, WS-DRK, WS-DFV) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 2.1: Ace face value = 11 (used for Ace detection in inline scoring) → [Source: docs/implementation-artifacts/2-1-deck-module-initialization-and-shuffle.md]
- Story 2.3: Inline scoring algorithm (same Ace adjustment logic) → [Source: docs/implementation-artifacts/2-3-scoring-module-hand-value-calculation.md#Ace Scoring Algorithm]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Rewrote `src/bjack-dealer.cob` from stub to full implementation.
- DATA DIVISION: removed COPY WS-HANDS/WS-GAME from WORKING-STORAGE; added LINKAGE SECTION with COPY WS-DECK, COPY WS-HANDS, COPY WS-GAME (in that order); added 77-level WS-X1 (PIC 999), WS-CT2 (PIC 99), WS-CT3 (PIC 99).
- WS-CT1 is NOT redeclared locally — it comes from the WS-DECK LINKAGE and serves as the deck pointer.
- PROC-A: IF WS-DT >= 17 → GO TO CHECK-X (stand); else GO TO LOOP-A (draw).
- LOOP-A: increments WS-DC, copies card at WS-CT1 into dealer hand array, increments WS-CT1.
- CALC-1/CALC-2/CALC-3/CALC-4: inline dealer scoring (sum all WS-DFV, Ace adjustment loop) → writes WS-DT, loops back to PROC-A.
- CHECK-X: GOBACK.
- Anti-patterns: 3 wrong comments ("SOFT 17 LOGIC ADDED", "NEVADA GAMING COMMISSION", "DRAWS FROM SHUFFLED SUBSET ONLY"), GOTO-driven, cryptic names, no EVALUATE, no SECTIONS, GOBACK.
- Compiled: `cobc -c -I copy/ src/bjack-dealer.cob` — exit code 0.

### File List

- src/bjack-dealer.cob (modified — full rewrite from stub)
