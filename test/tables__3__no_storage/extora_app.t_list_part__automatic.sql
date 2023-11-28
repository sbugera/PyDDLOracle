PROMPT Table EXTORA_APP.T_LIST_PART__AUTOMATIC
CREATE TABLE EXTORA_APP.T_LIST_PART__AUTOMATIC
(
    ID            NUMBER,
    COUNTRY_CODE  VARCHAR2(5 BYTE),
    CUSTOMER_ID   NUMBER,
    ORDER_DATE    DATE,
    ORDER_TOTAL   NUMBER(8,2)
)
NOCOMPRESS
PARTITION BY LIST (COUNTRY_CODE)
(
  PARTITION PART_USA VALUES ('USA') AUTOMATIC
    LOGGING
    NOCOMPRESS,
  PARTITION PART_UK_AND_IRELAND VALUES ('GBR', 'IRL') AUTOMATIC
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES ('BGR') AUTOMATIC
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES ('POL') AUTOMATIC
    LOGGING
    NOCOMPRESS
)
RESULT_CACHE (MODE DEFAULT);
