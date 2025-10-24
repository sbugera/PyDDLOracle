PROMPT Table pyddl_test.t_list_part__multicolumn
CREATE TABLE pyddl_test.t_list_part__multicolumn
(
    sale_date         DATE,
    region            VARCHAR2(50 BYTE),
    product_category  VARCHAR2(50 BYTE),
    amount            NUMBER
)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY LIST (region, product_category)
(
  PARTITION north_electronics VALUES (( 'North', 'Electronics' ))
    LOGGING
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      default
                ),
  PARTITION north_clothing VALUES (( 'North', 'Clothing' ))
    LOGGING
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION south_electronics VALUES (( 'South', 'Electronics' ))
    LOGGING
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION south_clothing VALUES (( 'South', 'Clothing' ))
    LOGGING
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      default
                ),
  PARTITION other_sales VALUES (DEFAULT)
    LOGGING
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
RESULT_CACHE (MODE DEFAULT);
