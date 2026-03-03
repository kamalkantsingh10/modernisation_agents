# Story 6.1: Payout Rounding Error on Natural Blackjack

Status: review

## Story

As a developer,
I want the 3:2 natural blackjack payout to contain a truncation bug from integer division,
so that odd bet amounts produce visibly incorrect payouts demonstrable during a demo.

## Acceptance Criteria

1. **Given** the betting system from Epic 5 is implemented with 3:2 natural blackjack payout,
   **When** the payout for a natural blackjack is calculated,
   **Then** the calculation uses integer division (e.g., `COMPUTE WS-PAY = WS-BET * 3 / 2`) which truncates fractional chips.

2. **And** bet of 5 pays 7 instead of 7.5 (truncated), bet of 3 pays 4 instead of 4.5 (truncated) — inconsistent truncation behavior is demonstrable.

3. **And** the truncation is a code-visible defect: anyone reading the COMPUTE or DIVIDE statement can see there is no rounding.

4. **And** the game still completes a full round without abnormal termination on normal input.

5. **And** the bug is independently verifiable by testing natural blackjack with odd bet amounts.

## Tasks / Subtasks

- [x] Task 1: Inspect PROC-NB in bjack-main.cob and confirm or implement truncation bug (AC: #1, #3)
  - [x] Check current PROC-NB: `COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2`
  - [x] If formula is already present → bug IS already implemented (no code change needed)
  - [x] If formula uses correct rounding → change to `COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2` (integer div truncates)
  - [x] Confirm WS-BAL is PIC 9(4) (no decimal places = no fractional storage)
- [x] Task 2: Verify truncation behavior mathematically (AC: #2)
  - [x] WS-BET=5 → 5*3=15 → 15/2=7 in COBOL integer arithmetic (not 7.5)
  - [x] WS-BET=3 → 3*3=9 → 9/2=4 (not 4.5)
  - [x] WS-BET=10 → 10*3=30 → 30/2=15 (even bet — no truncation, works correctly)
- [x] Task 3: Full compile test and behavior verification (AC: #4, #5)
  - [x] `./build.sh` exits clean (all 8 modules compile and link)
  - [x] Play game with odd bet amount to verify truncation occurs

## Dev Notes

### Current State of PROC-NB (Pre-Implementation Check)

The natural blackjack payout paragraph in `src/bjack-main.cob` is:

```cobol
       PROC-NB.
           COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
           MOVE 1 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           DISPLAY "   *** NATURAL BLACKJACK ***"
           GO TO CHECK-X.
```

**The truncation bug IS already present in this formula.** COBOL COMPUTE evaluates `WS-BET * 3 / 2` using integer arithmetic (left-to-right, no implicit rounding). Since WS-BAL is `PIC 9(4)` (no decimal places), the fractional part is silently dropped.

**Expected dev outcome:** No code change required to PROC-NB. Verify the formula is exactly as above and confirm truncation behavior by calculation/test. If any rounding (`+ 0.5`, `ROUNDED`, or separate DIVIDE with REMAINDER) is present — remove it.

### Why This Bug Exists (Demo Context)

COBOL `COMPUTE` with integer-typed fields truncates silently. A 1980s programmer computing `WS-BET * 3 / 2` would see no error, no warning — the game works perfectly on even bets (10 → 15 ✓) and silently shortchanges the player on odd bets (5 → 7 instead of 7.5). This is the classic "looks right, works most of the time" defect.

### COBOL Integer Division Mechanics

```cobol
* WS-BET = 5 (odd bet example):
COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
*   → WS-BET * 3 = 15
*   → 15 / 2 = 7 (integer truncation, not rounding)
*   → WS-BAL = WS-BAL + 7  (player short-changed 0.5 chip)
```

No ROUNDED clause exists. No REMAINDER check. The truncation is silent and only visible if you manually calculate expected vs actual payout.

### Demo Talking Point

"This payout formula — `WS-BET * 3 / 2` — looks correct at a glance. It IS correct for even bets. But COBOL integer division quietly truncates the fractional chip on odd bets. The player gets 7 chips instead of 7.5. In a real casino this would be a regulatory violation. The bug has lived here since 1985 and nobody noticed because even bets always pay correctly."

### Game Flow — PROC-NB Position

```
PROC-A → [check: WS-PC=2 AND WS-PT=21] → GO TO PROC-NB
PROC-NB → payout → BJACK-DISPL → GO TO CHECK-X
```

PROC-NB bypasses PROC-C and CALC-2 entirely. It jumps directly to CHECK-X. No conflict with Story 5.5 payout logic (which lives in PROC-C for non-natural outcomes).

### Verification Test (Manual)

To verify independently without full game run:

1. Set `WS-BAL = 100`, `WS-BET = 5` in a test harness
2. Execute `COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2`
3. Expected if bug present: `WS-BAL = 107` (not 107.5)
4. Expected if bug absent: same result — COBOL can't store 107.5 in PIC 9(4) anyway

Alternative: play game, get natural blackjack with bet=5, verify balance increases by 7 (not 8 — that would require full float precision, and COBOL doesn't provide it here).

### Architecture Compliance

**MUST:**
- COMPUTE formula uses integer division (no ROUNDED clause) ✓
- No separate COMPUTE with fractional intermediate storage
- PROC-NB uses `GO TO CHECK-X` (GOTO-driven flow) ✓
- No return code check after BJACK-DISPL call ✓

**MUST NOT:**
- Add ROUNDED clause to the COMPUTE
- Use a PIC 9V9 intermediate variable to preserve fractional chips
- Add a DIVIDE WITH REMAINDER to compute correct payout

### Project Structure Notes

- **Only file affected:** `src/bjack-main.cob` (PROC-NB paragraph)
- **No copybook changes** — WS-BAL (PIC 9(4)) and WS-BET (PIC 9(4)) in WS-GAME.cpy are unchanged
- **No other modules affected** — PROC-NB is local to BJACK-MAIN, no cross-module impact

### References

- FR43: Payout rounding error on 3:2 natural blackjack → [Source: docs/planning-artifacts/epics.md#Story 6.1]
- FR35: Natural blackjack detection and immediate resolution → [Source: docs/planning-artifacts/epics.md#Story 5.3]
- PROC-NB current implementation → [Source: src/bjack-main.cob:52-57]
- Architecture: payout rounding error in BJACK-MAIN → [Source: docs/planning-artifacts/architecture.md#Deliberate Defects FR43]
- Story 5.3 implementation of PROC-NB → [Source: docs/implementation-artifacts/5-3-natural-blackjack-detection-and-payout.md]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — bug was pre-existing, no code changes required.

### Completion Notes List

- Verified PROC-NB at `src/bjack-main.cob:55`: `COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2` — truncation bug present, no change needed.
- Confirmed WS-BAL is `PIC 9(4)` (WS-GAME.cpy:11) — no fractional storage possible.
- Verified mathematically: BET=5→107 (not 107.5), BET=3→104 (not 104.5), BET=10→115 (correct).
- Wrote `test/t61-payout-round.cob`: COBOL test harness that exercises the COMPUTE statement and verifies truncation output. T61 passes — BUG CONFIRMED ACTIVE.
- All 7 tests (T31–T34, T61–T63) pass with no regressions.

### File List

- test/t61-payout-round.cob (new)
- test/run-tests.sh (modified — added T61 section)

### Change Log

- 2026-02-28: Story 6.1 verified — payout truncation bug confirmed present in PROC-NB. Test harness t61 added and passing.
- 2026-02-28: Code review fixes — T61 assertions added (RETURN-CODE 1 on value mismatch); source guard added to run-tests.sh (grep on truncation formula in bjack-main.cob); t61/t62/t63 added to .gitignore.
