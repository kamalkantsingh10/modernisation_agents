# Story 2.1: Deck Module — Initialization and Shuffle

Status: review

## Story

As a developer,
I want `bjack-deck.cob` implemented with deck initialization and shuffle logic,
so that a shuffled 52-card deck is available in shared memory for all other modules to use.

## Acceptance Criteria

1. **Given** copybooks from Story 1.1 are in place,
   **When** BJACK-DECK is called by BJACK-MAIN,
   **Then** WS-DECK (WS-DK group) is populated with all 52 cards — 4 suits × 13 ranks — with correct face values in WS-CDS(1) through WS-CDS(52).

2. **Given** the deck is initialized,
   **When** the shuffle procedure runs,
   **Then** the deck order is non-sequential after initialization (cards are shuffled, even if biased).

3. **Given** initialization and shuffle complete,
   **When** WS-CT1 is inspected,
   **Then** the deck index WS-CT1 = 1 (pointing to first card to deal; COBOL OCCURS are 1-indexed).

4. **Given** BJACK-DECK is implemented,
   **When** the shuffle procedure executes,
   **Then** BJACK-DECK calls `LEGACY-RANDOM-GEN` via `CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2` with no return-code check.

5. **Given** the module code is inspected,
   **When** code quality is evaluated,
   **Then** the module contains: GOTO-driven flow, cryptic WS-XX variable names, vague paragraph names (PROC-A/CALC-1 pattern), at least one wrong or outdated comment, zero return-code checks after CALL.

6. **Given** the module code is inspected,
   **When** language constructs are evaluated,
   **Then** the module does NOT use EVALUATE/WHEN — all conditionals use nested IF trees.

## Tasks / Subtasks

