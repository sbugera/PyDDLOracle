CREATE TABLE pyddl_test.t_list_part
(
    sale_date  DATE NOT NULL,
    region     VARCHAR2(50 BYTE),
    amount     NUMBER
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PARTITION BY LIST (region)
(
  PARTITION north_sales VALUES ('North')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION south_sales VALUES ('South')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION west_sales VALUES ('West')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION east_sales VALUES ('East')
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


CREATE UNIQUE INDEX pyddl_test.pk_t_list_part ON pyddl_test.t_list_part
(sale_date)
LOGGING
TABLESPACE pyddl_test_data;


ALTER TABLE pyddl_test.t_list_part ADD (
  CONSTRAINT pk_t_list_part
  PRIMARY KEY (sale_date)
  USING INDEX pyddl_test.pk_t_list_part
  ENABLE VALIDATE);
