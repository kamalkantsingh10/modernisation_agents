# Story 2.6: Main Game Loop — Full Playable Round

Status: review

## Story

As a demo presenter (Kamal),
I want `bjack-main.cob` implemented as the game orchestrator and `./build.sh` fully wired to compile and launch the complete application,
so that I can run a complete Blackjack round — deal, hit/stand, dealer turn, outcome, play-again — from a single command.

## Acceptance Criteria

1. **Given** all 5 game modules from Stories 2.1–2.5 are implemented and copybooks are locked,
   **When** `./build.sh` is executed on a fresh Ubuntu machine with GnuCOBOL 3.1+,
   **Then** all 8 modules compile and link without errors and the game launches within 5 seconds of command entry.

2. **Given** the game is running,
   **When** a round begins,
   **Then** BJACK-MAIN calls modules in sequence: BJACK-DECK → BJACK-DEAL (initial) → BJACK-SCORE → BJACK-DISPL → player hit/stand loop → BJACK-DEALER → BJACK-SCORE (final) → BJACK-DISPL (outcome) → CASINO-AUDIT-LOG → play-again prompt.

3. **Given** the player hit/stand prompt is displayed,
   **When** the player is prompted,
   **Then** the prompt uses period-accurate 1980s terminal conventions (e.g. `   ENTER H OR S:`).

4. **Given** the player enters `S` (stand),
   **When** BJACK-MAIN processes input,
   **Then** BJACK-MAIN proceeds to the dealer turn (BJACK-DEALER call) without dealing another card.

5. **Given** the player enters `H` (hit),
   **When** BJACK-MAIN processes input,
   **Then** BJACK-MAIN calls BJACK-DEAL (hit), BJACK-SCORE, BJACK-DISPL and returns to the hit/stand prompt (unless player has busted: WS-PT > 21).

6. **Given** the player's hand total exceeds 21 (WS-PT > 21),
   **When** BJACK-MAIN detects bust,
   **Then** BJACK-MAIN skips the dealer turn and jumps directly to outcome determination (WS-RC = 2 dealer wins).

7. **Given** the dealer turn is complete,
   **When** BJACK-MAIN determines the outcome,
   **Then** WS-RC is set: 1 (player wins), 2 (dealer wins), 3 (push) — per comparison of WS-PT and WS-DT, with bust checks.

8. **Given** ACCEPT for hit/stand input is used,
   **When** the code is inspected,
   **Then** ACCEPT appears ONLY in BJACK-MAIN — no other module uses ACCEPT. No input validation exists on hit/stand (FR24).

9. **Given** all CALL statements are inspected,
   **When** the code is evaluated,
   **Then** every CALL uses `BY REFERENCE` — no exceptions. No return-code checks appear after any CALL in any module.

10. **Given** a complete round ends with play-again prompt,
    **When** the player enters `Y`,
    **Then** BJACK-MAIN resets game state (MOVE ZEROS TO WS-HND; MOVE ZEROS TO WS-GM) and starts a new round without recompilation or perceptible lag.

## Tasks / Subtasks

