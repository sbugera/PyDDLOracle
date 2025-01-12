CREATE TABLE pyddl_test.t_list_part__multicolumn
(
    sale_date         DATE,
    region            VARCHAR2(50 BYTE),
    product_category  VARCHAR2(50 BYTE),
    amount            NUMBER
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PARTITION BY LIST (region, product_category)
(
  PARTITION north_electronics VALUES (( 'North', 'Electronics' ))
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION north_clothing VALUES (( 'North', 'Clothing' ))
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION south_electronics VALUES (( 'South', 'Electronics' ))
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION south_clothing VALUES (( 'South', 'Clothing' ))
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION other_sales VALUES (DEFAULT)
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
