       IDENTIFICATION DIVISION.
       PROGRAM-ID. THRU-TEST.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X PIC 9.
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM STEP-A THRU STEP-C.
           STOP RUN.
       STEP-A.
           MOVE 1 TO WS-X.
       STEP-B.
           MOVE 2 TO WS-X.
       STEP-C.
           MOVE 3 TO WS-X.
