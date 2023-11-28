PROMPT Table extora_app.t_range_part_interval_number
CREATE TABLE extora_app.t_range_part_interval_number
(
    sale_id  NUMBER NOT NULL,
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


CREATE INDEX extora_app.uk_t_range_part_interval_number ON extora_app.t_range_part_interval_number
(region)
LOGGING
TABLESPACE extora_app_data
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

CREATE UNIQUE INDEX extora_app.uq_t_range_part_interval_number ON extora_app.t_range_part_interval_number
(sale_id)
LOGGING
TABLESPACE extora_app_data
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


ALTER TABLE extora_app.t_range_part_interval_number ADD (
  CONSTRAINT pk_t_range_part_interval_number
  PRIMARY KEY (sale_id)
  USING INDEX extora_app.uq_t_range_part_interval_number
  ENABLE VALIDATE,
  CONSTRAINT uk_t_range_part_interval_number
  UNIQUE (region)
  USING INDEX extora_app.uk_t_range_part_interval_number
  ENABLE VALIDATE);
