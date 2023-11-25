CREATE TABLE EXTORA_APP.SALES
(
    SALE_ID      NUMBER,
    SALE_DATE    DATE,
    SALE_AMOUNT  NUMBER
)
NOCOMPRESS
PARTITION BY RANGE (SALE_DATE)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION P1 VALUES LESS THAN (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION P2 VALUES LESS THAN (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION P3 VALUES LESS THAN (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION P4 VALUES LESS THAN (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
)
RESULT_CACHE (MODE DEFAULT);


COMMENT ON TABLE EXTORA_APP.SALES IS 'Sales';

COMMENT ON COLUMN EXTORA_APP.SALES.SALE_ID     IS 'Sale ID';

COMMENT ON COLUMN EXTORA_APP.SALES.SALE_DATE   IS 'Sale Date';

COMMENT ON COLUMN EXTORA_APP.SALES.SALE_AMOUNT IS 'Sale Ammount';


CREATE INDEX EXTORA_APP.PK_SALES ON EXTORA_APP.SALES
(SALE_ID)
LOGGING;

CREATE INDEX EXTORA_APP.UK_SALES ON EXTORA_APP.SALES
(SALE_AMOUNT)
LOGGING;


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
