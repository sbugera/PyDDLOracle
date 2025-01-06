PROMPT Table PYDDL_TEST.T_LIST_PART__AUTOMATIC
CREATE TABLE PYDDL_TEST.T_LIST_PART__AUTOMATIC
(
    ID            NUMBER,
    COUNTRY_CODE  VARCHAR2(5 BYTE),
    CUSTOMER_ID   NUMBER,
    ORDER_DATE    DATE,
    ORDER_TOTAL   NUMBER(8,2)
)
NOCOMPRESS
TABLESPACE PYDDL_TEST_DATA
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      DEFAULT
            )
PARTITION BY LIST (COUNTRY_CODE) AUTOMATIC
(
  PARTITION PART_USA VALUES ('USA')
    LOGGING
    NOCOMPRESS
    TABLESPACE PYDDL_TEST_DATA
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
  PARTITION PART_UK_AND_IRELAND VALUES ('GBR', 'IRL')
    LOGGING
    NOCOMPRESS
    TABLESPACE PYDDL_TEST_DATA
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
  PARTITION VALUES ('BGR')
    LOGGING
    NOCOMPRESS
    TABLESPACE PYDDL_TEST_DATA
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
  PARTITION VALUES ('POL')
    LOGGING
    NOCOMPRESS
    TABLESPACE PYDDL_TEST_DATA
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      DEFAULT
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
