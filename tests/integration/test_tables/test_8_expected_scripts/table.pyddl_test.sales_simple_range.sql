PROMPT Table pyddl_test.sales_simple_range
CREATE TABLE pyddl_test.sales_simple_range
(
    sale_date  DATE NOT NULL,
    amount     NUMBER
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY RANGE (sale_date)
(
  PARTITION sales_q1 VALUES LESS THAN (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_q2 VALUES LESS THAN (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_q3 VALUES LESS THAN (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_q4 VALUES LESS THAN (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_data_future VALUES LESS THAN (MAXVALUE)
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE;


PROMPT Index pyddl_test.idx_sales_simple_range_01
CREATE UNIQUE INDEX pyddl_test.idx_sales_simple_range_01 ON pyddl_test.sales_simple_range
(sale_date)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

PROMPT Index pyddl_test.idx_sales_simple_range_local
CREATE INDEX pyddl_test.idx_sales_simple_range_local ON pyddl_test.sales_simple_range
(amount)
STORAGE    (
            BUFFER_POOL      default
            )
LOCAL;

PROMPT Index pyddl_test.idx_sales_simple_range_monitored
CREATE INDEX pyddl_test.idx_sales_simple_range_monitored ON pyddl_test.sales_simple_range
(sale_date, amount)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

ALTER INDEX pyddl_test.idx_sales_simple_range_monitored
  MONITORING USAGE;
