CREATE TABLE EXTORA_APP.SALES_SIMPLE_RANGE
(
    SALE_DATE  DATE NOT NULL,
    AMOUNT     NUMBER
)
NOCOMPRESS
TABLESPACE EXTORA_APP_DATA
PARTITION BY RANGE (SALE_DATE)
(
  PARTITION SALES_Q1 VALUES LESS THAN (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA,
  PARTITION SALES_Q2 VALUES LESS THAN (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA,
  PARTITION SALES_Q3 VALUES LESS THAN (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA,
  PARTITION SALES_Q4 VALUES LESS THAN (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA,
  PARTITION SALES_DATA_FUTURE VALUES LESS THAN (MAXVALUE)
    LOGGING
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
)
NOCACHE;


CREATE UNIQUE INDEX EXTORA_APP.IDX_SALES_SIMPLE_RANGE_01 ON EXTORA_APP.SALES_SIMPLE_RANGE
(SALE_DATE)
LOGGING
TABLESPACE EXTORA_APP_DATA;

CREATE INDEX EXTORA_APP.IDX_SALES_SIMPLE_RANGE_LOCAL ON EXTORA_APP.SALES_SIMPLE_RANGE
(AMOUNT)
LOCAL;

CREATE INDEX EXTORA_APP.IDX_SALES_SIMPLE_RANGE_MONITORED ON EXTORA_APP.SALES_SIMPLE_RANGE
(SALE_DATE, AMOUNT)
LOGGING
TABLESPACE EXTORA_APP_DATA;

ALTER INDEX EXTORA_APP.IDX_SALES_SIMPLE_RANGE_MONITORED
  MONITORING USAGE;


ALTER TABLE EXTORA_APP.SALES_SIMPLE_RANGE ADD (
  CONSTRAINT CK_SALES_SIMPLE_RANGE
  CHECK (SALE_DATE = trunc(SALE_DATE))
  ENABLE VALIDATE,
  CONSTRAINT PK_SALES_SIMPLE_RANGE
  PRIMARY KEY (SALE_DATE)
  USING INDEX EXTORA_APP.IDX_SALES_SIMPLE_RANGE_01
  ENABLE VALIDATE,
  CONSTRAINT UK_SALES_SIMPLE_RANGE
  UNIQUE (SALE_DATE, AMOUNT)
  USING INDEX EXTORA_APP.IDX_SALES_SIMPLE_RANGE_MONITORED
  ENABLE VALIDATE);
