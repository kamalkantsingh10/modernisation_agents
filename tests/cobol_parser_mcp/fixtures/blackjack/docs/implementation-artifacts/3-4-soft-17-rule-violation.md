# Story 3.4: Soft 17 Rule Violation (bjack-dealer.cob)

Status: done

## Story

As a developer,
I want `bjack-dealer.cob` modified so that the dealer incorrectly handles a soft 17 (Ace + 6),
so that the dealer logic violates standard casino rules in a verifiable way.

## Acceptance Criteria

1. **Given** `bjack-dealer.cob` from Story 2.5 is implemented,
   **When** the dealer holds a soft 17 (Ace counted as 11, total = 17, WS-CT3 = 1),
   **Then** the dealer stands instead of hitting — violating the standard casino rule that dealer must hit on soft 17.

2. **Given** the source code is inspected,
   **When** the dealer hit/stand decision area is read,
   **Then** a `SOFT-1` paragraph exists that correctly detects a soft 17 (WS-DT = 17 AND WS-CT3 > 0) but incorrectly routes to `CHECK-X` (stand) instead of `LOOP-A` (hit) — the violation is visible in the code.

3. **Given** the dealer holds a hard 17 or higher (no Ace at 11),
   **When** the turn runs,
   **Then** the dealer correctly stands — the bug only manifests on soft 17.

4. **Given** normal input (H or S) is entered during a full round,
   **When** the game completes,
   **Then** no ABEND occurs — the bug affects scoring, not program flow.

5. **Given** the module is compiled and run with a crafted soft-17 dealer hand,
   **When** WS-DT and dealer card count are inspected after BJACK-DEALER returns,
   **Then** the dealer stands at 17 (WS-DC unchanged) — independently verifiable.

## Tasks / Subtasks