- [x] Task 1: Restructure DATA DIVISION for shared deck data via LINKAGE SECTION (AC: #1, #4)
  - [x] Remove `COPY WS-DECK.` from WORKING-STORAGE SECTION
  - [x] Add LINKAGE SECTION after WORKING-STORAGE SECTION
  - [x] Place `COPY WS-DECK.` in LINKAGE SECTION
  - [x] Change PROCEDURE DIVISION header to: `PROCEDURE DIVISION USING WS-DK.`
  - [x] Declare all local 77-level items in WORKING-STORAGE: WS-X1 PIC 9, WS-CT2 PIC 99, WS-CT3 PIC 99, WS-CT4 PIC 99, WS-X2 PIC 99, WS-TS PIC X, WS-TR PIC XX, WS-TV PIC 99

- [x] Task 2: Implement deck initialization (AC: #1, #5, #6)
  - [x] INIT-1 paragraph: initialize WS-CT2, WS-CT3, WS-CT4 to 0 or 1 as needed, GOTO PROC-A
  - [x] PROC-A paragraph: set up outer suit loop (WS-CT2 = 1), GOTO CALC-1
  - [x] CALC-1 paragraph (suit loop): IF WS-CT2 > 4 GOTO LOOP-A; set WS-CT3 = 1; GOTO CALC-2
  - [x] CALC-2 paragraph (rank loop): IF WS-CT3 > 13 GOTO CALC-3 (exit rank loop); ADD 1 TO WS-CT4; fill WS-S1(WS-CT4) with suit char based on WS-CT2 using nested IF; fill WS-RK(WS-CT4) and WS-FV(WS-CT4) based on WS-CT3 using nested IF; ADD 1 TO WS-CT3; GOTO CALC-2
  - [x] CALC-3 paragraph: ADD 1 TO WS-CT2; GOTO CALC-1
  - [x] Use nested IF trees only — no EVALUATE/WHEN
  - [x] Suit mapping: WS-CT2=1→'H', 2→'D', 3→'C', 4→'S'
  - [x] Rank/face value mapping: WS-CT3=1→('A ',11), 2→('2 ',2), 3→('3 ',3), 4→('4 ',4), 5→('5 ',5), 6→('6 ',6), 7→('7 ',7), 8→('8 ',8), 9→('9 ',9), 10→('10',10), 11→('J ',10), 12→('Q ',10), 13→('K ',10)

- [x] Task 3: Implement shuffle (AC: #2, #4, #5)
  - [x] LOOP-A paragraph: MOVE 1 TO WS-CT2; GOTO LOOP-B
  - [x] LOOP-B paragraph (shuffle loop): IF WS-CT2 > 52 GOTO CHECK-X; CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2 (NO return-code check); perform 3-step card swap WS-CDS(WS-CT2) ↔ WS-CDS(WS-X2) using WS-TS/WS-TR/WS-TV; ADD 1 TO WS-CT2; GOTO LOOP-B

- [x] Task 4: Set deck index and exit (AC: #3)
  - [x] CHECK-X paragraph: MOVE 1 TO WS-CT1; GOBACK

- [x] Task 5: Verify anti-pattern compliance (AC: #5, #6)
  - [x] At least 1 GOTO per paragraph (loop structure provides many)
  - [x] All local WORKING-STORAGE names are cryptic (WS-CT2, WS-CT3, WS-X2, WS-TS, WS-TR, WS-TV)
  - [x] All paragraph names are vague (INIT-1, PROC-A, CALC-1, CALC-2, CALC-3, LOOP-A, LOOP-B, CHECK-X)
  - [x] At least 1 wrong/outdated comment in the module
  - [x] Zero return-code checks after any CALL
  - [x] No EVALUATE/WHEN anywhere in the file
  - [x] No SECTIONS in PROCEDURE DIVISION

- [x] Task 6: Compile validation
  - [x] Run `cobc -c -I copy/ src/bjack-deck.cob` — must produce zero COBOL errors
  - [x] `_FORTIFY_SOURCE` GCC warning is expected and acceptable (GnuCOBOL 3.1.2 on Ubuntu Noble — exit code still 0)

## Dev Notes

### CRITICAL: Shared Data Via LINKAGE SECTION (Most Likely Disaster Point)

**The `COPY WS-DECK.` statement MUST go in the LINKAGE SECTION, NOT WORKING-STORAGE.**

If `COPY WS-DECK.` is placed in WORKING-STORAGE, BJACK-DECK initializes its own private local copy of the deck. BJACK-MAIN's WS-DK remains empty — the game cannot deal any cards. This is the single most critical mistake to avoid.

**Correct DATA DIVISION structure:**

```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 9.
           77 WS-CT2         PIC 99.
           77 WS-CT3         PIC 99.
           77 WS-CT4         PIC 99.
           77 WS-X2          PIC 99.
           77 WS-TS          PIC X.
           77 WS-TR          PIC XX.
           77 WS-TV          PIC 99.
       LINKAGE SECTION.
           COPY WS-DECK.
       PROCEDURE DIVISION USING WS-DK.
```

**BJACK-MAIN (Story 2.6) will call BJACK-DECK as:**
```cobol
       CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
```
This passes BJACK-MAIN's WS-DK by address. Every write to WS-DK inside BJACK-DECK directly modifies BJACK-MAIN's data. When BJACK-DECK GOBACKs, BJACK-MAIN's WS-DK contains the initialized, shuffled deck.

### CRITICAL: GOBACK Not STOP RUN

BJACK-DECK is a subprogram called by BJACK-MAIN. It MUST use `GOBACK` to return control to BJACK-MAIN. `STOP RUN` terminates the entire run unit — the game would exit immediately after the first deck shuffle. The existing stub has `STOP RUN` — this MUST be replaced with `GOBACK`.

### Deck Initialization — Full Card Table

Populate WS-CDS(1) through WS-CDS(52) in suit order. Each card sets WS-S1(n), WS-RK(n), WS-FV(n):

**WS-S1 (PIC X) — suit character:** H, D, C, S

**WS-RK (PIC XX) — rank:** Ranks MUST be padded to 2 characters.
- Single-char ranks: `'A '`, `'2 '`, `'3 '`, `'4 '`, `'5 '`, `'6 '`, `'7 '`, `'8 '`, `'9 '`, `'J '`, `'Q '`, `'K '`
- Two-char rank: `'10'` (exact fit, no padding needed)
- **CRITICAL:** MOVE `'A'` to WS-RK(n) (PIC XX) would produce `'A '` automatically. MOVE `'10'` would produce `'10'`. This is correct COBOL behavior.

**WS-FV (PIC 99) — face value:**
- Ace (WS-CT3=1): 11 — BJACK-SCORE adjusts to 1 if player total > 21
- 2–9 (WS-CT3=2–9): face value equals rank number
- 10 (WS-CT3=10): 10
- J, Q, K (WS-CT3=11–13): 10

**Suit order by WS-CT2:**
- WS-CT2 = 1 → WS-S1 = 'H', positions 1–13
- WS-CT2 = 2 → WS-S1 = 'D', positions 14–26
- WS-CT2 = 3 → WS-S1 = 'C', positions 27–39
- WS-CT2 = 4 → WS-S1 = 'S', positions 40–52

### Deck Index: WS-CT1 = 1 (Not 0)

After shuffle, set `MOVE 1 TO WS-CT1`. COBOL OCCURS tables are 1-indexed — WS-CDS(0) is invalid and will cause undefined behavior or ABEND. The epics AC says "reset to 0" which is imprecise — use 1 to point to the first valid card position.

**BJACK-DEAL (Story 2.2) contract:** BJACK-DEAL will deal the card at WS-CDS(WS-CT1) and then ADD 1 TO WS-CT1. Starting at 1 makes WS-CDS(WS-CT1) immediately usable.

### Shuffle Algorithm — LEGACY-RANDOM-GEN Interface

LEGACY-RANDOM-GEN (Story 1.2) is already implemented. It always returns 7 via its LINKAGE parameter LS-R1 (PIC 99). BJACK-DECK receives this value into WS-X2 (PIC 99 — matching type):

```cobol
       CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2
```
After the CALL, WS-X2 = 7 always. **Do NOT add an IF RETURN-CODE check** — zero return-code checks is an architectural mandate.

**Effect of always-7 return:** Every shuffle iteration swaps WS-CDS(WS-CT2) with WS-CDS(7). When WS-CT2 = 7, the swap is a no-op (swapping with itself). For all other positions, the card at position 7 is repeatedly exchanged. This produces a predictable, non-random deck — the deliberate bias required by Epic 3 (Story 3.1). The game still runs correctly on normal input.

**3-step card swap implementation:**
```cobol
       MOVE WS-S1(WS-CT2) TO WS-TS
       MOVE WS-RK(WS-CT2) TO WS-TR
       MOVE WS-FV(WS-CT2) TO WS-TV
       MOVE WS-S1(WS-X2)  TO WS-S1(WS-CT2)
       MOVE WS-RK(WS-X2)  TO WS-RK(WS-CT2)
       MOVE WS-FV(WS-X2)  TO WS-FV(WS-CT2)
       MOVE WS-TS         TO WS-S1(WS-X2)
       MOVE WS-TR         TO WS-RK(WS-X2)
       MOVE WS-TV         TO WS-FV(WS-X2)
```

### Paragraph Structure (Full Skeleton)

```cobol
      * BJACK-DECK -- CARD MANAGEMENT ROUTINE
      * WRITTEN 01/12/84 -- UPDATED 06/88 FOR NEW DECK SIZE
      * UPDATED 05/89 FOR NEW DECK PROTOCOL
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DECK.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 9.
           77 WS-CT2         PIC 99.
           77 WS-CT3         PIC 99.
           77 WS-CT4         PIC 99.
           77 WS-X2          PIC 99.
           77 WS-TS          PIC X.
           77 WS-TR          PIC XX.
           77 WS-TV          PIC 99.
       LINKAGE SECTION.
           COPY WS-DECK.
       PROCEDURE DIVISION USING WS-DK.
       INIT-1.
           MOVE 0 TO WS-CT2
           MOVE 0 TO WS-CT3
           MOVE 0 TO WS-CT4
           GO TO PROC-A.
       PROC-A.
           MOVE 1 TO WS-CT2
           GO TO CALC-1.
       CALC-1.
           IF WS-CT2 > 4
               GO TO LOOP-A
           END-IF
           MOVE 1 TO WS-CT3
           GO TO CALC-2.
       CALC-2.
           IF WS-CT3 > 13
               GO TO CALC-3
           END-IF
           ADD 1 TO WS-CT4
           [suit nested IF block setting WS-S1(WS-CT4)]
           [rank/value nested IF block setting WS-RK(WS-CT4) WS-FV(WS-CT4)]
           ADD 1 TO WS-CT3
           GO TO CALC-2.
       CALC-3.
           ADD 1 TO WS-CT2
           GO TO CALC-1.
       LOOP-A.
           MOVE 1 TO WS-CT2
           GO TO LOOP-B.
       LOOP-B.
           IF WS-CT2 > 52
               GO TO CHECK-X
           END-IF
           CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2
           [3-step card swap WS-CDS(WS-CT2) <-> WS-CDS(WS-X2)]
           ADD 1 TO WS-CT2
           GO TO LOOP-B.
       CHECK-X.
           MOVE 1 TO WS-CT1
           GOBACK.
```

**Paragraph naming rules (NO descriptive names):**
- `INIT-1` not `INIT-DECK`
- `PROC-A` not `SETUP-LOOP`
- `CALC-1` not `SUIT-LOOP`
- `CALC-2` not `FILL-CARD`
- `CALC-3` not `NEXT-SUIT`
- `LOOP-A` not `START-SHUFFLE`
- `LOOP-B` not `SHUFFLE-LOOP`
- `CHECK-X` not `DONE-SHUFFLE`

### Wrong/Outdated Comment Requirement

At minimum, keep the existing header comments (already wrong — "UPDATED 06/88 FOR NEW DECK SIZE" is meaningless). Add one more, e.g.:
```cobol
      * UPDATED 05/89 FOR NEW DECK PROTOCOL
```
(There is no deck protocol. The comment describes nothing real.)

### Local WORKING-STORAGE Variables — All 77-Level

Use `77` level for all local independent items (not under any group):
- `WS-X1` (PIC 9) — unused carry-over from stub; leave as dead field (authentic anti-pattern)
- `WS-CT2` (PIC 99) — outer loop counter (suit 1–4, then shuffle 1–52)
- `WS-CT3` (PIC 99) — inner loop counter (rank 1–13)
- `WS-CT4` (PIC 99) — card fill index (1–52, incremented as each card is placed)
- `WS-X2` (PIC 99) — receives return from LEGACY-RANDOM-GEN (always 7)
- `WS-TS` (PIC X) — temp suit for card swap
- `WS-TR` (PIC XX) — temp rank for card swap
- `WS-TV` (PIC 99) — temp face value for card swap

### Architecture Compliance (From architecture.md Enforcement Guidelines)

**MUST:**
- `COPY WS-DECK.` in LINKAGE SECTION
- `PROCEDURE DIVISION USING WS-DK.`
- All local WORKING-STORAGE names: WS-XX pattern (WS-CT2, WS-X2, etc.)
- All paragraph names: vague (PROC-A, CALC-1, LOOP-B, CHECK-X pattern)
- At least 1 GOTO per module (loop structure provides many)
- `CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-X2` (BY REFERENCE, no exceptions)
- Zero return-code checks after any CALL
- At least 1 wrong/outdated comment
- Exit with `GOBACK` (NOT `STOP RUN`)

**MUST NOT:**
- EVALUATE/WHEN anywhere in the file
- Descriptive variable names (WS-SUIT-COUNTER, WS-CARD-INDEX = failures)
- SECTIONS in PROCEDURE DIVISION
- Return-code checks after CALL
- STOP RUN (terminates entire run unit)
- Descriptive paragraph names (FILL-DECK, SHUFFLE-CARDS = failures)

### GnuCOBOL Compilation Notes (Inherited from Stories 1.1 and 1.2)

- **Compile command:** `cobc -c -I copy/ src/bjack-deck.cob` (run from project root)
- **`_FORTIFY_SOURCE` warning:** GnuCOBOL 3.1.2 on Ubuntu Noble emits a GCC-level warning on every compilation — not a COBOL error. Exit code remains 0. Ignore this warning.
- **77-level items:** Valid for independent local variables declared after COPY statements. Each needs `77` level prefix, not `05`.
- **COPY in LINKAGE SECTION:** GnuCOBOL accepts `COPY WS-DECK.` in LINKAGE SECTION. This is valid COBOL syntax.
- **Subscripting with 77-level vars:** `WS-CDS(WS-CT2)` where WS-CT2 is PIC 99 is valid — GnuCOBOL accepts data-name subscripts.

### Project Structure Notes

- **Only file changing:** `src/bjack-deck.cob` — complete rewrite of PROCEDURE DIVISION and restructure of DATA DIVISION
- **Copybooks:** `copy/WS-DECK.cpy` — read-only, do NOT modify
- **build.sh:** No changes — compile command for bjack-deck.cob is already in build.sh as `cobc -c -I copy/ src/bjack-deck.cob`
- **No new files** created in this story

### Downstream Dependencies (Critical for Story Sequencing)

- **Story 2.2 (BJACK-DEAL):** Reads cards from WS-CDS using WS-CT1 as the deal pointer. Requires WS-CT1 = 1 and WS-CDS(1–52) fully populated after BJACK-DECK returns. Depends entirely on this story being correct.
- **Story 2.6 (BJACK-MAIN):** Calls `CALL 'BJACK-DECK' USING BY REFERENCE WS-DK` at the start of each game round. Must match the PROCEDURE DIVISION USING signature established here.
- **Epic 3 / Story 3.1:** The always-7 return from LEGACY-RANDOM-GEN creates the biased shuffle (FR21). This story sets up that bias. Story 3.1 will add the dead code paragraph to this same file — do NOT add unreachable paragraphs now (that's Story 3.1's work).

### References

- Epics: Story 2.1 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 2.1]
- Architecture: BY REFERENCE calling convention → [Source: docs/planning-artifacts/architecture.md#Inter-Module Communication]
- Architecture: COPY statement placement per module → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
- Architecture: Naming patterns (WS-XX-Y, PROC-A) → [Source: docs/planning-artifacts/architecture.md#Naming Patterns]
- Architecture: Enforcement guidelines (MUST/MUST NOT) → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Architecture: Data flow (game round sequence step 2) → [Source: docs/planning-artifacts/architecture.md#Integration Points]
- Architecture: BJACK-DECK internal call to LEGACY-RANDOM-GEN → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- Story 1.1: Canonical copybook field names (WS-CT1, WS-CDS, WS-S1, WS-RK, WS-FV) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]
- Story 1.2: LEGACY-RANDOM-GEN LINKAGE interface (LS-R1 PIC 99, hardcoded return = 7) → [Source: docs/implementation-artifacts/1-2-middleware-stubs-and-build-pipeline-validation.md#LINKAGE SECTION Pattern for Middleware Stubs]
- Story 1.2: GnuCOBOL link fix (cobc -x must compile from source, not .o) → [Source: docs/implementation-artifacts/1-2-middleware-stubs-and-build-pipeline-validation.md#Debug Log References]
- Story 1.1: GnuCOBOL debug notes (_FORTIFY_SOURCE, 77-level items) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Debug Log References]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- Fixed column-72 overflow in fixed-format COBOL: 13-level nested IF for rank/value was truncating tokens beyond col 72. Resolved by splitting the rank tree at WS-CT3 < 8 — left branch handles ranks 1-7 (6 deep), right branch handles ranks 8-13 (5 deep). Max MOVE statement ends at col 70.

### Completion Notes List

- Implemented complete `src/bjack-deck.cob` rewrite: COPY WS-DECK in LINKAGE SECTION, PROCEDURE DIVISION USING WS-DK, 8 77-level local vars in WORKING-STORAGE.
- Deck init: GOTO-driven nested loops (INIT-1→PROC-A→CALC-1→CALC-2→CALC-3) populate all 52 cards in suit order (H×13, D×13, C×13, S×13) with correct ranks and face values via nested IF trees only.
- Shuffle: LOOP-A→LOOP-B iterates positions 1-52, calls LEGACY-RANDOM-GEN USING BY REFERENCE WS-X2 (no return-code check), performs 3-step card swap using WS-TS/WS-TR/WS-TV temporaries. WS-X2 always=7 producing deliberate bias (Epic 3 setup).
- CHECK-X: MOVE 1 TO WS-CT1; GOBACK (not STOP RUN).
- All anti-patterns verified: 10 GOTOs, 0 EVALUATE, 0 STOP RUN, 0 return-code checks, 0 PROCEDURE DIVISION SECTIONs, 2 outdated comments, cryptic names throughout.
- Full build passes: `bash build.sh` exit 0 (only expected _FORTIFY_SOURCE GCC warnings).

### File List

- src/bjack-deck.cob
