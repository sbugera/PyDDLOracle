PROMPT Table EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
CREATE TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(
    SALE_ID  NUMBER NOT NULL,
    REGION   VARCHAR2(50 BYTE),
    AMOUNT   NUMBER
)
NOCOMPRESS
TABLESPACE EXTORA_APP_DATA
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      DEFAULT
            )
PARTITION BY RANGE (SALE_ID)
INTERVAL (1000)
(
  PARTITION INITIAL_PARTITION VALUES LESS THAN (1000)
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
  PARTITION VALUES LESS THAN (2000)
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
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX EXTORA_APP.UK_T_RANGE_PART_INTERVAL_NUMBER ON EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(REGION)
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

CREATE UNIQUE INDEX EXTORA_APP.UQ_T_RANGE_PART_INTERVAL_NUMBER ON EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(SALE_ID)
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


ALTER TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER ADD (
  CONSTRAINT PK_T_RANGE_PART_INTERVAL_NUMBER
  PRIMARY KEY (SALE_ID)
  USING INDEX EXTORA_APP.UQ_T_RANGE_PART_INTERVAL_NUMBER
  ENABLE VALIDATE,
  CONSTRAINT UK_T_RANGE_PART_INTERVAL_NUMBER
  UNIQUE (REGION)
  USING INDEX EXTORA_APP.UK_T_RANGE_PART_INTERVAL_NUMBER
  ENABLE VALIDATE);
