# Story 6.2: Double-Down-Anytime Rule Violation

Status: review

## Story

As a developer,
I want the game to allow double down after the player has already hit (a rule violation),
so that the game has a business rule defect demonstrable during a live demo.

## Acceptance Criteria

1. **Given** the double down action from Story 5.4 is implemented,
   **When** the player has already hit (hand has more than 2 cards),
   **Then** the 'D' option is still accepted at the action prompt (no check for card count).

2. **And** the double down proceeds normally — bet doubles, one card dealt, auto-stand.

3. **And** the missing validation is visible in the code: the action prompt paragraph has no `IF WS-PC = 2` before allowing 'D'.

4. **And** the game still completes a full round without abnormal termination.

5. **And** the bug is independently verifiable by hitting once, then entering 'D'.

## Tasks / Subtasks

- [x] Task 1: Inspect LOOP-A in bjack-main.cob and confirm the rule violation is present (AC: #1, #3)
  - [x] Locate the 'D' branch in LOOP-A
  - [x] Confirm there is NO `IF WS-PC = 2` (or equivalent WS-PC check) before the double-down logic
  - [x] Confirm there is NO card count check of any kind gating the 'D' input path
  - [x] If the check IS absent → bug is already implemented (no code change needed)
  - [x] If a card count check exists → remove it entirely
- [x] Task 2: Verify WS-PC is the correct field for card count (AC: #1)
  - [x] WS-PC is defined in WS-HANDS.cpy as `05 WS-PC PIC 99` (player card count)
  - [x] After initial deal: WS-PC = 2
  - [x] After one hit: WS-PC = 3
  - [x] The valid double-down rule: only when WS-PC = 2 (initial two-card hand)
  - [x] The bug: no such check exists → 'D' works at any WS-PC value
- [x] Task 3: Manual verification of bug trigger sequence (AC: #4, #5)
  - [x] Full build exits clean: `./build.sh` compiles all 8 modules and links
  - [x] Walkthrough sequence: place bet → get dealt cards → enter 'H' → enter 'D' → game completes round without ABEND

## Dev Notes

### Current State of LOOP-A (Pre-Implementation Check)

The player action loop in `src/bjack-main.cob` is:

```cobol
      * LOOP-A -- VALIDATES INPUT AND ROUTES TO HIT OR STAND
      * UPDATED 07/89 -- ADDED SPLIT HAND SUPPORT
       LOOP-A.
           DISPLAY "   ENTER H, S, OR D:"
           ACCEPT WS-FLG-A
           IF WS-FLG-A = 'S'
               GO TO PROC-B
           END-IF
           IF WS-FLG-A = 'D'
               COMPUTE WS-BET = WS-BET * 2
               CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
               CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
               MOVE 0 TO WS-STAT
               CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
               IF WS-PT > 21
                   GO TO PROC-C
               END-IF
               GO TO PROC-B
           END-IF
           GO TO CALC-1.
```

**The rule violation IS already present.** There is no `IF WS-PC = 2` check before the `IF WS-FLG-A = 'D'` branch. The 'D' option is accepted regardless of how many cards the player holds.

**Expected dev outcome:** No code change required to LOOP-A. Verify the code is as above (no card count check) and confirm the bug trigger sequence works without ABEND.

### Why This Is a Bug

Standard casino blackjack rule: double down is only available on the initial two-card hand (WS-PC = 2). After hitting, the player has 3+ cards and is no longer eligible to double down.

The correct implementation would be:

```cobol
*  ← CORRECT IMPLEMENTATION (DO NOT ADD THIS — it would FIX the bug)
           IF WS-FLG-A = 'D'
               IF WS-PC NOT = 2
                   GO TO LOOP-A   *  or display error
               END-IF
               COMPUTE WS-BET = WS-BET * 2
               ...
```

The missing validation makes 'D' a permanent option. Non-COBOL readers can see there's no card count check just by reading the IF chain.

### Bug Trigger Sequence

To demonstrate during a live demo:

1. Place a bet (e.g., 20 chips)
2. Receive initial 2-card deal
3. Enter **H** (hit) → receive 3rd card, WS-PC = 3
4. Enter **D** (double down) → game accepts it, doubles the bet, deals one more card, auto-stands
5. Round completes without ABEND

This is impossible in any real casino. A dealer would refuse step 4. The code allows it silently.

### WS-PC Field Context

```cobol
* From copy/WS-HANDS.cpy:
       01 WS-HND.
          05 WS-PC           PIC 99.    * ← player card count
          05 WS-PHD OCCURS 11 TIMES.   * ← player hand cards
          ...
```

WS-PC is incremented by BJACK-DEAL each time a card is dealt to the player:
- Initial deal (2 cards): WS-PC = 2
- After H (hit): WS-PC = 3, 4, 5...
- After D (double-down): BJACK-DEAL called once more → WS-PC incremented
- WS-PC is shared via BY REFERENCE → LOOP-A can see current value but does NOT check it

### Architecture Compliance

**MUST:**
- LOOP-A uses GOTO-driven flow (`GO TO PROC-B`, `GO TO CALC-1`) ✓
- No return code check after any CALL ✓
- No EVALUATE/WHEN ✓
- `IF WS-FLG-A = 'D'` branch present and functional ✓

**MUST NOT:**
- Add `IF WS-PC = 2` before accepting 'D' — this would fix the bug
- Add any card count validation anywhere in LOOP-A
- Remove the 'D' option from the prompt text

### Demo Talking Point

"See this IF chain? Hit, stand, double. But there's no card count check here. In a real casino, double down is only available on your first two cards. This code lets you double after hitting — any time, any number of cards. The validation just isn't there. To add it, you'd need to understand WS-PC, where it comes from, how it's shared across modules via the copybook... that's the modernization work."

### Project Structure Notes

- **Only file affected:** `src/bjack-main.cob` (LOOP-A paragraph verification only)
- **No copybook changes** — WS-PC is already in WS-HANDS.cpy (read-only for this story)
- **No other modules affected** — BJACK-DEAL increments WS-PC normally; the bug is the absence of checking it in BJACK-MAIN

### References

- FR44: Double-down-anytime rule violation → [Source: docs/planning-artifacts/epics.md#Story 6.2]
- FR36: Double down action (Story 5.4 implementation) → [Source: docs/planning-artifacts/epics.md#Story 5.4]
- LOOP-A current implementation → [Source: src/bjack-main.cob:59-77]
- WS-PC field definition → [Source: copy/WS-HANDS.cpy:4]
- Architecture: FR44 double-down-anytime in bjack-main.cob → [Source: docs/planning-artifacts/architecture.md#Deliberate Defects FR44]
- Story 5.4 double-down implementation notes → [Source: docs/implementation-artifacts/5-4-double-down-action.md]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — bug was pre-existing, no code changes required.

### Completion Notes List

- Verified LOOP-A at `src/bjack-main.cob:62-79`: `IF WS-FLG-A = 'D'` branch has no preceding `IF WS-PC = 2` check — rule violation confirmed present.
- Confirmed WS-PC is `05 WS-PC PIC 99` in `copy/WS-HANDS.cpy:4`.
- Wrote `test/t62-double-down-anytime.cob`: sets WS-PC=3, WS-FLG-A='D', replicates LOOP-A D-branch logic, verifies WS-BET doubles from 20 to 40 with no guard rejection. T62 passes — BUG CONFIRMED ACTIVE.
- All 7 tests (T31–T34, T61–T63) pass with no regressions.

### File List

- test/t62-double-down-anytime.cob (new)
- test/run-tests.sh (modified — added T62 section)

### Change Log

- 2026-02-28: Story 6.2 verified — double-down-anytime rule violation confirmed present in LOOP-A. Test harness t62 added and passing.
- 2026-02-28: Code review fixes — T62 assertion added (WS-BET NOT = 40 → RETURN-CODE 1); source guard added to run-tests.sh (grep for D-branch, grep-NOT for WS-PC NOT = 2); t61/t62/t63 added to .gitignore.
