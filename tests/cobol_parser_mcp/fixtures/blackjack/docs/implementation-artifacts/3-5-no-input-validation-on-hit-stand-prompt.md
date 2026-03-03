# Story 3.5: No Input Validation on Hit/Stand Prompt (bjack-main.cob)

Status: done

## Story

As a developer,
I want `bjack-main.cob` to have no input validation on the hit/stand ACCEPT prompt,
so that unexpected input produces undefined, demonstrable behavior — a specified defect that can be shown live.

## Acceptance Criteria

1. **Given** `bjack-main.cob` from Story 2.6 is implemented,
   **When** a value other than H or S is entered at the hit/stand prompt,
   **Then** the game does not validate the input — it falls through to the hit path (CALC-1), treating any non-S input as a hit.

2. **Given** the source code is inspected,
   **When** the ACCEPT paragraph (LOOP-A) is read,
   **Then** the absence of validation is visible: there is only `IF WS-FLG-A = 'S'` — no IF for 'H', no ERR-1 paragraph, no DISPLAY of error message for invalid input.

3. **Given** a wrong comment is added to LOOP-A claiming validation exists,
   **When** the code is reviewed,
   **Then** the comment contradicts the actual behavior — the anti-pattern is amplified.

4. **Given** H or S is entered,
   **When** a full round plays through,
   **Then** the game completes without ABEND — normal input path is unaffected.

5. **Given** the ACCEPT paragraph is inspected standalone,
   **When** a non-COBOL reader reads it,
   **Then** the missing validation is clear: there is no error branch for invalid input.

## Tasks / Subtasks

