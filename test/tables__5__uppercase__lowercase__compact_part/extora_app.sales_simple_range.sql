PROMPT Table extora_app.sales_simple_range
CREATE TABLE extora_app.sales_simple_range
(
    sale_date  DATE NOT NULL,
    amount     NUMBER
)
NOCOMPRESS
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY RANGE (sale_date)
(
  PARTITION sales_q1 VALUES LESS THAN (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_q2 VALUES LESS THAN (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_q3 VALUES LESS THAN (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_q4 VALUES LESS THAN (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION sales_data_future VALUES LESS THAN (MAXVALUE)
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
RESULT_CACHE (MODE DEFAULT);


PROMPT Index extora_app.idx_sales_simple_range_01
CREATE UNIQUE INDEX extora_app.idx_sales_simple_range_01 ON extora_app.sales_simple_range
(sale_date)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

PROMPT Index extora_app.idx_sales_simple_range_local
CREATE INDEX extora_app.idx_sales_simple_range_local ON extora_app.sales_simple_range
(amount)
STORAGE    (
            BUFFER_POOL      default
            )
LOCAL;

PROMPT Index extora_app.idx_sales_simple_range_monitored
CREATE INDEX extora_app.idx_sales_simple_range_monitored ON extora_app.sales_simple_range
(sale_date, amount)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

ALTER INDEX extora_app.idx_sales_simple_range_monitored
  MONITORING USAGE;


ALTER TABLE extora_app.sales_simple_range ADD (
  CONSTRAINT ck_sales_simple_range
  CHECK (SALE_DATE = trunc(SALE_DATE))
  ENABLE VALIDATE,
  CONSTRAINT pk_sales_simple_range
  PRIMARY KEY (sale_date)
  USING INDEX extora_app.idx_sales_simple_range_01
  ENABLE VALIDATE,
  CONSTRAINT uk_sales_simple_range
  UNIQUE (sale_date, amount)
  USING INDEX extora_app.idx_sales_simple_range_monitored
  ENABLE VALIDATE);
