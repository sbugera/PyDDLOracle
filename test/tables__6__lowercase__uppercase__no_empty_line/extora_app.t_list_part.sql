create table EXTORA_APP.T_LIST_PART
(
    SALE_DATE  date not null,
    REGION     varchar2(50 byte),
    AMOUNT     number
)
nocompress
tablespace EXTORA_APP_DATA
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
  partition SOUTH_SALES values ('South')
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
  partition WEST_SALES values ('West')
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition EAST_SALES values ('East')
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition OTHER_SALES values (DEFAULT)
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                )
)
nocache
result_cache (mode default);
