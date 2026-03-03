# Story 6.3: Bet-Over-Balance from Stale Variable

Status: review

## Story

As a developer,
I want the bet validation to check a stale balance variable under a specific sequence,
so that the player can occasionally bet more chips than they have — a subtle business logic defect.

## Acceptance Criteria

1. **Given** the bet placement from Story 5.2 is implemented,
   **When** the player completes a round and the chip balance changes,
   **Then** under a specific sequence (the validation compares WS-BET against a local copy of balance that was captured at session start and never refreshed), the player can bet more than their current actual balance.

2. **And** the stale variable is visible in the code: a local WS-XX variable stores balance at session start and is never refreshed after payout.

3. **And** the game still completes a full round without abnormal termination — the over-bet simply results in a negative balance or unexpected state.

4. **And** the bug is independently verifiable through targeted testing with a specific bet/lose/bet sequence.

## Tasks / Subtasks

- [x] Task 1: Add stale balance variable to WORKING-STORAGE (AC: #2)
  - [x] Add `77 WS-BL PIC 9(4)` after existing `77 WS-AM PIC X(50)` declaration in bjack-main.cob
  - [x] Variable name: WS-BL (cryptic, consistent with naming conventions)
- [x] Task 2: Initialize WS-BL at session start in STRT-1 (AC: #1, #2)
  - [x] In STRT-1: add `MOVE 100 TO WS-BL` immediately after `MOVE 100 TO WS-BAL`
  - [x] WS-BL is set ONCE at session start and NEVER updated again
  - [x] Do NOT update WS-BL in INIT-1, PROC-C, CALC-2, or anywhere else
- [x] Task 3: Wire BET-1 to validate against WS-BL instead of WS-BAL (AC: #1, #2)
  - [x] In BET-1: change `IF WS-BET > WS-BAL` to `IF WS-BET > WS-BL`
  - [x] The display line `DISPLAY "   ENTER BET (1-" WS-BAL "):"` can stay as-is (shows current real balance as hint, but validation uses stale value — adds to the confusion)
  - [x] First loop-back check `IF WS-BET < 1 GO TO BET-1` is unchanged
- [x] Task 4: Add an incorrect comment to STRT-1 or BET-1 to increase authenticity (AC: #2)
  - [x] Example: `* WS-BL -- TRACKS MAX BET LIMIT PER SESSION RULES 1983` (misleading — it's actually just the starting balance and breaks validation)
- [x] Task 5: Verify bug trigger sequence without full game crash (AC: #3, #4)
  - [x] Full build exits clean: `./build.sh` compiles all 8 modules and links
  - [x] Trigger sequence: bet 80, lose → WS-BAL=20 but WS-BL=100; play again, bet 50 → BET-1 accepts (50 <= WS-BL=100) even though WS-BAL=20; round completes (possibly with balance wraparound on PIC 9(4) underflow)

## Dev Notes

### Current State of BET-1 (Before This Story)

```cobol
      * BET-1 -- INPUT VALIDATION ROUTINE WITH RANGE CHECK
       BET-1.
           DISPLAY "   BAL: " WS-BAL
           DISPLAY "   ENTER BET (1-" WS-BAL "):"
           ACCEPT WS-BET
           IF WS-BET < 1
               GO TO BET-1
           END-IF
           IF WS-BET > WS-BAL
               GO TO BET-1
           END-IF
           GO TO PROC-A.
```

**The bug is NOT yet present.** `IF WS-BET > WS-BAL` uses the live, current balance — this is correct behavior. This story introduces the stale variable to break that validation.

### Target State After This Story

**WORKING-STORAGE additions:**
```cobol
           77 WS-X1          PIC 9.
           77 WS-AM          PIC X(50).
           77 WS-BL          PIC 9(4).     * ← ADD THIS
```

**STRT-1 after modification:**
```cobol
       STRT-1.
           MOVE 100 TO WS-BAL
           MOVE 100 TO WS-BL             * ← ADD THIS LINE
           GO TO INIT-1.
```

**BET-1 after modification (one line changed):**
```cobol
      * BET-1 -- INPUT VALIDATION ROUTINE WITH RANGE CHECK
       BET-1.
           DISPLAY "   BAL: " WS-BAL
           DISPLAY "   ENTER BET (1-" WS-BAL "):"
           ACCEPT WS-BET
           IF WS-BET < 1
               GO TO BET-1
           END-IF
           IF WS-BET > WS-BL             * ← CHANGE WS-BAL to WS-BL
               GO TO BET-1
           END-IF
           GO TO PROC-A.
```

**No other changes to any other paragraph or file.**

### How the Bug Works

WS-BL is initialized to 100 at session start (STRT-1). It is NEVER updated — not in INIT-1, not after payout in PROC-C, not anywhere. It permanently holds the starting balance value (100).

BET-1 validates the player's bet against WS-BL (stale = 100), not against WS-BAL (live current balance).

**Trigger sequence:**
```
Round 1: WS-BAL=100, WS-BL=100
  → Bet 80 (80 ≤ WS-BL=100 → accepted)
  → Lose: PROC-C: COMPUTE WS-BAL = WS-BAL - WS-BET → WS-BAL = 20
  → Play again: INIT-1 runs (resets hand state, does NOT touch WS-BAL or WS-BL)

Round 2: WS-BAL=20, WS-BL=100  ← stale!
  → BET-1 displays: "BAL: 0020" and "ENTER BET (1-0020):"
  → Player enters 50
  → BET-1 checks: 50 < 1? No. 50 > WS-BL (100)? No → ACCEPTED
  → But 50 > WS-BAL (20)! Over-bet accepted.

Round 2 plays out:
  → Player loses: COMPUTE WS-BAL = WS-BAL - WS-BET = 20 - 50
  → PIC 9(4) unsigned arithmetic wraps: 0020 - 0050 = 9970 (or 0000)
  → Unexpected balance state — but no ABEND
```

### Why WS-BAL Display Hint Makes Bug Harder to Spot

The display line shows the real WS-BAL: `DISPLAY "   ENTER BET (1-" WS-BAL "):"`. So the player sees `ENTER BET (1-0020):` suggesting max bet is 20. But the validation uses WS-BL (100). A player could enter 50, see the hint says max is 20, but the game accepts it anyway — a confusing and subtle bug visible to anyone reading the code who notices the display uses WS-BAL but the check uses WS-BL.

### Demo Talking Point

"Watch BET-1 carefully. The prompt shows the real balance — twenty chips. But the validation here checks WS-BL, not WS-BAL. WS-BL was set to 100 at session start and never updated. So after losing down to 20, the player can still bet up to 100. The validation is checking stale data. This is a classic mainframe defect: a snapshot variable that drifts out of sync with the live value. In production banking systems, this class of bug has cost millions."

### Architecture Compliance

**MUST:**
- WS-BL named cryptically (no descriptive name like WS-CURR-BAL-COPY) ✓
- Wrong or misleading comment on WS-BL or in STRT-1 ✓
- No return code checks in BET-1 ✓
- GOTO-driven flow (`GO TO BET-1`, `GO TO PROC-A`) preserved ✓

**MUST NOT:**
- Update WS-BL in INIT-1 (this would fix the bug — INIT-1 runs each round)
- Update WS-BL anywhere in PROC-C, CALC-2, or CHECK-X
- Use WS-BL for anything other than the broken BET-1 validation check
- Use a descriptive name for the stale variable

### CRITICAL: Do NOT Refresh WS-BL in INIT-1

INIT-1 runs at the start of every round (it's the round reset paragraph). If WS-BL were updated in INIT-1 (e.g., `MOVE WS-BAL TO WS-BL`), the bug would not trigger — WS-BL would always match WS-BAL at bet time. The bug requires WS-BL to be frozen at its session-start value (100) and never updated.

```cobol
*  INIT-1 MUST NOT contain this (it would fix the bug):
*      MOVE WS-BAL TO WS-BL
```

### Balance Underflow Behavior (PIC 9(4))

When an over-bet loss causes `COMPUTE WS-BAL = WS-BAL - WS-BET` with WS-BAL < WS-BET:

- GnuCOBOL: unsigned PIC 9(4) wraps (20 - 50 = 9970 in modular arithmetic), OR truncates to 0
- Behavior may be implementation-defined, but will NOT cause an ABEND
- CHECK-X tests `IF WS-BAL = 0` — if it wraps to 9970, the game incorrectly continues (another subtle defect layered on top)
- This is acceptable per AC#3: "the over-bet simply results in a negative balance or unexpected state"

### Project Structure Notes

- **Only file affected:** `src/bjack-main.cob`
  - WORKING-STORAGE: add `77 WS-BL PIC 9(4)`
  - STRT-1: add `MOVE 100 TO WS-BL`
  - BET-1: change `IF WS-BET > WS-BAL` to `IF WS-BET > WS-BL`
- **No copybook changes** — WS-BL is a local variable in bjack-main.cob only
- **No other modules affected** — bet validation is entirely local to BJACK-MAIN

### References

- FR45: Bet-over-balance from stale variable → [Source: docs/planning-artifacts/epics.md#Story 6.3]
- FR34: Bet placement min 1, max balance → [Source: docs/planning-artifacts/epics.md#Story 5.2]
- BET-1 current implementation → [Source: src/bjack-main.cob:29-40]
- STRT-1 / INIT-1 current implementation → [Source: src/bjack-main.cob:15-28]
- WORKING-STORAGE current declarations → [Source: src/bjack-main.cob:8-13]
- Architecture: FR45 bet-over-balance stale variable in bjack-main.cob → [Source: docs/planning-artifacts/architecture.md#Deliberate Defects FR45]
- Architecture: naming convention WS-XX for local variables → [Source: docs/planning-artifacts/architecture.md#Naming Patterns]
- Story 5.2 BET-1 implementation → [Source: docs/implementation-artifacts/5-2-bet-placement-and-validation.md]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- Comment syntax error on first attempt: `* comment` placed inline after period on same line as 77-level declaration. Fixed by moving comment to preceding line in column 7 (standard fixed-format COBOL comment indicator).

### Completion Notes List

- Added `77 WS-BL PIC 9(4)` to WORKING-STORAGE in `src/bjack-main.cob:14-15` (preceded by misleading comment `* WS-BL -- TRACKS MAX BET LIMIT PER SESSION RULES 1983`).
- Added `MOVE 100 TO WS-BL` in STRT-1 at `src/bjack-main.cob:18`. WS-BL is set once at session start and never updated again (INIT-1, PROC-C, CALC-2 untouched).
- Changed `IF WS-BET > WS-BAL` to `IF WS-BET > WS-BL` in BET-1 at `src/bjack-main.cob:39`. Display line still shows real WS-BAL — adds to confusion.
- Wrote `test/t63-bet-over-balance.cob`: simulates full trigger sequence (lose 80 chips, then bet 50 vs stale WS-BL=100 and real WS-BAL=20). T63 output: "BET ACCEPTED (50<=WS-BL=100) -- BUG ACTIVE". BUG CONFIRMED ACTIVE.
- All 7 tests (T31–T34, T61–T63) pass with no regressions.

### File List

- src/bjack-main.cob (modified — added WS-BL, MOVE 100 TO WS-BL, changed BET-1 validation)
- test/t63-bet-over-balance.cob (new)
- test/run-tests.sh (modified — added T63 section)

### Change Log

- 2026-02-28: Story 6.3 implemented — stale variable WS-BL introduced, BET-1 wired to check WS-BL instead of WS-BAL. Test harness t63 added and passing.
- 2026-02-28: Code review fixes — T63 assertions added (BUG NOT ACTIVE → RETURN-CODE 1; over-bet condition not met → RETURN-CODE 1); source guard added to run-tests.sh (grep for IF WS-BET > WS-BL); t61/t62/t63 added to .gitignore.