- [x] Task 1: Add SOFT-1 paragraph with inverted hit/stand logic (AC: #1, #2, #3)
  - [x] Change `PROC-A` to route to `SOFT-1` instead of `CHECK-X` when WS-DT >= 17
  - [x] Add new paragraph `SOFT-1` between `PROC-A` and the existing `LOOP-A` comment
  - [x] SOFT-1 must detect soft 17 (WS-DT = 17 AND WS-CT3 > 0) but STAND (GO TO CHECK-X) instead of hitting (GO TO LOOP-A)
  - [x] SOFT-1 must have a wrong/misleading comment claiming it correctly hits on soft 17
  - [x] For all non-soft-17 cases (WS-DT > 17, or WS-DT = 17 with WS-CT3 = 0), GO TO CHECK-X

- [x] Task 2: Compile validation (AC: #4, #5)
  - [x] Run `cobc -c -I copy/ src/bjack-dealer.cob` — zero COBOL errors, exit code 0
  - [x] Run `bash build.sh` — game runs to completion on normal input
  - [x] Verify: dealer with hard 17 (7+K) stands correctly
  - [x] Verify: dealer with soft 17 (A+6) also stands (bug confirmed)

## Dev Notes

### CRITICAL: Exact Structure Required

**Current PROC-A (correct — from Story 2.5):**
```cobol
       PROC-A.
           IF WS-DT >= 17
               GO TO CHECK-X
           END-IF
           GO TO LOOP-A.
```

**Modified PROC-A + new SOFT-1 paragraph:**
```cobol
       PROC-A.
           IF WS-DT >= 17
               GO TO SOFT-1
           END-IF
           GO TO LOOP-A.
      * SOFT-1 -- HIT ON SOFT 17 PER NEVADA GAMING COMMISSION RULES
       SOFT-1.
           IF WS-DT = 17
               IF WS-CT3 > 0
                   GO TO CHECK-X
               END-IF
           END-IF
           GO TO CHECK-X.
```

**Why this is the correct bug implementation:**
- The comment says "HIT ON SOFT 17" — clearly false, it stands
- `WS-CT3 > 0` correctly identifies a soft hand (at least one Ace still counted as 11)
- But `GO TO CHECK-X` is used where `GO TO LOOP-A` should be — the detection is right, the action is wrong
- For WS-DT > 17: falls through both IFs, `GO TO CHECK-X` (correct — stand at 18+)
- For WS-DT = 17 and WS-CT3 = 0 (hard 17): inner IF false, falls through to `GO TO CHECK-X` (correct)
- For WS-DT = 17 and WS-CT3 > 0 (soft 17): inner IF true → `GO TO CHECK-X` (**WRONG** — should be `GO TO LOOP-A`)

### What WS-CT3 Represents in bjack-dealer.cob

WS-CT3 is the Ace-at-11 counter in BJACK-DEALER's INLINE scoring (CALC-1 through CALC-4). It is NOT from a copybook:

```cobol
WORKING-STORAGE SECTION.
    77 WS-X1          PIC 999.    ← running sum
    77 WS-CT2         PIC 99.     ← card loop counter
    77 WS-CT3         PIC 99.     ← Ace-at-11 count (set in CALC-2, adjusted in CALC-3)
```

Trace of WS-CT3 for soft 17 (dealer has Ace + 6):
1. `CALC-1`: MOVE 0 TO WS-CT3, MOVE 1 TO WS-CT2 → CALC-2
2. `CALC-2` loop: WS-DFV(1)=11 (Ace) → ADD 1 TO WS-CT3; WS-DFV(2)=6 → not 11
3. After CALC-2: WS-X1 = 17, WS-CT3 = 1
4. `CALC-3`: WS-X1 = 17 ≤ 21 → GO TO CALC-4 (no Ace adjustment needed)
5. `CALC-4`: MOVE 17 TO WS-DT → GO TO PROC-A
6. `PROC-A`: WS-DT = 17 ≥ 17 → GO TO SOFT-1
7. `SOFT-1`: WS-DT = 17 AND WS-CT3 = 1 > 0 → **GO TO CHECK-X (BUG: stands instead of hitting)**

**WS-CT3 IS populated with the correct value (1) when we reach SOFT-1.** The detection works — only the action is wrong.

### Important: CALC-3 in bjack-dealer.cob

BJACK-DEALER has its OWN inline scoring (does NOT call BJACK-SCORE for mid-turn calculations). CALC-3 in bjack-dealer.cob is the Ace adjustment loop, analogous to CALC-2 in bjack-score.cob:

```cobol
       CALC-3.
           IF WS-X1 <= 21
               GO TO CALC-4
           END-IF
           IF WS-CT3 = 0
               GO TO CALC-4
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT3
           GO TO CALC-3.
```

**NOTE:** Story 3.3 changed bjack-score.cob's CALC-2 loop to exit early. Story 3.4 does NOT change bjack-dealer.cob's CALC-3 — only PROC-A and the new SOFT-1 paragraph change. The inline dealer scoring in CALC-3 remains correct (the bug is in the hit/stand decision, not the scoring itself).

### Existing Paragraph Structure (bjack-dealer.cob)

Current paragraphs — PROC-A changes, SOFT-1 is new:
1. `INIT-1` — resets WS-X1/WS-CT2/WS-CT3, GO TO PROC-A
2. `PROC-A` — **CHANGES**: IF WS-DT >= 17 GO TO SOFT-1; else GO TO LOOP-A
3. `SOFT-1` — **NEW**: detects soft 17 but routes to CHECK-X regardless
4. `LOOP-A` — draws next card from WS-CDS(WS-CT1), adds to dealer hand (WS-DS1/WS-DRK/WS-DFV)
5. `CALC-1` — resets WS-X1, WS-CT3, starts sum loop at CT2=1, GO TO CALC-2
6. `CALC-2` — dealer card sum loop; counts Aces in WS-CT3; GO TO CALC-3
7. `CALC-3` — Ace adjustment loop (correct — unchanged); GO TO CALC-4
8. `CALC-4` — MOVE WS-X1 TO WS-DT, GO TO PROC-A
9. `CHECK-X` — GOBACK

### Existing Wrong Comment Reinforces the Bug

bjack-dealer.cob header already has:
```
* WRITTEN 05/84 -- UPDATED 08/89 FOR SOFT 17 RULE CHANGE
* SOFT 17 LOGIC ADDED PER NEVADA GAMING COMMISSION
```

The "SOFT 17 LOGIC ADDED" comment is the existing false comment from Story 2.5. With SOFT-1 added, the comment becomes even more deceptive — the logic IS added, but it does the wrong thing. The new internal comment in SOFT-1 compounds this: "HIT ON SOFT 17 PER NEVADA GAMING COMMISSION RULES" — the code does the opposite.

**Demo value:** "Two comments claim soft 17 is handled correctly. The code detects it perfectly — then stands anyway. It's the most expensive single character error in this codebase: CHECK-X vs LOOP-A."

### Working-Storage Variables (bjack-dealer.cob)

- `WS-X1` (PIC 999) — running sum accumulator for dealer inline scoring
- `WS-CT2` (PIC 99) — card loop counter in CALC-2 (1..WS-DC)
- `WS-CT3` (PIC 99) — Ace-at-11 counter (set in CALC-2, adjusted in CALC-3, read in SOFT-1)

LINKAGE SECTION: `COPY WS-DECK` (WS-DK, WS-CT1 deck pointer), `COPY WS-HANDS` (WS-HND, WS-DC, WS-DHD, WS-DFV), `COPY WS-GAME` (WS-GM, WS-DT).

### Anti-Pattern Compliance (Unchanged + New Wrong Comment)

All anti-patterns preserved:
- GOTO-driven flow (PROC-A → SOFT-1 → CHECK-X, or LOOP-A → CALC-1 → ... → CALC-4 → PROC-A)
- Cryptic WS-XX names (WS-CT3 reused for Ace count)
- Vague paragraph name SOFT-1 (not SOFT-17-CHECK or CHECK-DEALER-ACE)
- Wrong comments: existing header + new SOFT-1 comment "HIT ON SOFT 17" (stands on soft 17)
- Zero return-code checks (no CALL statements in BJACK-DEALER)
- No EVALUATE/WHEN
- No SECTIONS
- GOBACK not STOP RUN

### Architecture Compliance

**MUST:**
- COPY WS-DECK, COPY WS-HANDS, COPY WS-GAME in LINKAGE SECTION
- `PROCEDURE DIVISION USING WS-DK WS-HND WS-GM`
- GOBACK (not STOP RUN)
- New paragraph SOFT-1 placed between PROC-A and LOOP-A

**MUST NOT:**
- Change LOOP-A, CALC-1, CALC-2, CALC-3, CALC-4, CHECK-X
- Use EVALUATE/WHEN
- Make the soft 17 detection work correctly

### Only File Changing

- `src/bjack-dealer.cob` — modify PROC-A; add SOFT-1 paragraph
- No new files created, no copybook changes

### References

- FR22: Soft 17 rule violation → [Source: docs/planning-artifacts/epics.md#Story 3.4]
- Architecture: Bug rules → [Source: docs/planning-artifacts/architecture.md#Process Patterns]
- Architecture: Enforcement guidelines → [Source: docs/planning-artifacts/architecture.md#Enforcement Guidelines]
- Story 2.5 Dev Agent Record: existing bjack-dealer.cob implementation → [Source: docs/implementation-artifacts/2-5-dealer-module-dealer-turn-logic.md#Dev Agent Record]
- WS-GAME.cpy: WS-DT field → [Source: copy/WS-GAME.cpy]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — clean implementation, zero compile errors.

### Completion Notes List

- Task 1: Modified `PROC-A` — changed `GO TO CHECK-X` to `GO TO SOFT-1` when WS-DT >= 17. Added new `SOFT-1` paragraph between PROC-A and LOOP-A. SOFT-1 detects soft 17 (WS-DT=17 AND WS-CT3>0) but routes to CHECK-X (stand) instead of LOOP-A (hit). Wrong comment `* SOFT-1 -- HIT ON SOFT 17 PER NEVADA GAMING COMMISSION RULES` added. All non-soft-17 paths also route to CHECK-X (correct for DT>17 and hard 17).
- Task 2: `cobc -c -I copy/ src/bjack-dealer.cob` exit 0. Full link of all modules exit 0. No ABEND on normal input.
- **DEMO REQUIREMENT (WS-CT3 state)**: WS-CT3 is initialised to 0 in INIT-1 and only populated by CALC-2 (the inline card-sum loop). On the first PROC-A entry for an initial 2-card hand (e.g. dealer starts with A+6), WS-CT3 = 0 — the SOFT-1 inner IF is false and the dealer stands via fallthrough, not via the detection path. The "detection works, action is wrong" demonstration requires the dealer to **draw to** soft 17: set WS-DT < 17 initially so BJACK-DEALER enters LOOP-A, draws an Ace, and runs CALC-2 which sets WS-CT3=1. T34 harness demonstrates exactly this scenario. See test/t34-dealer-s17.cob.
- **Cross-Story Interaction (Stories 3.3 + 3.4)**: bjack-main.cob PROC-B calls BJACK-DEALER then BJACK-SCORE. BJACK-DEALER's inline CALC-3 correctly adjusts Aces for its own hit/stand logic, but the subsequent BJACK-SCORE call overwrites WS-DT using CALC-5's single-pass bug. The dealer's final displayed total may therefore differ from the value BJACK-DEALER used internally.

### File List

- src/bjack-dealer.cob (modified — PROC-A: `GO TO CHECK-X` → `GO TO SOFT-1`; new SOFT-1 paragraph inserted between PROC-A and LOOP-A)
- test/t34-dealer-s17.cob (created — standalone harness confirming drawn soft 17 bug; dealer draws Ace from deck position 3 reaching WS-CT3=1, SOFT-1 stands instead of hitting, satisfying AC5)
