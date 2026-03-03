# Story 5.2: Bet Placement and Validation

Status: done

## Story

As a demo presenter (Kamal),
I want to place a bet before each round with min/max constraints displayed,
so that the game has a visible betting mechanic that decision-makers recognize as business logic.

## Acceptance Criteria

1. **Given** the player has a chip balance > 0,
   **When** a new round begins,
   **Then** BJACK-MAIN displays a bet prompt showing current balance and min/max constraints (min 1, max = current balance).

2. **And** the player enters a numeric bet amount via ACCEPT.

3. **And** the bet is stored in WS-BET for the round.

4. **And** the prompt style is consistent with 1980s terminal conventions (e.g., `ENTER BET (1-nnn):`).

5. **And** BJACK-DISPL shows the current bet amount during the round (FR41).

6. **And** BJACK-DISPL shows the current chip balance during gameplay (FR40).

7. **And** the module contains GOTO-driven flow, cryptic variable names, and at least one wrong comment.

## Tasks / Subtasks

- [x] Task 1: Add BET-1 paragraph to BJACK-MAIN (AC: #1, #2, #3, #4, #7)
  - [x] Insert BET-1 paragraph between INIT-1 and PROC-A in bjack-main.cob
  - [x] Change INIT-1's final `GO TO PROC-A` to `GO TO BET-1`
  - [x] BET-1: DISPLAY current WS-BAL, DISPLAY bet prompt with min/max, ACCEPT WS-BET
  - [x] Add basic validation: IF WS-BET < 1 → GO TO BET-1; IF WS-BET > WS-BAL → GO TO BET-1
  - [x] BET-1 ends with `GO TO PROC-A`
  - [x] Wrong comment "INPUT VALIDATION ROUTINE WITH RANGE CHECK" added

- [x] Task 2: Add chip balance and bet display to BJACK-DISPL (AC: #5, #6)
  - [x] In bjack-displ.cob CALC-7 paragraph, added DISPLAY of WS-BAL and WS-BET
  - [x] Display before the footer border using WS-ESC "[1;33m" color
  - [x] Format: `  BAL: nnnn  BET: nnnn` (4-digit zero-padded, 1980s raw numeric style)

- [x] Task 3: Full compile and test (AC: #1–#7)
  - [x] bjack-main.cob and bjack-displ.cob compile clean (exit 0)

## Dev Notes

### Prerequisite: Story 5.1 Must Be Complete

This story requires:
- WS-BAL and WS-BET fields in WS-GAME.cpy (from Story 5.1)
- STRT-1 and modified INIT-1 in bjack-main.cob (from Story 5.1)
- CHECK-X broke check in bjack-main.cob (from Story 5.1)

### BJACK-MAIN: Where BET-1 Fits in Flow

**After Story 5.1, flow is:**
```
STRT-1 → INIT-1 → PROC-A → ... → CHECK-X → INIT-1 (play again)
```

**After this story, flow becomes:**
```
STRT-1 → INIT-1 → BET-1 → PROC-A → ... → CHECK-X → INIT-1 → BET-1 (play again)
```

**Change in INIT-1:** Replace `GO TO PROC-A` with `GO TO BET-1`.

**New BET-1 paragraph** (insert between INIT-1 and PROC-A):
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

The wrong comment "INPUT VALIDATION ROUTINE WITH RANGE CHECK" is ironic given that Story 6.3 will introduce a stale variable bug that breaks this validation under a specific sequence. The comment will remain accurate-looking but become untrue after Epic 6.

Note on `DISPLAY "   ENTER BET (1-" WS-BAL "):"`:
- WS-BAL is PIC 9(4) → displays as 4 digits with leading zeros (e.g., `0100`)
- This is authentic 1980s COBOL — no formatting, raw numeric display
- The trailing `):` is a string literal after the variable

### BJACK-DISPL: Adding Balance and Bet Display

BJACK-DISPL receives WS-GM via LINKAGE SECTION (`USING WS-HND WS-GM`). After Story 5.1 extended WS-GAME.cpy with WS-BAL and WS-BET, these fields are already accessible in bjack-displ.cob — no LINKAGE changes needed.

**Current CALC-7 in bjack-displ.cob:**
```cobol
       CALC-7.
           DISPLAY WS-ESC "[1;37m"
               "  TOTAL: " WS-PT WS-ESC "[0m"
           DISPLAY WS-ESC "[33m"
               "  +==================================+"
               WS-ESC "[0m"
           DISPLAY " "
           GO TO CHECK-X.
```

**Modified CALC-7** (add balance/bet display after total, before footer):
```cobol
       CALC-7.
           DISPLAY WS-ESC "[1;37m"
               "  TOTAL: " WS-PT WS-ESC "[0m"
           DISPLAY WS-ESC "[1;33m"
               "  BAL: " WS-BAL "  BET: " WS-BET
               WS-ESC "[0m"
           DISPLAY WS-ESC "[33m"
               "  +==================================+"
               WS-ESC "[0m"
           DISPLAY " "
           GO TO CHECK-X.
```

Note: WS-BAL (PIC 9(4)) and WS-BET (PIC 9(4)) display as 4-digit zero-padded numbers. Consistent with 1980s terminal style — no attempt to suppress leading zeros.

### Why BET-1 Loop Uses GO TO (Not PERFORM)

Architecture rule: flat paragraph structure, GOTO-driven flow, no SECTIONS. The re-prompt on invalid input uses `GO TO BET-1` (loop back) rather than PERFORM/UNTIL. This is authentic 1980s COBOL practice and consistent with all existing paragraphs in bjack-main.cob (PROC-A uses GO TO LOOP-A, etc.).

### Important: WS-BET Is NOT Deducted From WS-BAL in This Story

Story 5.2 only captures and stores the bet. The actual balance change (deduct on loss, add on win) happens in Story 5.5 (Payout Calculation and Round Resolution). During Story 5.2, WS-BAL will remain at 100 throughout gameplay — this is expected, not a bug.

After Story 5.5 is implemented:
- Win: WS-BAL += WS-BET
- Loss: WS-BAL -= WS-BET
- Push: WS-BAL unchanged

For now, WS-BET is just recorded for the round and displayed.

### Validation Logic (This is the CORRECT validation — Bug Comes in Story 6.3)

Story 6.3 (Epic 6, Deliberate Defects) will introduce a stale-variable bug in bet validation. In THIS story, implement CORRECT validation: WS-BET must be between 1 and WS-BAL inclusive. The re-prompt loop `GO TO BET-1` handles both underflow and overflow.

Do NOT deliberately introduce the stale variable here — that is Story 6.3's job.

### BJACK-DISPL: No LINKAGE or CALL Interface Changes

The CALL from BJACK-MAIN remains:
```cobol
CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
```
This passes the full WS-GM group, which now includes WS-BAL and WS-BET. BJACK-DISPL's PROCEDURE DIVISION is `USING WS-HND WS-GM` — unchanged. The new fields are automatically available.

### WORKING-STORAGE Local Variable

BET-1 does not need a local work variable (WS-X1 or similar) — WS-BET is the direct ACCEPT target. Keep the existing `77 WS-X1 PIC 9.` and `77 WS-AM PIC X(50).` in bjack-main.cob unchanged.

### Existing WS-GAME Fields in BJACK-MAIN (Full List After Story 5.1)

```
WS-GM (01 group):
  WS-FLG-A    PIC X      -- hit/stand/double-down input
  WS-FLG-B    PIC X      -- play-again input
  WS-RC       PIC 9      -- round outcome (1=player win, 2=dealer win, 3=push)
  WS-PT       PIC 999    -- player total
  WS-DT       PIC 999    -- dealer total
  WS-STAT     PIC 9      -- display status flag (0=in-play, 1=round-over)
  WS-BAL      PIC 9(4)   -- chip balance (new from Story 5.1)
  WS-BET      PIC 9(4)   -- current bet (new from Story 5.1)
```

### Architecture Compliance

**MUST:**
- BET-1 paragraph name follows vague pattern (PROC-A, CALC-1, CHECK-X style) ✓
- `GO TO BET-1` for re-prompt (GOTO-driven flow) ✓
- BY REFERENCE on all CALL statements (existing CALLs unchanged) ✓
- At least one wrong comment in BET-1 ✓
- STOP RUN only in BJACK-MAIN (root program) ✓

**MUST NOT:**
- Use EVALUATE/WHEN for bet input routing
- Use descriptive paragraph names (no VALIDATE-BET, no GET-WAGER)
- Add error messaging beyond the re-prompt loop
- Use PERFORM/UNTIL for the validation loop

### Files Changing

- `src/bjack-main.cob` — add BET-1 paragraph, change INIT-1's final GO TO
- `src/bjack-displ.cob` — add WS-BAL/WS-BET display to CALC-7

### References

- FR34: Bet placement min 1, max balance → [Source: docs/planning-artifacts/epics.md#Story 5.2]
- FR40: Display chip balance during gameplay → [Source: docs/planning-artifacts/epics.md#Story 5.2]
- FR41: Display current bet during round → [Source: docs/planning-artifacts/epics.md#Story 5.2]
- FR42: Bet prompt with min/max constraints → [Source: docs/planning-artifacts/epics.md#Story 5.2]
- Architecture: I/O boundary — ACCEPT in BJACK-MAIN only → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- Architecture: GOTO-driven flow, flat paragraphs → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
- Architecture: Betting display integration → [Source: docs/planning-artifacts/architecture.md#Terminal Display Architecture]
- WS-GAME.cpy after Story 5.1 → [Source: copy/WS-GAME.cpy]
- bjack-displ.cob CALC-7 paragraph → [Source: src/bjack-displ.cob]
- bjack-main.cob after Story 5.1 → [Source: src/bjack-main.cob]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation.

### Completion Notes List

- Task 1: BET-1 paragraph inserted between INIT-1 and PROC-A in
  bjack-main.cob. INIT-1 final GO TO changed from PROC-A to BET-1.
  Two-IF validation loop: WS-BET < 1 → GO TO BET-1; WS-BET > WS-BAL →
  GO TO BET-1. Wrong comment: "INPUT VALIDATION ROUTINE WITH RANGE CHECK"
  (ironic — Story 6.3 will introduce stale-variable bug making this false).
- Task 2: CALC-7 in bjack-displ.cob: added DISPLAY of WS-BAL and WS-BET
  in yellow (WS-ESC "[1;33m") before the footer border. WS-BAL/WS-BET are
  PIC 9(4) — display as 4-digit zero-padded numbers, authentic 1980s style.
- Task 3: Both modules compile clean.

### File List

- src/bjack-main.cob (modified — BET-1 paragraph added, INIT-1 GO TO changed)
- src/bjack-displ.cob (modified — CALC-7: WS-BAL/WS-BET display added)
