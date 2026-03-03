      * T33-SCORE-ACE -- VERIFY ACE RECALCULATION FAILURE (FR23)
      * STORY 3.3: A+A+K MUST SCORE 022 NOT 012 WITH BUG ACTIVE
       IDENTIFICATION DIVISION.
       PROGRAM-ID. T33-SCORE-ACE.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION.
       MAIN-1.
           DISPLAY "=== T33: ACE RECALCULATION FAILURE ==="
           MOVE ZEROS TO WS-HND
           MOVE ZEROS TO WS-GM
           MOVE 3     TO WS-PC
           MOVE 'H'   TO WS-PS1(1)
           MOVE 'A'   TO WS-PRK(1)
           MOVE 11    TO WS-PFV(1)
           MOVE 'H'   TO WS-PS1(2)
           MOVE 'A'   TO WS-PRK(2)
           MOVE 11    TO WS-PFV(2)
           MOVE 'S'   TO WS-PS1(3)
           MOVE 'K'   TO WS-PRK(3)
           MOVE 10    TO WS-PFV(3)
           MOVE 0     TO WS-DC
           DISPLAY "HAND: ACE(11) + ACE(11) + KING(10) = 32 RAW"
           CALL 'BJACK-SCORE' USING BY REFERENCE WS-HND WS-GM
           DISPLAY "  WS-PT (REPORTED) = " WS-PT
           DISPLAY "  CORRECT TOTAL    = 012 (BOTH ACES REDUCED)"
           DISPLAY "  BUG TOTAL        = 022 (ONE ACE REDUCED)"
           STOP RUN.
