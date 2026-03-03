# Story 2.2: Deal Module — Initial Hand Distribution

Status: review

## Story

As a developer,
I want `bjack-deal.cob` implemented to distribute cards from the deck into player and dealer hands,
so that a two-card starting hand is dealt to both player and dealer at the start of each round and additional cards can be dealt on a hit.

## Acceptance Criteria

1. **Given** WS-DECK is populated and shuffled (Story 2.1), WS-HANDS copybook is in place,
   **When** BJACK-DEAL is called for the initial deal (WS-PC = 0, WS-DC = 0),
   **Then** the player receives exactly 2 cards drawn sequentially from WS-CDS using WS-CT1 as the pointer.

2. **Given** WS-DECK is populated and shuffled,
   **When** BJACK-DEAL is called for the initial deal,
   **Then** the dealer receives exactly 2 cards drawn sequentially from WS-CDS.

3. **Given** cards are dealt,
   **When** WS-HANDS is inspected,
   **Then** WS-PC = 2 (player card count) and WS-DC = 2 (dealer card count), and WS-CT1 has advanced by 4.

4. **Given** the player has cards in hand (WS-PC > 0),
   **When** BJACK-DEAL is called for a hit,
   **Then** one additional card is drawn from WS-CDS(WS-CT1) and added to WS-PHD(WS-PC+1); WS-PC increments by 1; WS-CT1 advances by 1.

5. **Given** the module code is inspected,
   **When** code quality is evaluated,
   **Then** the module contains: GOTO-driven flow, cryptic WS-XX variable names, vague paragraph names, at least one wrong or outdated comment, zero return-code checks.

6. **Given** the module code is inspected,
   **When** language constructs are evaluated,
   **Then** the module does NOT use EVALUATE/WHEN — all conditionals use nested IF trees.

## Tasks / Subtasks

