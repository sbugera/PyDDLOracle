prompt Table EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
create table EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(
    SALE_ID  number not null,
    REGION   varchar2(50 byte),
    AMOUNT   number
)
nocompress
tablespace EXTORA_APP_DATA
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
    tablespace EXTORA_APP_DATA
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
    tablespace EXTORA_APP_DATA
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
