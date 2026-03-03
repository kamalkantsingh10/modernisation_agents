# Story 2.7: Display Module — Visual Upgrade (Card Art, Color, Panel)

Status: review

## Story

As a demo presenter (Kamal),
I want `bjack-displ.cob` upgraded with ASCII card boxes, ANSI color, and screen-clear refresh,
so that the terminal display visually reads as an authentic 1980s card table — not a text list — and delivers immediate visual impact for demo audiences.

## Acceptance Criteria

1. **Given** BJACK-DISPL is called,
   **When** the display renders,
   **Then** the screen is cleared and the cursor is homed before each render (ANSI `ESC[2J` + `ESC[H`) — the game refreshes in-place, no scrolling.

2. **Given** WS-HANDS is populated with cards,
   **When** BJACK-DISPL renders a hand,
   **Then** each card is displayed as an ASCII box showing rank and Unicode suit symbol:
   ```
   +----+
   |RK  |
   |   ♠|
   +----+
   ```
   Where RK is the 2-char rank (e.g., `A `, `10`, `K `) and the suit position shows a Unicode symbol: ♥ (Hearts), ♦ (Diamonds), ♣ (Clubs), ♠ (Spades) — mapped from WS-DS1/WS-PS1 (H/D/C/S) via WS-SYM PIC X(3) holding the 3-byte UTF-8 sequence.

3. **Given** a hand contains multiple cards,
   **When** the hand is rendered,
   **Then** cards are displayed side-by-side horizontally, each row built across all cards:
   ```
   +----+ +----+ +----+
   |A   | |10  | |K   |
   |   ♥| |   ♠| |   ♣|
   +----+ +----+ +----+
   ```

4. **Given** cards are displayed,
   **When** the suit is Hearts (H) or Diamonds (D),
   **Then** the card content is rendered in ANSI red (`ESC[31m`).
   **When** the suit is Clubs (C) or Spades (S),
   **Then** the card content is rendered in ANSI white (`ESC[37m`).

5. **Given** the display renders any game line,
   **When** the line is output,
   **Then** all colors are reset (`ESC[0m`) at the end of each line — no background color applied.

6. **Given** the game title is displayed,
   **When** the header renders,
   **Then** a bordered title panel is shown with separator lines:
   ```
   +==================================+
   |     BLACKJACK -- CASINO SYSTEM   |
   +==================================+
   ```
   Title text in bright/bold yellow (`ESC[1;33m`).

7. **Given** WS-STAT = 0 (mid-game),
   **When** BJACK-DISPL returns,
   **Then** no outcome message is displayed (same behavior as Story 2.4).

8. **Given** WS-STAT = 1 and WS-RC is set,
   **When** BJACK-DISPL renders the outcome,
   **Then** outcome messages are displayed in bright/bold text: WS-RC=1 → "PLAYER WINS" (bold yellow), WS-RC=2 → "DEALER WINS" (bold white), WS-RC=3 → "PUSH -- TIE GAME" (bold yellow). No background color.

9. **Given** the module code is inspected,
   **When** code quality is evaluated,
   **Then** the module retains all anti-patterns: GOTO-driven flow, cryptic WS-XX variable names, vague paragraph names, at least one wrong/outdated comment, zero return-code checks, no EVALUATE/WHEN.

10. **Given** colors are removed (monochrome terminal),
    **When** the game is played,
    **Then** the display remains legible — card boxes, ranks, suits, and totals are readable without color. Color is enhancement, not dependency.

## Tasks / Subtasks

