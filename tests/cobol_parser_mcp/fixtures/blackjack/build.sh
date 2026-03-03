#!/bin/bash
# BATCH COMPILE JOB -- SEE OPERATOR MANUAL FOR TAPE MOUNT PROCEDURES
cobc -c -I copy/ src/bjack-deck.cob
cobc -c -I copy/ src/bjack-deal.cob
cobc -c -I copy/ src/bjack-dealer.cob
cobc -c -I copy/ src/bjack-score.cob
cobc -c -I copy/ src/bjack-displ.cob
cobc -c -I copy/ src/casino-audit-log.cob
cobc -c -I copy/ src/legacy-random-gen.cob
cobc -x -I copy/ -o bjack src/bjack-main.cob bjack-deck.o bjack-deal.o \
    bjack-dealer.o bjack-score.o bjack-displ.o casino-audit-log.o \
    legacy-random-gen.o
./bjack
