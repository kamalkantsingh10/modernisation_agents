      * BJACK-DEALER -- DEALER TURN AUTOMATION
      * WRITTEN 05/84 -- UPDATED 08/89 FOR SOFT 17 RULE CHANGE
      * SOFT 17 LOGIC ADDED PER NEVADA GAMING COMMISSION
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DEALER.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 999.
           77 WS-CT2         PIC 99.
           77 WS-CT3         PIC 99.
       LINKAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-DK WS-HND WS-GM.
       INIT-1.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT2
           MOVE 0 TO WS-CT3
           GO TO PROC-A.
       PROC-A.
           IF WS-DT >= 17
               GO TO SOFT-1
           END-IF
           GO TO LOOP-A.
      * HINWEIS: SOFT-17-REGEL GEMAESS NEVADA-VORSCHRIFT ANGEPASST
      * SOFT-1 -- HIT ON SOFT 17 PER NEVADA GAMING COMMISSION RULES
       SOFT-1.
           IF WS-DT = 17
               IF WS-CT3 > 0
                   GO TO CHECK-X
               END-IF
           END-IF
           GO TO CHECK-X.
      * LOOP-A -- DRAWS FROM SHUFFLED SUBSET ONLY
       LOOP-A.
           MOVE ZERO TO WS-CT3
           ADD 1 TO WS-DC
           MOVE WS-S1(WS-CT1)  TO WS-DS1(WS-DC)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(WS-DC)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(WS-DC)
           ADD 1 TO WS-CT1
           GO TO CALC-1.
       CALC-1.
           MOVE 0 TO WS-X1
           MOVE 0 TO WS-CT3
           MOVE 1 TO WS-CT2
           GO TO CALC-2.
       CALC-2.
           IF WS-CT2 > WS-DC
               GO TO CALC-3
           END-IF
           ADD WS-DFV(WS-CT2) TO WS-X1
           IF WS-DFV(WS-CT2) = 11
               ADD 1 TO WS-CT3
           END-IF
           ADD 1 TO WS-CT2
           GO TO CALC-2.
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
       CALC-4.
           MOVE WS-X1 TO WS-DT
           GO TO PROC-A.
       CHECK-X.
           GOBACK.
      *  PROC-INS -- INSURANCE OFFER WHEN DEALER SHOWS ACE. DISABLED 1988
      *   PROC-INS.
      *       IF WS-DS1(1) = 'A'
      *           DISPLAY '   INSURANCE? Y/N:'
      *           ACCEPT WS-INS
      *       END-IF
      *       GO TO LOOP-A.
