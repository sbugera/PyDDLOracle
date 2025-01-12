PROMPT Table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
CREATE TABLE pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    sale_date        DATE,
    region           VARCHAR2(50 BYTE),
    amount           NUMBER,
    "Col_lowercase"  VARCHAR2(10 BYTE) DEFAULT 'test' NOT NULL
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
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION sales_data_initial VALUES LESS THAN (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


PROMPT Index pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
CREATE INDEX pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(sale_date, region)
LOGGING
TABLESPACE pyddl_test_index
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      default
            );

PROMPT Index pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
CREATE INDEX pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(amount)
LOGGING
TABLESPACE pyddl_test_index
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      default
            );
