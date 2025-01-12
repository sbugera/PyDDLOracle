PROMPT Table pyddl_test.t_range_part_interval_number
CREATE TABLE pyddl_test.t_range_part_interval_number
(
    sale_id  NUMBER NOT NULL,
    region   VARCHAR2(50 BYTE),
    amount   NUMBER
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY RANGE (sale_id)
INTERVAL (1000)
(
  PARTITION initial_partition VALUES LESS THAN (1000)
    NOCOMPRESS
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
  PARTITION VALUES LESS THAN (2000)
    NOCOMPRESS
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
                )
)
NOCACHE;


PROMPT Index pyddl_test.uk_t_range_part_interval_number
CREATE INDEX pyddl_test.uk_t_range_part_interval_number ON pyddl_test.t_range_part_interval_number
(region)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      default
            );

PROMPT Index pyddl_test.uq_t_range_part_interval_number
CREATE UNIQUE INDEX pyddl_test.uq_t_range_part_interval_number ON pyddl_test.t_range_part_interval_number
(sale_id)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      default
            );