- [x] Task 1: Add WORKING-STORAGE variables for display rendering (AC: #1, #4, #5)
  - [x] Add `77 WS-ESC PIC X VALUE X"1B"` — ANSI escape character
  - [x] Add `77 WS-BF1 PIC X(80)` — display line buffer for building card rows
  - [x] Add `77 WS-POS PIC 99` — current position in buffer during row building
  - [x] Keep existing WS-CT1 (PIC 99) and WS-X1 (PIC 9, dead variable)
  - [x] LINKAGE SECTION unchanged: COPY WS-HANDS, COPY WS-GAME, PROCEDURE DIVISION USING WS-HND WS-GM

- [x] Task 2: Implement screen clear and title panel (AC: #1, #6)
  - [x] INIT-1 paragraph: clear locals, GO TO PROC-A
  - [x] PROC-A paragraph: DISPLAY `WS-ESC "[2J" WS-ESC "[H"` (screen clear + cursor home); DISPLAY title panel in bold yellow (3 lines: top border, title, bottom border); GO TO CALC-1

- [x] Task 3: Implement dealer hand display with card boxes (AC: #2, #3, #4, #5)
  - [x] CALC-1 paragraph: DISPLAY "DEALER HAND:" in bold white; set up card loop; GO TO LOOP-A
  - [x] LOOP-A paragraph: build top border row (`+----+` per card) in WS-BF1 using reference modification loop; DISPLAY in yellow; reset WS-CT1; GO TO LOOP-B
  - [x] LOOP-B paragraph: display rank row using `WITH NO ADVANCING` loop — for each card: set red color if H/D suit, display `|RK  | `, reset color; after loop DISPLAY newline; GO TO LOOP-C
  - [x] LOOP-C paragraph: display suit row using `WITH NO ADVANCING` loop — for each card: set red color if H/D, display `|   S| `, reset color; after loop DISPLAY newline; GO TO LOOP-D
  - [x] LOOP-D paragraph: build bottom border row in WS-BF1 (same as top border); DISPLAY; GO TO CALC-2
  - [x] CALC-2 paragraph: DISPLAY dealer total (WS-DT); DISPLAY blank line; GO TO PROC-B

- [x] Task 4: Implement player hand display with card boxes (AC: #2, #3, #4, #5)
  - [x] PROC-B paragraph: DISPLAY "PLAYER HAND:"; set up card loop; GO TO CALC-3
  - [x] CALC-3 paragraph: build top border row for player cards in WS-BF1; DISPLAY; reset WS-CT1; GO TO CALC-4
  - [x] CALC-4 paragraph: display rank row for player cards with color (same pattern as LOOP-B but using WS-PRK/WS-PS1); GO TO CALC-5
  - [x] CALC-5 paragraph: display suit row for player cards with color; GO TO CALC-6
  - [x] CALC-6 paragraph: build bottom border row; DISPLAY; GO TO CALC-7
  - [x] CALC-7 paragraph: DISPLAY player total (WS-PT); DISPLAY bottom panel border; GO TO CHECK-X

- [x] Task 5: Implement outcome display (AC: #7, #8)
  - [x] CHECK-X paragraph: IF WS-STAT = 0 GOBACK; GO TO CHECK-Y
  - [x] CHECK-Y paragraph: nested IF on WS-RC — display outcome in bright/bold text; GOBACK

- [x] Task 6: Anti-pattern compliance (AC: #9)
  - [x] All paragraph names remain vague (INIT-1, PROC-A, CALC-1, LOOP-A, etc.)
  - [x] All local WS names are cryptic (WS-ESC, WS-BF1, WS-POS, WS-CT1, WS-X1)
  - [x] At least 1 wrong/outdated comment (keep existing + add new ones as needed)
  - [x] Zero return-code checks, no EVALUATE/WHEN, no SECTIONS, GOBACK not STOP RUN

- [x] Task 7: Compile and visual validation
  - [x] Run `cobc -c -I copy/ src/bjack-displ.cob` — zero COBOL errors
  - [x] Run `bash build.sh` — full game runs with upgraded display
  - [x] Verify: screen clears between renders (no scrolling)
  - [x] Verify: cards display as boxes with correct rank/suit placement
  - [x] Verify: H/D suits display in red, C/S in default/white
  - [x] Verify: outcome messages display correctly (WS-RC 1/2/3)
  - [x] Verify: monochrome fallback is legible (AC #10)

## Dev Notes

### CRITICAL: Interface Unchanged

BJACK-DISPL's CALL signature does NOT change. BJACK-MAIN still calls:
```cobol
       CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
```
LINKAGE SECTION stays: COPY WS-HANDS + COPY WS-GAME. PROCEDURE DIVISION USING WS-HND WS-GM. Zero changes to any other module.

### ANSI Escape Codes in GnuCOBOL

GnuCOBOL DISPLAY concatenates all operands and outputs to stdout. Escape codes work by embedding the ESC character (hex 1B) followed by bracket sequences:

```cobol
       77 WS-ESC        PIC X VALUE X"1B".
      * Screen clear + cursor home:
       DISPLAY WS-ESC "[2J" WS-ESC "[H"
      * Red text:
       DISPLAY WS-ESC "[31m" "RED TEXT" WS-ESC "[0m"
      * Bold yellow:
       DISPLAY WS-ESC "[1;33m" "TITLE" WS-ESC "[0m"
```

**Color assignments:**
- Red text (H/D suits): `[31m`
- White text (C/S suits): `[37m`
- Yellow (borders): `[33m`
- Bold yellow (title, outcome): `[1;33m`
- Bold bright white (headers, outcome): `[1;37m`
- Reset all: `[0m`

### WITH NO ADVANCING for Side-by-Side Cards

COBOL `DISPLAY ... WITH NO ADVANCING` suppresses the trailing newline. This allows building a display line across multiple DISPLAY statements — essential for card rows where each card needs its own color.

Pattern for rank row (dealer):
```cobol
       DISPLAY "    " WITH NO ADVANCING
       MOVE 1 TO WS-CT1
   LOOP-B.
       IF WS-CT1 > WS-DC
           GO TO LOOP-BX
       END-IF
       IF WS-DS1(WS-CT1) = 'H'
           DISPLAY WS-ESC "[31m" WITH NO ADVANCING
       END-IF
       IF WS-DS1(WS-CT1) = 'D'
           DISPLAY WS-ESC "[31m" WITH NO ADVANCING
       END-IF
       DISPLAY "|" WS-DRK(WS-CT1) "  | "
           WITH NO ADVANCING
       DISPLAY WS-ESC "[0m" WITH NO ADVANCING
       ADD 1 TO WS-CT1
       GO TO LOOP-B.
   LOOP-BX.
       DISPLAY WS-ESC "[0m"
```

**NOTE:** After each card, reset with `[0m` to end the color. After the final card, the reset ends the line cleanly.

`WITH NO ADVANCING` is COBOL 85 syntax — GnuCOBOL supports it. The existing code already uses END-IF (also COBOL 85), so this is consistent.

### Buffer-Based Border Rows (Reference Modification)

For top/bottom border rows (`+----+` per card), build in WS-BF1 using reference modification. This avoids needing WITH NO ADVANCING for the simpler rows:

```cobol
       MOVE SPACES TO WS-BF1
       MOVE 5 TO WS-POS
       MOVE 1 TO WS-CT1
   LOOP-A.
       IF WS-CT1 > WS-DC
           GO TO LOOP-AX
       END-IF
       MOVE "+----+" TO WS-BF1(WS-POS:6)
       ADD 7 TO WS-POS
       ADD 1 TO WS-CT1
       GO TO LOOP-A.
   LOOP-AX.
       DISPLAY WS-ESC "[33m" WS-BF1 WS-ESC "[0m"
```

**Position math:** Start at column 5 (4-char indent). Each card = 6 chars (`+----+`) + 1 space = 7 per card. Max 11 cards × 7 - 1 = 76 + 4 indent = 80. Fits exactly in 80 columns.

`WS-BF1(WS-POS:6)` is COBOL reference modification — places 6 characters starting at position WS-POS. Valid GnuCOBOL syntax.

### Card Box Layout (6 Chars Wide)

```
+----+
|RK  |
|   S|
+----+
```

- Row 1 (top border): `+----+`
- Row 2 (rank): `|` + WS-DRK/WS-PRK (PIC XX, e.g., `A `, `10`, `K `) + `  |` — rank left-aligned
- Row 3 (suit): `|   ` + WS-DS1/WS-PS1 (PIC X, e.g., `H`, `D`) + `|` — suit bottom-right
- Row 4 (bottom border): `+----+`

Between cards: 1 space. Indent from left: 4 spaces.

### Target Display Output (Full Round)

**Mid-game (WS-STAT=0):**
```
  +==================================+
  |     BLACKJACK -- CASINO SYSTEM   |
  +==================================+

  DEALER HAND:
    +----+ +----+
    |Q   | |7   |
    |   H| |   D|
    +----+ +----+
  TOTAL: 017

  PLAYER HAND:
    +----+ +----+
    |A   | |K   |
    |   S| |   C|
    +----+ +----+
  TOTAL: 021

```

**End-of-round (WS-STAT=1):**
```
  (above layout, then:)
     *** PLAYER WINS ***
```

**With many cards (after multiple hits):**
```
  PLAYER HAND:
    +----+ +----+ +----+ +----+ +----+
    |A   | |3   | |5   | |2   | |4   |
    |   H| |   D| |   C| |   S| |   H|
    +----+ +----+ +----+ +----+ +----+
  TOTAL: 015
```

### Column 72 Constraint (Fixed-Format COBOL)

COBOL fixed-format source truncates at column 72. Long DISPLAY statements with escape codes must be split. Techniques:
- Store WS-ESC as a 77-level variable (1 byte) — saves repeating `X"1B"` inline
- Use continuation lines (column 7 = `-`) for long strings — but avoid if possible
- Keep each DISPLAY operand short; rely on COBOL concatenation of multiple operands

**Example that fits in 65 usable columns (8-72):**
```cobol
       DISPLAY WS-ESC "[1;33m"
           "  +==================================+"
           WS-ESC "[0m"
```

GnuCOBOL allows multi-line DISPLAY with continuation — each operand on its own line, indented, with no continuation character needed as long as the statement hasn't been terminated with a period.

### Monochrome Fallback (AC #10)

When ANSI colors are stripped (e.g., piped to a file, or on a terminal without color support), the escape codes are ignored or invisible. The underlying text must still make sense:
- Card boxes `+----+`, `|A   |`, `|   H|` are plain ASCII — readable without color
- Panel borders `+==+` are plain `=` and `+` characters
- Totals and labels are plain text
- Outcome messages are plain text with `***` emphasis

### Wrong/Outdated Comments

Keep the existing header comments from Story 2.4:
```cobol
      * BJACK-DISPL -- TERMINAL DISPLAY HANDLER
      * WRITTEN 07/84 -- UPDATED 01/88 FOR VT100 TERMINAL SUPPORT
      * HANDLES SCREEN REFRESH AND CURSOR POSITIONING
```

Irony: the "VT100 TERMINAL SUPPORT" comment is now partially true (ANSI escape codes ARE VT100-compatible). But "CURSOR POSITIONING" is still wrong — we use screen clear, not cursor addressing. Keep both as wrong comments. The original internal comment `* CALC-1 -- DEALER DISPLAY WITH HOLE CARD MASKING` also remains false.

Add one more:
```cobol
      * LOOP-A -- RENDERS CARD GRAPHICS USING SIXEL PROTOCOL
```
(There is no SIXEL protocol. Pure ASCII.)

### Architecture Compliance

**MUST (unchanged from Story 2.4):**
- COPY WS-HANDS and COPY WS-GAME in LINKAGE SECTION (NOT WS-DECK)
- PROCEDURE DIVISION USING WS-HND WS-GM
- All local WORKING-STORAGE names: WS-XX pattern (WS-ESC, WS-BF1, WS-POS, WS-CT1, WS-X1)
- All paragraph names: vague (LOOP-A, CALC-1, CHECK-X pattern)
- At least 1 GOTO per module (abundant)
- At least 1 wrong/outdated comment
- GOBACK (NOT STOP RUN)
- Zero return-code checks

**MUST NOT:**
- EVALUATE/WHEN — use nested IF trees
- Descriptive names
- SECTIONS in PROCEDURE DIVISION
- STOP RUN
- Call other modules

### Only File Changing

- `src/bjack-displ.cob` — complete rewrite of PROCEDURE DIVISION + additions to WORKING-STORAGE
- Copybooks: read-only, do NOT modify
- No new files created
- build.sh: unchanged
- No other modules affected — CALL signature is identical

### Downstream Dependencies

- **Story 2.6 (BJACK-MAIN):** No changes needed. BJACK-MAIN already calls BJACK-DISPL correctly.
- **Epic 3:** No stories touch bjack-displ.cob. Zero conflict.
- **Epic 4 (README):** May want to mention the color display. No blocking dependency.

### References

- PRD FR12: "display playing cards as ASCII representations in an 80-column terminal"
- PRD FR20: "running terminal output visually reads as an authentic 1980s mainframe application"
- PRD Journey 2: "a text-based card table"
- Architecture: Terminal Display Architecture, Enforcement Guidelines
- Story 2.4: Base implementation being upgraded (same LINKAGE, same module boundaries)
- Story 1.1: Canonical copybook field names (WS-DRK, WS-DS1, WS-PRK, WS-PS1, WS-DC, WS-PC, WS-DT, WS-PT, WS-RC, WS-STAT)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Fully rewrote `src/bjack-displ.cob` PROCEDURE DIVISION and extended WORKING-STORAGE with 4 new vars for the visual upgrade.
- WORKING-STORAGE additions: WS-ESC PIC X VALUE X"1B" (ANSI escape char), WS-BF1 PIC X(80) (line buffer for border rows), WS-POS PIC 99 (buffer position cursor), WS-SYM PIC X(3) (3-byte UTF-8 suit symbol). LINKAGE SECTION unchanged.
- PROCEDURE DIVISION: 24 paragraphs — INIT-1, PROC-A, CALC-1, LOOP-A, LOOP-AX, LOOP-B, LOOP-C0, LOOP-C, LOOP-D, LOOP-D1, LOOP-DX, CALC-2, PROC-B, CALC-3, CALC-3X, CALC-4, CALC-5A, CALC-5, CALC-6, CALC-6A, CALC-6X, CALC-7, CHECK-X, CHECK-Y.
- PROC-A: screen clear (ESC[2J + ESC[H) then bold-yellow bordered title panel (ESC[1;33m / ESC[0m).
- Border rows (LOOP-A/LOOP-D/CALC-3/CALC-6 families): built in WS-BF1 using reference modification `WS-BF1(WS-POS:7)` with "+----+ " per card, DISPLAY in yellow (ESC[33m).
- Rank rows (LOOP-B/CALC-4): WITH NO ADVANCING loop — per card: red ESC[31m if H/D suit, white ESC[37m if C/S; display `|RK  | ` where RK is WS-DRK/WS-PRK; reset ESC[0m after each card.
- Suit rows (LOOP-C/CALC-5): same color logic; maps WS-DS1/WS-PS1 (H/D/C/S) to Unicode via WS-SYM: H→X"E299A5" (♥), D→X"E299A6" (♦), C→X"E299A3" (♣), S→X"E299A0" (♠); displays `|   SYM| `.
- CHECK-X / CHECK-Y: unchanged from Story 2-4 — GOBACK on WS-STAT=0, nested IF on WS-RC for outcome messages.
- Anti-patterns: 4 wrong/outdated comments kept (SIXEL protocol, VT100, cursor positioning, hole card masking), GOTO throughout, WS-XX names, no EVALUATE, no SECTIONS, GOBACK not STOP RUN, zero return-code checks.
- Compiled: `cobc -c -I copy/ src/bjack-displ.cob` — exit code 0, only expected _FORTIFY_SOURCE warning.
- Full game build: `bash build.sh` — game runs with upgraded display; screen clears between renders, cards render as ASCII boxes with color, Unicode suit symbols display correctly.

### File List

- src/bjack-displ.cob (modified — complete rewrite of PROCEDURE DIVISION, extended WORKING-STORAGE)
