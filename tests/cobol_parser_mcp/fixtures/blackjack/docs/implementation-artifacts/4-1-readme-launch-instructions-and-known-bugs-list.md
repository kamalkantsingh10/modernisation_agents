# Story 4.1: README — Launch Instructions and Known Bugs List

Status: done

## Story

As a demo presenter (Kamal),
I want a README at the project root with step-by-step compile/run instructions and a complete known bugs list,
so that I can set up the demo on any fresh machine and know exactly which code locations to highlight for each of the 9 deliberate defects.

## Acceptance Criteria

1. **Given** the completed application from Epics 1–3 and 5–6,
   **When** Kamal reads the README,
   **Then** the compile/run section provides step-by-step instructions sufficient to get from a fresh Ubuntu install with GnuCOBOL 3.1+ to a running game — no assumed knowledge.

2. **When** Kamal reads the known bugs section,
   **Then** all 9 bugs are listed with: the bug name, the module/file it lives in, the paragraph or line where it appears, and a plain-English description of what it does wrong.

3. **And** each bug entry contains enough detail for Kamal to locate it in the code during a live demo without searching.

4. **And** the README itself follows 1980s mainframe conventions — plain text format, no markdown rendering, terse style, no decorative formatting.

5. **And** the README does NOT accurately describe all code behavior — at least one statement should be outdated or incorrect (consistent with the project's authenticity requirements).

## Tasks / Subtasks

- [x] Task 1: Write compile/run section in plain-text README (AC: #1, #4)
  - [x] Step-by-step Ubuntu prerequisite check (GnuCOBOL 3.1+)
  - [x] Single-command build and launch: `./build.sh`
  - [x] Include at least one inaccurate/outdated statement (e.g., wrong GnuCOBOL version, wrong flag)
  - [x] Plain text only — no markdown headers, bullets, or decorative formatting

- [x] Task 2: Write known bugs section — all 9 bugs (AC: #2, #3)
  - [x] Bug 1: Biased shuffle — bjack-deck.cob, LOOP-B paragraph (LEGACY-RANDOM-GEN always returns 7; confirmed from 3.1)
  - [x] Bug 2: Dead code paragraph — bjack-deck.cob, DEAD-1 paragraph (unreachable after GOBACK; confirmed from 3.1 — not CHECK-X)
  - [x] Bug 3: Off-by-one in deal array — bjack-deal.cob, CALC-3 paragraph (confirmed from 3.2 — not CALC-1)
  - [x] Bug 4: Ace recalculation failure (two Aces) — bjack-score.cob, CALC-2 paragraph
  - [x] Bug 5: Soft 17 rule violation — bjack-dealer.cob, LOOP-A paragraph
  - [x] Bug 6: No input validation on hit/stand/double-down — bjack-main.cob, LOOP-A paragraph
  - [x] Bug 7: Payout rounding error on natural blackjack (3:2 truncation) — bjack-main.cob, paragraph TBD (Epic 5 not done; placeholder noted in README)
  - [x] Bug 8: Double-down-anytime rule violation — bjack-main.cob, LOOP-A (placeholder; Epic 6 not done)
  - [x] Bug 9: Bet-over-balance from stale variable — bjack-main.cob, BET-1 (placeholder; Epic 6 not done)
  - [x] Each entry: bug name, file, paragraph name, plain-English explanation of the defect

- [x] Task 3: Apply 1980s style to entire README (AC: #4, #5)
  - [x] Uppercase section headers, no markdown
  - [x] Terse, imperative language
  - [x] Inaccurate comment embedded (e.g., "TESTED ON GNUCOBOL 2.0 AND ABOVE" — wrong version)

## Dev Notes

### CRITICAL: Implement This Story LAST (After Epics 5 and 6)

The AC precondition is "Given the completed application from Epics 1–3 and 5–6". This story should be implemented **after Story 6.3 is done**, so all 9 bugs are confirmed implemented and their exact paragraph names are known.

Do NOT implement this story before Epics 5 and 6 are complete. The bug entries require accurate paragraph names from bjack-main.cob after all betting logic and defects are added.

If implementing out of order, document bugs 7–9 based on the spec with placeholder paragraph names and update after Epic 6 completes.

### File to Modify

**Only file:** `README` (project root, no extension)

The current content is `PLACEHOLDER`. Replace entirely. Do not touch `README.md` (that is the GitHub-facing file; this project's 1980s-style README is the no-extension file).

### Required README Format

1980s mainframe plain text. Rules:
- ALL CAPS section headers, separated by lines of dashes
- No markdown (no `#`, `*`, `-`, backticks)
- Width: max 72 characters per line (punched card era)
- Terse imperative style: "INSTALL GNUCOBOL. RUN BUILD SCRIPT. PLAY GAME."
- No decorative ASCII art
- At least one factually wrong or outdated statement (authenticity requirement — FR17)

Example structure:
```
BLACKJACK -- CASINO SYSTEM  REV 3.1  1985
----------------------------------------

SYSTEM REQUIREMENTS
  GNUCOBOL 2.2 OR LATER ON UNIX/LINUX SYSTEM   <-- intentionally wrong version
  STANDARD C COMPILER REQUIRED FOR LINK STEP

BUILD AND RUN
  1. VERIFY GNUCOBOL INSTALLED: COBC --VERSION
  2. COMPILE AND LAUNCH: ./BUILD.SH
  NOTE -- SCRIPT RUNS CLEAN ON MOST SYSTEMS. NO WARRANTY.

KNOWN BUGS AND DEFECTS
  ...
```

### Bug Paragraph Names (as of Epic 3 completion)

Paragraph names confirmed from implemented source files:

**bjack-deck.cob:**
- Shuffle loop: PROC-A (calls LEGACY-RANDOM-GEN with hardcoded return → biased distribution)
- Dead code: CHECK-X paragraph (named but never PERFORMed or GOTOed from any live path)

**bjack-deal.cob:**
- Deal loop: CALC-1 (off-by-one in loop bound or index — verify exact line in file after Epic 3 story 3.2)

**bjack-score.cob:**
- Ace adjust: CALC-2 paragraph (only adjusts first Ace, not second — two-Ace hand gets wrong total)

**bjack-dealer.cob:**
- Dealer hit/stand decision: LOOP-A paragraph (soft 17 handling violates standard casino rule)

**bjack-main.cob (Epic 3 state):**
- LOOP-A: `IF WS-FLG-A = 'S'` only — any non-S falls through to CALC-1 (no validation)

**bjack-main.cob (after Epics 5–6 — verify paragraph names before writing):**
- Natural blackjack payout: paragraph added in Story 5.3 (exact name TBD by dev)
- Double-down-anytime: LOOP-A — 'D' accepted with no WS-PC = 2 check (Story 6.2)
- Stale bet variable: BET-1 paragraph (Story 6.3 — stale local variable used in validation)

**ACTION REQUIRED:** Before writing bug 7–9 entries, grep bjack-main.cob for the exact paragraph names added in Stories 5.3, 6.2, 6.3.

### Plain-English Bug Descriptions (Examples)

Write for a non-COBOL audience — Kamal will narrate these live:

- Biased shuffle: "The shuffle calls a random-number module that always returns the same value. Cards never truly randomize — they cluster in predictable patterns every game."
- Dead code: "A named paragraph exists in the deck module that is never called from anywhere in the program. It's dead weight from a feature that was abandoned."
- Off-by-one: "The deal loop starts (or ends) at the wrong array position. The defect is in the loop index — classic off-by-one error."
- Ace recalculation: "When two Aces are held, only the first is adjusted from 11 to 1. A two-Ace hand scores 12 instead of 2."
- Soft 17: "The dealer either hits or stands incorrectly on a soft 17 (Ace + 6 = 17 with Ace counted as 11). Standard casino rule violated."
- No validation: "The hit/stand/double-down prompt has one check: if you entered S, stand. Anything else — including garbage input — falls through and hits."
- Payout truncation: "Natural blackjack 3:2 payout uses integer division. A bet of 5 pays 7 chips, not 7.5. Odd bet amounts silently shortchange the player."
- Double-down-anytime: "The 'D' option is offered at every action prompt regardless of card count. Standard rules allow double down on initial two-card hand only."
- Stale balance: "Bet validation checks a balance variable that was captured before the last payout. Under a specific win-then-bet sequence, the player can wager more chips than they actually have."

### Architecture Compliance

- README is a plain file, not a .md or .txt — no extension (FR19: project structure reflects 1980s mainframe convention)
- README must contain at least one inaccurate statement per FR17 (1980s code style)
- No COBOL changes in this story — documentation only

### References

- FR31: README compile/run instructions → [Source: docs/planning-artifacts/epics.md#Story 4.1]
- FR32: README known bugs list (9 bugs) → [Source: docs/planning-artifacts/epics.md#Story 4.1]
- FR17: Identifiable 1980s-era code style including wrong comments → [Source: docs/planning-artifacts/architecture.md#Comment Style]
- FR19: Project structure reflects 1980s mainframe anti-patterns → [Source: docs/planning-artifacts/architecture.md#Infrastructure & Deployment]
- Bug paragraph names: confirmed from story dev notes in docs/implementation-artifacts/3-1-*.md through 3-5-*.md
- Betting bug specs: [Source: docs/planning-artifacts/epics.md#Epic 6]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — documentation-only story, no COBOL changes.

### Completion Notes List

- Task 1: Wrote SYSTEM REQUIREMENTS and BUILD AND RUN sections in
  1980s plain-text format. Intentionally wrong version "GNUCOBOL 2.0
  OR LATER" (actual requirement is 3.1+) satisfies FR17/AC#5.
  Max line width 72 chars enforced. Zero markdown characters (verified
  via grep).
- Task 2: All 9 bugs documented with FILE, PARAGRAPH, and plain-English
  description. Paragraph name corrections vs story spec:
  * Bug 1 LOOP-B (not PROC-A) — PROC-A initializes deck, LOOP-B calls
    LEGACY-RANDOM-GEN; confirmed from src/bjack-deck.cob and 3.1 story.
  * Bug 2 DEAD-1 (not CHECK-X) — DEAD-1 is placed after GOBACK in
    CHECK-X and is unreachable; confirmed from 3.1 story dev notes.
  * Bug 3 CALC-3 (not CALC-1) — off-by-one is in CALC-3 hit path;
    confirmed from 3.2 story dev notes.
  * Bugs 7-9 use placeholder paragraph names per dev notes (Epics 5-6
    not yet implemented). Placeholders noted inline in README.
- Task 3: ALL CAPS headers, dashes separators, terse imperative style
  applied throughout. "TESTED ON GNUCOBOL 2.0" embedded as required
  inaccurate statement (FR17).
- No COBOL source files modified. Documentation-only story.

### Code Review Fixes (claude-sonnet-4-6)

- H1: Bug 7 paragraph name updated from placeholder to `PROC-NB` (confirmed
  from bjack-main.cob:52 after Epic 5 completion).
- H2: Bug 6 description updated — "one check only" was stale after Story 5.4
  added the 'D' double-down branch. New description accurately states two
  explicit checks (S and D) with garbage-input fallthrough to hit.
- M4: Bug 8 paragraph note `(SEE STORY 6.2 TO CONFIRM AFTER EPIC 6 DONE)`
  removed — LOOP-A confirmed from bjack-main.cob:60.
- M3: Bug 9 description unchanged (documents planned Epic 6 defect) but added
  `NOTE -- DEFECT NOT YET ACTIVE. PENDING EPIC 6 IMPLEMENTATION.` to prevent
  demo presenter from pointing at code that doesn't yet exhibit the defect.

### Code Review Fixes — Epic 6 Complete (claude-sonnet-4-6)

- Bug 9 "PENDING EPIC 6 IMPLEMENTATION" note removed — Epic 6 done, defect now active.
- Bug 9 trigger description corrected: was "WIN-THEN-BET", actual trigger is
  lose-chips-then-over-bet (WS-BL frozen at 100; WS-BAL drops after loss;
  player can bet up to original starting amount).
- Bug 9 paragraph reference cleaned: removed "(SEE STORY 6.3 TO CONFIRM AFTER EPIC 6 DONE)".

### File List

- README (replaced — was PLACEHOLDER, now full 1980s-style plain-text)
