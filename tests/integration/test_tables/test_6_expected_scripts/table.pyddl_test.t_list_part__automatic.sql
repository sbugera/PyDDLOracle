CREATE TABLE pyddl_test.t_list_part__automatic
(
    id            NUMBER,
    country_code  VARCHAR2(5 BYTE),
    customer_id   NUMBER,
    order_date    DATE,
    order_total   NUMBER(8,2)
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PARTITION BY LIST (country_code) AUTOMATIC
(
  PARTITION part_usa VALUES ('USA')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION part_uk_and_ireland VALUES ('GBR', 'IRL')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION VALUES ('BGR')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION VALUES ('POL')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
