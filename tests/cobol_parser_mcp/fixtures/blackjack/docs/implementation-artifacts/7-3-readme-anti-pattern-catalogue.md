# Story 7.3: README Anti-Pattern Catalogue

Status: done

## Story

As a demo presenter (Kamal),
I want the README to contain a new section listing all structural anomalies
and technical debt patterns by file and paragraph,
So that during a live demo I can point to specific anomalies as examples of
accumulated debt without searching.

## Acceptance Criteria

1. README contains a new section headed `CODE ANOMALIES AND TECHNICAL DEBT` inserted after `SOURCE FILE INDEX` and before `END OF FILE`
2. Section lists Anomaly A: Orphaned split-hand paragraphs (PROC-SP/PROC-DS/CALC-8/CALC-8A/CALC-8X) with file references
3. Section lists Anomaly B: Five-card charlie bonus orphan (PROC-CB in BJACK-SCORE) with file reference
4. Section lists Anomaly C: Insurance offer orphan (PROC-INS in BJACK-DEALER) with file reference
5. Section lists Anomaly D: Original LCG RNG orphan (PROC-R1 in LEGACY-RANDOM-GEN) with file reference
6. Section lists Anomaly E: Ghost variables (WS-X2 in BJACK-DEAL, WS-CB in BJACK-SCORE) with file references
7. Section lists Anomaly F: No-op patches (BJACK-MAIN INIT-1, BJACK-DEALER LOOP-A) with file references
8. Section lists Anomaly G: Foreign-language comments with file list (French: BJACK-SCORE/BJACK-DISPL/LEGACY-RANDOM-GEN; German: BJACK-DEAL/BJACK-DEALER/CASINO-AUDIT-LOG)
9. Section follows 1980s format: ALL CAPS section header, dashes separator, max 72 characters per line, no markdown
10. Section contains at least one misleading or inaccurate statement (consistent with FR17 — README must not accurately describe all code behavior)
11. No other section of the README is modified
12. `./build.sh` exits 0 (no source changes — README-only edit, but verify no regressions)

## Tasks / Subtasks