- [x] Task 1: Update DATA DIVISION (AC: #2, #9)
  - [x] Keep `COPY WS-DECK.`, `COPY WS-HANDS.`, `COPY WS-GAME.` in WORKING-STORAGE SECTION (root program — NOT LINKAGE)
  - [x] Add local 77-level items: WS-AM PIC X(50)
  - [x] Keep WS-X1 PIC 9 (already in stub — leave in place as anti-pattern noise)
  - [x] No LINKAGE SECTION and no USING clause on PROCEDURE DIVISION (root program)

- [x] Task 2: Implement new-round initialization (AC: #10)
  - [x] INIT-1 paragraph: MOVE ZEROS TO WS-HND; MOVE ZEROS TO WS-GM; MOVE SPACES TO WS-AM; GO TO PROC-A
  - [x] PROC-A paragraph: call shuffle/deal/score/display sequence; GO TO LOOP-A

- [x] Task 3: Implement initial round setup calls (AC: #2)
  - [x] PROC-A: CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
  - [x] PROC-A: CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
  - [x] PROC-A: CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
  - [x] PROC-A: MOVE 0 TO WS-STAT; CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
  - [x] PROC-A: GO TO LOOP-A

- [x] Task 4: Implement player hit/stand loop (AC: #3, #4, #5, #8)
  - [x] LOOP-A paragraph: DISPLAY period-accurate prompt "   ENTER H OR S:"; ACCEPT WS-FLG-A (no validation); IF WS-FLG-A = 'S' GO TO PROC-B; GO TO CALC-1
  - [x] CALC-1 paragraph (player hits): CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND; CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM; MOVE 0 TO WS-STAT; CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM; IF WS-PT > 21 GO TO PROC-C; GO TO LOOP-A

- [x] Task 5: Implement dealer turn (AC: #2, #6)
  - [x] PROC-B paragraph: CALL 'BJACK-DEALER' USING BY REFERENCE WS-DK WS-HND WS-GM; CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM; GO TO PROC-C

- [x] Task 6: Implement outcome determination (AC: #6, #7)
  - [x] PROC-C paragraph: nested IF tree to set WS-RC:
    - IF WS-PT > 21: MOVE 2 TO WS-RC; GO TO CALC-2
    - IF WS-DT > 21: MOVE 1 TO WS-RC; GO TO CALC-2
    - IF WS-PT > WS-DT: MOVE 1 TO WS-RC; GO TO CALC-2
    - IF WS-DT > WS-PT: MOVE 2 TO WS-RC; GO TO CALC-2
    - MOVE 3 TO WS-RC; GO TO CALC-2

- [x] Task 7: Implement outcome display and audit log (AC: #2)
  - [x] CALC-2 paragraph: MOVE 1 TO WS-STAT; CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM; CALL 'CASINO-AUDIT-LOG' USING BY REFERENCE WS-FLG-A WS-AM; GO TO CHECK-X

- [x] Task 8: Implement play-again loop (AC: #10)
  - [x] CHECK-X paragraph: DISPLAY "   PLAY AGAIN? (Y/N):"; ACCEPT WS-FLG-B; IF WS-FLG-B = 'Y' GO TO INIT-1; STOP RUN

- [x] Task 9: Anti-pattern compliance (AC: #9)
  - [x] All local WORKING-STORAGE names are cryptic (WS-X1, WS-AM)
  - [x] All paragraph names are vague (INIT-1, PROC-A, PROC-B, PROC-C, LOOP-A, CALC-1, CALC-2, CHECK-X)
  - [x] At least 1 wrong/outdated comment
  - [x] Zero return-code checks after every CALL (absolute rule)
  - [x] No EVALUATE/WHEN — only nested IF trees
  - [x] No SECTIONS in PROCEDURE DIVISION

- [x] Task 10: Full build validation (AC: #1)
  - [x] Run `bash build.sh` from project root — all 8 modules must compile and link
  - [x] Run the game, play a round: deal, hit (H), stand (S), verify outcome displays
  - [x] Verify play-again: enter Y, confirm new round starts; enter N, confirm game exits

## Dev Notes

### BJACK-MAIN Is the Root Program — No LINKAGE SECTION

Unlike all subprograms (BJACK-DECK, BJACK-DEAL, BJACK-SCORE, BJACK-DISPL, BJACK-DEALER), BJACK-MAIN is the **root program** (the main entry point of the run unit). It does NOT have a LINKAGE SECTION. It does NOT use `PROCEDURE DIVISION USING ...`.

- All three copybooks remain in WORKING-STORAGE SECTION (already in stub — correct)
- PROCEDURE DIVISION has no USING clause
- BJACK-MAIN uses `STOP RUN` to terminate (NOT GOBACK — only subprograms use GOBACK)

**Correct DATA DIVISION:**
```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
           COPY WS-GAME.
           77 WS-X1          PIC 9.
           77 WS-AM          PIC X(50).
       PROCEDURE DIVISION.
```

### CRITICAL: STOP RUN (Not GOBACK) in BJACK-MAIN

BJACK-MAIN is the root program. Use `STOP RUN` to terminate the run unit when the player chooses not to play again. All subprograms (BJACK-DECK, BJACK-DEAL, BJACK-SCORE, BJACK-DISPL, BJACK-DEALER, CASINO-AUDIT-LOG, LEGACY-RANDOM-GEN) use GOBACK. Only BJACK-MAIN uses STOP RUN.

### CRITICAL: New-Round State Reset

When the player chooses to play again, execution returns to INIT-1 via `GO TO INIT-1`. INIT-1 must reset all shared game state before calling PROC-A:

```cobol
       INIT-1.
           MOVE ZEROS TO WS-HND
           MOVE ZEROS TO WS-GM
           MOVE SPACES TO WS-AM
           GO TO PROC-A.
```

`MOVE ZEROS TO WS-HND` sets WS-PC=0 and WS-DC=0 (and zeroes all card arrays). This is how BJACK-DEAL detects the initial deal vs hit mode (WS-PC=0 → initial deal path).

`MOVE ZEROS TO WS-GM` clears WS-FLG-A, WS-FLG-B, WS-RC, WS-PT, WS-DT, WS-STAT.

`MOVE ZEROS TO WS-DK` is NOT needed — BJACK-DECK reinitializes and reshuffles WS-DK on every call to PROC-A.

### CALL Interfaces (All Established by Previous Stories)

Every CALL uses `BY REFERENCE`. No exceptions. Zero return-code checks after any CALL.

```cobol
       CALL 'BJACK-DECK'    USING BY REFERENCE WS-DK
       CALL 'BJACK-DEAL'    USING BY REFERENCE WS-DK WS-HND
       CALL 'BJACK-SCORE'   USING BY REFERENCE WS-HND WS-GM
       CALL 'BJACK-DISPL'   USING BY REFERENCE WS-HND WS-GM
       CALL 'BJACK-DEALER'  USING BY REFERENCE WS-DK WS-HND WS-GM
       CALL 'CASINO-AUDIT-LOG' USING BY REFERENCE WS-FLG-A WS-AM
```

**CASINO-AUDIT-LOG interface** (`src/casino-audit-log.cob`):
`PROCEDURE DIVISION USING LS-A1 LS-A2.` where LS-A1 is PIC X and LS-A2 is PIC X(50).
- Pass `WS-FLG-A` (PIC X from WS-GAME) as LS-A1 — reuse of an existing field; arbitrary choice
- Pass `WS-AM` (local 77-level PIC X(50)) as LS-A2 — local buffer
- CASINO-AUDIT-LOG is a no-op (GOBACK immediately) — the parameters are accepted but nothing happens

### WS-STAT and WS-RC Setting Rules (Contract With BJACK-DISPL)

BJACK-MAIN sets these before every BJACK-DISPL call:

**WS-STAT:**
- `MOVE 0 TO WS-STAT` before mid-game display calls (after initial deal, after each hit)
- `MOVE 1 TO WS-STAT` in CALC-2 before the outcome display call

**WS-RC:**
- Set in PROC-C after all cards are played:
  - `1` = player wins
  - `2` = dealer wins
  - `3` = push (tie)

**Outcome determination logic (nested IF, no EVALUATE):**
```cobol
       PROC-C.
           IF WS-PT > 21
               MOVE 2 TO WS-RC
               GO TO CALC-2
           END-IF
           IF WS-DT > 21
               MOVE 1 TO WS-RC
               GO TO CALC-2
           END-IF
           IF WS-PT > WS-DT
               MOVE 1 TO WS-RC
               GO TO CALC-2
           END-IF
           IF WS-DT > WS-PT
               MOVE 2 TO WS-RC
               GO TO CALC-2
           END-IF
           MOVE 3 TO WS-RC
           GO TO CALC-2.
```

Player bust is checked first (CALC-1 already GOTOs PROC-C when WS-PT > 21 after a hit, bypassing the dealer turn). Dealer bust and comparison are checked in PROC-C.

**NOTE:** When a player busts in CALC-1 (WS-PT > 21 after a hit), execution goes directly to PROC-C — skipping PROC-B (dealer turn). PROC-C then checks WS-PT > 21 first, sets WS-RC = 2, and jumps to CALC-2 for outcome display. The dealer's hand is NOT played out when the player busts. This is correct blackjack behavior.

### No Input Validation — FR24 (Specified Defect for Epic 2)

ACCEPT for hit/stand reads into WS-FLG-A. There is NO IF to validate the input:

```cobol
       LOOP-A.
           DISPLAY "   ENTER H OR S:"
           ACCEPT WS-FLG-A
           IF WS-FLG-A = 'S'
               GO TO PROC-B
           END-IF
           GO TO CALC-1.
```

If the player enters anything other than `H` or `S`, the code falls through to GO TO CALC-1 (treats all non-S input as a hit). This is the specified behavior per FR24. Do NOT add an `ELSE IF WS-FLG-A = 'H'` guard or any error branch. The absence of validation IS the defect. Epic 3 Story 3.5 formally documents this as a bug — do NOT "fix" it.

**Similarly, no validation on play-again input:**
```cobol
       CHECK-X.
           DISPLAY "   PLAY AGAIN? (Y/N):"
           ACCEPT WS-FLG-B
           IF WS-FLG-B = 'Y'
               GO TO INIT-1
           END-IF
           STOP RUN.
```

Non-Y input falls through to STOP RUN (exits). No validation needed or wanted.

### Complete Game Flow Diagram

```
INIT-1: Reset WS-HND, WS-GM, WS-AM → PROC-A
  │
PROC-A: CALL BJACK-DECK (shuffle)
        CALL BJACK-DEAL (initial deal — WS-PC=0, WS-DC=0 → 2 cards each)
        CALL BJACK-SCORE (calculate WS-PT, WS-DT)
        MOVE 0 TO WS-STAT
        CALL BJACK-DISPL (show initial state)
        → LOOP-A
  │
LOOP-A: DISPLAY "   ENTER H OR S:"
        ACCEPT WS-FLG-A (no validation)
        IF WS-FLG-A = 'S' → PROC-B
        → CALC-1
  │
CALC-1: CALL BJACK-DEAL (hit — WS-PC > 0 → deals 1 card to player)
        CALL BJACK-SCORE (recalculate WS-PT, WS-DT)
        MOVE 0 TO WS-STAT
        CALL BJACK-DISPL (show updated state)
        IF WS-PT > 21 → PROC-C (player bust)
        → LOOP-A
  │
PROC-B: CALL BJACK-DEALER (dealer draws until WS-DT >= 17)
        CALL BJACK-SCORE (authoritative final totals)
        → PROC-C
  │
PROC-C: (nested IF) set WS-RC based on WS-PT, WS-DT
        → CALC-2
  │
CALC-2: MOVE 1 TO WS-STAT
        CALL BJACK-DISPL (show final hands + outcome)
        CALL CASINO-AUDIT-LOG (no-op)
        → CHECK-X
  │
CHECK-X: DISPLAY "   PLAY AGAIN? (Y/N):"
         ACCEPT WS-FLG-B
         IF WS-FLG-B = 'Y' → INIT-1
         STOP RUN
```

### Copybook Fields Used Directly by BJACK-MAIN

**WS-DECK.cpy (`01 WS-DK`):**
- `WS-DK` — passed BY REFERENCE to BJACK-DECK and BJACK-DEAL and BJACK-DEALER

**WS-HANDS.cpy (`01 WS-HND`):**
- `WS-PC` — read to check reset (MOVE ZEROS TO WS-HND sets this to 0)
- `WS-HND` — passed BY REFERENCE to BJACK-DEAL, BJACK-SCORE, BJACK-DISPL, BJACK-DEALER

**WS-GAME.cpy (`01 WS-GM`):**
- `WS-FLG-A` — ACCEPT target for hit/stand input; also passed to CASINO-AUDIT-LOG as LS-A1
- `WS-FLG-B` — ACCEPT target for play-again input
- `WS-RC` — set by BJACK-MAIN in PROC-C (1=player, 2=dealer, 3=push)
- `WS-PT` — read by BJACK-MAIN for bust check (WS-PT > 21) and outcome comparison
- `WS-DT` — read by BJACK-MAIN for outcome comparison
- `WS-STAT` — set by BJACK-MAIN (0=mid-game, 1=end-game) before BJACK-DISPL calls
- `WS-GM` — passed BY REFERENCE to BJACK-SCORE, BJACK-DISPL, BJACK-DEALER

**Local WORKING-STORAGE (77-level):**
- `WS-X1` (PIC 9) — unused but present (dead variable; authentic anti-pattern noise)
- `WS-AM` (PIC X(50)) — audit log message buffer passed to CASINO-AUDIT-LOG as LS-A2

### Paragraph Structure (Full Skeleton)

```cobol
      * BJACK-MAIN -- MAIN GAME CONTROLLER
      * WRITTEN 01/85 -- UPDATED 05/90 FOR MULTI-PLAYER MODE
      * PROC-A -- STARTS NEW ROUND AND CHECKS HIGH SCORE TABLE
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-MAIN.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
           COPY WS-GAME.
           77 WS-X1          PIC 9.
           77 WS-AM          PIC X(50).
       PROCEDURE DIVISION.
       INIT-1.
           MOVE ZEROS TO WS-HND
           MOVE ZEROS TO WS-GM
           MOVE SPACES TO WS-AM
           GO TO PROC-A.
       PROC-A.
           CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
           CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           MOVE 0 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           GO TO LOOP-A.
       LOOP-A.
           DISPLAY "   ENTER H OR S:"
           ACCEPT WS-FLG-A
           IF WS-FLG-A = 'S'
               GO TO PROC-B
           END-IF
           GO TO CALC-1.
       CALC-1.
           CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           MOVE 0 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           IF WS-PT > 21
               GO TO PROC-C
           END-IF
           GO TO LOOP-A.
       PROC-B.
           CALL 'BJACK-DEALER' USING BY REFERENCE WS-DK WS-HND WS-GM
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           GO TO PROC-C.
       PROC-C.
           IF WS-PT > 21
               MOVE 2 TO WS-RC
               GO TO CALC-2
           END-IF
           IF WS-DT > 21
               MOVE 1 TO WS-RC
               GO TO CALC-2
           END-IF
           IF WS-PT > WS-DT
               MOVE 1 TO WS-RC
               GO TO CALC-2
           END-IF
           IF WS-DT > WS-PT
               MOVE 2 TO WS-RC
               GO TO CALC-2
           END-IF
           MOVE 3 TO WS-RC
           GO TO CALC-2.
       CALC-2.
           MOVE 1 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           CALL 'CASINO-AUDIT-LOG' USING BY REFERENCE WS-FLG-A WS-AM
           GO TO CHECK-X.
       CHECK-X.
           DISPLAY "   PLAY AGAIN? (Y/N):"
           ACCEPT WS-FLG-B
           IF WS-FLG-B = 'Y'
               GO TO INIT-1
           END-IF
           STOP RUN.
```

**Paragraph names — MUST be vague:**
- `INIT-1` not `INIT-GAME`
- `PROC-A` not `START-ROUND`
- `LOOP-A` not `PLAYER-TURN`
- `CALC-1` not `PLAYER-HIT`
- `PROC-B` not `DEALER-TURN`
- `PROC-C` not `DETERMINE-OUTCOME`
- `CALC-2` not `DISPLAY-OUTCOME`
- `CHECK-X` not `PLAY-AGAIN`

### Wrong/Outdated Comment Requirement

The stub header has period-authentic wrong comments. Keep them and use as-is:

```cobol
      * BJACK-MAIN -- MAIN GAME CONTROLLER
      * WRITTEN 01/85 -- UPDATED 05/90 FOR MULTI-PLAYER MODE
```

"MULTI-PLAYER MODE" — there is no multi-player mode. The comment is false.

Add one more wrong comment inside, already in the skeleton above:
```cobol
      * PROC-A -- STARTS NEW ROUND AND CHECKS HIGH SCORE TABLE
```
(There is no high score table. PROC-A does no such check.)

### build.sh Validation

`build.sh` was implemented in Story 1.2. It already compiles all 8 modules in the correct order and links them. With Story 2.6 complete, `bash build.sh` should:
1. Compile all 8 `.cob` files with `cobc -c -I copy/`
2. Link all `.o` files with `cobc -x`
3. Launch `./bjack` immediately

**Do NOT modify `build.sh`** unless it is broken. Check by running `bash build.sh` and verifying the game reaches the first display before the player prompt. If build.sh has issues, debug — do not add error checking (that would violate the no-error-checking architecture rule).

Expected `build.sh` structure (for reference — do not change):
```bash
cobc -c -I copy/ src/bjack-deck.cob
cobc -c -I copy/ src/bjack-deal.cob
cobc -c -I copy/ src/bjack-dealer.cob
cobc -c -I copy/ src/bjack-score.cob
cobc -c -I copy/ src/bjack-displ.cob
cobc -c -I copy/ src/casino-audit-log.cob
cobc -c -I copy/ src/legacy-random-gen.cob
cobc -c -I copy/ src/bjack-main.cob
cobc -x -o bjack bjack-main.o bjack-deck.o bjack-deal.o bjack-dealer.o \
    bjack-score.o bjack-displ.o casino-audit-log.o legacy-random-gen.o
./bjack
```

### Anti-Pattern Checklist for the Full Codebase

After this story, the full codebase must demonstrate 4+ distinct pointable examples of messiness (FR18). Inherited from all modules:
1. **Cryptic naming everywhere** — WS-CT1, WS-FLG-A, PROC-A, CALC-1 in every file
2. **GOTO spaghetti** — every module has multiple GOTOs including backward jumps
3. **Dead variables** — WS-X1 in BJACK-MAIN (never read after initialization), WS-X1 in BJACK-DISPL (never used)
4. **Wrong/outdated comments** — every module has at least one factually false comment
5. **Zero error handling** — no return-code checks, no ACCEPT validation, no bounds checking

Any code reviewer or static analysis tool will surface multiple issues on first inspection. This is the goal.

### GnuCOBOL Notes (Inherited + Root Program Specifics)

- **Compile:** `cobc -c -I copy/ src/bjack-main.cob` from project root
- **`_FORTIFY_SOURCE` warning:** Expected, exit code 0, ignore
- **Root program WORKING-STORAGE:** COPY statements in WORKING-STORAGE resolve at compile time via `-I copy/` flag — confirmed working from Story 1.2
- **ACCEPT statement:** `ACCEPT WS-FLG-A` reads one character from stdin in GnuCOBOL. User types input and presses Enter. The PIC X field receives one character. Any input longer than 1 character is truncated to the first character.
- **MOVE ZEROS TO group:** `MOVE ZEROS TO WS-HND` zeroes all PIC 9/99/999 fields and spaces out all PIC X/XX fields within WS-HND. This correctly resets all hand data for a new round.
- **STOP RUN:** Terminates the entire run unit. Correct for the root program. Confirmed: all subprograms use GOBACK; only BJACK-MAIN uses STOP RUN.

### Project Structure Notes

- **Only file changing:** `src/bjack-main.cob` — complete rewrite of stub
- **Copybooks:** `copy/WS-DECK.cpy`, `copy/WS-HANDS.cpy`, `copy/WS-GAME.cpy` — read-only, do NOT modify
- **`build.sh`:** Should NOT need modification — already handles all 8 modules from Story 1.2
- **No new files** created in this story

### Epic 3 Dependencies

The following Epic 3 stories will modify modules completed by this epic:
- Story 3.1: Modify `bjack-deck.cob` (biased shuffle + dead code)
- Story 3.2: Modify `bjack-deal.cob` (off-by-one in deal array)
- Story 3.3: Modify `bjack-score.cob` (Ace recalculation failure)
- Story 3.4: Modify `bjack-dealer.cob` (soft 17 rule violation)
- Story 3.5: `bjack-main.cob` already has the no-input-validation defect by design (FR24) — no additional modification needed for Story 3.5

### References

- Epics: Story 2.6 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 2.6]
- Architecture: BJACK-MAIN orchestrator pattern → [Source: docs/planning-artifacts/architecture.md#Communication Patterns]
- Architecture: Full game round data flow (steps 1–12) → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Architecture: All CALL patterns (BY REFERENCE) → [Source: docs/planning-artifacts/architecture.md#Format Patterns]
- Architecture: Enforcement guidelines (MUST / MUST NOT) → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Architecture: Orchestration boundary (sole orchestrator) → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- Architecture: build.sh strategy → [Source: docs/planning-artifacts/architecture.md#Infrastructure & Deployment]
- Story 1.1: Canonical copybook field names → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 2.2: BJACK-DEAL initial vs hit mode detection (WS-PC=0) → [Source: docs/implementation-artifacts/2-2-deal-module-initial-hand-distribution.md#Deal Mode Detection: Initial vs Hit]
- Story 2.4: WS-STAT and WS-RC encoding (0/1 and 1/2/3) → [Source: docs/implementation-artifacts/2-4-display-module-terminal-rendering.md#WS-STAT and WS-RC Semantics]
- casino-audit-log.cob: Interface (LS-A1 PIC X, LS-A2 PIC X(50)) → [Source: src/casino-audit-log.cob]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile/link errors.

### Completion Notes List

- Rewrote `src/bjack-main.cob` from stub to full root-program implementation.
- DATA DIVISION: kept COPY WS-DECK/WS-HANDS/WS-GAME in WORKING-STORAGE; kept WS-X1 (PIC 9, dead variable); added WS-AM (PIC X(50)) as audit log buffer. No LINKAGE SECTION (root program).
- INIT-1: MOVE ZEROS TO WS-HND, MOVE ZEROS TO WS-GM, MOVE SPACES TO WS-AM → PROC-A (resets all game state for each new round).
- PROC-A: calls BJACK-DECK, BJACK-DEAL (initial), BJACK-SCORE, sets WS-STAT=0, calls BJACK-DISPL → LOOP-A.
- LOOP-A: DISPLAY "   ENTER H OR S:", ACCEPT WS-FLG-A (no validation — FR24), IF 'S' → PROC-B else → CALC-1.
- CALC-1 (hit): BJACK-DEAL, BJACK-SCORE, WS-STAT=0, BJACK-DISPL; bust check WS-PT>21 → PROC-C; else → LOOP-A.
- PROC-B (dealer turn): BJACK-DEALER, BJACK-SCORE → PROC-C.
- PROC-C (outcome): nested IF tree sets WS-RC (bust check, dealer bust, compare totals, push) → CALC-2.
- CALC-2: WS-STAT=1, BJACK-DISPL (outcome), CASINO-AUDIT-LOG → CHECK-X.
- CHECK-X: play-again prompt; Y → INIT-1; else STOP RUN.
- All CALLs use BY REFERENCE, zero return-code checks.
- Full build: all 8 modules compile + link; game runs end-to-end (hit/stand/bust/win/dealer-bust/push/play-again all confirmed).

### File List

- src/bjack-main.cob (modified — full rewrite from stub)
