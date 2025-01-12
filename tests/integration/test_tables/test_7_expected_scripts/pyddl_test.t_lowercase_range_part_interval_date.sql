prompt Table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
create table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    SALE_DATE        date,
    REGION           varchar2(50 byte),
    AMOUNT           number,
    "Col_lowercase"  varchar2(10 byte) default 'test' not null
)
nocompress
tablespace PYDDL_TEST_DATA
partition by range (SALE_DATE)
interval (NUMTOYMINTERVAL(1, 'MONTH'))
(
  partition SALES_DATA_INITIAL values less than (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values less than (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values less than (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index PYDDL_TEST."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
(SALE_DATE, REGION)
logging
tablespace PYDDL_TEST_INDEX;

prompt Index PYDDL_TEST."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index PYDDL_TEST."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
(AMOUNT)
logging
tablespace PYDDL_TEST_INDEX;
