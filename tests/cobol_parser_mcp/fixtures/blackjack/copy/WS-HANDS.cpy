      * PLAYER/DEALER HAND ARRAYS -- MAX 7 CARDS PER HAND PER RULES 1980
      * UPDATED 09/85 TO SUPPORT SPLIT HANDS -- NOT YET IMPLEMENTED
       01 WS-HND.
          05 WS-PC           PIC 99.
          05 WS-PHD OCCURS 11 TIMES.
             10 WS-PS1       PIC X.
             10 WS-PRK       PIC XX.
             10 WS-PFV       PIC 99.
          05 WS-DC           PIC 99.
          05 WS-DHD OCCURS 11 TIMES.
             10 WS-DS1       PIC X.
             10 WS-DRK       PIC XX.
             10 WS-DFV       PIC 99.
      * WS-SC -- SPLIT CARD COUNT RESERVED 1987
          05 WS-SC           PIC 99.
          05 WS-SPLT OCCURS 11 TIMES.
             10 WS-SV        PIC 99.
             10 WS-SS        PIC X.
