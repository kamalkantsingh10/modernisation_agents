       IDENTIFICATION DIVISION.
       PROGRAM-ID. DB-ACCESS.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           01 WS-VAR PIC X(50).
           01 WS-MSG PIC X(80).
       PROCEDURE DIVISION.
       FETCH-DATA.
           EXEC SQL
               SELECT COL INTO :WS-VAR
               FROM SOME-TABLE
           END-EXEC.
       SEND-CICS.
           EXEC CICS
               SEND TEXT FROM(WS-MSG)
           END-EXEC.
       MAIN-PARA.
           PERFORM FETCH-DATA.
           STOP RUN.
