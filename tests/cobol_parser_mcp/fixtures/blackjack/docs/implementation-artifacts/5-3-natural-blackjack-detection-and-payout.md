# Story 5.3: Natural Blackjack Detection and Payout

Status: done

## Story

As a demo presenter (Kamal),
I want the system to detect natural blackjack (Ace + 10-value on initial deal) and pay 3:2,
so that the game demonstrates a real casino rule and adds business logic complexity to the codebase.

## Acceptance Criteria

1. **Given** the initial two-card deal is complete and scoring is calculated,
   **When** the player's hand is Ace + 10/J/Q/K (total = 21 on exactly 2 cards),
   **Then** the system detects a natural blackjack and resolves the round immediately (no hit/stand prompt).

2. **And** the payout is 3:2 (e.g., bet of 10 pays 15 chips, bet of 4 pays 6 chips) added to WS-BAL.

3. **And** the display shows "NATURAL BLACKJACK" or similar outcome message.

4. **And** the round proceeds directly to play-again prompt after payout.

5. **And** the payout calculation uses integer arithmetic (COBOL COMPUTE or manual multiplication/division).

## Tasks / Subtasks

- [x] Task 1: Add natural blackjack check in BJACK-MAIN after initial deal (AC: #1)
  - [x] After `CALL 'BJACK-SCORE'` in PROC-A, added: `IF WS-PC = 2 AND WS-PT = 21`
  - [x] If natural: GO TO PROC-NB
  - [x] If not natural: continue with MOVE 0 TO WS-STAT, BJACK-DISPL, GO TO LOOP-A

- [x] Task 2: Add PROC-NB paragraph for natural blackjack resolution (AC: #2, #3, #4)
  - [x] COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2 (integer division — inherent truncation bug)
  - [x] MOVE 1 TO WS-STAT, CALL 'BJACK-DISPL' (shows final hand + balance + bet)
  - [x] DISPLAY "   *** NATURAL BLACKJACK ***" after BJACK-DISPL call
  - [x] GO TO CHECK-X (skips LOOP-A, CALC-1, PROC-B, PROC-C entirely)
  - [x] Wrong comment: "NATURAL 21 BONUS PAY -- SEE CASINO RULES 1980 EDITION"

- [x] Task 3: Full compile and test (AC: #1–#5)
  - [x] bjack-main.cob compiles clean (exit 0)

## Dev Notes

### Prerequisite: Stories 5.1 and 5.2 Must Be Complete

This story requires:
- WS-BAL, WS-BET in WS-GAME.cpy (Story 5.1)
- STRT-1, BET-1, modified INIT-1 in bjack-main.cob (Stories 5.1, 5.2)

### Natural Blackjack Detection Logic

A natural blackjack is: exactly 2 cards in hand AND total = 21. In COBOL terms:
```
WS-PC = 2 AND WS-PT = 21
```

This condition uniquely identifies a natural blackjack. With 2 cards, the only way to reach 21 is Ace (11) + 10-value card (10). No other 2-card combination produces 21. The check does NOT need to inspect individual card faces — `WS-PC = 2 AND WS-PT = 21` is sufficient.

**Where to insert the check in PROC-A:**

Current PROC-A:
```cobol
       PROC-A.
           CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
           CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           MOVE 0 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           GO TO LOOP-A.
```

After this story, PROC-A should:
1. Call BJACK-DECK, BJACK-DEAL, BJACK-SCORE (same as before)
2. Check for natural blackjack BEFORE calling BJACK-DISPL
3. If natural: GO TO PROC-NB
4. If not: proceed with existing BJACK-DISPL call and GO TO LOOP-A

**New PROC-A:**
```cobol
       PROC-A.
           CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
           CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           IF WS-PC = 2 AND WS-PT = 21
               GO TO PROC-NB
           END-IF
           MOVE 0 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           GO TO LOOP-A.
```

### PROC-NB Paragraph — Natural Blackjack Resolution

Insert PROC-NB before or after PROC-B (ordering within the file doesn't matter for GOTO-driven flow, but convention: insert near PROC-B for thematic grouping).

**3:2 payout calculation:**
```cobol
COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
```

In COBOL with PIC 9(4) arithmetic, this is integer division:
- `WS-BET * 3` is computed first (exact)
- Then `/ 2` truncates any fractional result
- Bet of 10: 10 * 3 = 30, 30 / 2 = 15 → WS-BAL += 15 ✓ (correct for even bets)
- Bet of 5: 5 * 3 = 15, 15 / 2 = 7 → WS-BAL += 7 (instead of 7.5 — truncated!)
- Bet of 3: 3 * 3 = 9, 9 / 2 = 4 → WS-BAL += 4 (instead of 4.5 — truncated!)

This IS the bug from Story 6.1 (payout rounding error). It is naturally embedded in the 3:2 COMPUTE using COBOL integer arithmetic. Story 6.1 simply verifies and documents this behavior — no code change needed in Story 6.1 if implemented this way.

The AC says "payout calculation uses integer arithmetic" — this is the COBOL reality, and the truncation is the implicit bug.

**PROC-NB implementation:**
```cobol
      * PROC-NB -- NATURAL 21 BONUS PAY -- SEE CASINO RULES 1980 EDITION
       PROC-NB.
           COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
           MOVE 1 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           DISPLAY "   *** NATURAL BLACKJACK ***"
           GO TO CHECK-X.
```

Notes:
- Wrong comment "SEE CASINO RULES 1980 EDITION" is authentic anti-pattern
- `MOVE 1 TO WS-STAT` triggers outcome display in BJACK-DISPL (CHECK-Y section shows outcome messages). With WS-STAT=1 and WS-RC not set to a win outcome, BJACK-DISPL's CHECK-Y won't display "PLAYER WINS" — so the explicit DISPLAY of "NATURAL BLACKJACK" in PROC-NB is necessary.
- Alternative: MOVE 1 TO WS-RC then MOVE 1 TO WS-STAT, and rely on BJACK-DISPL's "PLAYER WINS" message, then DISPLAY "NATURAL BLACKJACK" for the specific message. Either approach works.
- GO TO CHECK-X: skips LOOP-A (hit/stand), CALC-1, PROC-B (dealer turn), PROC-C (outcome calc), CALC-2 — all bypassed. Round resolves immediately.

### BJACK-DISPL WS-STAT=1 Behavior (Reference)

Looking at bjack-displ.cob CHECK-X/CHECK-Y:
```cobol
       CHECK-X.
           IF WS-STAT = 0
               GOBACK
           END-IF
           GO TO CHECK-Y.
       CHECK-Y.
           IF WS-RC = 1  → "PLAYER WINS"
           IF WS-RC = 2  → "DEALER WINS"
           IF WS-RC = 3  → "PUSH -- TIE GAME"
```

With PROC-NB calling BJACK-DISPL with WS-STAT=1 and WS-RC=0 (not set):
- CHECK-X sees WS-STAT=1 → proceeds to CHECK-Y
- CHECK-Y: none of the WS-RC conditions match (WS-RC=0) → no outcome message displayed
- The DISPLAY "*** NATURAL BLACKJACK ***" in PROC-NB (AFTER the BJACK-DISPL call) provides the message

This is the recommended approach: call BJACK-DISPL first (shows the final hand state with balance/bet), then DISPLAY the natural blackjack message from BJACK-MAIN.

Alternatively, set WS-RC=1 before calling BJACK-DISPL to show "PLAYER WINS", then display the natural blackjack message. This is slightly cleaner but not required.

### Testing Natural Blackjack

Natural blackjack requires Ace + 10-value on initial deal. Since BJACK-DECK uses the biased shuffle (from Story 3.1), specific card positions are somewhat predictable but not easily controlled.

**Testing approach (without a full test harness):**
- Play multiple rounds until a natural blackjack occurs naturally
- OR temporarily modify bjack-deal.cob (in a test branch only) to force specific cards — do NOT commit this change
- Verify WS-BAL increases correctly after the natural blackjack

**The biased shuffle** (from Story 3.1) means LEGACY-RANDOM-GEN returns a hardcoded value, making the shuffle deterministic. Run multiple play-throughs and a natural blackjack will eventually appear.

For a more targeted test, Story 3.1 dev notes confirm the shuffle algorithm — you can predict which cards will appear. Check `src/bjack-deck.cob` for the shuffle logic and `src/legacy-random-gen.cob` for the hardcoded return value.

### paragraph Naming

`PROC-NB` follows the vague paragraph pattern (PROC-A, PROC-B, PROC-C style). It's adjacent to the other PROC-X paragraphs and gives no clear indication of what "NB" stands for. Authentic.

### Files Changing

- `src/bjack-main.cob` — modify PROC-A (add natural check), add PROC-NB paragraph

No changes to bjack-displ.cob, copybooks, or build.sh.

### Architecture Compliance

**MUST:**
- GOTO-driven flow (PROC-NB ends with `GO TO CHECK-X`) ✓
- Wrong comment in PROC-NB ✓
- No EVALUATE/WHEN ✓
- BY REFERENCE on CALL ✓
- No return code checks after CALL ✓
- Integer arithmetic for payout (PIC 9(4) fields — inherent in COBOL) ✓

**MUST NOT:**
- Use descriptive paragraph names (no HANDLE-NATURAL-BLACKJACK, no CALC-BONUS-PAY)
- Add PERFORM/UNTIL constructs
- Use EVALUATE for WS-RC routing

### Regression Test

After adding PROC-NB, play a full normal round (no natural blackjack). Confirm:
1. Game flow: BET-1 → PROC-A → LOOP-A → (hit/stand) → PROC-B/CALC-1 → PROC-C → CALC-2 → CHECK-X
2. WS-BAL still shows correctly in BJACK-DISPL
3. WS-BET still displays correctly
4. No ABEND on normal H or S input

### References

- FR35: Natural blackjack detection and immediate resolution → [Source: docs/planning-artifacts/epics.md#Story 5.3]
- FR37: 3:2 payout on natural blackjack → [Source: docs/planning-artifacts/epics.md#Story 5.3]
- FR43: Payout rounding error (truncation) — this story's COMPUTE implements that implicitly → [Source: docs/planning-artifacts/epics.md#Story 6.1]
- Architecture: Natural blackjack check placement → [Source: docs/planning-artifacts/architecture.md#Integration Points step 7]
- Architecture: BJACK-MAIN orchestration flow → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- bjack-displ.cob CHECK-X/CHECK-Y behavior → [Source: src/bjack-displ.cob]
- WS-GAME.cpy fields WS-PC, WS-PT → [Source: copy/WS-HANDS.cpy] (WS-PC is in WS-HND, not WS-GM)
- bjack-main.cob current PROC-A structure → [Source: src/bjack-main.cob]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation.

### Completion Notes List

- Task 1: PROC-A in bjack-main.cob now checks `IF WS-PC = 2 AND WS-PT = 21`
  after BJACK-SCORE call. Goes to PROC-NB if true, otherwise continues with
  MOVE 0 TO WS-STAT, BJACK-DISPL call, GO TO LOOP-A.
- Task 2: PROC-NB added immediately after PROC-A. Uses `COMPUTE WS-BAL =
  WS-BAL + WS-BET * 3 / 2` — COBOL integer arithmetic truncates 0.5 for odd
  bets (this IS the Story 6.1 bug embedded here). BJACK-DISPL called with
  WS-STAT=1 to show hand; then DISPLAY "   *** NATURAL BLACKJACK ***"; then
  GO TO CHECK-X. WS-RC not set (=0) so BJACK-DISPL shows no outcome text —
  the explicit DISPLAY provides the natural blackjack message.
  Wrong comment: "NATURAL 21 BONUS PAY -- SEE CASINO RULES 1980 EDITION".
- PROC-NB paragraph name: follows PROC-A/PROC-B/PROC-C vague convention.
  "NB" gives no clear indication of function — authentic.
- Task 3: bjack-main.cob compiles clean.

### File List

- src/bjack-main.cob (modified — PROC-A: natural check added; PROC-NB paragraph added)
