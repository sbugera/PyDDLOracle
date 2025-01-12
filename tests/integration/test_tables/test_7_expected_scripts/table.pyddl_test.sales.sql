prompt Table PYDDL_TEST.SALES
create table PYDDL_TEST.SALES
(
    SALE_ID      number,
    SALE_DATE    date,
    SALE_AMOUNT  number
)
nocompress
tablespace PYDDL_TEST_DATA
partition by range (SALE_DATE)
interval (NUMTOYMINTERVAL(1, 'MONTH'))
(
  partition P1 values less than (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition P2 values less than (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition P3 values less than (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition P4 values less than (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values less than (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values less than (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.PK_SALES
create index PYDDL_TEST.PK_SALES on PYDDL_TEST.SALES
(SALE_ID)
logging
tablespace PYDDL_TEST_DATA;

prompt Index PYDDL_TEST.UK_SALES
create index PYDDL_TEST.UK_SALES on PYDDL_TEST.SALES
(SALE_AMOUNT)
logging
tablespace PYDDL_TEST_DATA;

prompt Index PYDDL_TEST.UK_SALES_02
create index PYDDL_TEST.UK_SALES_02 on PYDDL_TEST.SALES
(SALE_DATE, SALE_AMOUNT)
logging
tablespace PYDDL_TEST_DATA;
