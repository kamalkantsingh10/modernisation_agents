      * T31-DECK-BIAS -- VERIFY BIASED SHUFFLE OUTPUT
      * STORY 3.1: DECK ORDER IS IDENTICAL ACROSS ALL RUNS
       IDENTIFICATION DIVISION.
       PROGRAM-ID. T31-DECK-BIAS.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY WS-DECK.
           77 WS-I           PIC 99.
       PROCEDURE DIVISION.
       MAIN-1.
           DISPLAY "=== T31: BIASED SHUFFLE VERIFICATION ==="
           MOVE ZEROS TO WS-DK
           CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
           DISPLAY "RUN 1 -- FIRST 7 CARDS:"
           MOVE 1 TO WS-I
           GO TO SHOW-1.
       SHOW-1.
           IF WS-I > 7
               GO TO RUN-2
           END-IF
           DISPLAY "  CARD " WS-I ": " WS-S1(WS-I)
               WS-RK(WS-I) " FV=" WS-FV(WS-I)
           ADD 1 TO WS-I
           GO TO SHOW-1.
       RUN-2.
           DISPLAY " "
           MOVE ZEROS TO WS-DK
           CALL 'BJACK-DECK' USING BY REFERENCE WS-DK
           DISPLAY "RUN 2 -- FIRST 7 CARDS:"
           MOVE 1 TO WS-I
           GO TO SHOW-2.
       SHOW-2.
           IF WS-I > 7
               GO TO DONE-1
           END-IF
           DISPLAY "  CARD " WS-I ": " WS-S1(WS-I)
               WS-RK(WS-I) " FV=" WS-FV(WS-I)
           ADD 1 TO WS-I
           GO TO SHOW-2.
       DONE-1.
           DISPLAY " "
           DISPLAY "EXPECTED: BOTH RUNS IDENTICAL (BIASED SHUFFLE)"
           STOP RUN.
