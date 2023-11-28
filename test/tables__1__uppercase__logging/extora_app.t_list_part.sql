PROMPT Table EXTORA_APP.T_LIST_PART
CREATE TABLE EXTORA_APP.T_LIST_PART
(
    SALE_DATE  DATE NOT NULL,
    REGION     VARCHAR2(50 BYTE),
    AMOUNT     NUMBER
)
NOCOMPRESS
TABLESPACE EXTORA_APP_DATA
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      DEFAULT
            )
PARTITION BY LIST (REGION)
(
  PARTITION NORTH_SALES VALUES ('North')
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      DEFAULT
                ),
  PARTITION SOUTH_SALES VALUES ('South')
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      DEFAULT
                ),
  PARTITION WEST_SALES VALUES ('West')
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                ),
  PARTITION EAST_SALES VALUES ('East')
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                ),
  PARTITION OTHER_SALES VALUES (DEFAULT)
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE UNIQUE INDEX EXTORA_APP.PK_T_LIST_PART ON EXTORA_APP.T_LIST_PART
(SALE_DATE)
TABLESPACE EXTORA_APP_DATA
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            );


ALTER TABLE EXTORA_APP.T_LIST_PART ADD (
  CONSTRAINT PK_T_LIST_PART
  PRIMARY KEY (SALE_DATE)
  USING INDEX EXTORA_APP.PK_T_LIST_PART
  ENABLE VALIDATE);
