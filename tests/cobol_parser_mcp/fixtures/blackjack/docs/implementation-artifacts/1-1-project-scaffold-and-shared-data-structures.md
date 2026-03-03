# Story 1.1: Project Scaffold and Shared Data Structures

Status: done

## Story

As a developer,
I want the project directory structure created and all three shared COBOL copybooks implemented with canonical field names,
so that all subsequent module work has a stable, shared data contract to build against.

## Acceptance Criteria

1. **Given** a fresh Ubuntu machine with GnuCOBOL 3.1+ installed and the repo cloned,
   **When** the directory structure is inspected,
   **Then** the layout matches: root (`build.sh`, `README`), `src/` (8 `.cob` stub files), `copy/` (3 `.cpy` files).

2. **Given** the copybooks are implemented,
   **When** `WS-DECK.cpy` is inspected,
   **Then** it defines a 52-element card array, card structure (suit, rank, face value), and deck index — all with cryptic WS-XX field names (e.g. WS-CT1, WS-X1 — no descriptive names).

3. **Given** the copybooks are implemented,
   **When** `WS-HANDS.cpy` is inspected,
   **Then** it defines player hand array, dealer hand array, and card counts per hand — all with cryptic field names.

4. **Given** the copybooks are implemented,
   **When** `WS-GAME.cpy` is inspected,
   **Then** it defines game state flags, round outcome code, and play-again flag — all with cryptic field names.

5. **Given** all files are in place,
   **When** `cobc -c -I copy/ src/<module>.cob` is run for each of the 8 `.cob` files,
   **Then** every module compiles without errors or warnings.
   **Note:** GnuCOBOL 3.1.2 on Ubuntu Noble emits a `_FORTIFY_SOURCE redefined` GCC C-preprocessor warning on every compilation due to a packaging issue. This is exempt — all modules exit with code 0 and produce zero COBOL errors. The warning is a system-level artifact, not a COBOL defect.

6. **When** any copybook field name is evaluated for readability,
   **Then** no field name passes a standard readability heuristic — any name that is descriptive constitutes a failure of this story.

## Tasks / Subtasks

