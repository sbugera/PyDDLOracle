prompt Table PYDDL_TEST.SALES_SIMPLE_RANGE
create table PYDDL_TEST.SALES_SIMPLE_RANGE
(
    SALE_DATE  date not null,
    AMOUNT     number
)
nocompress
tablespace PYDDL_TEST_DATA
partition by range (SALE_DATE)
(
  partition SALES_Q1 values less than (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SALES_Q2 values less than (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SALES_Q3 values less than (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SALES_Q4 values less than (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SALES_DATA_FUTURE values less than (MAXVALUE)
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_01
create unique index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_01 on PYDDL_TEST.SALES_SIMPLE_RANGE
(SALE_DATE)
logging
tablespace PYDDL_TEST_DATA;

prompt Index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_LOCAL
create index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_LOCAL on PYDDL_TEST.SALES_SIMPLE_RANGE
(AMOUNT)
local;

prompt Index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED
create index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED on PYDDL_TEST.SALES_SIMPLE_RANGE
(SALE_DATE, AMOUNT)
logging
tablespace PYDDL_TEST_DATA;

alter index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED
  monitoring usage;
