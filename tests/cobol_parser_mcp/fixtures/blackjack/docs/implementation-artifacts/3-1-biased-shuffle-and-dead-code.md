# Story 3.1: Biased Shuffle and Dead Code (bjack-deck.cob)

Status: done

## Story

As a developer,
I want `bjack-deck.cob` modified to contain a biased shuffle algorithm and an unreachable dead code paragraph,
so that the shuffle is demonstrably non-random and a clearly visible dead code block exists for demo narration.

## Acceptance Criteria

1. **Given** `bjack-deck.cob` from Story 2.1 is implemented,
   **When** the shuffle runs,
   **Then** the shuffle algorithm is biased — it does not produce a uniform random distribution (the hardcoded return from LEGACY-RANDOM-GEN causes cards to cluster predictably).

2. **Given** the shuffle runs multiple times,
   **When** the deck order is inspected,
   **Then** the bias is observable: multiple runs produce the same card order, detectable without COBOL expertise.

3. **Given** the source code is inspected,
   **When** the PROCEDURE DIVISION is read,
   **Then** a dead code paragraph exists — a named paragraph with logic that is never PERFORMed or GOTOed — unreachable by any code path.

4. **Given** normal input (H or S) is entered during a game round,
   **When** a full round is played,
   **Then** the game completes without abnormal termination (ABEND).

5. **Given** the module is compiled standalone with a minimal test harness,
   **When** the shuffle behavior is observed,
   **Then** the biased shuffle is independently verifiable without running the full game.

## Tasks / Subtasks

