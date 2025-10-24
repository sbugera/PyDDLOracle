prompt Table PYDDL_TEST.T_LIST_PART__MULTICOLUMN
create table PYDDL_TEST.T_LIST_PART__MULTICOLUMN
(
    SALE_DATE         date,
    REGION            varchar2(50 byte),
    PRODUCT_CATEGORY  varchar2(50 byte),
    AMOUNT            number
)
nocompress
tablespace PYDDL_TEST_DATA
partition by list (REGION, PRODUCT_CATEGORY)
(
  partition NORTH_ELECTRONICS values (( 'North', 'Electronics' ))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition NORTH_CLOTHING values (( 'North', 'Clothing' ))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SOUTH_ELECTRONICS values (( 'South', 'Electronics' ))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition SOUTH_CLOTHING values (( 'South', 'Clothing' ))
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
