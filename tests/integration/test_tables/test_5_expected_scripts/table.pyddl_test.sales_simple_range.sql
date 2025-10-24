CREATE TABLE pyddl_test.sales_simple_range
(
    sale_date  DATE NOT NULL,
    amount     NUMBER
)
NOCOMPRESS
PARTITION BY RANGE (sale_date)
(
  PARTITION sales_q1 VALUES LESS THAN (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION sales_q2 VALUES LESS THAN (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION sales_q3 VALUES LESS THAN (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION sales_q4 VALUES LESS THAN (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION sales_data_future VALUES LESS THAN (MAXVALUE)
    LOGGING
    NOCOMPRESS
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE UNIQUE INDEX pyddl_test.idx_sales_simple_range_01 ON pyddl_test.sales_simple_range
(sale_date)
LOGGING;

CREATE INDEX pyddl_test.idx_sales_simple_range_local ON pyddl_test.sales_simple_range
(amount)
LOCAL;

CREATE INDEX pyddl_test.idx_sales_simple_range_monitored ON pyddl_test.sales_simple_range
(sale_date, amount)
LOGGING;

ALTER INDEX pyddl_test.idx_sales_simple_range_monitored
  MONITORING USAGE;


ALTER TABLE pyddl_test.sales_simple_range ADD (
  CONSTRAINT ck_sales_simple_range
  CHECK (SALE_DATE = trunc(SALE_DATE))
  ENABLE VALIDATE,
  CONSTRAINT pk_sales_simple_range
  PRIMARY KEY (sale_date)
  USING INDEX pyddl_test.idx_sales_simple_range_01
  ENABLE VALIDATE,
  CONSTRAINT uk_sales_simple_range
  UNIQUE (sale_date, amount)
  USING INDEX pyddl_test.idx_sales_simple_range_monitored
  ENABLE VALIDATE);
