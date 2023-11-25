CREATE TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_DATE
(
    SALE_DATE  DATE,
    REGION     VARCHAR2(50 BYTE),
    AMOUNT     NUMBER
)
NOCOMPRESS
TABLESPACE EXTORA_APP_DATA
PARTITION BY RANGE (SALE_DATE)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION SALES_DATA_INITIAL VALUES LESS THAN (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA,
  PARTITION VALUES LESS THAN (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA,
  PARTITION VALUES LESS THAN (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
)
NOCACHE;


CREATE INDEX EXTORA_APP."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON EXTORA_APP.T_RANGE_PART_INTERVAL_DATE
(SALE_DATE, REGION)
LOGGING
TABLESPACE EXTORA_APP_INDEX;


ALTER TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_DATE ADD (
  CONSTRAINT "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  PRIMARY KEY
  (SALE_DATE, REGION)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX EXTORA_APP."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE);