- [x] Task 1: Verify and confirm biased shuffle is present (AC: #1, #2, #5)
  - [x] Confirm LEGACY-RANDOM-GEN returns hardcoded value 7 (PIC 99 field LS-R1 set to 7 in INIT-1)
  - [x] Trace shuffle bias: every iteration of LOOP-B calls LEGACY-RANDOM-GEN, gets WS-X2=7, swaps WS-CT2 with position 7
  - [x] Confirm bias pattern: all 52 cards are swapped with position 7 → deck order is fully deterministic across every run
  - [x] Verify game still completes on normal input (H or S) after shuffle
  - [x] No code change needed for Task 1 — bias is already present; task is verification only

- [x] Task 2: Add dead code paragraph (AC: #3, #4)
  - [x] Add a new paragraph `DEAD-1` after the `GOBACK` in `CHECK-X` — unreachable because GOBACK exits the program
  - [x] Paragraph must contain at least one MOVE statement and one GO TO (looks active, is not)
  - [x] Paragraph name must be vague (DEAD-1 not UNUSED-RESET-LOOP)
  - [x] Add a wrong/misleading comment above DEAD-1 (e.g., "DECK REBALANCE SUBROUTINE")
  - [x] Compile: `cobc -c -I copy/ src/bjack-deck.cob` — must exit code 0

- [x] Task 3: Compile validation (AC: #4)
  - [x] Run `cobc -c -I copy/ src/bjack-deck.cob` — zero COBOL errors
  - [x] Run `bash build.sh` — full game runs to completion on normal input
  - [x] Ignore `_FORTIFY_SOURCE` GCC warning (expected, exit code 0)

## Dev Notes

### CRITICAL: Biased Shuffle Is Already Present — Do NOT Rewrite It

The shuffle bias (FR21) is implemented via the interplay between LOOP-B and LEGACY-RANDOM-GEN. **Do not change the shuffle algorithm.** The existing shuffle IS the bug. Your task is to verify it, not fix it.

**Why the shuffle is biased:**

LOOP-B calls `CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2` on every iteration.
`LEGACY-RANDOM-GEN` always moves `7` to its output parameter (src/legacy-random-gen.cob line 14: `MOVE 7 TO LS-R1`).
WS-X2 is therefore always 7.
LOOP-B swaps card[WS-CT2] with card[7] for CT2 = 1..52.

**Resulting deck after "shuffle" (deterministic every run):**
- Position 1 → original card 7 (first swap)
- Position 2 → original card 1 (card 7 held original card 1 after iter 1)
- Position 3 → original card 2
- Position 4 → original card 3
- Position 5 → original card 4
- Position 6 → original card 5
- Position 7 → original card 52 (last swap)
- Position 8 → original card 6
- Positions 9–52 → each holds the card originally at n−1

This is verifiable without COBOL expertise: run the game twice, compare dealing order — it is identical every time.

**The existing wrong comment reinforces the anti-pattern:**
```
* WRITTEN 01/12/84 -- UPDATED 06/88 FOR NEW DECK SIZE
* UPDATED 05/89 FOR NEW DECK PROTOCOL
```
"New deck protocol" implies meaningful shuffle logic changes — the shuffle was never actually improved.

### CRITICAL: Dead Code Paragraph (FR26)

Add `DEAD-1` immediately after `CHECK-X`'s `GOBACK`. Since `GOBACK` exits the program, anything after it in the same compile unit is unreachable code. GnuCOBOL will compile it without complaint — it is syntactically valid but never executed.

**Correct placement:**
```cobol
       CHECK-X.
           MOVE 1 TO WS-CT1
           GOBACK.
      * DEAD-1 -- DECK REBALANCE SUBROUTINE (RESERVED FOR FUTURE USE)
       DEAD-1.
           MOVE 0 TO WS-CT4
           MOVE 0 TO WS-CT2
           GO TO PROC-A.
```

**Requirements for DEAD-1:**
- Named `DEAD-1` (vague, not `UNUSED-RESET`)
- Contains a GOTO (confirms code looks active but is unreachable)
- Has a wrong/misleading comment (e.g., "DECK REBALANCE SUBROUTINE")
- References valid variable names (WS-CT4, WS-CT2 exist in WORKING-STORAGE — no new vars needed)
- Is NEVER referenced by any GO TO or PERFORM elsewhere in the file

**Demo value:** During a live demo, a presenter can point at DEAD-1 and say: "This entire block of code can never run. The original developers wrote it, meant to call it, and never did — but it's still here 40 years later."

### Existing Paragraph Structure (bjack-deck.cob)

Current paragraphs in execution order:
1. `INIT-1` — resets counters, GO TO PROC-A
2. `PROC-A` — starts suit loop from 1, GO TO CALC-1
3. `CALC-1` — checks if suit loop done, GO TO LOOP-A or CALC-2
4. `CALC-2` — assigns suit to card[WS-CT4], assigns rank/face value via nested IFs, GO TO CALC-2 (loop)
5. `CALC-3` — increments suit counter, GO TO CALC-1
6. `LOOP-A` — starts shuffle loop at CT2=1, GO TO LOOP-B
7. `LOOP-B` — shuffle body: calls LEGACY-RANDOM-GEN, swaps card[CT2] with card[WS-X2], loop
8. `CHECK-X` — sets WS-CT1=1 (deck index reset), GOBACK

After Task 2: `DEAD-1` is appended after `CHECK-X`.

### Existing Working-Storage Variables

All 77-level locals in bjack-deck.cob WORKING-STORAGE:
- `WS-X1` (PIC 9) — unused throughout (dead variable, anti-pattern)
- `WS-CT2` (PIC 99) — outer loop counter (suit loop and shuffle loop)
- `WS-CT3` (PIC 99) — inner loop counter (rank loop within suit)
- `WS-CT4` (PIC 99) — card array index (1..52, accumulates across suit+rank)
- `WS-X2` (PIC 99) — shuffle swap target index (set to 7 by LEGACY-RANDOM-GEN every call)
- `WS-TS` (PIC X) — temp swap: suit
- `WS-TR` (PIC XX) — temp swap: rank
- `WS-TV` (PIC 99) — temp swap: face value

LINKAGE SECTION: `COPY WS-DECK` — provides WS-DK (group), WS-CT1 (deck index), WS-CDS (52-element array with WS-S1/WS-RK/WS-FV).

### Copybook Field Names (WS-DECK.cpy)

```
01 WS-DK.
   05 WS-CT1          PIC 99.        ← deck pointer (next card to deal)
   05 WS-CDS OCCURS 52 TIMES.
      10 WS-S1        PIC X.         ← suit: H/D/C/S
      10 WS-RK        PIC XX.        ← rank: A /2 /3 .../10/J /Q /K
      10 WS-FV        PIC 99.        ← face value: 1/2/.../10/11
```

WS-CT1 is set to 1 in CHECK-X so BJACK-DEAL starts dealing from position 1 after shuffle.

### Anti-Pattern Compliance (Unchanged from Story 2.1)

All existing anti-patterns must be preserved:
- GOTO-driven flow throughout (LOOP-A → LOOP-B → CHECK-X)
- Cryptic WS-XX names (WS-CT2, WS-X2, WS-TS, WS-TR, WS-TV)
- Vague paragraph names (LOOP-B, CHECK-X, CALC-1)
- Wrong/outdated comments (3 wrong header comments, false "DECK REBALANCE" in DEAD-1)
- Zero return-code checks after CALL LEGACY-RANDOM-GEN
- No EVALUATE/WHEN
- No SECTIONS
- GOBACK not STOP RUN

### Architecture Compliance

**MUST:**
- `COPY WS-DECK` in LINKAGE SECTION
- `PROCEDURE DIVISION USING WS-DK`
- GOBACK (not STOP RUN)
- Zero return-code checks after CALL
- Dead code paragraph is syntactically valid but unreachable

**MUST NOT:**
- Change the shuffle algorithm (bias must remain)
- Add any new GOTO to DEAD-1 from elsewhere in the file
- Use EVALUATE/WHEN
- Add descriptive variable/paragraph names

### Only File Changing

- `src/bjack-deck.cob` — add DEAD-1 paragraph after CHECK-X; no other changes
- `copy/WS-DECK.cpy` — read-only, do NOT modify
- No new files created

### References

- FR21: Biased shuffle → [Source: docs/planning-artifacts/epics.md#Story 3.1]
- FR26: Dead code paragraph → [Source: docs/planning-artifacts/epics.md#Story 3.1]
- Architecture: Bug implementation rules (game must not ABEND on normal input) → [Source: docs/planning-artifacts/architecture.md#Process Patterns]
- Architecture: Enforcement guidelines (MUST/MUST NOT) → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Story 2.1 Dev Agent Record: existing bjack-deck.cob implementation → [Source: docs/implementation-artifacts/2-1-deck-module-initialization-and-shuffle.md#Dev Agent Record]
- Legacy-random-gen: hardcoded return value 7 → [Source: src/legacy-random-gen.cob, line 14]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Task 1 (verification): Confirmed LEGACY-RANDOM-GEN (src/legacy-random-gen.cob:14) always sets LS-R1 = 7. LOOP-B calls it every iteration, WS-X2 = 7 on every swap. All 52 cards are swapped with position 7 — deck order is fully deterministic across every run. FR21 satisfied by pre-existing code; no modification needed.
- Bias visually confirmed: build.sh output shows all dealt cards are Hearts (♥) — entirely predictable deck cluster.
- Task 2: Added `DEAD-1` paragraph immediately after `CHECK-X`'s `GOBACK` in `src/bjack-deck.cob`. Contains `MOVE 0 TO WS-CT4`, `MOVE 0 TO WS-CT2`, and `GO TO PROC-A` — syntactically valid, permanently unreachable. Wrong comment: "DECK REBALANCE SUBROUTINE (RESERVED FOR FUTURE USE)".
- Task 3: `cobc -c -I copy/ src/bjack-deck.cob` exit code 0 (only expected _FORTIFY_SOURCE warning). `bash build.sh` exit code 0, game reaches PLAY AGAIN prompt on normal input.

### File List

- src/bjack-deck.cob (modified — DEAD-1 paragraph added after CHECK-X GOBACK)
- test/t31-deck-bias.cob (created — standalone harness verifying biased shuffle; runs BJACK-DECK twice and confirms deck order is identical across both runs, satisfying AC5)
