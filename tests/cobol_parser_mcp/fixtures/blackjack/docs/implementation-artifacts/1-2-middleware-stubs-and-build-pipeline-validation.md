# Story 1.2: Middleware Stubs and Build Pipeline Validation

Status: review

## Story

As a developer,
I want both middleware stubs fully implemented and `./build.sh` compiling and linking the full 8-module project,
so that the build pipeline is end-to-end validated before any game logic is written.

## Acceptance Criteria

1. **Given** the scaffold and copybooks from Story 1.1 are in place,
   **When** `./build.sh` is executed,
   **Then** all 8 `.cob` files compile without errors using `cobc -c -I copy/`.

2. **Given** all object files are produced,
   **When** the link step runs,
   **Then** all object files link into a single executable without errors using `cobc -x`.

3. **Given** `casino-audit-log.cob` is inspected,
   **When** the LINKAGE SECTION is reviewed,
   **Then** it accepts parameters via LINKAGE SECTION and performs no operation in PROCEDURE DIVISION (pure no-op).

4. **Given** `legacy-random-gen.cob` is inspected,
   **When** the LINKAGE SECTION is reviewed,
   **Then** it accepts a parameter via LINKAGE SECTION and sets it to a hardcoded value (no actual randomness).

5. **Given** both middleware stubs are inspected,
   **When** code quality is evaluated,
   **Then** each contains: at least one GOTO statement, cryptic WS-XX variable names, at least one wrong or outdated comment, and zero return-code checks.

6. **Given** `build.sh` is inspected,
   **When** error handling is evaluated,
   **Then** `build.sh` contains no error checking between compile/link steps (`set -e` or similar is forbidden).

7. **Given** the project structure is inspected,
   **When** file names, directory names, and build script style are evaluated,
   **Then** the project reads as 1980s mainframe convention (FR19).

## Tasks / Subtasks

