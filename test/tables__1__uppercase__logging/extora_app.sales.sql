CREATE TABLE EXTORA_APP.SALES
(
    SALE_ID      NUMBER,
    SALE_DATE    DATE,
    SALE_AMOUNT  NUMBER
)
NOCOMPRESS
TABLESPACE EXTORA_APP_DATA
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      DEFAULT
            )
PARTITION BY RANGE (SALE_DATE)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION P1 VALUES LESS THAN (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                ),
  PARTITION P2 VALUES LESS THAN (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION P3 VALUES LESS THAN (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION P4 VALUES LESS THAN (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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


COMMENT ON TABLE EXTORA_APP.SALES IS 'Sales';

COMMENT ON COLUMN EXTORA_APP.SALES.SALE_ID     IS 'Sale ID';

COMMENT ON COLUMN EXTORA_APP.SALES.SALE_DATE   IS 'Sale Date';

COMMENT ON COLUMN EXTORA_APP.SALES.SALE_AMOUNT IS 'Sale Ammount';


CREATE INDEX EXTORA_APP.PK_SALES ON EXTORA_APP.SALES
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

CREATE INDEX EXTORA_APP.UK_SALES ON EXTORA_APP.SALES
(SALE_AMOUNT)
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


ALTER TABLE EXTORA_APP.SALES ADD (
  CONSTRAINT PK_SALES
  PRIMARY KEY
  (SALE_ID)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX EXTORA_APP.PK_SALES
  ENABLE VALIDATE,
  CONSTRAINT UK_SALES
  UNIQUE
  (SALE_AMOUNT)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX EXTORA_APP.UK_SALES
  ENABLE VALIDATE);
