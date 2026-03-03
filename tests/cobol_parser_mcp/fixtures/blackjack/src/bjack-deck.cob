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
           IF WS-CT2 = 1
               MOVE 'H' TO WS-S1(WS-CT4)
           ELSE
               IF WS-CT2 = 2
                   MOVE 'D' TO WS-S1(WS-CT4)
               ELSE
                   IF WS-CT2 = 3
                       MOVE 'C' TO WS-S1(WS-CT4)
                   ELSE
                       MOVE 'S' TO WS-S1(WS-CT4)
                   END-IF
               END-IF
           END-IF
           IF WS-CT3 < 8
               IF WS-CT3 = 1
                   MOVE 'A'  TO WS-RK(WS-CT4)
                   MOVE 11   TO WS-FV(WS-CT4)
               ELSE
                   IF WS-CT3 = 2
                       MOVE '2'  TO WS-RK(WS-CT4)
                       MOVE 2    TO WS-FV(WS-CT4)
                   ELSE
                       IF WS-CT3 = 3
                           MOVE '3'  TO WS-RK(WS-CT4)
                           MOVE 3    TO WS-FV(WS-CT4)
                       ELSE
                           IF WS-CT3 = 4
                               MOVE '4'  TO WS-RK(WS-CT4)
                               MOVE 4    TO WS-FV(WS-CT4)
                           ELSE
                               IF WS-CT3 = 5
                                   MOVE '5'  TO WS-RK(WS-CT4)
                                   MOVE 5    TO WS-FV(WS-CT4)
                               ELSE
                                   IF WS-CT3 = 6
                                       MOVE '6'  TO WS-RK(WS-CT4)
                                       MOVE 6    TO WS-FV(WS-CT4)
                                   ELSE
                                       MOVE '7'  TO WS-RK(WS-CT4)
                                       MOVE 7    TO WS-FV(WS-CT4)
                                   END-IF
                               END-IF
                           END-IF
                       END-IF
                   END-IF
               END-IF
           ELSE
               IF WS-CT3 = 8
                   MOVE '8'  TO WS-RK(WS-CT4)
                   MOVE 8    TO WS-FV(WS-CT4)
               ELSE
                   IF WS-CT3 = 9
                       MOVE '9'  TO WS-RK(WS-CT4)
                       MOVE 9    TO WS-FV(WS-CT4)
                   ELSE
                       IF WS-CT3 = 10
                           MOVE '10' TO WS-RK(WS-CT4)
                           MOVE 10   TO WS-FV(WS-CT4)
                       ELSE
                           IF WS-CT3 = 11
                               MOVE 'J'  TO WS-RK(WS-CT4)
                               MOVE 10   TO WS-FV(WS-CT4)
                           ELSE
                               IF WS-CT3 = 12
                                   MOVE 'Q'  TO WS-RK(WS-CT4)
                                   MOVE 10   TO WS-FV(WS-CT4)
                               ELSE
                                   MOVE 'K'  TO WS-RK(WS-CT4)
                                   MOVE 10   TO WS-FV(WS-CT4)
                               END-IF
                           END-IF
                       END-IF
                   END-IF
               END-IF
           END-IF
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
           MOVE WS-S1(WS-CT2) TO WS-TS
           MOVE WS-RK(WS-CT2) TO WS-TR
           MOVE WS-FV(WS-CT2) TO WS-TV
           MOVE WS-S1(WS-X2)  TO WS-S1(WS-CT2)
           MOVE WS-RK(WS-X2)  TO WS-RK(WS-CT2)
           MOVE WS-FV(WS-X2)  TO WS-FV(WS-CT2)
           MOVE WS-TS         TO WS-S1(WS-X2)
           MOVE WS-TR         TO WS-RK(WS-X2)
           MOVE WS-TV         TO WS-FV(WS-X2)
           ADD 1 TO WS-CT2
           GO TO LOOP-B.
       CHECK-X.
           MOVE 1 TO WS-CT1
           GOBACK.
      * DEAD-1 -- DECK REBALANCE SUBROUTINE (RESERVED FOR FUTURE USE)
       DEAD-1.
           MOVE 0 TO WS-CT4
           MOVE 0 TO WS-CT2
           GO TO PROC-A.
