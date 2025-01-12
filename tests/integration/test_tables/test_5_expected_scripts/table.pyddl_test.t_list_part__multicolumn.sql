CREATE TABLE pyddl_test.t_list_part__multicolumn
(
    sale_date         DATE,
    region            VARCHAR2(50 BYTE),
    product_category  VARCHAR2(50 BYTE),
    amount            NUMBER
)
NOCOMPRESS
PARTITION BY LIST (region, product_category)
(
  PARTITION north_electronics VALUES (( 'North', 'Electronics' ))
    LOGGING
    NOCOMPRESS,
  PARTITION north_clothing VALUES (( 'North', 'Clothing' ))
    LOGGING
    NOCOMPRESS,
  PARTITION south_electronics VALUES (( 'South', 'Electronics' ))
    LOGGING
    NOCOMPRESS,
  PARTITION south_clothing VALUES (( 'South', 'Clothing' ))
    LOGGING
    NOCOMPRESS,
  PARTITION other_sales VALUES (DEFAULT)
    LOGGING
    NOCOMPRESS
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
