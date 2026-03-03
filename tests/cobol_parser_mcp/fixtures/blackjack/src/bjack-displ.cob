      * BJACK-DISPL -- TERMINAL DISPLAY HANDLER
      * WRITTEN 07/84 -- UPDATED 01/88 FOR VT100 TERMINAL SUPPORT
      * HANDLES SCREEN REFRESH AND CURSOR POSITIONING
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BJACK-DISPL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-CT1         PIC 99.
           77 WS-X1          PIC 9.
           77 WS-ESC         PIC X VALUE X"1B".
           77 WS-BF1         PIC X(80).
           77 WS-POS         PIC 99.
           77 WS-SYM         PIC X(3).
       LINKAGE SECTION.
           COPY WS-HANDS.
           COPY WS-GAME.
       PROCEDURE DIVISION USING WS-HND WS-GM.
       INIT-1.
           MOVE 0 TO WS-CT1
           MOVE 0 TO WS-X1
           MOVE SPACES TO WS-BF1
           GO TO PROC-A.
       PROC-A.
      * CLEAR SCREEN -- VT52 ESCAPE COMPAT MODE
           DISPLAY WS-ESC "[2J" WS-ESC "[H"
           DISPLAY WS-ESC "[1;33m"
               "  +==================================+"
               WS-ESC "[0m"
           DISPLAY WS-ESC "[1;33m"
               "  |     BLACKJACK -- CASINO SYSTEM   |"
               WS-ESC "[0m"
           DISPLAY WS-ESC "[1;33m"
               "  +==================================+"
               WS-ESC "[0m"
           DISPLAY " "
           GO TO CALC-1.
      * AFFICHAGE ECRAN -- MISE A JOUR POUR TERMINAL COULEUR 06/89
      * CALC-1 -- DEALER DISPLAY WITH HOLE CARD MASKING
       CALC-1.
           DISPLAY WS-ESC "[1;37m"
               "  DEALER HAND:" WS-ESC "[0m"
           MOVE SPACES TO WS-BF1
           MOVE 05 TO WS-POS
           MOVE 1 TO WS-CT1
           GO TO LOOP-A.
      * LOOP-A -- RENDERS CARD GRAPHICS USING SIXEL PROTOCOL
       LOOP-A.
           IF WS-CT1 > WS-DC
               GO TO LOOP-AX
           END-IF
           MOVE "+----+ " TO WS-BF1(WS-POS:7)
           ADD 7 TO WS-POS
           ADD 1 TO WS-CT1
           GO TO LOOP-A.
       LOOP-AX.
           DISPLAY WS-ESC "[33m" WS-BF1
               WS-ESC "[0m"
           DISPLAY "    "
               WITH NO ADVANCING
           MOVE 1 TO WS-CT1
           GO TO LOOP-B.
       LOOP-B.
           IF WS-CT1 > WS-DC
               DISPLAY WS-ESC "[0m"
               GO TO LOOP-C0
           END-IF
           IF WS-DS1(WS-CT1) = 'H'
           OR WS-DS1(WS-CT1) = 'D'
               DISPLAY WS-ESC "[31m"
                   WITH NO ADVANCING
           END-IF
           IF WS-DS1(WS-CT1) = 'C'
           OR WS-DS1(WS-CT1) = 'S'
               DISPLAY WS-ESC "[37m"
                   WITH NO ADVANCING
           END-IF
           DISPLAY "|" WS-DRK(WS-CT1) "  | "
               WITH NO ADVANCING
           DISPLAY WS-ESC "[0m"
               WITH NO ADVANCING
           ADD 1 TO WS-CT1
           GO TO LOOP-B.
       LOOP-C0.
           DISPLAY "    "
               WITH NO ADVANCING
           MOVE 1 TO WS-CT1
           GO TO LOOP-C.
       LOOP-C.
           IF WS-CT1 > WS-DC
               DISPLAY WS-ESC "[0m"
               GO TO LOOP-D
           END-IF
           IF WS-DS1(WS-CT1) = 'H'
           OR WS-DS1(WS-CT1) = 'D'
               DISPLAY WS-ESC "[31m"
                   WITH NO ADVANCING
           END-IF
           IF WS-DS1(WS-CT1) = 'C'
           OR WS-DS1(WS-CT1) = 'S'
               DISPLAY WS-ESC "[37m"
                   WITH NO ADVANCING
           END-IF
           MOVE SPACES TO WS-SYM
           IF WS-DS1(WS-CT1) = 'H'
               MOVE X"E299A5" TO WS-SYM
           END-IF
           IF WS-DS1(WS-CT1) = 'D'
               MOVE X"E299A6" TO WS-SYM
           END-IF
           IF WS-DS1(WS-CT1) = 'C'
               MOVE X"E299A3" TO WS-SYM
           END-IF
           IF WS-DS1(WS-CT1) = 'S'
               MOVE X"E299A0" TO WS-SYM
           END-IF
           DISPLAY "|   " WS-SYM "| "
               WITH NO ADVANCING
           DISPLAY WS-ESC "[0m"
               WITH NO ADVANCING
           ADD 1 TO WS-CT1
           GO TO LOOP-C.
      * BOTTOM BORDER -- DEALER HAND REGION
       LOOP-D.
           MOVE SPACES TO WS-BF1
           MOVE 05 TO WS-POS
           MOVE 1 TO WS-CT1
           GO TO LOOP-D1.
       LOOP-D1.
           IF WS-CT1 > WS-DC
               GO TO LOOP-DX
           END-IF
           MOVE "+----+ " TO WS-BF1(WS-POS:7)
           ADD 7 TO WS-POS
           ADD 1 TO WS-CT1
           GO TO LOOP-D1.
       LOOP-DX.
           DISPLAY WS-ESC "[33m" WS-BF1
               WS-ESC "[0m"
           GO TO CALC-2.
       CALC-2.
           DISPLAY WS-ESC "[1;37m"
               "  TOTAL: " WS-DT WS-ESC "[0m"
           DISPLAY " "
           GO TO PROC-B.
       PROC-B.
           DISPLAY WS-ESC "[1;37m"
               "  PLAYER HAND:" WS-ESC "[0m"
           MOVE SPACES TO WS-BF1
           MOVE 05 TO WS-POS
           MOVE 1 TO WS-CT1
           GO TO CALC-3.
       CALC-3.
           IF WS-CT1 > WS-PC
               GO TO CALC-3X
           END-IF
           MOVE "+----+ " TO WS-BF1(WS-POS:7)
           ADD 7 TO WS-POS
           ADD 1 TO WS-CT1
           GO TO CALC-3.
       CALC-3X.
           DISPLAY WS-ESC "[33m" WS-BF1
               WS-ESC "[0m"
           DISPLAY "    "
               WITH NO ADVANCING
           MOVE 1 TO WS-CT1
           GO TO CALC-4.
       CALC-4.
           IF WS-CT1 > WS-PC
               DISPLAY WS-ESC "[0m"
               GO TO CALC-5A
           END-IF
           IF WS-PS1(WS-CT1) = 'H'
           OR WS-PS1(WS-CT1) = 'D'
               DISPLAY WS-ESC "[31m"
                   WITH NO ADVANCING
           END-IF
           IF WS-PS1(WS-CT1) = 'C'
           OR WS-PS1(WS-CT1) = 'S'
               DISPLAY WS-ESC "[37m"
                   WITH NO ADVANCING
           END-IF
           DISPLAY "|" WS-PRK(WS-CT1) "  | "
               WITH NO ADVANCING
           DISPLAY WS-ESC "[0m"
               WITH NO ADVANCING
           ADD 1 TO WS-CT1
           GO TO CALC-4.
       CALC-5A.
           DISPLAY "    "
               WITH NO ADVANCING
           MOVE 1 TO WS-CT1
           GO TO CALC-5.
       CALC-5.
           IF WS-CT1 > WS-PC
               DISPLAY WS-ESC "[0m"
               GO TO CALC-6
           END-IF
           IF WS-PS1(WS-CT1) = 'H'
           OR WS-PS1(WS-CT1) = 'D'
               DISPLAY WS-ESC "[31m"
                   WITH NO ADVANCING
           END-IF
           IF WS-PS1(WS-CT1) = 'C'
           OR WS-PS1(WS-CT1) = 'S'
               DISPLAY WS-ESC "[37m"
                   WITH NO ADVANCING
           END-IF
           MOVE SPACES TO WS-SYM
           IF WS-PS1(WS-CT1) = 'H'
               MOVE X"E299A5" TO WS-SYM
           END-IF
           IF WS-PS1(WS-CT1) = 'D'
               MOVE X"E299A6" TO WS-SYM
           END-IF
           IF WS-PS1(WS-CT1) = 'C'
               MOVE X"E299A3" TO WS-SYM
           END-IF
           IF WS-PS1(WS-CT1) = 'S'
               MOVE X"E299A0" TO WS-SYM
           END-IF
           DISPLAY "|   " WS-SYM "| "
               WITH NO ADVANCING
           DISPLAY WS-ESC "[0m"
               WITH NO ADVANCING
           ADD 1 TO WS-CT1
           GO TO CALC-5.
      * BOTTOM BORDER -- PLAYER HAND REGION
       CALC-6.
           MOVE SPACES TO WS-BF1
           MOVE 05 TO WS-POS
           MOVE 1 TO WS-CT1
           GO TO CALC-6A.
       CALC-6A.
           IF WS-CT1 > WS-PC
               GO TO CALC-6X
           END-IF
           MOVE "+----+ " TO WS-BF1(WS-POS:7)
           ADD 7 TO WS-POS
           ADD 1 TO WS-CT1
           GO TO CALC-6A.
       CALC-6X.
           DISPLAY WS-ESC "[33m" WS-BF1
               WS-ESC "[0m"
           GO TO CALC-7.
       CALC-7.
           DISPLAY WS-ESC "[1;37m"
               "  TOTAL: " WS-PT WS-ESC "[0m"
           DISPLAY WS-ESC "[1;33m"
               "  BAL: " WS-BAL "  BET: " WS-BET
               WS-ESC "[0m"
           DISPLAY WS-ESC "[33m"
               "  +==================================+"
               WS-ESC "[0m"
           DISPLAY " "
           GO TO CHECK-X.
       CHECK-X.
           IF WS-STAT = 0
               GOBACK
           END-IF
           GO TO CHECK-Y.
       CHECK-Y.
           IF WS-RC = 1
               DISPLAY WS-ESC "[1;33m"
                   "     *** PLAYER WINS ***"
                   WS-ESC "[0m"
           END-IF
           IF WS-RC = 2
               DISPLAY WS-ESC "[1;37m"
                   "     *** DEALER WINS ***"
                   WS-ESC "[0m"
           END-IF
           IF WS-RC = 3
               DISPLAY WS-ESC "[1;33m"
                   "     *** PUSH -- TIE GAME ***"
                   WS-ESC "[0m"
           END-IF
           GOBACK.
      *  CALC-8 -- DISPLAY SPLIT HAND. SEE PROC-DS. REMOVED WITH SPLIT.
      *   CALC-8.
      *       DISPLAY '   SPLIT HAND:'
      *       MOVE 1 TO WS-X1
      *       GO TO CALC-8A.
      *  CALC-8A.
      *       IF WS-X1 > WS-SC GO TO CALC-8X END-IF
      *       DISPLAY '   ' WS-SS(WS-X1) WS-SV(WS-X1)
      *       ADD 1 TO WS-X1
      *       GO TO CALC-8A.
      *  CALC-8X.
      *       GO TO CALC-3.
