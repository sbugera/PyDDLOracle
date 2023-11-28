PROMPT Table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
CREATE TABLE extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    sale_date        DATE,
    region           VARCHAR2(50 BYTE),
    amount           NUMBER,
    "Col_lowercase"  VARCHAR2(10 BYTE) DEFAULT 'test' NOT NULL
)
NOCOMPRESS
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY RANGE (sale_date)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION sales_data_initial VALUES LESS THAN (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


COMMENT ON TABLE extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" IS 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';

COMMENT ON COLUMN extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE".sale_date IS 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';

COMMENT ON COLUMN extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" IS 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';


CREATE INDEX extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
(sale_date, region)
LOGGING
TABLESPACE extora_app_index
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

CREATE INDEX extora_app."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
(amount)
LOGGING
TABLESPACE extora_app_index
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


ALTER TABLE extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" ADD (
  CONSTRAINT "ck_lowercase_T_RANGE_PART_INTERVAL_DATE"
  CHECK (amount BETWEEN 1 and 1000000 )
  DEFERRABLE INITIALLY DEFERRED
  ENABLE VALIDATE,
  CONSTRAINT "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  PRIMARY KEY (sale_date, region)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE,
  CONSTRAINT "uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  UNIQUE (amount)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX extora_app."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE);
