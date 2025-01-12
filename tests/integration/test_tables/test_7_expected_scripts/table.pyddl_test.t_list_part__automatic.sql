prompt Table PYDDL_TEST.T_LIST_PART__AUTOMATIC
create table PYDDL_TEST.T_LIST_PART__AUTOMATIC
(
    ID            number,
    COUNTRY_CODE  varchar2(5 byte),
    CUSTOMER_ID   number,
    ORDER_DATE    date,
    ORDER_TOTAL   number(8,2)
)
nocompress
tablespace PYDDL_TEST_DATA
partition by list (COUNTRY_CODE) automatic
(
  partition PART_USA values ('USA')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition PART_UK_AND_IRELAND values ('GBR', 'IRL')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values ('BGR')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA,
  partition values ('POL')
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
)
nocache
result_cache (mode default);
