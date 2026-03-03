#!/bin/bash
# EPIC 3 DEFECT VERIFICATION TEST SUITE
# Compiles each test harness against pre-built module objects and runs it.
# Run from project root: bash test/run-tests.sh
set -e

echo "--- COMPILING MODULES ---"
cobc -c -I copy/ src/bjack-deck.cob
cobc -c -I copy/ src/bjack-deal.cob
cobc -c -I copy/ src/bjack-score.cob
cobc -c -I copy/ src/bjack-dealer.cob
cobc -c -I copy/ src/legacy-random-gen.cob

echo ""
echo "=== T31: BIASED SHUFFLE VERIFICATION (STORY 3.1) ==="
cobc -x -I copy/ -o t31 test/t31-deck-bias.cob \
    bjack-deck.o legacy-random-gen.o
./t31

echo ""
echo "=== T32: OFF-BY-ONE DEAL VERIFICATION (STORY 3.2) ==="
cobc -x -I copy/ -o t32 test/t32-deal-obo.cob \
    bjack-deck.o bjack-deal.o legacy-random-gen.o
./t32

echo ""
echo "=== T33: ACE RECALCULATION FAILURE (STORY 3.3) ==="
cobc -x -I copy/ -o t33 test/t33-score-ace.cob \
    bjack-score.o
./t33

echo ""
echo "=== T34: SOFT 17 STAND BUG (STORY 3.4) ==="
cobc -x -I copy/ -o t34 test/t34-dealer-s17.cob \
    bjack-dealer.o
./t34

echo ""
echo "=== T61: PAYOUT ROUNDING ERROR (STORY 6.1) ==="
grep -qF "WS-BET * 3 / 2" src/bjack-main.cob || \
    { echo "FAIL: T61 source guard -- truncation formula not found in PROC-NB"; exit 1; }
echo "  [SRC] PASS: truncation formula confirmed in bjack-main.cob PROC-NB"
cobc -x -I copy/ -o t61 test/t61-payout-round.cob
./t61

echo ""
echo "=== T62: DOUBLE-DOWN-ANYTIME RULE VIOLATION (STORY 6.2) ==="
grep -qF "COMPUTE WS-BET = WS-BET * 2" src/bjack-main.cob || \
    { echo "FAIL: T62 source guard -- D-branch not found in LOOP-A"; exit 1; }
if grep -qF "WS-PC NOT = 2" src/bjack-main.cob; then
    echo "FAIL: T62 source guard -- WS-PC NOT = 2 guard found (bug was fixed)"; exit 1
fi
echo "  [SRC] PASS: D-branch present, no WS-PC NOT = 2 guard in bjack-main.cob"
cobc -x -I copy/ -o t62 test/t62-double-down-anytime.cob
./t62

echo ""
echo "=== T63: BET-OVER-BALANCE STALE VARIABLE (STORY 6.3) ==="
grep -qF "IF WS-BET > WS-BL" src/bjack-main.cob || \
    { echo "FAIL: T63 source guard -- WS-BL check not found in BET-1"; exit 1; }
echo "  [SRC] PASS: stale variable check confirmed in bjack-main.cob BET-1"
cobc -x -I copy/ -o t63 test/t63-bet-over-balance.cob
./t63

echo ""
echo "--- ALL DEFECT VERIFICATIONS COMPLETE ---"