- [x] Task 1: Restructure DATA DIVISION for shared data via LINKAGE SECTION (AC: #1–4)
  - [x] Remove `COPY WS-DECK.` and `COPY WS-HANDS.` from WORKING-STORAGE SECTION
  - [x] Add LINKAGE SECTION after WORKING-STORAGE SECTION
  - [x] Place `COPY WS-DECK.` and `COPY WS-HANDS.` in LINKAGE SECTION (in that order)
  - [x] Change PROCEDURE DIVISION header to: `PROCEDURE DIVISION USING WS-DK WS-HND.`
  - [x] Declare local 77-level items in WORKING-STORAGE: WS-X1 PIC 9

- [x] Task 2: Implement deal mode detection and routing (AC: #1, #4)
  - [x] INIT-1 paragraph: entry point, GOTO PROC-A
  - [x] PROC-A paragraph: check WS-PC — IF WS-PC = 0 GOTO CALC-1 (initial deal) ELSE GOTO CALC-3 (hit)

- [x] Task 3: Implement initial deal (AC: #1, #2, #3)
  - [x] CALC-1 paragraph (deal player card 1): copy WS-CDS(WS-CT1) fields into WS-PHD(1); ADD 1 TO WS-CT1; GOTO CALC-2
  - [x] CALC-2 paragraph (deal player card 2): copy WS-CDS(WS-CT1) fields into WS-PHD(2); MOVE 2 TO WS-PC; ADD 1 TO WS-CT1; GOTO CALC-4
  - [x] CALC-4 paragraph (deal dealer card 1): copy WS-CDS(WS-CT1) fields into WS-DHD(1); ADD 1 TO WS-CT1; GOTO CALC-5
  - [x] CALC-5 paragraph (deal dealer card 2): copy WS-CDS(WS-CT1) fields into WS-DHD(2); MOVE 2 TO WS-DC; ADD 1 TO WS-CT1; GOTO CHECK-X
  - [x] Card copy = 3 MOVE statements: WS-S1(WS-CT1) to WS-PSx / WS-RK(WS-CT1) to WS-PRK / WS-FV(WS-CT1) to WS-PFV (see field names below)

- [x] Task 4: Implement hit (deal one card to player) (AC: #4)
  - [x] CALC-3 paragraph: ADD 1 TO WS-PC; copy WS-CDS(WS-CT1) fields into WS-PHD(WS-PC) using player hand fields; ADD 1 TO WS-CT1; GOTO CHECK-X

- [x] Task 5: Exit (AC: #5)
  - [x] CHECK-X paragraph: GOBACK (NOT STOP RUN)

- [x] Task 6: Anti-pattern compliance (AC: #5, #6)
  - [x] All local WORKING-STORAGE names are cryptic (WS-X1 only local needed)
  - [x] All paragraph names are vague (INIT-1, PROC-A, CALC-1, CALC-2, CALC-3, CALC-4, CALC-5, CHECK-X)
  - [x] At least 1 wrong/outdated comment
  - [x] Zero return-code checks (no CALL statements in this module anyway)
  - [x] No EVALUATE/WHEN — only nested IF trees
  - [x] No SECTIONS in PROCEDURE DIVISION

- [x] Task 7: Compile validation
  - [x] Run `cobc -c -I copy/ src/bjack-deal.cob` — must produce zero COBOL errors
  - [x] Ignore `_FORTIFY_SOURCE` GCC warning (expected, exit code still 0)

## Dev Notes

### CRITICAL: Shared Data Via LINKAGE SECTION (Same Pattern as BJACK-DECK)

Both `COPY WS-DECK.` and `COPY WS-HANDS.` MUST go in LINKAGE SECTION. BJACK-DEAL must modify BJACK-MAIN's WS-DK and WS-HND directly via BY REFERENCE. If either COPY is in WORKING-STORAGE, the deal operates on local copies — BJACK-MAIN sees no changes.

**Correct DATA DIVISION:**
```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 9.
       LINKAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
       PROCEDURE DIVISION USING WS-DK WS-HND.
```

**BJACK-MAIN (Story 2.6) will call BJACK-DEAL as:**
```cobol
       CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
```

### CRITICAL: GOBACK Not STOP RUN

BJACK-DEAL is a subprogram. Exit with `GOBACK`. `STOP RUN` terminates the entire run unit. The stub has `STOP RUN` — replace it.

### Deal Mode Detection: Initial vs Hit

BJACK-DEAL cannot use a separate parameter for mode — it only receives WS-DK and WS-HND. Mode is detected from WS-PC (player card count from WS-HND):

- **Initial deal:** BJACK-MAIN resets WS-PC = 0 and WS-DC = 0 before calling. BJACK-DEAL sees WS-PC = 0 → deals 2 cards to player, 2 cards to dealer.
- **Hit:** BJACK-MAIN calls after the initial deal when WS-PC > 0 → BJACK-DEAL deals 1 additional card to player only.

**BJACK-MAIN responsibility (Story 2.6 forward reference):** Before the initial deal call each round, BJACK-MAIN must `MOVE 0 TO WS-PC` and `MOVE 0 TO WS-DC` to reset the hand counts. Otherwise BJACK-DEAL cannot distinguish initial deal from hit.

### Copybook Field Names (Locked — From Story 1.1)

**WS-DECK.cpy fields used by BJACK-DEAL:**
- `WS-CT1` — deck pointer (PIC 99), read and incremented here
- `WS-CDS(n)` — card array (OCCURS 52 TIMES), subscripted by WS-CT1
  - `WS-S1(WS-CT1)` — suit (PIC X)
  - `WS-RK(WS-CT1)` — rank (PIC XX)
  - `WS-FV(WS-CT1)` — face value (PIC 99)

**WS-HANDS.cpy fields used by BJACK-DEAL:**
- `WS-PC` — player card count (PIC 99), updated here
- `WS-PHD(n)` — player hand array (OCCURS 11 TIMES), subscripted by card position
  - `WS-PS1(n)` — player card suit (PIC X)
  - `WS-PRK(n)` — player card rank (PIC XX)
  - `WS-PFV(n)` — player card face value (PIC 99)
- `WS-DC` — dealer card count (PIC 99), updated here
- `WS-DHD(n)` — dealer hand array (OCCURS 11 TIMES)
  - `WS-DS1(n)` — dealer card suit (PIC X)
  - `WS-DRK(n)` — dealer card rank (PIC XX)
  - `WS-DFV(n)` — dealer card face value (PIC 99)

### Card Copy Pattern (3 MOVE Statements)

Dealing a card from deck position WS-CT1 into player hand position WS-PC:
```cobol
       MOVE WS-S1(WS-CT1)  TO WS-PS1(WS-PC)
       MOVE WS-RK(WS-CT1)  TO WS-PRK(WS-PC)
       MOVE WS-FV(WS-CT1)  TO WS-PFV(WS-PC)
```

Dealing into dealer hand position WS-DC:
```cobol
       MOVE WS-S1(WS-CT1)  TO WS-DS1(WS-DC)
       MOVE WS-RK(WS-CT1)  TO WS-DRK(WS-DC)
       MOVE WS-FV(WS-CT1)  TO WS-DFV(WS-DC)
```

**NOTE:** For the initial deal paragraphs, the hand position is hardcoded (1 or 2) rather than using WS-PC as a subscript, since WS-PC is set after the copy. Example for first player card (CALC-1):
```cobol
       MOVE WS-S1(WS-CT1)  TO WS-PS1(1)
       MOVE WS-RK(WS-CT1)  TO WS-PRK(1)
       MOVE WS-FV(WS-CT1)  TO WS-PFV(1)
       ADD 1 TO WS-CT1
```
Then in CALC-2 (second player card), hardcode index 2. For hit (CALC-3): ADD 1 TO WS-PC first, then use WS-PC as the subscript.

### Paragraph Structure (Full Skeleton)

```cobol
      * BJACK-DEAL -- CARD DISTRIBUTION MODULE
      * WRITTEN 04/84 -- UPDATED 08/88 FOR MULTI-DECK SUPPORT
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DEAL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 9.
       LINKAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
       PROCEDURE DIVISION USING WS-DK WS-HND.
       INIT-1.
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           IF WS-PC = 0
               GO TO CALC-1
           END-IF
           GO TO CALC-3.
       CALC-1.
           MOVE WS-S1(WS-CT1)  TO WS-PS1(1)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(1)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(1)
           ADD 1 TO WS-CT1
           GO TO CALC-2.
       CALC-2.
           MOVE WS-S1(WS-CT1)  TO WS-PS1(2)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(2)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(2)
           MOVE 2 TO WS-PC
           ADD 1 TO WS-CT1
           GO TO CALC-4.
       CALC-3.
           ADD 1 TO WS-PC
           MOVE WS-S1(WS-CT1)  TO WS-PS1(WS-PC)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(WS-PC)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(WS-PC)
           ADD 1 TO WS-CT1
           GO TO CHECK-X.
       CALC-4.
           MOVE WS-S1(WS-CT1)  TO WS-DS1(1)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(1)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(1)
           ADD 1 TO WS-CT1
           GO TO CALC-5.
       CALC-5.
           MOVE WS-S1(WS-CT1)  TO WS-DS1(2)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(2)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(2)
           MOVE 2 TO WS-DC
           ADD 1 TO WS-CT1
           GO TO CHECK-X.
       CHECK-X.
           GOBACK.
```

**Paragraph names — MUST be vague:**
- `INIT-1` not `INIT-DEAL`
- `PROC-A` not `CHECK-DEAL-TYPE`
- `CALC-1` not `DEAL-PLAYER-CARD-1`
- `CALC-2` not `DEAL-PLAYER-CARD-2`
- `CALC-3` not `HIT-PLAYER`
- `CALC-4` not `DEAL-DEALER-CARD-1`
- `CALC-5` not `DEAL-DEALER-CARD-2`
- `CHECK-X` not `EXIT-DEAL`

### Wrong/Outdated Comment Requirement

Keep the intentionally wrong header comment pattern. Example:
```cobol
      * BJACK-DEAL -- CARD DISTRIBUTION MODULE
      * WRITTEN 04/84 -- UPDATED 08/88 FOR MULTI-DECK SUPPORT
```
"MULTI-DECK SUPPORT" — there is no multi-deck support. The comment is false. Exactly right.

Add one more wrong comment inside, e.g.:
```cobol
      * HANDLES SPLIT HANDS PER CASINO RULES
```
(There is no split hand logic. The comment describes functionality that was never implemented.)

### No CALL Statements in BJACK-DEAL

BJACK-DEAL does not call any other module. No `CALL 'LEGACY-RANDOM-GEN'` here — that is BJACK-DECK's concern. No return-code checks needed (no CALLs), but the zero-return-code-checks rule is still enforced architecturally.

### Architecture Compliance (From architecture.md Enforcement Guidelines)

**MUST:**
- `COPY WS-DECK.` and `COPY WS-HANDS.` in LINKAGE SECTION
- `PROCEDURE DIVISION USING WS-DK WS-HND.`
- All local WORKING-STORAGE names: WS-XX pattern
- All paragraph names: vague (PROC-A, CALC-1 pattern)
- At least 1 GOTO per module (loop/branch structure provides many)
- At least 1 wrong/outdated comment
- Exit with `GOBACK` (NOT `STOP RUN`)
- BY REFERENCE on every CALL (no CALLs in this module, but rule is global)

**MUST NOT:**
- EVALUATE/WHEN — use nested IF trees
- Descriptive paragraph or variable names
- SECTIONS in PROCEDURE DIVISION
- STOP RUN

### Epic 3 Dependency — Do NOT Add the Bug Yet

Story 3.2 (off-by-one in deal array) will modify `bjack-deal.cob` to introduce an off-by-one error in the deal loop/array index. Story 2.2 must implement the deal logic CORRECTLY — the deliberate defect is added in Epic 3, not here. Do not anticipate or introduce the off-by-one in this story.

### GnuCOBOL Notes (Inherited from Stories 1.1, 1.2, 2.1)

- **Compile:** `cobc -c -I copy/ src/bjack-deal.cob` from project root
- **`_FORTIFY_SOURCE` warning:** Expected, exit code 0, ignore
- **COPY in LINKAGE SECTION:** Valid GnuCOBOL syntax
- **77-level items:** Use `77` for local independent items; `WS-X1 PIC 9` is the only local needed here
- **Subscripting with group-level vars:** `WS-PHD(1)` uses OCCURS subscript — this addresses the entire group (suit+rank+face). But since we MOVE individual sub-fields, use `WS-PS1(1)`, `WS-PRK(1)`, `WS-PFV(1)` separately

### Project Structure Notes

- **Only file changing:** `src/bjack-deal.cob` — complete rewrite
- **Copybooks:** `copy/WS-DECK.cpy` and `copy/WS-HANDS.cpy` — read-only, do NOT modify
- **No new files** created in this story

### Downstream Dependencies

- **Story 2.3 (BJACK-SCORE):** Reads WS-PHD and WS-DHD populated here; WS-PC and WS-DC counts drive its loops. If BJACK-DEAL sets wrong counts, BJACK-SCORE calculates wrong totals.
- **Story 2.4 (BJACK-DISPL):** Reads WS-PHD and WS-DHD for display. Depends on correctly populated hand arrays.
- **Story 2.6 (BJACK-MAIN):** Must reset WS-PC=0, WS-DC=0 before each initial deal call. Must call BJACK-DEAL once for initial deal, then once per hit.
- **Story 3.2 (Epic 3):** Adds off-by-one bug to THIS file. Story 2.2 output must be correct first.

### References

- Epics: Story 2.2 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 2.2]
- Architecture: BY REFERENCE calling convention → [Source: docs/planning-artifacts/architecture.md#Inter-Module Communication]
- Architecture: BJACK-DEAL COPY statements → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
- Architecture: Naming patterns → [Source: docs/planning-artifacts/architecture.md#Naming Patterns]
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Architecture: Data flow sequence (step 3) → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Story 1.1: Canonical WS-HANDS field names (WS-PC, WS-PHD, WS-PS1, WS-PRK, WS-PFV, WS-DC, WS-DHD, WS-DS1, WS-DRK, WS-DFV) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 2.1: LINKAGE SECTION pattern for BJACK-DECK (same pattern applies here) → [Source: docs/implementation-artifacts/2-1-deck-module-initialization-and-shuffle.md#CRITICAL: Shared Data Via LINKAGE SECTION]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Rewrote `src/bjack-deal.cob`: COPY WS-DECK and WS-HANDS moved to LINKAGE SECTION; PROCEDURE DIVISION USING WS-DK WS-HND; only WS-X1 (PIC 9) remains in WORKING-STORAGE.
- PROC-A detects mode via WS-PC = 0 (initial deal) or > 0 (hit) using nested IF with GOTO.
- Initial deal: CALC-1 deals player card 1 (hardcoded index 1), CALC-2 deals player card 2 (index 2, sets WS-PC=2), CALC-4/CALC-5 deal dealer cards 1 and 2 (sets WS-DC=2). WS-CT1 incremented after each deal.
- Hit: CALC-3 increments WS-PC first then uses WS-PC as subscript for WS-PHD.
- CHECK-X: GOBACK. Anti-patterns: 7 GOTOs, 0 EVALUATE, 0 STOP RUN, 0 return-code checks, 0 PROCEDURE SECTIONs, 2 wrong header comments + 1 false internal comment.
- Full build: `bash build.sh` exit 0 ✓

### File List

- src/bjack-deal.cob
