PROMPT Table EXTORA_APP.T_RANGE_PART__RANGE_SUBPART
CREATE TABLE EXTORA_APP.T_RANGE_PART__RANGE_SUBPART
(
    ID      NUMBER,
    SUB_ID  NUMBER
)
NOCOMPRESS
TABLESPACE USERS
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      DEFAULT
            )
PARTITION BY RANGE (ID)
INTERVAL (10)
(
  PARTITION P_0 VALUES LESS THAN (0)
    COMPRESS BASIC
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    0
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
