CREATE TABLE pyddl_test.t_list_part__automatic
(
    id            NUMBER,
    country_code  VARCHAR2(5 BYTE),
    customer_id   NUMBER,
    order_date    DATE,
    order_total   NUMBER(8,2)
)
NOCOMPRESS
PARTITION BY LIST (country_code) AUTOMATIC
(
  PARTITION part_usa VALUES ('USA')
    LOGGING
    NOCOMPRESS,
  PARTITION part_uk_and_ireland VALUES ('GBR', 'IRL')
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES ('BGR')
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES ('POL')
    LOGGING
    NOCOMPRESS
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
