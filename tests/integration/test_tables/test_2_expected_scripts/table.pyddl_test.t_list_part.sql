prompt Table PYDDL_TEST.T_LIST_PART
create table PYDDL_TEST.T_LIST_PART
(
    SALE_DATE  date not null,
    REGION     varchar2(50 byte),
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
partition by list (REGION)
(
  partition NORTH_SALES values ('North')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition SOUTH_SALES values ('South')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition WEST_SALES values ('West')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition EAST_SALES values ('East')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition OTHER_SALES values (DEFAULT)
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


prompt Index PYDDL_TEST.PK_T_LIST_PART
create unique index PYDDL_TEST.PK_T_LIST_PART on PYDDL_TEST.T_LIST_PART
(SALE_DATE)
logging
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   2
maxtrans   255
storage    (
            initial          64K
            next             1M
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      DEFAULT
            );


prompt Constraints for table PYDDL_TEST.T_LIST_PART
alter table PYDDL_TEST.T_LIST_PART add (
  constraint PK_T_LIST_PART
  primary key (SALE_DATE)
  using index PYDDL_TEST.PK_T_LIST_PART
  enable validate);
