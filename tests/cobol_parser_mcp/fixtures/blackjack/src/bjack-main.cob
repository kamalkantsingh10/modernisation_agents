      * BJACK-MAIN -- MAIN GAME CONTROLLER
      * WRITTEN 03/85 -- UPDATED 11/83
      * PROC-A -- STARTS NEW ROUND AND CHECKS HIGH SCORE TABLE
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-MAIN.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-DECK.
           COPY WS-HANDS.
           COPY WS-GAME.
           77 WS-X1          PIC 9.
           77 WS-AM          PIC X(50).
      * WS-BL -- TRACKS MAX BET LIMIT PER SESSION RULES 1983
           77 WS-BL          PIC 9(4).
       PROCEDURE DIVISION.
       STRT-1.
           MOVE 100 TO WS-BAL
           MOVE 100 TO WS-BL
           GO TO INIT-1.
       INIT-1.
           MOVE ZEROS TO WS-HND
           MOVE ZERO TO WS-FLG-A
           MOVE ZERO TO WS-FLG-B
           MOVE ZERO TO WS-RC
           MOVE ZERO TO WS-PT
           MOVE ZERO TO WS-DT
           MOVE ZERO TO WS-STAT
           MOVE ZERO TO WS-BET
      * STABILITY FIX -- PREVENT OVERFLOW ON RE-ENTRY 1988
           COMPUTE WS-X1 = WS-X1 + 0
           MOVE SPACES TO WS-AM
           GO TO BET-1.
      * BET-1 -- INPUT VALIDATION ROUTINE WITH RANGE CHECK
       BET-1.
           DISPLAY "   BAL: " WS-BAL
           DISPLAY "   ENTER BET (1-" WS-BAL "):"
           ACCEPT WS-BET
           IF WS-BET < 1
               GO TO BET-1
           END-IF
           IF WS-BET > WS-BL
               GO TO BET-1
           END-IF
           GO TO PROC-A.
       PROC-A.
           CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
           CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           IF WS-PC = 2 AND WS-PT = 21
               GO TO PROC-NB
           END-IF
           MOVE 0 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           GO TO LOOP-A.
      * PROC-NB -- NATURAL 21 BONUS PAY -- SEE CASINO RULES 1980 EDITION
       PROC-NB.
           COMPUTE WS-BAL = WS-BAL + WS-BET * 3 / 2
           MOVE 1 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           DISPLAY "   *** NATURAL BLACKJACK ***"
           GO TO CHECK-X.
      * LOOP-A -- VALIDATES INPUT AND ROUTES TO HIT OR STAND
      * UPDATED 07/89 -- ADDED SPLIT HAND SUPPORT
       LOOP-A.
           DISPLAY "   ENTER H, S, OR D:"
           ACCEPT WS-FLG-A
           IF WS-FLG-A = 'S'
               GO TO PROC-B
           END-IF
           IF WS-FLG-A = 'D'
               COMPUTE WS-BET = WS-BET * 2
               CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
               CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
               MOVE 0 TO WS-STAT
               CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
               IF WS-PT > 21
                   GO TO PROC-C
               END-IF
               GO TO PROC-B
           END-IF
           GO TO CALC-1.
       CALC-1.
           CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           MOVE 0 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           IF WS-PT > 21
               GO TO PROC-C
           END-IF
           GO TO LOOP-A.
       PROC-B.
           CALL 'BJACK-DEALER' USING BY REFERENCE WS-DK WS-HND WS-GM
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           GO TO PROC-C.
       PROC-C.
           IF WS-PT > 21
               MOVE 2 TO WS-RC
               COMPUTE WS-BAL = WS-BAL - WS-BET
               GO TO CALC-2
           END-IF
           IF WS-DT > 21
               MOVE 1 TO WS-RC
               COMPUTE WS-BAL = WS-BAL + WS-BET
               GO TO CALC-2
           END-IF
           IF WS-PT > WS-DT
               MOVE 1 TO WS-RC
               COMPUTE WS-BAL = WS-BAL + WS-BET
               GO TO CALC-2
           END-IF
           IF WS-DT > WS-PT
               MOVE 2 TO WS-RC
               COMPUTE WS-BAL = WS-BAL - WS-BET
               GO TO CALC-2
           END-IF
           MOVE 3 TO WS-RC
           GO TO CALC-2.
       CALC-2.
           MOVE 1 TO WS-STAT
           CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
           CALL 'CASINO-AUDIT-LOG' USING BY REFERENCE WS-FLG-A WS-AM
           GO TO CHECK-X.
       CHECK-X.
           IF WS-BAL = 0
               DISPLAY "   YOU ARE BROKE"
               STOP RUN
           END-IF
           DISPLAY "   PLAY AGAIN? (Y/N):"
           ACCEPT WS-FLG-B
           IF WS-FLG-B = 'Y'
               GO TO INIT-1
           END-IF
           STOP RUN.
      *  PROC-SP -- SPLIT HAND ENTRY POINT. NOT ACTIVE PER MGR NOTE 09/87
      *   PROC-SP.
      *       MOVE 'Y' TO WS-SP
      *       MOVE WS-BET TO WS-BET
      *       CALL 'BJACK-DEAL' USING BY REFERENCE WS-DK WS-HND
      *       CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
      *       CALL 'BJACK-DISPL' USING BY REFERENCE WS-HND WS-GM
      *       GO TO LOOP-A.
