CREATE TABLE pyddl_test.t_range_part_interval_number
(
    sale_id  NUMBER NOT NULL,
    region   VARCHAR2(50 BYTE),
    amount   NUMBER
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PARTITION BY RANGE (sale_id)
INTERVAL (1000)
(
  PARTITION initial_partition VALUES LESS THAN (1000)
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data,
  PARTITION VALUES LESS THAN (2000)
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX pyddl_test.uk_t_range_part_interval_number ON pyddl_test.t_range_part_interval_number
(region)
LOGGING
TABLESPACE pyddl_test_data;

CREATE UNIQUE INDEX pyddl_test.uq_t_range_part_interval_number ON pyddl_test.t_range_part_interval_number
(sale_id)
LOGGING
TABLESPACE pyddl_test_data;


ALTER TABLE pyddl_test.t_range_part_interval_number ADD (
  CONSTRAINT pk_t_range_part_interval_number
  PRIMARY KEY (sale_id)
  USING INDEX pyddl_test.uq_t_range_part_interval_number
  ENABLE VALIDATE,
  CONSTRAINT uk_t_range_part_interval_number
  UNIQUE (region)
  USING INDEX pyddl_test.uk_t_range_part_interval_number
  ENABLE VALIDATE);
