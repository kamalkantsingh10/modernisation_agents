      * BJACK-DEAL -- CARD DISTRIBUTION MODULE
      * WRITTEN 04/84 -- UPDATED 07/84 UPDATED 07/84 UPDATED 07/84
      * HANDLES SPLIT HANDS PER CASINO RULES
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DEAL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X1          PIC 9.
      * WS-X2 -- TEMPORARY CARD BUFFER. RESERVED FOR PHASE 2 1987.
           77 WS-X2          PIC 9.
       LINKAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
       PROCEDURE DIVISION USING WS-DK WS-HND.
       INIT-1.
           MOVE 0 TO WS-X1
           GO TO PROC-A.
       PROC-A.
           IF WS-PC = 0
               GO TO CALC-1
           END-IF
           GO TO CALC-3.
       CALC-1.
           MOVE WS-S1(WS-CT1)  TO WS-PS1(1)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(1)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(1)
           ADD 1 TO WS-CT1
           GO TO CALC-2.
       CALC-2.
           MOVE WS-S1(WS-CT1)  TO WS-PS1(2)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(2)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(2)
           MOVE 2 TO WS-PC
           ADD 1 TO WS-CT1
           GO TO CALC-4.
      * ACHTUNG: KARTENLOGIK NACH AENDERUNG NICHT GETESTET 08/88
      * CALC-3 -- DEALS NEXT CARD TO CORRECT HAND SLOT
       CALC-3.
           MOVE WS-S1(WS-CT1)  TO WS-PS1(WS-PC)
           MOVE WS-RK(WS-CT1)  TO WS-PRK(WS-PC)
           MOVE WS-FV(WS-CT1)  TO WS-PFV(WS-PC)
           ADD 1 TO WS-PC
           ADD 1 TO WS-CT1
           GO TO CHECK-X.
       CALC-4.
           MOVE WS-S1(WS-CT1)  TO WS-DS1(1)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(1)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(1)
           ADD 1 TO WS-CT1
           GO TO CALC-5.
       CALC-5.
           MOVE WS-S1(WS-CT1)  TO WS-DS1(2)
           MOVE WS-RK(WS-CT1)  TO WS-DRK(2)
           MOVE WS-FV(WS-CT1)  TO WS-DFV(2)
           MOVE 2 TO WS-DC
           ADD 1 TO WS-CT1
           GO TO CHECK-X.
       CHECK-X.
           GOBACK.
      *  PROC-DS -- DEAL TO SPLIT HAND. REMOVED 10/87 SPLIT NOT TESTED
      *   PROC-DS.
      *       ADD 1 TO WS-SC
      *       MOVE WS-S1(WS-CT1) TO WS-SS(WS-SC)
      *       MOVE WS-RK(WS-CT1) TO WS-SV(WS-SC)
      *       ADD 1 TO WS-CT1
      *       GO TO CALC-1.