- [x] Task 1: Verify existing no-validation behavior is present (AC: #1, #2)
  - [x] Confirm LOOP-A in current bjack-main.cob has only `IF WS-FLG-A = 'S'` — any non-S falls through to CALC-1 (hit)
  - [x] Confirm no ERR-1 paragraph, no validation IF for 'H', no input check exists in LOOP-A
  - [x] No code change needed for validation absence — FR24 is already satisfied by the existing LOOP-A

- [x] Task 2: Add wrong comment to LOOP-A to amplify the anti-pattern (AC: #2, #3)
  - [x] Add a comment directly above or inside `LOOP-A` claiming input is validated
  - [x] Example: `* LOOP-A -- VALIDATES INPUT AND ROUTES TO HIT OR STAND`
  - [x] The comment must be factually false (no validation exists)

- [x] Task 3: Compile validation (AC: #4)
  - [x] Run `cobc -c -I copy/ src/bjack-main.cob` — zero COBOL errors, exit code 0
  - [x] Run `bash build.sh` — game runs to completion on input H and S

## Dev Notes

### CRITICAL: The Bug Is Already Present — Verification Only

FR24 (no input validation) is satisfied by the existing LOOP-A code from Story 2.6. **Do not add validation and do not change the control flow.** The only code change in this story is adding one wrong comment.

**Current LOOP-A (from bjack-main.cob Story 2.6):**
```cobol
       LOOP-A.
           DISPLAY "   ENTER H OR S:"
           ACCEPT WS-FLG-A
           IF WS-FLG-A = 'S'
               GO TO PROC-B
           END-IF
           GO TO CALC-1.
```

**Modified LOOP-A (after this story — wrong comment added):**
```cobol
      * LOOP-A -- VALIDATES INPUT AND ROUTES TO HIT OR STAND
       LOOP-A.
           DISPLAY "   ENTER H OR S:"
           ACCEPT WS-FLG-A
           IF WS-FLG-A = 'S'
               GO TO PROC-B
           END-IF
           GO TO CALC-1.
```

**That is the entire change for this story.** One comment line added.

### Why the Existing Code Already Satisfies FR24

The LOOP-A paragraph has exactly ONE conditional: `IF WS-FLG-A = 'S'`.

- Input = 'S' → GO TO PROC-B (stand path)
- Input = 'H' → IF false, fall through → GO TO CALC-1 (hit path)
- Input = 'X' → IF false, fall through → GO TO CALC-1 (hit path — undefined behavior)
- Input = '1' → IF false, fall through → GO TO CALC-1 (hit path — undefined behavior)
- Input = '' (enter key) → IF false, fall through → GO TO CALC-1 (infinite hit loop possible)

There is no:
- `IF WS-FLG-A = 'H' GO TO CALC-1` — 'H' works by coincidence, not by design
- `ERR-1` paragraph or error display
- Any branch that rejects invalid input

**Demo value:** "ENTER H OR S. The code only checks for S. Anything else — including nothing — hits. Typo H? Works. Typo Q? Also hits. This is the original developers not bothering with validation because 'users will enter the right thing'."

### Existing bjack-main.cob Structure (Do NOT Change)

Full paragraph sequence — LOOP-A gets one comment, nothing else changes:
1. `INIT-1` — resets WS-HND, WS-GM, WS-AM, GO TO PROC-A
2. `PROC-A` — calls BJACK-DECK, BJACK-DEAL, BJACK-SCORE; sets WS-STAT=0; calls BJACK-DISPL; GO TO LOOP-A
3. `LOOP-A` — **COMMENT ADDED**; ACCEPT WS-FLG-A; IF 'S' GO TO PROC-B; else GO TO CALC-1
4. `CALC-1` — calls BJACK-DEAL (hit), BJACK-SCORE; sets WS-STAT=0; calls BJACK-DISPL; IF WS-PT > 21 GO TO PROC-C; else GO TO LOOP-A
5. `PROC-B` — calls BJACK-DEALER, BJACK-SCORE; GO TO PROC-C
6. `PROC-C` — outcome determination (WS-PT vs WS-DT comparisons, sets WS-RC); GO TO CALC-2
7. `CALC-2` — sets WS-STAT=1; calls BJACK-DISPL; calls CASINO-AUDIT-LOG; GO TO CHECK-X
8. `CHECK-X` — play again prompt; ACCEPT WS-FLG-B; IF 'Y' GO TO INIT-1; else STOP RUN

### WS-FLG-A Field Definition

`WS-FLG-A` is defined in `copy/WS-GAME.cpy`:
```
05 WS-FLG-A        PIC X.
```
It is a 1-byte field. ACCEPT reads a single character from stdin. The field is in WS-GM which is WORKING-STORAGE in BJACK-MAIN (the only module using ACCEPT).

### Working-Storage Variables Relevant to LOOP-A

- `WS-FLG-A` (from COPY WS-GAME) — the ACCEPT target, PIC X
- `WS-PT` (from COPY WS-GAME) — player total, checked in CALC-1 for bust detection

### Existing Wrong Comments (Preserved)

bjack-main.cob already has 3 wrong/outdated comments from Story 2.6:
- `* WRITTEN 01/85 -- UPDATED 05/90 FOR MULTI-PLAYER MODE` — no multi-player mode exists
- `* PROC-A -- STARTS NEW ROUND AND CHECKS HIGH SCORE TABLE` — no high score table
- (and the game header)

The new comment on LOOP-A adds a 4th: "VALIDATES INPUT AND ROUTES TO HIT OR STAND" — neither 'H' nor invalid input is validated.

### Architecture Compliance

**MUST:**
- COPY WS-DECK, COPY WS-HANDS, COPY WS-GAME in WORKING-STORAGE SECTION
- STOP RUN (BJACK-MAIN is the root program — STOP RUN is correct here, not GOBACK)
- WS-FLG-A ACCEPT in BJACK-MAIN only — no other module uses ACCEPT

**MUST NOT:**
- Add input validation (the bug is the ABSENCE of validation)
- Change LOOP-A control flow
- Use EVALUATE/WHEN

### Only File Changing

- `src/bjack-main.cob` — add one wrong comment line above/inside LOOP-A
- No new files created, no copybook changes

### References

- FR24: No input validation on hit/stand prompt → [Source: docs/planning-artifacts/epics.md#Story 3.5]
- Architecture: I/O boundary — ACCEPT in BJACK-MAIN only → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- Architecture: Bug rules → [Source: docs/planning-artifacts/architecture.md#Process Patterns]
- Story 2.6 Dev Agent Record: existing bjack-main.cob implementation → [Source: docs/implementation-artifacts/2-6-main-game-loop-full-playable-round.md#Dev Agent Record]
- WS-GAME.cpy: WS-FLG-A field (PIC X, 1-byte) → [Source: copy/WS-GAME.cpy]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — trivial change, zero compile errors.

### Completion Notes List

- Task 1: Confirmed `LOOP-A` in bjack-main.cob contains only `IF WS-FLG-A = 'S'`. No ERR-1, no 'H' branch, no validation. FR24 already satisfied by existing code from Story 2.6 — no control-flow change needed.
- Task 2: Added `* LOOP-A -- VALIDATES INPUT AND ROUTES TO HIT OR STAND` comment directly above `LOOP-A`. Comment is factually false — code only checks for 'S'; any other input (including 'H') falls through to CALC-1 by coincidence.
- Task 3: `cobc -c -I copy/ src/bjack-main.cob` exit 0. Full link exit 0. No ABEND.
- **Related Undocumented Defect — WS-FLG-B (bjack-main.cob:74)**: The play-again prompt `ACCEPT WS-FLG-B` in CHECK-X has the identical validation gap. `IF WS-FLG-B = 'Y'` is the only branch — any non-Y input (empty, typo, garbage) silently falls through and executes `STOP RUN`, terminating the game with no feedback. This is a second unvalidated ACCEPT in bjack-main.cob not covered by any Epic 3 story. Preserved as-is; it is part of the authentic anti-pattern and could be noted during a demo ("the developers didn't validate any input, including the play-again prompt").

### File List

- src/bjack-main.cob (modified — added wrong comment above LOOP-A paragraph)
