prompt Table EXTORA_APP.T_LIST_PART__AUTOMATIC
create table EXTORA_APP.T_LIST_PART__AUTOMATIC
(
    ID            number,
    COUNTRY_CODE  varchar2(5 byte),
    CUSTOMER_ID   number,
    ORDER_DATE    date,
    ORDER_TOTAL   number(8,2)
)
nocompress
tablespace EXTORA_APP_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by list (COUNTRY_CODE)
(
  partition PART_USA values ('USA') automatic
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
  partition PART_UK_AND_IRELAND values ('GBR', 'IRL') automatic
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
  partition values ('BGR') automatic
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
  partition values ('POL') automatic
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
