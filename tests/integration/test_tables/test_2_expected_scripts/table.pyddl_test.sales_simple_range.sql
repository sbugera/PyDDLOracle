prompt Table PYDDL_TEST.SALES_SIMPLE_RANGE
create table PYDDL_TEST.SALES_SIMPLE_RANGE
(
    SALE_DATE  date not null,
    AMOUNT     number
)
nocompress
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by range (SALE_DATE)
(
  partition SALES_Q1 values less than (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition SALES_Q2 values less than (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition SALES_Q3 values less than (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition SALES_Q4 values less than (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition SALES_DATA_FUTURE values less than (MAXVALUE)
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                )
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_01
create unique index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_01 on PYDDL_TEST.SALES_SIMPLE_RANGE
(SALE_DATE)
logging
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      DEFAULT
            );

prompt Index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_LOCAL
create index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_LOCAL on PYDDL_TEST.SALES_SIMPLE_RANGE
(AMOUNT)
storage    (
            buffer_pool      DEFAULT
            )
local;

prompt Index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED
create index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED on PYDDL_TEST.SALES_SIMPLE_RANGE
(SALE_DATE, AMOUNT)
logging
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      DEFAULT
            );

alter index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED
  monitoring usage;


prompt Constraints for table PYDDL_TEST.SALES_SIMPLE_RANGE
alter table PYDDL_TEST.SALES_SIMPLE_RANGE add (
  constraint CK_SALES_SIMPLE_RANGE
  check (SALE_DATE = trunc(SALE_DATE))
  enable validate,
  constraint PK_SALES_SIMPLE_RANGE
  primary key (SALE_DATE)
  using index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_01
  enable validate,
  constraint UK_SALES_SIMPLE_RANGE
  unique (SALE_DATE, AMOUNT)
  using index PYDDL_TEST.IDX_SALES_SIMPLE_RANGE_MONITORED
  enable validate);
