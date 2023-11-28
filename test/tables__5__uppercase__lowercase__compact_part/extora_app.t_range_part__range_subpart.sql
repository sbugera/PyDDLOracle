PROMPT Table extora_app.t_range_part__range_subpart
CREATE TABLE extora_app.t_range_part__range_subpart
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
    NOLOGGING
    COMPRESS BASIC
    TABLESPACE extora_app_data
    PCTFREE    0
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
