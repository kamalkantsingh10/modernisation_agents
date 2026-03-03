# Story 3.2: Off-By-One in Deal Array (bjack-deal.cob)

Status: done

## Story

As a developer,
I want `bjack-deal.cob` modified to contain an off-by-one error in the deal array index,
so that the deal loop has a subtle but verifiable indexing defect.

## Acceptance Criteria

1. **Given** `bjack-deal.cob` from Story 2.2 is implemented,
   **When** BJACK-DEAL is called for a hit (WS-PC > 0),
   **Then** the deal loop contains an off-by-one error in the array index: the new card is stored at the current WS-PC index (overwriting the last dealt card) instead of WS-PC+1 (the next empty slot).

2. **Given** the source code is inspected,
   **When** the hit path paragraph (CALC-3) is read,
   **Then** the error is visible: `MOVE ... TO WS-PS1(WS-PC)` appears BEFORE `ADD 1 TO WS-PC`, making the store one position too early.

3. **Given** normal input (H or S) is entered,
   **When** a full round plays through including a hit,
   **Then** the game completes without ABEND — the off-by-one does not cause an out-of-bounds subscript.

4. **Given** the module is compiled and called in isolation with crafted input,
   **When** a hit is applied to a two-card hand,
   **Then** the off-by-one is independently verifiable: WS-PRK(2) shows the hit card (not the original 2nd card), WS-PC = 3, but WS-PRK(3) is blank.

## Tasks / Subtasks

