      * GAME STATE FLAGS AND TOTALS -- SINGLE PLAYER MODE ONLY 1981
      * UPDATED 02/86 FOR MULTI-PLAYER SUPPORT -- ABANDONED
       01 WS-GM.
          05 WS-FLG-A        PIC X.
          05 WS-FLG-B        PIC X.
          05 WS-RC           PIC 9.
          05 WS-PT           PIC 999.
          05 WS-DT           PIC 999.
          05 WS-STAT         PIC 9.
      * CHIP COUNTERS -- ADDED FOR TOURNAMENT MODE 1988
          05 WS-BAL          PIC 9(4).
          05 WS-BET          PIC 9(4).
      * WS-SP -- SPLIT ACTIVE FLAG. WS-INS -- INSURANCE TAKEN FLAG
          05 WS-SP           PIC X.
          05 WS-INS          PIC X.
