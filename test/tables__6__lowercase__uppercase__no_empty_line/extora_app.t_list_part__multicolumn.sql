prompt Table EXTORA_APP.T_LIST_PART__MULTICOLUMN
create table EXTORA_APP.T_LIST_PART__MULTICOLUMN
(
    SALE_DATE         date,
    REGION            varchar2(50 byte),
    PRODUCT_CATEGORY  varchar2(50 byte),
    AMOUNT            number
)
nocompress
tablespace EXTORA_APP_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by list (REGION, PRODUCT_CATEGORY)
(
  partition NORTH_ELECTRONICS values (( 'North', 'Electronics' ))
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
  partition NORTH_CLOTHING values (( 'North', 'Clothing' ))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition SOUTH_ELECTRONICS values (( 'South', 'Electronics' ))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition SOUTH_CLOTHING values (( 'South', 'Clothing' ))
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
nocache;
