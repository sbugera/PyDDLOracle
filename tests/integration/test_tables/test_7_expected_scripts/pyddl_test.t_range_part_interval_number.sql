prompt Table PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
create table PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
(
    SALE_ID  number not null,
    REGION   varchar2(50 byte),
    AMOUNT   number
)
nocompress
tablespace PYDDL_TEST_DATA
partition by range (SALE_ID)
interval (1000)
(
  partition INITIAL_PARTITION values less than (1000)
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values less than (2000)
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.UK_T_RANGE_PART_INTERVAL_NUMBER
create index PYDDL_TEST.UK_T_RANGE_PART_INTERVAL_NUMBER on PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
(REGION)
logging
tablespace PYDDL_TEST_DATA;

prompt Index PYDDL_TEST.UQ_T_RANGE_PART_INTERVAL_NUMBER
create unique index PYDDL_TEST.UQ_T_RANGE_PART_INTERVAL_NUMBER on PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
(SALE_ID)
logging
tablespace PYDDL_TEST_DATA;
