CREATE TABLE EXTORA_APP.T_LIST_PART__MULTICOLUMN
(
    SALE_DATE         DATE,
    REGION            VARCHAR2(50 BYTE),
    PRODUCT_CATEGORY  VARCHAR2(50 BYTE),
    AMOUNT            NUMBER
)
NOCOMPRESS
PARTITION BY LIST (REGION, PRODUCT_CATEGORY)
(
  PARTITION NORTH_ELECTRONICS VALUES (( 'North', 'Electronics' ))
    LOGGING
    NOCOMPRESS,
  PARTITION NORTH_CLOTHING VALUES (( 'North', 'Clothing' ))
    LOGGING
    NOCOMPRESS,
  PARTITION SOUTH_ELECTRONICS VALUES (( 'South', 'Electronics' ))
    LOGGING
    NOCOMPRESS,
  PARTITION SOUTH_CLOTHING VALUES (( 'South', 'Clothing' ))
    LOGGING
    NOCOMPRESS,
  PARTITION OTHER_SALES VALUES (DEFAULT)
    LOGGING
    NOCOMPRESS
)
RESULT_CACHE (MODE DEFAULT);