- [x] Task 1: Introduce off-by-one error in CALC-3 (AC: #1, #2, #3)
  - [x] In paragraph `CALC-3`, move the three `MOVE WS-S1/WS-RK/WS-FV` statements to BEFORE `ADD 1 TO WS-PC`
  - [x] Result: card is stored at current WS-PC (= 2 on first hit) not at WS-PC+1 (= 3)
  - [x] Leave `ADD 1 TO WS-CT1` and `GO TO CHECK-X` positions unchanged
  - [x] Do NOT change CALC-1 or CALC-2 (initial deal is unaffected)
  - [x] Add or update wrong comment on CALC-3: e.g., `* CALC-3 -- DEALS NEXT CARD TO CORRECT HAND SLOT`

- [x] Task 2: Compile validation (AC: #3, #4)
  - [x] Run `cobc -c -I copy/ src/bjack-deal.cob` — zero COBOL errors, exit code 0
  - [x] Run `bash build.sh` — game launches, hit path runs without ABEND
  - [x] Ignore `_FORTIFY_SOURCE` GCC warning (expected)

## Dev Notes

### CRITICAL: Exact Change Required in CALC-3

**Current CALC-3 (correct — from Story 2.2):**
```cobol
       CALC-3.
           ADD 1 TO WS-PC
           MOVE WS-S1(WS-CT1)  TO WS-PS1(WS-PC)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(WS-PC)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(WS-PC)
           ADD 1 TO WS-CT1
           GO TO CHECK-X.
```

**Modified CALC-3 (with off-by-one bug):**
```cobol
      * CALC-3 -- DEALS NEXT CARD TO CORRECT HAND SLOT
       CALC-3.
           MOVE WS-S1(WS-CT1)  TO WS-PS1(WS-PC)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(WS-PC)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(WS-PC)
           ADD 1 TO WS-PC
           ADD 1 TO WS-CT1
           GO TO CHECK-X.
```

**What changes:** The three MOVE statements now execute before `ADD 1 TO WS-PC`, so the new card is stored at the current (pre-increment) WS-PC instead of the next slot.

### Bug Behavior Analysis

**Initial state when BJACK-DEAL is called for a hit:**
- WS-PC = 2 (player has 2 cards from initial deal)
- Player cards: WS-PRK(1) = card 1 rank, WS-PRK(2) = card 2 rank

**With the off-by-one bug (first hit):**
1. `MOVE WS-RK(WS-CT1) TO WS-PRK(WS-PC)` — WS-PC is still 2 → **overwrites WS-PRK(2)** with hit card
2. `ADD 1 TO WS-PC` — WS-PC becomes 3
3. Returns to BJACK-MAIN

**Observable effects:**
- WS-PC = 3 (claims 3 cards)
- WS-PRK(1) = original card 1 (correct)
- WS-PRK(2) = hit card (overwrote original card 2)
- WS-PRK(3) = spaces/zeros (never written — empty slot)
- Score module (BJACK-SCORE CALC-1) loops 1..3: WS-PFV(1) + WS-PFV(2) + WS-PFV(3) = card1_fv + hit_fv + 0 → wrong total (2 card values not 3)
- Display shows 3 card boxes: box 1 correct, box 2 shows hit card, box 3 is blank

**Why it doesn't ABEND:**
- WS-PC = 3 ≤ 11 (array OCCURS 11 TIMES in WS-HANDS.cpy) → no out-of-bounds
- WS-PFV(3) = 0 (initialized from MOVE ZEROS TO WS-HND in bjack-main.cob INIT-1)
- All subscript accesses are within array bounds

**Demo value:** A presenter can show the code and say: "The counter is incremented AFTER storing, so each hit overwrites the previous card's slot. The game says you have 3 cards but card 3 is blank."

### Existing Paragraph Structure (bjack-deal.cob)

Current paragraphs — only CALC-3 changes:
1. `INIT-1` — resets WS-X1, GO TO PROC-A
2. `PROC-A` — if WS-PC=0 (initial deal) GO TO CALC-1; else GO TO CALC-3 (hit)
3. `CALC-1` — deals player card 1 to WS-PS1(1)/WS-PRK(1)/WS-PFV(1), GO TO CALC-2
4. `CALC-2` — deals player card 2, sets WS-PC=2, GO TO CALC-4
5. `CALC-3` — **BUG HERE** — hit path: store at WS-PC before increment
6. `CALC-4` — deals dealer card 1 to WS-DS1(1)/WS-DRK(1)/WS-DFV(1), GO TO CALC-5
7. `CALC-5` — deals dealer card 2, sets WS-DC=2, GO TO CHECK-X
8. `CHECK-X` — GOBACK

### CALC-1 and CALC-2 Are Unchanged

Do NOT touch the initial deal paragraphs:
- CALC-1 correctly stores to WS-PS1(1) with explicit subscript 1 (no loop variable)
- CALC-2 correctly stores to WS-PS1(2) with explicit subscript 2
- These paragraphs do not use WS-PC as a subscript during the store

The off-by-one is ONLY in CALC-3 (the hit path, which uses WS-PC dynamically).

### Copybook Field Names (WS-HANDS.cpy)

```
01 WS-HND.
   05 WS-PC           PIC 99.       ← player card count
   05 WS-PHD OCCURS 11 TIMES.
      10 WS-PS1       PIC X.        ← player suit (H/D/C/S)
      10 WS-PRK       PIC XX.       ← player rank (A /2 /.../10/J /Q /K )
      10 WS-PFV       PIC 99.       ← player face value (1..11)
   05 WS-DC           PIC 99.       ← dealer card count
   05 WS-DHD OCCURS 11 TIMES.
      10 WS-DS1       PIC X.        ← dealer suit
      10 WS-DRK       PIC XX.       ← dealer rank
      10 WS-DFV       PIC 99.       ← dealer face value
```

### Working-Storage Variables (bjack-deal.cob)

Only one 77-level local:
- `WS-X1` (PIC 9) — initialized to 0, never used again (dead variable, anti-pattern)

LINKAGE SECTION: `COPY WS-DECK` (provides WS-DK, WS-CT1 as deck pointer, WS-CDS array) and `COPY WS-HANDS` (provides WS-HND, WS-PC, WS-PHD, WS-DC, WS-DHD).

### Anti-Pattern Compliance (Unchanged from Story 2.2)

All anti-patterns must be preserved:
- GOTO-driven flow (PROC-A → CALC-1 → CALC-2 → CALC-4 → CALC-5 → CHECK-X for initial deal)
- Cryptic WS-X1 name (dead variable)
- Vague paragraph names (CALC-3, CHECK-X)
- At least one wrong comment (existing "HANDLES SPLIT HANDS PER CASINO RULES" is false — no split logic exists)
- New wrong comment on CALC-3: "DEALS NEXT CARD TO CORRECT HAND SLOT" (it doesn't — off by one)
- Zero return-code checks (no CALL statements in this module)
- No EVALUATE/WHEN
- No SECTIONS
- GOBACK not STOP RUN

### Architecture Compliance

**MUST:**
- `COPY WS-DECK` and `COPY WS-HANDS` in LINKAGE SECTION (order matters)
- `PROCEDURE DIVISION USING WS-DK WS-HND`
- GOBACK (not STOP RUN)
- Change confined to CALC-3 only

**MUST NOT:**
- Touch CALC-1, CALC-2, CALC-4, CALC-5, CHECK-X
- Use EVALUATE/WHEN
- Add descriptive names

### Only File Changing

- `src/bjack-deal.cob` — CALC-3 paragraph: swap order of MOVE statements and ADD 1 TO WS-PC; add wrong comment
- No new files created, no copybook changes

### References

- FR25: Off-by-one in deal array → [Source: docs/planning-artifacts/epics.md#Story 3.2]
- Architecture: Bug rules (no ABEND on normal input) → [Source: docs/planning-artifacts/architecture.md#Process Patterns]
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Story 2.2 Dev Agent Record: existing bjack-deal.cob implementation → [Source: docs/implementation-artifacts/2-2-deal-module-initial-hand-distribution.md#Dev Agent Record]
- WS-HANDS.cpy: hand array structure (OCCURS 11 TIMES) → [Source: copy/WS-HANDS.cpy]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Task 1: In `CALC-3` (hit path), moved the three `MOVE WS-S1/WS-RK/WS-FV` statements to before `ADD 1 TO WS-PC`. On first hit (WS-PC=2), card is stored at WS-PS1(2), overwriting the initial deal's second card. WS-PC then increments to 3. Added wrong comment: "DEALS NEXT CARD TO CORRECT HAND SLOT". CALC-1 and CALC-2 (initial deal, explicit subscripts) unchanged.
- Task 2: `cobc -c -I copy/ src/bjack-deal.cob` exit code 0. `bash build.sh` exit code 0. Bug confirmed in output: after first hit, player card 2 displays hit card (overwrites original), card 3 shows blank `|00  |` ghost slot. Score reduced by one card value (WS-PFV(3)=0). No ABEND.

### File List

- src/bjack-deal.cob (modified — CALC-3 paragraph: MOVE statements reordered before ADD 1 TO WS-PC; wrong comment added)
- test/t32-deal-obo.cob (created — standalone harness confirming off-by-one; after initial deal + one hit: SLOT 2 shows hit card (overwritten), SLOT 3 blank, satisfying AC4)
