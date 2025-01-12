PROMPT Table pyddl_test.t_range_part__range_subpart
CREATE TABLE pyddl_test.t_range_part__range_subpart
(
    id      NUMBER,
    sub_id  NUMBER
)
NOCOMPRESS
TABLESPACE users
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY RANGE (id)
INTERVAL (10)
(
  PARTITION p_0 VALUES LESS THAN (0)
    COMPRESS BASIC
    TABLESPACE pyddl_test_data
    PCTFREE    0
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE;
