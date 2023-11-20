CREATE TABLE EXTORA_APP.T_LIST_PART__MULTICOLUMN
(
    SALE_DATE         DATE,
    REGION            VARCHAR2(50 BYTE),
    PRODUCT_CATEGORY  VARCHAR2(50 BYTE),
    AMOUNT            NUMBER
)
NOCOMPRESS
TABLESPACE EXTORA_APP_DATA
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      DEFAULT
            )
PARTITION BY LIST (REGION, PRODUCT_CATEGORY)
(
  PARTITION NORTH_ELECTRONICS VALUES (( 'North', 'Electronics' ))
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      DEFAULT
                ),
  PARTITION NORTH_CLOTHING VALUES (( 'North', 'Clothing' ))
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                ),
  PARTITION SOUTH_ELECTRONICS VALUES (( 'South', 'Electronics' ))
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                ),
  PARTITION SOUTH_CLOTHING VALUES (( 'South', 'Clothing' ))
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      DEFAULT
                ),
  PARTITION OTHER_SALES VALUES (DEFAULT)
    NOCOMPRESS
    TABLESPACE EXTORA_APP_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      DEFAULT
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);