prompt Table PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
create table PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
(
    SALE_ID  number not null,
    REGION   varchar2(50 byte),
    AMOUNT   number
)
nocompress
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by range (SALE_ID)
interval (1000)
(
  partition INITIAL_PARTITION values less than (1000)
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
  partition values less than (2000)
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
                )
)
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.UK_T_RANGE_PART_INTERVAL_NUMBER
create index PYDDL_TEST.UK_T_RANGE_PART_INTERVAL_NUMBER on PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
(REGION)
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

prompt Index PYDDL_TEST.UQ_T_RANGE_PART_INTERVAL_NUMBER
create unique index PYDDL_TEST.UQ_T_RANGE_PART_INTERVAL_NUMBER on PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
(SALE_ID)
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


prompt Constraints for table PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER
alter table PYDDL_TEST.T_RANGE_PART_INTERVAL_NUMBER add (
  constraint PK_T_RANGE_PART_INTERVAL_NUMBER
  primary key (SALE_ID)
  using index PYDDL_TEST.UQ_T_RANGE_PART_INTERVAL_NUMBER
  enable validate,
  constraint UK_T_RANGE_PART_INTERVAL_NUMBER
  unique (REGION)
  using index PYDDL_TEST.UK_T_RANGE_PART_INTERVAL_NUMBER
  enable validate);
