       IDENTIFICATION DIVISION.
       PROGRAM-ID. GOTO-COMPLEX.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           77 WS-X PIC 9.
       PROCEDURE DIVISION.
       MAIN-PARA.
           GO TO STEP-1.
       STEP-1.
           GO TO STEP-2.
       STEP-2.
           GO TO STEP-3.
       STEP-3.
           GO TO STEP-4.
       STEP-4.
           GO TO STEP-5.
       STEP-5.
           STOP RUN.
