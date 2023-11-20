CREATE TABLE extora_app.t_range_part_interval_number
(
    sale_id  NUMBER,
    region   VARCHAR2(50 BYTE),
    amount   NUMBER
)
NOCOMPRESS
TABLESPACE extora_app_data
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
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
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
NOCACHE
RESULT_CACHE (MODE DEFAULT);
