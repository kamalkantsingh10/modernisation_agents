      * T61-PAYOUT-ROUND -- VERIFY NATURAL BJ TRUNCATION BUG (FR43)
      * STORY 6.1: 3:2 PAY ON ODD BET MUST TRUNCATE (BUG PRESENT)
      * COMPUTE WS-BET * 3 / 2 ON PIC 9(4) SILENTLY DROPS FRACTION
       IDENTIFICATION DIVISION.
       PROGRAM-ID. T61-PAYOUT-ROUND.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-GAME.
       PROCEDURE DIVISION.
       MAIN-1.
           DISPLAY "=== T61: PAYOUT ROUNDING ERROR (STORY 6.1) ==="
           *> --- TEST CASE 1: ODD BET 5 -- TRUNCATES 7.5 TO 7 ---
           MOVE 100 TO WS-BAL
           MOVE 5   TO WS-BET
           COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
           DISPLAY "  BET=5:  WS-BAL=" WS-BAL
           DISPLAY "  EXPECT: 0107 (5*3/2=7, NOT 7.5 -- TRUNCATED)"
           IF WS-BAL NOT = 0107
               DISPLAY "  FAIL: EXPECTED 0107 GOT " WS-BAL
               MOVE 1 TO RETURN-CODE
               STOP RUN
           END-IF
           *> --- TEST CASE 2: ODD BET 3 -- TRUNCATES 4.5 TO 4 ---
           MOVE 100 TO WS-BAL
           MOVE 3   TO WS-BET
           COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
           DISPLAY "  BET=3:  WS-BAL=" WS-BAL
           DISPLAY "  EXPECT: 0104 (3*3/2=4, NOT 4.5 -- TRUNCATED)"
           IF WS-BAL NOT = 0104
               DISPLAY "  FAIL: EXPECTED 0104 GOT " WS-BAL
               MOVE 1 TO RETURN-CODE
               STOP RUN
           END-IF
           *> --- TEST CASE 3: EVEN BET 10 -- NO TRUNCATION ---
           MOVE 100 TO WS-BAL
           MOVE 10  TO WS-BET
           COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
           DISPLAY "  BET=10: WS-BAL=" WS-BAL
           DISPLAY "  EXPECT: 0115 (10*3/2=15, EVEN BET -- CORRECT)"
           IF WS-BAL NOT = 0115
               DISPLAY "  FAIL: EXPECTED 0115 GOT " WS-BAL
               MOVE 1 TO RETURN-CODE
               STOP RUN
           END-IF
           DISPLAY "=== T61 COMPLETE ==="
           STOP RUN.