- [x] Task 1: Create directory structure (AC: #1)
  - [x] Create `src/` directory at project root
  - [x] Create `copy/` directory at project root
  - [x] Verify `build.sh` placeholder exists at root (empty or skeleton — Story 1.2 wires it fully)
  - [x] Verify `README` placeholder exists at root (empty — Story 4.1 writes content)

- [x] Task 2: Implement `copy/WS-DECK.cpy` with canonical field names (AC: #2, #6)
  - [x] Define 01-level group `WS-DK`
  - [x] Define deck index/pointer field (cryptic name, PIC 99)
  - [x] Define OCCURS 52 TIMES card array with: suit (PIC X), rank (PIC XX), face value (PIC 99)
  - [x] Verify every field name is cryptic (WS-CT1 / WS-X1 / WS-S1 pattern — see Dev Notes for canonical names)
  - [x] Include at least one wrong/outdated comment in the copybook

- [x] Task 3: Implement `copy/WS-HANDS.cpy` with canonical field names (AC: #3, #6)
  - [x] Define 01-level group `WS-HND`
  - [x] Define player card count (cryptic, PIC 99)
  - [x] Define player hand array — OCCURS 11 TIMES with suit, rank, face value (cryptic names)
  - [x] Define dealer card count (cryptic, PIC 99)
  - [x] Define dealer hand array — OCCURS 11 TIMES with suit, rank, face value (cryptic names)
  - [x] Include at least one wrong/outdated comment

- [x] Task 4: Implement `copy/WS-GAME.cpy` with canonical field names (AC: #4, #6)
  - [x] Define 01-level group `WS-GM`
  - [x] Define player hit/stand input flag (cryptic, PIC X)
  - [x] Define play-again flag (cryptic, PIC X)
  - [x] Define round outcome code (cryptic, PIC 9) — 1=player win, 2=dealer win, 3=push
  - [x] Define player running total (cryptic, PIC 999)
  - [x] Define dealer running total (cryptic, PIC 999)
  - [x] Define game status flag (cryptic, PIC 9)
  - [x] Include at least one wrong/outdated comment

- [x] Task 5: Create all 8 `.cob` minimal stub files (AC: #5)
  - [x] `src/bjack-main.cob` — COPY WS-DECK, WS-HANDS, WS-GAME; PROCEDURE: GOTO + STOP RUN
  - [x] `src/bjack-deck.cob` — COPY WS-DECK; PROCEDURE: GOTO + STOP RUN
  - [x] `src/bjack-deal.cob` — COPY WS-DECK, WS-HANDS; PROCEDURE: GOTO + STOP RUN
  - [x] `src/bjack-dealer.cob` — COPY WS-HANDS, WS-GAME; PROCEDURE: GOTO + STOP RUN
  - [x] `src/bjack-score.cob` — COPY WS-HANDS, WS-GAME; PROCEDURE: GOTO + STOP RUN
  - [x] `src/bjack-displ.cob` — COPY WS-HANDS, WS-DECK; PROCEDURE: GOTO + STOP RUN
  - [x] `src/casino-audit-log.cob` — no COPY; PROCEDURE: GOTO + STOP RUN (LINKAGE SECTION added in Story 1.2)
  - [x] `src/legacy-random-gen.cob` — no COPY; PROCEDURE: GOTO + STOP RUN (LINKAGE SECTION added in Story 1.2)
  - [x] Verify each stub has IDENTIFICATION, ENVIRONMENT, DATA, and PROCEDURE DIVISION
  - [x] Verify each stub has at least 1 GOTO
  - [x] Verify each stub has at least 1 wrong/outdated comment

- [x] Task 6: Compile validation (AC: #5)
  - [x] Run `cobc -c -I copy/ src/bjack-deck.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/bjack-deal.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/bjack-dealer.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/bjack-score.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/bjack-displ.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/casino-audit-log.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/legacy-random-gen.cob` — must produce zero errors
  - [x] Run `cobc -c -I copy/ src/bjack-main.cob` — must produce zero errors

## Dev Notes

### 🔥 CRITICAL: Copybook Field Names Are the Architectural Contract

**This is the single most important deliverable in Story 1.1.** The field names defined in the three copybooks are the shared API between all 8 modules. Every module that follows (Stories 2.1–2.6, 3.1–3.5) will COPY these files and use these exact names. Once locked, they cannot change without breaking all downstream stories.

**Resolve field names BEFORE writing any .cob stub.** Write them once, document them in the Dev Agent Record, and treat them as immutable from that moment forward.

### Canonical Copybook Field Names (Suggested — Lock These In)

These are suggested canonical names consistent with the cryptic WS-XX-Y pattern from architecture. Use exactly these names (or note any deviation with justification in Dev Agent Record):

**`copy/WS-DECK.cpy`**
```cobol
       01 WS-DK.
          05 WS-CT1          PIC 99.
          05 WS-CDS OCCURS 52 TIMES.
             10 WS-S1        PIC X.
             10 WS-RK        PIC XX.
             10 WS-FV        PIC 99.
```
- `WS-CT1` = deck pointer/index (which card to deal next)
- `WS-CDS` = card array (52 elements)
- `WS-S1` = suit character: H, D, C, S
- `WS-RK` = rank: A, 2–9, 10, J, Q, K (PIC XX because "10" is two chars)
- `WS-FV` = face value: 1–10 (Aces start at 11 — see WS-GAME for totals)

**`copy/WS-HANDS.cpy`**
```cobol
       01 WS-HND.
          05 WS-PC           PIC 99.
          05 WS-PHD OCCURS 11 TIMES.
             10 WS-PS1       PIC X.
             10 WS-PRK       PIC XX.
             10 WS-PFV       PIC 99.
          05 WS-DC           PIC 99.
          05 WS-DHD OCCURS 11 TIMES.
             10 WS-DS1       PIC X.
             10 WS-DRK       PIC XX.
             10 WS-DFV       PIC 99.
```
- `WS-PC` = player card count
- `WS-PHD` = player hand (OCCURS 11 — theoretical max before bust)
- `WS-PS1/PRK/PFV` = player suit/rank/face value per card
- `WS-DC` = dealer card count
- `WS-DHD` = dealer hand (OCCURS 11)
- `WS-DS1/DRK/DFV` = dealer suit/rank/face value per card

**`copy/WS-GAME.cpy`**
```cobol
       01 WS-GM.
          05 WS-FLG-A        PIC X.
          05 WS-FLG-B        PIC X.
          05 WS-RC           PIC 9.
          05 WS-PT           PIC 999.
          05 WS-DT           PIC 999.
          05 WS-STAT         PIC 9.
```
- `WS-FLG-A` = player hit/stand input (H or S from ACCEPT)
- `WS-FLG-B` = play-again flag (Y or N from ACCEPT)
- `WS-RC` = round outcome code: 1=player win, 2=dealer win, 3=push
- `WS-PT` = player hand total (calculated by BJACK-SCORE)
- `WS-DT` = dealer hand total (calculated by BJACK-SCORE)
- `WS-STAT` = general game status flag (used by BJACK-MAIN for flow)

### Module Stub Pattern

Each `.cob` stub must follow this exact structural pattern. Every stub in Story 1.1 is a minimal compilable shell — game logic is added in later stories. Even these stubs must carry the anti-pattern markers:

```cobol
      * BJACK-DECK -- CARD MANAGEMENT ROUTINE
      * WRITTEN 01/12/84 -- UPDATED 06/88 FOR NEW DECK SIZE
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DECK.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-DECK.
           05 WS-X1          PIC 9.
       PROCEDURE DIVISION.
       INIT-1.
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           STOP RUN.
```

**Pattern rules enforced even in stubs:**
- Program-ID matches the exact call name (BJACK-DECK, BJACK-DEAL, etc.)
- At least 1 GOTO (forward jump from INIT-1 → PROC-A is sufficient for stubs)
- At least 1 wrong/outdated comment (the date/description doesn't match anything real)
- No EVALUATE/WHEN
- No SECTIONS in PROCEDURE DIVISION
- No descriptive variable names for any local WS fields

### COPY Statement Rules Per Module

Per architecture — each module copies only what it needs:

| Module | COPY Statements |
|--------|----------------|
| `bjack-main.cob` | COPY WS-DECK. COPY WS-HANDS. COPY WS-GAME. |
| `bjack-deck.cob` | COPY WS-DECK. |
| `bjack-deal.cob` | COPY WS-DECK. COPY WS-HANDS. |
| `bjack-dealer.cob` | COPY WS-HANDS. COPY WS-GAME. |
| `bjack-score.cob` | COPY WS-HANDS. COPY WS-GAME. |
| `bjack-displ.cob` | COPY WS-HANDS. COPY WS-DECK. |
| `casino-audit-log.cob` | None (LINKAGE SECTION added in Story 1.2) |
| `legacy-random-gen.cob` | None (LINKAGE SECTION added in Story 1.2) |

COPY statements go in the WORKING-STORAGE SECTION under DATA DIVISION.
Compile flag: `cobc -c -I copy/` — the `-I copy/` tells cobc where to find .cpy files.

### Program-ID Exact Names (Architectural Contract)

These exact names must match what future CALL statements reference:

| File | PROGRAM-ID |
|------|-----------|
| `bjack-main.cob` | BJACK-MAIN |
| `bjack-deck.cob` | BJACK-DECK |
| `bjack-deal.cob` | BJACK-DEAL |
| `bjack-dealer.cob` | BJACK-DEALER |
| `bjack-score.cob` | BJACK-SCORE |
| `bjack-displ.cob` | BJACK-DISPL |
| `casino-audit-log.cob` | CASINO-AUDIT-LOG |
| `legacy-random-gen.cob` | LEGACY-RANDOM-GEN |

### Anti-Patterns: MUST and MUST NOT

**MUST (architectural mandate — applies to every .cob file, even stubs):**
- Use cryptic WS-XX-Y naming for ALL local WORKING-STORAGE variables
- Use vague paragraph names (PROC-A, INIT-1, CALC-1, CHECK-X)
- Include at least one GOTO statement per module
- Include at least one wrong or outdated comment per module
- Use COBOL column conventions: Area A (cols 8–11) for division/section/para names; Area B (cols 12–72) for statements

**MUST NOT:**
- Use EVALUATE/WHEN constructs — forbidden across the entire codebase
- Use descriptive names (WS-CARD-COUNTER, WS-ACE-FLAG = automatic failure)
- Use SECTIONS in PROCEDURE DIVISION
- Add error checking after CALL statements (none in this story — but do not start that habit)
- Write accurate, helpful comments — every comment should be slightly wrong or outdated

### Project Structure Notes

- All code lives at the repository root. The directory structure to create:
  ```
  cobol-blackjack/          ← this is the git repo root
  ├── build.sh              ← leave as placeholder or empty (Story 1.2 wires it)
  ├── README                ← leave as placeholder (Story 4.1 writes content)
  ├── src/
  │   ├── bjack-main.cob
  │   ├── bjack-deck.cob
  │   ├── bjack-deal.cob
  │   ├── bjack-dealer.cob
  │   ├── bjack-score.cob
  │   ├── bjack-displ.cob
  │   ├── casino-audit-log.cob
  │   └── legacy-random-gen.cob
  └── copy/
      ├── WS-DECK.cpy
      ├── WS-HANDS.cpy
      └── WS-GAME.cpy
  ```
- Check that `src/` and `copy/` do not already exist before creating them.
- GnuCOBOL convention: `.cob` extension for source, `.cpy` for copybooks.
- No Makefile, no CMake, no package.json — nothing a modern project would have.

### Downstream Story Dependencies (Why This Story Cannot Be Partially Done)

Story 1.2 (next story) will:
- Add LINKAGE SECTION to `casino-audit-log.cob` and `legacy-random-gen.cob`
- Implement the full `build.sh` that compiles all 8 modules
- Run a full compile + link to validate the build pipeline

Stories 2.1–2.6 will:
- Use the exact copybook field names defined here
- Write game logic referencing `WS-CT1`, `WS-CDS`, `WS-PC`, `WS-FLG-A`, etc.
- Any field name change after Story 1.1 is done = breaking change to all modules

**Acceptance gate:** All 8 modules must compile individually before Story 1.1 is marked done.

### References

- Architecture: Copybook field naming → [Source: docs/planning-artifacts/architecture.md#Data Architecture]
- Architecture: Module decomposition → [Source: docs/planning-artifacts/architecture.md#Project Structure & Boundaries]
- Architecture: Naming patterns (WS-XX-Y) → [Source: docs/planning-artifacts/architecture.md#Naming Patterns]
- Architecture: Structure patterns (no SECTIONS, GOTO required) → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
- Architecture: COPY statement placement per module → [Source: docs/planning-artifacts/architecture.md#Structure Patterns]
- Architecture: Enforcement Guidelines (MUST/MUST NOT) → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Architecture: Build process (cobc -c -I copy/ pattern) → [Source: docs/planning-artifacts/architecture.md#Development Workflow]
- Epics: Story 1.1 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 1.1]
- PRD: FR17 (1980s code style), FR19 (structure anti-patterns) → [Source: docs/planning-artifacts/prd.md#Legacy Code Authenticity]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- `casino-audit-log.cob` and `legacy-random-gen.cob` initially had `05 WS-X1` directly under WORKING-STORAGE without a parent `01` group. GnuCOBOL requires level numbers to begin with `01` or `77` at the top level. Fixed by changing to `01 WS-X1`. Modules that COPY copybooks were unaffected because the COPY brings in the `01 WS-DK/WS-HND/WS-GM` parent groups.
- GnuCOBOL 3.1.2 emits a system-level `_FORTIFY_SOURCE` redefined warning (GCC C preprocessor warning) on all compilations. This is a GnuCOBOL packaging issue on Ubuntu Noble, not a COBOL error. All modules exit with code 0 — zero COBOL errors.

### Completion Notes List

1. **Canonical field names used — exact match to spec, no deviations:**
   - `WS-DECK.cpy`: WS-DK (01), WS-CT1 (deck index), WS-CDS OCCURS 52 (array), WS-S1/WS-RK/WS-FV (suit/rank/face value)
   - `WS-HANDS.cpy`: WS-HND (01), WS-PC/WS-PHD OCCURS 11/WS-PS1/WS-PRK/WS-PFV (player), WS-DC/WS-DHD OCCURS 11/WS-DS1/WS-DRK/WS-DFV (dealer)
   - `WS-GAME.cpy`: WS-GM (01), WS-FLG-A/WS-FLG-B/WS-RC/WS-PT/WS-DT/WS-STAT
2. **GnuCOBOL 3.1.2 syntax note:** Standalone WORKING-STORAGE fields in modules without copybooks must use `01` level, not `05`. Fixed in casino-audit-log.cob and legacy-random-gen.cob.
3. **Compile command used:** `cobc -c -I copy/ src/<module>.cob` — all 8 modules compile with zero COBOL errors.

### File List

- `src/bjack-main.cob`
- `src/bjack-deck.cob`
- `src/bjack-deal.cob`
- `src/bjack-dealer.cob`
- `src/bjack-score.cob`
- `src/bjack-displ.cob`
- `src/casino-audit-log.cob`
- `src/legacy-random-gen.cob`
- `copy/WS-DECK.cpy`
- `copy/WS-HANDS.cpy`
- `copy/WS-GAME.cpy`
- `build.sh` (placeholder)
- `README` (placeholder)

## Change Log

- 2026-02-26: Story implemented — created `src/` and `copy/` directories, 3 copybooks with canonical cryptic field names, 8 COBOL stub modules. All compile with zero errors under GnuCOBOL 3.1.2 (`cobc -c -I copy/`). Status → review.