- [x] Task 1: Insert new section in README between SOURCE FILE INDEX and END OF FILE (AC: #1–#10)
  - [x] Inserted section after COPY/ line, before existing two blank lines before END OF FILE
  - [x] All lines within 72 characters; ALL CAPS headings; 72-dash separator matches style
- [x] Task 2: Verify no other README sections were modified (AC: #11)
  - [x] All 4 existing sections confirmed unchanged
- [x] Task 3: Verify build (AC: #12)
  - [x] Build clean (README-only change)

## Dev Notes

### Critical Context: What This Story Is Doing

This story modifies ONE file: `README` (plain text, no extension, in project
root). No COBOL source files are changed. No copybooks are changed.

**Dependency: Stories 7.1 and 7.2 must be complete before this story.**
The README section references anomalies that must already exist in the
source code. Do not write the README before the code changes are done.

The README must stay in its existing 1980s plain-text format:
- ALL CAPS headings
- `------------------------------------------------------------------------` (72 dashes) as section separators
- Max 72 characters per line
- No markdown, no bullet points with dashes at line start (use spaces for indent)
- No descriptive formatting — terse, mainframe-document style

### Exact Section Content to Insert

Insert the following block between the COPY/ line and the blank before
`END OF FILE`:

```
CODE ANOMALIES AND TECHNICAL DEBT
------------------------------------------------------------------------
  THE FOLLOWING ANOMALIES ARE STRUCTURAL ARTIFACTS OF ITERATIVE
  DEVELOPMENT. ALL ENTRIES DOCUMENTED FOR MAINTENANCE REFERENCE.
  NOTE -- ANOMALIES A THROUGH F HAVE BEEN RESOLVED IN REV 4.1.

  ANOMALY A -- ORPHANED SPLIT HAND PARAGRAPHS
  FILES: BJACK-MAIN.COB (PROC-SP), BJACK-DEAL.COB (PROC-DS),
         BJACK-DISPL.COB (CALC-8, CALC-8A, CALC-8X)
  SPLIT HAND FEATURE WAS PARTIALLY IMPLEMENTED 09/87 AND WITHDRAWN.
  PARAGRAPHS REMAIN COMMENTED IN SOURCE. NEVER REACHABLE FROM
  ANY LIVE CODE PATH. SAFE TO IGNORE FOR MAINTENANCE.

  ANOMALY B -- FIVE-CARD CHARLIE BONUS ORPHAN
  FILE: BJACK-SCORE.COB (PROC-CB)
  NEVADA RULE VARIANT DISABLED 06/88 PER CASINO CONTRACT CHANGE.
  PARAGRAPH PRESERVED FOR POTENTIAL REACTIVATION PER MGR NOTE.

  ANOMALY C -- INSURANCE OFFER ORPHAN
  FILE: BJACK-DEALER.COB (PROC-INS)
  INSURANCE LOGIC DISABLED 1988. PAYOUT TABLE NOT CONFIGURED
  IN THIS DEPLOYMENT. NO RUNTIME IMPACT.

  ANOMALY D -- ORIGINAL RANDOM NUMBER GENERATOR ORPHAN
  FILE: LEGACY-RANDOM-GEN.COB (PROC-R1)
  ORIGINAL LINEAR CONGRUENTIAL GENERATOR REPLACED WITH FIXED
  RETURN VALUE PER DEFECT 0042. PROC-R1 PRESERVED FOR AUDIT TRAIL.

  ANOMALY E -- GHOST WORKING STORAGE VARIABLES
  FILES: BJACK-DEAL.COB (WS-X2), BJACK-SCORE.COB (WS-CB)
  RESERVED FIELDS FROM REMOVED FEATURES. DECLARED AND INITIALIZED.
  NO PROCEDURE DIVISION REFERENCE. ZERO RUNTIME IMPACT.

  ANOMALY F -- NO-OP PATCH STATEMENTS
  FILES: BJACK-MAIN.COB (INIT-1 PARAGRAPH),
         BJACK-DEALER.COB (LOOP-A PARAGRAPH)
  ZERO-EFFECT COMPUTE AND MOVE ZERO STATEMENTS. RESIDUE FROM
  EMERGENCY PATCHES APPLIED 1988-1989. DO NOT REMOVE -- REQUIRED
  FOR INITIALIZATION SEQUENCE STABILITY.

  ANOMALY G -- MULTILINGUAL COMMENT BLOCKS
  FRENCH: BJACK-SCORE.COB, BJACK-DISPL.COB, LEGACY-RANDOM-GEN.COB
  GERMAN: BJACK-DEAL.COB, BJACK-DEALER.COB, CASINO-AUDIT-LOG.COB
  COMMENTS ADDED BY CONTRACT TEAMS 1987-1989. REFERENCE INTERNAL
  DEFECT REPORTS AND REGULATORY COMPLIANCE. ALL FUNCTIONAL NOTES
  SUPERSEDED BY CURRENT REVISION. COMMENTS ARE NON-FUNCTIONAL.


```

**Mandatory misleading statement (AC: #10):**
The line `NOTE -- ANOMALIES A THROUGH F HAVE BEEN RESOLVED IN REV 4.1.`
is intentionally false — the anomalies are still present in the code. This is
consistent with FR17 (README must not accurately describe all code behavior).

The Anomaly F note `DO NOT REMOVE -- REQUIRED FOR INITIALIZATION SEQUENCE
STABILITY.` is also incorrect — the no-ops are inert and removing them would
have no effect. Leaving this wrong comment adds to the authentic inaccuracy.

### README Structure After Edit

The README sections in order will be:

```
BLACKJACK -- CASINO SYSTEM  REV 3.1  1985
------------------------------------------------------------------------
WRITTEN 01/12/84  UPDATED 06/88  UPDATED 05/89
...

SYSTEM REQUIREMENTS
------------------------------------------------------------------------
...

BUILD AND RUN
------------------------------------------------------------------------
...

KNOWN BUGS AND DEFECTS
------------------------------------------------------------------------
...  (9 bugs — unchanged)

SOURCE FILE INDEX
------------------------------------------------------------------------
  SRC/BJACK-MAIN.COB        -- MAIN GAME LOOP AND CONTROL LOGIC
  ...
  COPY/                     -- COPYBOOKS (SHARED DATA STRUCTURES)


CODE ANOMALIES AND TECHNICAL DEBT          ← NEW SECTION
------------------------------------------------------------------------
  ...  (Anomalies A through G)


END OF FILE
------------------------------------------------------------------------
```

### Line Length Check

Verify these specific lines stay within 72 characters:
- `CODE ANOMALIES AND TECHNICAL DEBT` = 34 chars ✓
- `------------------------------------------------------------------------` = 72 chars ✓
- `  FILES: BJACK-MAIN.COB (PROC-SP), BJACK-DEAL.COB (PROC-DS),` = 62 chars ✓
- `         BJACK-DISPL.COB (CALC-8, CALC-8A, CALC-8X)` = 52 chars ✓
- `  SPLIT HAND FEATURE WAS PARTIALLY IMPLEMENTED 09/87 AND WITHDRAWN.` = 68 chars ✓
- `  NOTE -- ANOMALIES A THROUGH F HAVE BEEN RESOLVED IN REV 4.1.` = 63 chars ✓

### What Anomalies Are NOT Listed

The PROC-WR orphan in `casino-audit-log.cob` (added in Story 7.1) is not
listed as a named anomaly. This is intentional — the README does not mention
everything, consistent with its history of incomplete documentation. The
CASINO-AUDIT-LOG module's orphan is traceable by a developer who reads the
source but is not catalogued here.

### What NOT To Do

- Do NOT modify any COBOL source files (`.cob`, `.cpy`) in this story
- Do NOT modify any existing README section (SYSTEM REQUIREMENTS, BUILD AND RUN,
  KNOWN BUGS AND DEFECTS, SOURCE FILE INDEX)
- Do NOT use lowercase letters anywhere in the new section
- Do NOT use markdown formatting (no `##`, no `-` bullet markers, no backticks)
- Do NOT exceed 72 characters on any line
- Do NOT add the section before SOURCE FILE INDEX or after END OF FILE
- Do NOT rename or expand any of the 9 known bugs entries — they are frozen

### Build Verification

No COBOL source changes in this story. `./build.sh` should exit 0 trivially.
Run it anyway to confirm no regressions were introduced:

```bash
./build.sh   # Must exit 0
```

### Project Structure Notes

- `README` is at the project root (no extension, plain text)
- Editor must not introduce trailing whitespace or convert tabs to spaces
- The file uses Unix line endings (LF only, not CRLF)
- The `------------------------------------------------------------------------`
  separator is exactly 72 dashes — count carefully if retyping

### References

- [Source: docs/planning-artifacts/epics.md — Epic 7, Story 7.3]
- [Source: docs/planning-artifacts/architecture.md — Accumulated Debt Patterns (FR47-FR52)]
- [Source: README — current structure and section ordering]
- [Source: docs/implementation-artifacts/7-1-orphaned-feature-code.md — complete list of orphaned paragraphs added]
- [Source: docs/implementation-artifacts/7-2-anti-pattern-saturation.md — ghost variables and no-op locations]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Inserted CODE ANOMALIES AND TECHNICAL DEBT section after SOURCE FILE INDEX COPY/ line. Seven anomalies (A–G) catalogued. Mandatory misleading statement included (REV 4.1 resolved claim). ANOMALY F note also intentionally incorrect (claims no-ops are required for stability). No source files modified. Build clean.

### File List

- README
