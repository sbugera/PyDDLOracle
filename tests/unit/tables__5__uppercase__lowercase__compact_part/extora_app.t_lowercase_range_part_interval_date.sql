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
RESULT_CACHE (MODE DEFAULT);


COMMENT ON TABLE extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" IS 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';

COMMENT ON COLUMN extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE".sale_date IS 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';

COMMENT ON COLUMN extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" IS 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';


PROMPT Index extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
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

PROMPT Index extora_app."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
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


PROMPT Constraints for table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
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


PROMPT Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to app_role
GRANT ALTER, DEBUG, DELETE, FLASHBACK, INSERT, ON COMMIT REFRESH, QUERY REWRITE, READ, SELECT, UPDATE ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" TO app_role;

PROMPT Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to extora_usr
GRANT ALTER, DEBUG, FLASHBACK, INDEX, ON COMMIT REFRESH, QUERY REWRITE, READ, REFERENCES ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" TO extora_usr;
GRANT DELETE, INSERT, SELECT, UPDATE ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" TO extora_usr WITH GRANT OPTION;

PROMPT Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to read_role
GRANT READ ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" TO read_role;

PROMPT Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to user_role
GRANT SELECT ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" TO user_role;

PROMPT Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to "lowercase_Role"
GRANT DELETE, INSERT, UPDATE ON extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" TO "lowercase_Role";
