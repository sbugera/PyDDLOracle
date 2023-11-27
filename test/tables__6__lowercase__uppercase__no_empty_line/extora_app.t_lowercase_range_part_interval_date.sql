create table EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    SALE_DATE        date,
    REGION           varchar2(50 byte),
    AMOUNT           number,
    "Col_lowercase"  varchar2(10 byte) default 'test' not null
)
nocompress
tablespace EXTORA_APP_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by range (SALE_DATE)
interval (NUMTOYMINTERVAL(1, 'MONTH'))
(
  partition SALES_DATA_INITIAL values less than (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition values less than (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  partition values less than (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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


comment on table EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" is 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';
comment on column EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE".SALE_DATE       is 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';
comment on column EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" is 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';
