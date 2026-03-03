# Story 3.3: Ace Recalculation Failure (bjack-score.cob)

Status: done

## Story

As a developer,
I want `bjack-score.cob` modified so that the Ace recalculation logic fails when two Aces are held,
so that the scoring module has a demonstrable calculation defect in a specific hand scenario.

## Acceptance Criteria

1. **Given** `bjack-score.cob` from Story 2.3 is implemented,
   **When** a player hand contains two Aces plus a high-value card (e.g., A + A + K = 32 raw),
   **Then** the recalculation logic adjusts only one Ace (11→1), producing 22 instead of the correct 12 — the second Ace is never reduced.

2. **Given** the source code is inspected,
   **When** the Ace-adjust paragraph (CALC-2) is read,
   **Then** the defect is visible: `GO TO CALC-3` appears at the end of the adjust block instead of `GO TO CALC-2`, causing the loop to exit after one adjustment instead of continuing.

3. **Given** the same bug is applied to the dealer scoring section (CALC-5),
   **When** the dealer holds A + A + high card,
   **Then** the dealer's total is also miscalculated by the same off-by-one exit.

4. **Given** normal input (H or S) is entered during a round with no double-Ace scenario,
   **When** a full round plays through,
   **Then** the game completes without ABEND.

5. **Given** the module is compiled standalone with crafted input (two Aces + high card),
   **When** WS-PT is inspected after BJACK-SCORE returns,
   **Then** the incorrect total (22 instead of 12) is independently verifiable.

## Tasks / Subtasks

