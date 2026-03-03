       IDENTIFICATION DIVISION.
       PROGRAM-ID. NESTED-TEST.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X PIC 9.
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM OUTER-A THRU OUTER-B.
           STOP RUN.
       OUTER-A.
           PERFORM INNER-A THRU INNER-B.
       OUTER-B.
           MOVE 1 TO WS-X.
       INNER-A.
           MOVE 2 TO WS-X.
       INNER-B.
           MOVE 3 TO WS-X.
