prompt Table PYDDL_TEST.T_LIST_PART
create table PYDDL_TEST.T_LIST_PART
(
    SALE_DATE  date not null,
    REGION     varchar2(50 byte),
    AMOUNT     number
)
nocompress
tablespace PYDDL_TEST_DATA
partition by list (REGION)
(
  partition NORTH_SALES values ('North')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SOUTH_SALES values ('South')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition WEST_SALES values ('West')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition EAST_SALES values ('East')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition OTHER_SALES values (DEFAULT)
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.PK_T_LIST_PART
create unique index PYDDL_TEST.PK_T_LIST_PART on PYDDL_TEST.T_LIST_PART
(SALE_DATE)
logging
tablespace PYDDL_TEST_DATA;
