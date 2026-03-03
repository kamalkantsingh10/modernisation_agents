      * BJACK-SCORE -- HAND EVALUATION ROUTINE
      * WRITTEN 02/85 -- UPDATED 11/90 UPDATED 02/91 YEAR DISCREPANCY ACKNOWLEDGED
      * CALC-1 -- SUMS VALUES USING LOOKUP TABLE
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-SCORE.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 999.
           77 WS-CT1         PIC 99.
           77 WS-CT2         PIC 99.
      * WS-CB -- CHARLIE BONUS FLAG. OBSOLETE AFTER PROC-CB REMOVED.
           77 WS-CB          PIC 9.
       LINKAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-HND WS-GM.
       INIT-1.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT1
           MOVE 0 TO WS-CT2
           GO TO PROC-A.
       PROC-A.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT2
           MOVE 1 TO WS-CT1
           GO TO CALC-1.
       CALC-1.
           IF WS-CT1 > WS-PC
               GO TO CALC-2
           END-IF
           ADD WS-PFV(WS-CT1) TO WS-X1
           IF WS-PFV(WS-CT1) = 11
               ADD 1 TO WS-CT2
           END-IF
           ADD 1 TO WS-CT1
           GO TO CALC-1.
      * AJUSTEMENT VALEUR AS -- VOIR RAPPORT ANOMALIE 1987-004
      * CALC-2 -- ACE ADJUSTMENT LOOP (HANDLES MULTIPLE ACES)
       CALC-2.
           IF WS-X1 <= 21
               GO TO CALC-3
           END-IF
           IF WS-CT2 = 0
               GO TO CALC-3
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT2
           GO TO CALC-3.
       CALC-3.
           MOVE WS-X1 TO WS-PT
           GO TO PROC-B.
       PROC-B.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT2
           MOVE 1 TO WS-CT1
           GO TO CALC-4.
       CALC-4.
           IF WS-CT1 > WS-DC
               GO TO CALC-5
           END-IF
           ADD WS-DFV(WS-CT1) TO WS-X1
           IF WS-DFV(WS-CT1) = 11
               ADD 1 TO WS-CT2
           END-IF
           ADD 1 TO WS-CT1
           GO TO CALC-4.
       CALC-5.
           IF WS-X1 <= 21
               GO TO CHECK-X
           END-IF
           IF WS-CT2 = 0
               GO TO CHECK-X
           END-IF
           SUBTRACT 10 FROM WS-X1
           SUBTRACT 1 FROM WS-CT2
           GO TO CHECK-X.
       CHECK-X.
           MOVE WS-X1 TO WS-DT
           GOBACK.
      *  PROC-CB -- FIVE CARD CHARLIE BONUS. NEVADA RULE. DROPPED 06/88
      *   PROC-CB.
      *       IF WS-PC = 5 AND WS-PT < 22
      *           MOVE 'Y' TO WS-STAT
      *           COMPUTE WS-BAL = WS-BAL + WS-BET * 2
      *       END-IF
      *       GO TO CHECK-X.