- [x] Task 1: Implement LINKAGE SECTION in `casino-audit-log.cob` (AC: #3, #5)
  - [x] Add LINKAGE SECTION under DATA DIVISION with parameters (e.g., audit code PIC X, audit message PIC X(50)) using cryptic names
  - [x] Add `PROCEDURE DIVISION USING` clause referencing LINKAGE parameters
  - [x] Keep PROCEDURE DIVISION as a no-op: accept parameters, do nothing with them, exit
  - [x] Preserve existing GOTO statement (INIT-1 → PROC-A pattern)
  - [x] Ensure at least one wrong/outdated comment is present
  - [x] Ensure all variable names are cryptic (WS-XX pattern for WORKING-STORAGE, LS-XX pattern for LINKAGE)
  - [x] Remove `STOP RUN` — subprograms must use `GOBACK` or fall through (STOP RUN terminates the entire run unit)

- [x] Task 2: Implement LINKAGE SECTION in `legacy-random-gen.cob` (AC: #4, #5)
  - [x] Add LINKAGE SECTION under DATA DIVISION with a return parameter (e.g., PIC 99) using cryptic name
  - [x] Add `PROCEDURE DIVISION USING` clause referencing LINKAGE parameter
  - [x] In PROCEDURE DIVISION, set the return parameter to a hardcoded value (e.g., `MOVE 7 TO LS-R1`) — no actual randomness
  - [x] Preserve existing GOTO statement
  - [x] Ensure at least one wrong/outdated comment is present
  - [x] Ensure all variable names are cryptic
  - [x] Remove `STOP RUN` — use `GOBACK` or fall through

- [x] Task 3: Implement `build.sh` — compile + link + launch (AC: #1, #2, #6, #7)
  - [x] Write the compile step: `cobc -c -I copy/ src/<module>.cob` for each of the 8 modules
  - [x] Write the link step: `cobc -x -o bjack bjack-main.o bjack-deck.o bjack-deal.o bjack-dealer.o bjack-score.o bjack-displ.o casino-audit-log.o legacy-random-gen.o`
  - [x] Write the launch step: `./bjack`
  - [x] NO error checking between steps — no `set -e`, no `if` checks, no `|| exit` — raw sequential commands
  - [x] Ensure `build.sh` is executable (`chmod +x`)
  - [x] Style: terse, no decorative formatting, no usage messages — authentic 1980s shell script

- [x] Task 4: Full build pipeline validation (AC: #1, #2)
  - [x] Run `./build.sh` end-to-end
  - [x] Verify all 8 `.cob` files compile without COBOL errors (ignore `_FORTIFY_SOURCE` GCC warning — see Story 1.1 debug notes)
  - [x] Verify the link step produces the `bjack` executable without errors
  - [x] Verify the executable starts (it will immediately STOP RUN since stubs are minimal — that's expected at this stage)

- [x] Task 5: Verify anti-pattern compliance (AC: #5, #7)
  - [x] Verify both middleware stubs have at least 1 GOTO each
  - [x] Verify both middleware stubs have cryptic WS-XX / LS-XX variable names only
  - [x] Verify both middleware stubs have at least 1 wrong/outdated comment each
  - [x] Verify zero return-code checks anywhere in the codebase
  - [x] Verify no EVALUATE/WHEN in any file
  - [x] Verify no SECTIONS in PROCEDURE DIVISION

## Dev Notes

### CRITICAL: STOP RUN vs GOBACK in Subprograms

**This is the most likely developer mistake in this story.** The Story 1.1 stubs use `STOP RUN` because they were standalone compilation targets. Now that `casino-audit-log.cob` and `legacy-random-gen.cob` will be CALLed as subprograms from BJACK-MAIN, they **must not use STOP RUN**. `STOP RUN` terminates the entire run unit (the whole program), not just the subprogram. The correct exit from a COBOL subprogram is `GOBACK` (returns control to the caller).

**Do NOT leave STOP RUN in the middleware stubs.** Replace with `GOBACK`.

Note: The other 6 game modules (bjack-deck, bjack-deal, etc.) will also eventually be CALLed as subprograms, but their PROCEDURE DIVISIONs will be rewritten in Epic 2. For now, only the 2 middleware stubs need GOBACK because they are being finalized in this story.

### LINKAGE SECTION Pattern for Middleware Stubs

**`casino-audit-log.cob` — No-Op Stub (FR28):**

Per architecture, BJACK-MAIN will call this with:
```cobol
CALL 'CASINO-AUDIT-LOG' USING BY REFERENCE WS-AUD-CODE WS-AUD-MSG
```

The stub needs a LINKAGE SECTION that accepts these parameters but does nothing with them. Example structure:

```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           01 WS-X1          PIC 9.
       LINKAGE SECTION.
           01 LS-A1           PIC X.
           01 LS-A2           PIC X(50).
       PROCEDURE DIVISION USING LS-A1 LS-A2.
       INIT-1.
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           GOBACK.
```

- `LS-A1` = audit code (single character — cryptic name)
- `LS-A2` = audit message (50 chars — cryptic name)
- PROCEDURE DIVISION does nothing with the parameters — pure no-op
- The USING clause lists the LINKAGE items the caller passes

**`legacy-random-gen.cob` — Hardcoded Return Stub (FR29):**

Per architecture, BJACK-DECK will call this with:
```cobol
CALL 'LEGACY-RANDOM-GEN' USING BY REFERENCE WS-RND-VAL
```

The stub needs to accept a parameter and set it to a hardcoded value:

```cobol
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           01 WS-X1          PIC 9.
       LINKAGE SECTION.
           01 LS-R1           PIC 99.
       PROCEDURE DIVISION USING LS-R1.
       INIT-1.
           MOVE 7 TO LS-R1
           GO TO PROC-A.
       PROC-A.
           GOBACK.
```

- `LS-R1` = return value (PIC 99 — enough range for shuffle index)
- Hardcoded `MOVE 7 TO LS-R1` — this is what makes the shuffle biased in Epic 3
- No computation, no randomness — just returns a constant

### build.sh Exact Content

Per architecture, `build.sh` must follow this exact pattern:

```bash
#!/bin/bash
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

**Rules:**
- NO `set -e` — errors are silently ignored
- NO `echo` for progress — no verbosity
- NO `if` checks — no conditional logic
- NO comments explaining what each step does (maybe 1 wrong header comment for anti-pattern)
- Compile order doesn't matter for `cobc -c` (independent compilation) but link must include all `.o` files
- The `.o` files land in the current working directory (where you run `build.sh` from), not in `src/`
- `cobc -x -o bjack` creates the final executable named `bjack`
- `./bjack` launches immediately after link

### GnuCOBOL Compilation Notes from Story 1.1

- **`_FORTIFY_SOURCE` warning:** GnuCOBOL 3.1.2 on Ubuntu Noble emits a GCC-level `_FORTIFY_SOURCE redefined` warning on every compilation. This is a packaging issue, not a COBOL error. All modules compile with exit code 0.
- **Level numbers:** Standalone WORKING-STORAGE fields must use `01` level, not `05`. Modules with COPY statements get their `01` groups from the copybooks, so local fields after a COPY can be `05` (nested under the last COPY'd group). But in casino-audit-log.cob and legacy-random-gen.cob (no COPY), `01` is required.
- **Compile command:** `cobc -c -I copy/ src/<module>.cob` — the `-I copy/` tells cobc where to find `.cpy` files.

### Current State of Files Being Modified

**`src/casino-audit-log.cob` (current — from Story 1.1):**
```cobol
      * CASINO-AUDIT-LOG -- AUDIT TRAIL LOGGER FOR REGULATORY COMPLIANCE
      * WRITTEN 09/84 -- UPDATED 03/91 FOR NEW LOGGING FORMAT
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CASINO-AUDIT-LOG.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           01 WS-X1          PIC 9.
       PROCEDURE DIVISION.
       INIT-1.
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           STOP RUN.
```

Changes needed: Add LINKAGE SECTION, add USING clause, replace STOP RUN with GOBACK.

**`src/legacy-random-gen.cob` (current — from Story 1.1):**
```cobol
      * LEGACY-RANDOM-GEN -- PSEUDO-RANDOM NUMBER GENERATOR
      * WRITTEN 11/83 -- UPDATED 07/87 FOR 32-BIT SEED SUPPORT
       IDENTIFICATION DIVISION.
       PROGRAM-ID. LEGACY-RANDOM-GEN.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           01 WS-X1          PIC 9.
       PROCEDURE DIVISION.
       INIT-1.
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           STOP RUN.
```

Changes needed: Add LINKAGE SECTION, add USING clause, set hardcoded return value, replace STOP RUN with GOBACK.

**`build.sh` (current — placeholder from Story 1.1):**
```bash
#!/bin/bash
# PLACEHOLDER - build pipeline wired in Story 1.2
```

Changes needed: Replace with full compile + link + launch script.

### Anti-Patterns: MUST and MUST NOT (Inherited from Architecture)

**MUST:**
- Cryptic WS-XX-Y naming for ALL WORKING-STORAGE variables
- Cryptic LS-XX naming for ALL LINKAGE SECTION variables
- Vague paragraph names (PROC-A, INIT-1 pattern)
- At least one GOTO statement per module
- At least one wrong or outdated comment per module
- COBOL column conventions: Area A (cols 8-11) for division/section/para names; Area B (cols 12-72) for statements
- Use GOBACK (not STOP RUN) in subprograms

**MUST NOT:**
- Use EVALUATE/WHEN constructs
- Use descriptive names (LS-AUDIT-CODE, LS-RANDOM-RESULT = failure)
- Use SECTIONS in PROCEDURE DIVISION
- Add error checking after CALL statements
- Add error checking in build.sh (no set -e, no conditionals)
- Write accurate, helpful comments

### Program-ID Exact Names (Must Match — Architectural Contract)

| File | PROGRAM-ID |
|------|-----------|
| `casino-audit-log.cob` | CASINO-AUDIT-LOG |
| `legacy-random-gen.cob` | LEGACY-RANDOM-GEN |

These names must match exactly what future CALL statements use.

### Downstream Dependencies (Why This Story Matters)

- **Story 2.1 (BJACK-DECK):** Will `CALL 'LEGACY-RANDOM-GEN'` for shuffle — the LINKAGE interface must be in place
- **Story 2.6 (BJACK-MAIN):** Will `CALL 'CASINO-AUDIT-LOG'` — the LINKAGE interface must be in place
- **All Epic 2 stories:** Will use `./build.sh` as the compile + link + launch entry point
- **Epic 3 (Deliberate Defects):** The hardcoded return value in LEGACY-RANDOM-GEN is what makes the shuffle biased (FR21)

### References

- Architecture: Build process → [Source: docs/planning-artifacts/architecture.md#Development Workflow]
- Architecture: Calling conventions (BY REFERENCE) → [Source: docs/planning-artifacts/architecture.md#Inter-Module Communication]
- Architecture: Middleware stubs (FR28-FR30) → [Source: docs/planning-artifacts/architecture.md#Requirements to Structure Mapping]
- Architecture: Orchestration boundary (BJACK-MAIN) → [Source: docs/planning-artifacts/architecture.md#Architectural Boundaries]
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Epics: Story 1.2 acceptance criteria → [Source: docs/planning-artifacts/epics.md#Story 1.2]
- PRD: FR28 (CASINO-AUDIT-LOG), FR29 (LEGACY-RANDOM-GEN), FR30 (compile/link) → [Source: docs/planning-artifacts/prd.md]
- PRD: FR19 (project structure anti-patterns) → [Source: docs/planning-artifacts/prd.md]
- Story 1.1: Debug log (level numbers, _FORTIFY_SOURCE) → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Debug Log References]
- Story 1.1: Canonical field names → [Source: docs/implementation-artifacts/1-1-project-scaffold-and-shared-data-structures.md#Canonical Copybook Field Names]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6 (claude-opus-4-6)

### Debug Log References

- GnuCOBOL link issue: `cobc -x -o bjack *.o` fails with "undefined reference to main" when main program is pre-compiled with `cobc -c`. Fix: compile subprograms with `cobc -c`, then compile+link main with `cobc -x -I copy/ -o bjack src/bjack-main.cob <subprogram .o files>`. The `-x` flag generates the C main() entry point only during compilation from source, not when linking pre-compiled .o files.

### Completion Notes List

- Task 1: casino-audit-log.cob — Added LINKAGE SECTION (LS-A1 PIC X, LS-A2 PIC X(50)), USING clause, replaced STOP RUN with GOBACK, added wrong comment "RETURNS FORMATTED RECORD TO CALLER VIA LS-A2"
- Task 2: legacy-random-gen.cob — Added LINKAGE SECTION (LS-R1 PIC 99), USING clause, hardcoded MOVE 7 TO LS-R1, replaced STOP RUN with GOBACK, added wrong comment "USES LINEAR CONGRUENTIAL METHOD FOR UNIFORM DISTRIBUTION"
- Task 3: build.sh — 7 subprograms compiled with cobc -c, main compiled+linked with cobc -x, launch step, no error checking, wrong header comment about tape mount procedures
- Task 4: Full pipeline validated — all 8 modules compile, link produces 128KB bjack executable, executable runs and exits cleanly
- Task 5: Anti-pattern compliance verified — GOTOs present, cryptic names only, wrong comments present, zero return-code checks, no EVALUATE/WHEN, no PROCEDURE DIVISION SECTIONS

### Change Log

- 2026-02-26: Story 1.2 implementation complete — middleware stubs finalized, build pipeline validated

### File List

- src/casino-audit-log.cob (modified)
- src/legacy-random-gen.cob (modified)
- build.sh (modified)