- [x] Task 1: Break Ace recalculation loop in CALC-2 (player scoring) (AC: #1, #2, #4)
  - [x] In paragraph `CALC-2`, change the final `GO TO CALC-2` to `GO TO CALC-3`
  - [x] This converts the recalculation loop into a single-pass adjustment
  - [x] Add wrong comment on CALC-2: e.g., `* CALC-2 -- ACE ADJUSTMENT LOOP (HANDLES MULTIPLE ACES)`

- [x] Task 2: Break Ace recalculation loop in CALC-5 (dealer scoring) (AC: #3, #4)
  - [x] In paragraph `CALC-5`, change the final `GO TO CALC-5` to `GO TO CHECK-X`
  - [x] This applies the same single-pass failure to dealer scoring

- [x] Task 3: Compile validation (AC: #4, #5)
  - [x] Run `cobc -c -I copy/ src/bjack-score.cob` — zero COBOL errors, exit code 0
  - [x] Run `bash build.sh` — game runs to completion on normal input (H or S)
  - [x] Verify: A + K hand scores 21 correctly (single Ace case is unaffected)
  - [x] Verify: A + A + K scores 22 (wrong — confirms bug)

## Dev Notes

### CRITICAL: Exact Changes Required

**Current CALC-2 (correct — from Story 2.3):**
```cobol
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
```

**Modified CALC-2 (with bug — single-pass exit):**
```cobol
      * CALC-2 -- ACE ADJUSTMENT LOOP (HANDLES MULTIPLE ACES)
       CALC-2.
           IF WS-X1 <= 21
               GO TO CALC-3
           END-IF
           IF WS-CT2 = 0
               GO TO CALC-3
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT2
           GO TO CALC-3.
```

**Current CALC-5 (correct — from Story 2.3):**
```cobol
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
```

**Modified CALC-5 (with bug):**
```cobol
       CALC-5.
           IF WS-X1 <= 21
               GO TO CHECK-X
           END-IF
           IF WS-CT2 = 0
               GO TO CHECK-X
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT2
           GO TO CHECK-X.
```

### Bug Behavior Analysis

**How CALC-1 works (player sum):**
- Loops 1..WS-PC, adds WS-PFV(n) to WS-X1
- For each Ace: WS-PFV(n) = 11 initially (set by BJACK-DECK), so WS-CT2 increments per Ace
- Result: WS-X1 = raw sum with all Aces at 11, WS-CT2 = number of Aces

**With two Aces + King: WS-X1 = 11 + 11 + 10 = 32, WS-CT2 = 2**

**CALC-2 behavior WITH bug:**
1. WS-X1 = 32 > 21, WS-CT2 = 2 — enters adjustment
2. SUBTRACT 10 → WS-X1 = 22, SUBTRACT 1 → WS-CT2 = 1
3. `GO TO CALC-3` — exits loop immediately, WS-PT = 22 (**WRONG**: correct is 12)

**CALC-2 behavior WITHOUT bug (correct):**
1. WS-X1 = 32 > 21, WS-CT2 = 2 — first loop
2. SUBTRACT 10 → WS-X1 = 22, WS-CT2 = 1 — `GO TO CALC-2`
3. WS-X1 = 22 > 21, WS-CT2 = 1 — second loop
4. SUBTRACT 10 → WS-X1 = 12, WS-CT2 = 0 — `GO TO CALC-2`
5. WS-X1 = 12 ≤ 21 → `GO TO CALC-3`, WS-PT = 12 (correct)

**Cases unaffected by the bug (game still functional on normal play):**
- Single Ace + anything ≤ 10: WS-X1 ≤ 21 after one adjustment or no adjustment needed → `GO TO CALC-3` works correctly in both old and new code
- No Aces: WS-CT2 = 0 → second IF exits to CALC-3 immediately (identical behavior)
- Two Aces alone (A+A = 22): one adjustment → 12. Both old and new code give 12 (only one loop needed). **Not demonstrably broken for two Aces alone.**
- **The bug is only visible with: A + A + {any card with value ≥ 1} where raw sum > 31**

**Specific triggerable scenario:**
- Player holds A + A + K: score reported as 22 (busted), correct is 12 (safe hand)
- Player or dealer would incorrectly bust when they shouldn't

**Demo value:** "The scoring loop exits after adjusting only one Ace. If you hold two Aces plus a ten, the game says you're busted at 22 — but the correct score is 12. One GO TO and the whole scoring algorithm breaks."

### Existing Paragraph Structure (bjack-score.cob)

All paragraphs — only CALC-2 and CALC-5 change:
1. `INIT-1` — resets WS-X1, WS-CT1, WS-CT2, GO TO PROC-A
2. `PROC-A` — resets locals, starts player loop from CT1=1, GO TO CALC-1
3. `CALC-1` — player card sum loop (WS-PFV); counts Aces in WS-CT2; GO TO CALC-2
4. `CALC-2` — **BUG HERE** — player Ace adjustment; GO TO CALC-3 (was CALC-2)
5. `CALC-3` — writes WS-PT, GO TO PROC-B
6. `PROC-B` — resets locals, starts dealer loop from CT1=1, GO TO CALC-4
7. `CALC-4` — dealer card sum loop (WS-DFV); counts dealer Aces; GO TO CALC-5
8. `CALC-5` — **BUG HERE** — dealer Ace adjustment; GO TO CHECK-X (was CALC-5)
9. `CHECK-X` — writes WS-DT, GOBACK

### IMPORTANT: WS-CT2 vs WS-CT3

In bjack-score.cob:
- `WS-CT2` (PIC 99) — counts Aces for **player** scoring (PROC-A/CALC-1/CALC-2)
- In PROC-B, `WS-CT2` is **reset to 0** and reused for the dealer Ace count in CALC-4/CALC-5

This re-use is authentic period COBOL anti-pattern (variable reuse for different purposes). Do NOT add a separate WS-CT3 variable — use WS-CT2 as-is for both player and dealer sections.

### Working-Storage Variables (bjack-score.cob)

- `WS-X1` (PIC 999) — running sum accumulator (reset in PROC-A and PROC-B)
- `WS-CT1` (PIC 99) — card loop counter (1..WS-PC for player, 1..WS-DC for dealer)
- `WS-CT2` (PIC 99) — Ace counter (reset in both PROC-A and PROC-B; reused for player then dealer)

LINKAGE SECTION: `COPY WS-HANDS` (WS-HND, WS-PC, WS-PHD, WS-PFV, WS-DC, WS-DHD, WS-DFV) and `COPY WS-GAME` (WS-GM, WS-PT, WS-DT, WS-RC, WS-STAT, WS-FLG-A, WS-FLG-B).

### Copybook Reference

WS-GAME.cpy fields written by BJACK-SCORE:
- `WS-PT` (PIC 999) — player total written at CALC-3
- `WS-DT` (PIC 999) — dealer total written at CHECK-X

### Anti-Pattern Compliance (Unchanged from Story 2.3)

All anti-patterns preserved:
- GOTO-driven flow throughout
- Cryptic WS-XX names (WS-X1, WS-CT1, WS-CT2)
- Vague paragraph names (CALC-1 through CALC-5, CHECK-X)
- Wrong/outdated comments preserved (`* CALC-1 -- SUMS VALUES USING LOOKUP TABLE` — no lookup table)
- New wrong comment on CALC-2: "HANDLES MULTIPLE ACES" (it doesn't after the fix)
- Zero return-code checks (no CALLs in this module)
- No EVALUATE/WHEN
- No SECTIONS
- GOBACK not STOP RUN

### Architecture Compliance

**MUST:**
- `COPY WS-HANDS` then `COPY WS-GAME` in LINKAGE SECTION
- `PROCEDURE DIVISION USING WS-HND WS-GM`
- GOBACK (not STOP RUN)
- Changes confined to CALC-2 and CALC-5 only

**MUST NOT:**
- Change CALC-1, CALC-3, CALC-4, PROC-A, PROC-B, CHECK-X
- Add new variables
- Use EVALUATE/WHEN
- Fix either bug — both must remain

### Only File Changing

- `src/bjack-score.cob` — two single-line changes: CALC-2's `GO TO CALC-2` → `GO TO CALC-3`; CALC-5's `GO TO CALC-5` → `GO TO CHECK-X`
- No new files created, no copybook changes

### References

- FR23: Ace recalculation failure when two Aces held → [Source: docs/planning-artifacts/epics.md#Story 3.3]
- Architecture: Bug rules (no ABEND on normal input) → [Source: docs/planning-artifacts/architecture.md#Process Patterns]
- Story 2.3 Dev Agent Record: existing bjack-score.cob implementation → [Source: docs/implementation-artifacts/2-3-scoring-module-hand-value-calculation.md#Dev Agent Record]
- WS-GAME.cpy: WS-PT, WS-DT field definitions → [Source: copy/WS-GAME.cpy]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Task 1: In `CALC-2` (player Ace adjust), changed `GO TO CALC-2` → `GO TO CALC-3`. Added wrong comment `* CALC-2 -- ACE ADJUSTMENT LOOP (HANDLES MULTIPLE ACES)`. Loop now exits after one adjustment — A+A+K scores 22 instead of 12.
- Task 2: In `CALC-5` (dealer Ace adjust), changed `GO TO CALC-5` → `GO TO CHECK-X`. Same single-pass failure applied to dealer scoring.
- Task 3: `cobc -c -I copy/ src/bjack-score.cob` exit 0. `bash build.sh` exit 0 — game launched, no ABEND. Only `_FORTIFY_SOURCE` GCC warnings (expected).

### File List

- src/bjack-score.cob (modified — CALC-2: `GO TO CALC-2` → `GO TO CALC-3`, wrong comment added; CALC-5: `GO TO CALC-5` → `GO TO CHECK-X`)
- test/t33-score-ace.cob (created — standalone harness confirming A+A+K scores 022 not 012, satisfying AC5)

### Cross-Story Interaction Note (Stories 3.3 + 3.4)

bjack-main.cob PROC-B calls BJACK-DEALER then immediately calls BJACK-SCORE. BJACK-DEALER's inline CALC-3 performs a correct multi-pass Ace adjustment when computing its own hit/stand decisions (WS-CT3 loop). However, the subsequent BJACK-SCORE call overwrites WS-DT using CALC-5's single-pass bug. If the dealer drew to a hand requiring multiple Ace reductions, the displayed WS-DT (via BJACK-DISPL) may differ from the value BJACK-DEALER used internally — compounding the Story 3.3 and 3.4 defects in an observable way.
