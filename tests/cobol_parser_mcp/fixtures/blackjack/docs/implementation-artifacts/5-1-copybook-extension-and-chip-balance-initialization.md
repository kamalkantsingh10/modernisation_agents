# Story 5.1: Copybook Extension and Chip Balance Initialization

Status: done

## Story

As a developer,
I want WS-GAME.cpy extended with chip balance and bet amount fields, and BJACK-MAIN updated to initialize and manage chip state,
so that the betting data contract is established for all modules and the player starts each session with 100 chips.

## Acceptance Criteria

1. **Given** the existing WS-GAME.cpy copybook,
   **When** WS-GAME.cpy is inspected,
   **Then** it contains a chip balance field (WS-BAL, PIC 9(4)) and a bet amount field (WS-BET, PIC 9(4)) with cryptic field names.

2. **And** BJACK-MAIN initializes WS-BAL to 100 at session start (not per-round — balance persists across rounds).

3. **And** WS-BAL persists across rounds without reset.

4. **And** the session ends with a "YOU ARE BROKE" message when WS-BAL reaches zero (FR39).

5. **And** all modules still compile and link without errors after the copybook change.

6. **And** the game still completes a full round without abnormal termination.

## Tasks / Subtasks

- [x] Task 1: Extend WS-GAME.cpy with WS-BAL and WS-BET (AC: #1)
  - [x] Add `05 WS-BAL PIC 9(4).` inside 01 WS-GM group
  - [x] Add `05 WS-BET PIC 9(4).` inside 01 WS-GM group
  - [x] Add wrong/outdated comment above the new fields

- [x] Task 2: Add STRT-1 session-start paragraph to BJACK-MAIN (AC: #2, #3)
  - [x] Insert STRT-1 as the NEW first paragraph of PROCEDURE DIVISION (before INIT-1)
  - [x] STRT-1: `MOVE 100 TO WS-BAL`, then `GO TO INIT-1`
  - [x] PROCEDURE DIVISION entry falls into STRT-1 first (one-time session init)

- [x] Task 3: Modify INIT-1 to preserve WS-BAL across rounds (AC: #3)
  - [x] Replace `MOVE ZEROS TO WS-GM` with explicit resets of individual fields (NOT WS-BAL)
  - [x] Reset: WS-FLG-A, WS-FLG-B, WS-RC, WS-PT, WS-DT, WS-STAT, WS-BET (zero each round)
  - [x] WS-BAL must NOT be touched in INIT-1 — it persists
  - [x] INIT-1 still ends with `GO TO PROC-A` (changed to BET-1 in Story 5.2)

- [x] Task 4: Add broke check to CHECK-X (AC: #4)
  - [x] Before the play-again prompt, check `IF WS-BAL = 0`
  - [x] If broke: DISPLAY "   YOU ARE BROKE", then STOP RUN
  - [x] Use GOTO-driven flow consistent with existing CHECK-X paragraph style

- [x] Task 5: Full compile and test (AC: #5, #6)
  - [x] All modules affected by WS-GAME.cpy change compile clean (exit 0)
  - [x] bjack-main.cob, bjack-displ.cob, bjack-dealer.cob, bjack-score.cob all OK

## Dev Notes

### CRITICAL: The Core Problem — Separating Session Init from Round Reset

The current INIT-1 does `MOVE ZEROS TO WS-GM`, which resets ALL game state every round. After extending WS-GAME.cpy with WS-BAL, this would zero the chip balance on every play-again loop — destroying persistence.

**Solution: Two-phase initialization.**

Add STRT-1 as the PROCEDURE DIVISION entry point (first paragraph):
- STRT-1 runs once at session start, sets WS-BAL=100, then falls through to INIT-1
- INIT-1 resets per-round state only (WS-BAL excluded)
- CHECK-X still jumps to INIT-1 for play-again (bypasses STRT-1 → WS-BAL preserved)

### Exact WS-GAME.cpy Changes

**Current file** (`copy/WS-GAME.cpy`):
```cobol
      * GAME STATE FLAGS AND TOTALS -- SINGLE PLAYER MODE ONLY 1981
      * UPDATED 02/86 FOR MULTI-PLAYER SUPPORT -- ABANDONED
       01 WS-GM.
          05 WS-FLG-A        PIC X.
          05 WS-FLG-B        PIC X.
          05 WS-RC           PIC 9.
          05 WS-PT           PIC 999.
          05 WS-DT           PIC 999.
          05 WS-STAT         PIC 9.
```

**Add these two fields** (at the end of WS-GM group, before the blank line):
```cobol
          05 WS-BAL          PIC 9(4).
          05 WS-BET          PIC 9(4).
```

Add a wrong comment above them (consistent with architecture authenticity requirement):
```cobol
      * CHIP COUNTERS -- ADDED FOR TOURNAMENT MODE 1988
          05 WS-BAL          PIC 9(4).
          05 WS-BET          PIC 9(4).
```
(No tournament mode exists — the comment is factually wrong per architecture pattern rules.)

### Exact BJACK-MAIN Changes

**Current PROCEDURE DIVISION** (`src/bjack-main.cob`):
```cobol
       PROCEDURE DIVISION.
       INIT-1.
           MOVE ZEROS TO WS-HND
           MOVE ZEROS TO WS-GM
           MOVE SPACES TO WS-AM
           GO TO PROC-A.
```

**New PROCEDURE DIVISION:**
```cobol
       PROCEDURE DIVISION.
       STRT-1.
           MOVE 100 TO WS-BAL
           GO TO INIT-1.
       INIT-1.
           MOVE ZEROS TO WS-HND
           MOVE ZERO TO WS-FLG-A
           MOVE ZERO TO WS-FLG-B
           MOVE ZERO TO WS-RC
           MOVE ZERO TO WS-PT
           MOVE ZERO TO WS-DT
           MOVE ZERO TO WS-STAT
           MOVE ZERO TO WS-BET
           MOVE SPACES TO WS-AM
           GO TO PROC-A.
```

Note: `MOVE ZEROS TO WS-GM` is removed. Each field is now reset individually. WS-BAL is deliberately NOT in the INIT-1 reset list.

### Broke Check in CHECK-X

**Current CHECK-X:**
```cobol
       CHECK-X.
           DISPLAY "   PLAY AGAIN? (Y/N):"
           ACCEPT WS-FLG-B
           IF WS-FLG-B = 'Y'
               GO TO INIT-1
           END-IF
           STOP RUN.
```

**New CHECK-X (add broke check BEFORE play-again prompt):**
```cobol
       CHECK-X.
           IF WS-BAL = 0
               DISPLAY "   YOU ARE BROKE"
               STOP RUN
           END-IF
           DISPLAY "   PLAY AGAIN? (Y/N):"
           ACCEPT WS-FLG-B
           IF WS-FLG-B = 'Y'
               GO TO INIT-1
           END-IF
           STOP RUN.
```

Note: At this point in the sprint, payout logic doesn't exist yet (Story 5.5). WS-BAL will not actually decrease yet. The broke check is infrastructure — it will trigger once Story 5.5 adds payout calculations that can reduce WS-BAL to 0.

### Modules Affected by WS-GAME.cpy Change

All modules that COPY WS-GAME will auto-pick up the new fields at compile time:
- `src/bjack-main.cob` — COPY WS-GAME (all three copybooks)
- `src/bjack-displ.cob` — COPY WS-GAME in LINKAGE SECTION
- `src/bjack-dealer.cob` — COPY WS-GAME

Modules that do NOT copy WS-GAME (no impact):
- `src/bjack-deck.cob` — COPY WS-DECK only
- `src/bjack-deal.cob` — COPY WS-DECK, COPY WS-HANDS only
- `src/bjack-score.cob` — COPY WS-HANDS, COPY WS-GAME

Wait — bjack-score.cob does COPY WS-GAME. It will also auto-pick up the new fields. No code change needed in bjack-score.cob, but it must be recompiled.

**build.sh already recompiles all modules** — no change to build.sh needed.

### Variable Naming Rules (Architecture Compliance)

- `WS-BAL` and `WS-BET` are specified by name in the architecture document. Use exactly these names.
- `STRT-1` follows the vague paragraph naming pattern (PROC-A, CALC-1, CHECK-X style)
- No descriptive names like `SESSION-INIT` or `CHIP-BALANCE`

### Architecture Compliance

**MUST:**
- COPY WS-DECK, COPY WS-HANDS, COPY WS-GAME in WORKING-STORAGE SECTION of bjack-main.cob (already present)
- BY REFERENCE on all CALL statements (no change to existing CALLs)
- GOTO-driven flow in STRT-1 and CHECK-X
- At least one wrong comment in new code
- STOP RUN in BJACK-MAIN (root program — correct, not GOBACK)

**MUST NOT:**
- Use EVALUATE/WHEN
- Use descriptive paragraph names (no INITIALIZE-SESSION, no CHECK-BALANCE)
- Add error checking after any CALL statement
- Reset WS-BAL in INIT-1

### Only Files Changing

- `copy/WS-GAME.cpy` — add WS-BAL and WS-BET fields with wrong comment
- `src/bjack-main.cob` — add STRT-1 paragraph, modify INIT-1, modify CHECK-X

All other modules recompile unchanged via build.sh.

### Regression Check

After this story, the game should behave identically to pre-Epic-5 behavior (no visible difference to user yet — no bet prompt, no balance display). The STRT-1 change is internal. The CHECK-X broke check will not trigger because WS-BAL starts at 100 and no payout logic yet modifies it.

If WS-BAL somehow equals 0 after session start (shouldn't happen), investigate INIT-1 — confirm WS-BAL is not being zeroed there.

### Previous Story Context

The last story implemented was 3.5 (Epic 3 complete). Commit: `5cf9e4b Implement Epic 3: Deliberate Defects (Stories 3.1–3.5)`.

Key patterns from Epic 3 stories:
- Story 3.5 confirmed bjack-main.cob paragraph structure: INIT-1, PROC-A, LOOP-A, CALC-1, PROC-B, PROC-C, CALC-2, CHECK-X
- Story 3.5 confirmed WS-FLG-A is PIC X, WS-GM is the group holding all game state
- Dev agents have used GOTO-driven flow consistently — continue this pattern

### References

- FR33: Player starts with 100 chips → [Source: docs/planning-artifacts/epics.md#Story 5.1]
- FR38: Chip balance persists across rounds → [Source: docs/planning-artifacts/epics.md#Story 5.1]
- FR39: Session ends at zero balance → [Source: docs/planning-artifacts/epics.md#Story 5.1]
- Architecture: WS-BAL, WS-BET in WS-GAME.cpy → [Source: docs/planning-artifacts/architecture.md#Data Architecture]
- Architecture: BJACK-MAIN orchestrator, INIT-1 flow → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Architecture: Naming patterns WS-XX-Y → [Source: docs/planning-artifacts/architecture.md#Naming Patterns]
- Existing bjack-main.cob structure → [Source: src/bjack-main.cob]
- Existing WS-GAME.cpy → [Source: copy/WS-GAME.cpy]
- Story 3.5 dev notes (paragraph structure confirmation) → [Source: docs/implementation-artifacts/3-5-no-input-validation-on-hit-stand-prompt.md#Dev Notes]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation.

### Completion Notes List

- Task 1: Added WS-BAL PIC 9(4) and WS-BET PIC 9(4) to WS-GM group in
  copy/WS-GAME.cpy with wrong comment "CHIP COUNTERS -- ADDED FOR
  TOURNAMENT MODE 1988" (no tournament mode exists).
- Task 2: Added STRT-1 as first paragraph of PROCEDURE DIVISION in
  bjack-main.cob. MOVE 100 TO WS-BAL, GO TO INIT-1. Session init runs
  once; play-again loop (CHECK-X → INIT-1) bypasses STRT-1 preserving
  WS-BAL across rounds (AC#3).
- Task 3: Replaced MOVE ZEROS TO WS-GM with individual MOVE ZERO TO each
  field (WS-FLG-A, WS-FLG-B, WS-RC, WS-PT, WS-DT, WS-STAT, WS-BET).
  WS-BAL deliberately excluded. INIT-1 final GO TO is PROC-A (changed to
  BET-1 in Story 5.2 per that story's task 1).
- Task 4: Added IF WS-BAL = 0 broke check at top of CHECK-X before the
  play-again prompt. DISPLAY "   YOU ARE BROKE" then STOP RUN.
- Task 5: All 4 modules using WS-GAME.cpy compile clean (exit 0,
  _FORTIFY_SOURCE warnings expected and ignored).

### File List

- copy/WS-GAME.cpy (modified — WS-BAL and WS-BET fields added to WS-GM)
- src/bjack-main.cob (modified — STRT-1 added, INIT-1 changed, CHECK-X broke check added)
