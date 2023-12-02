CREATE TABLE EXTORA_APP.T_LIST_PART__AUTOMATIC
(
    ID            NUMBER,
    COUNTRY_CODE  VARCHAR2(5 BYTE),
    CUSTOMER_ID   NUMBER,
    ORDER_DATE    DATE,
    ORDER_TOTAL   NUMBER(8,2)
)
NOCOMPRESS
PARTITION BY LIST (COUNTRY_CODE) AUTOMATIC
(
  PARTITION PART_USA VALUES ('USA')
    LOGGING
    NOCOMPRESS,
  PARTITION PART_UK_AND_IRELAND VALUES ('GBR', 'IRL')
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES ('BGR')
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES ('POL')
    LOGGING
    NOCOMPRESS
)
RESULT_CACHE (MODE DEFAULT);
