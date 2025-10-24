PROMPT Table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
CREATE TABLE pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    sale_date        DATE,
    region           VARCHAR2(50 BYTE),
    amount           NUMBER,
    "Col_lowercase"  VARCHAR2(10 BYTE) DEFAULT 'test' NOT NULL
)
NOCOMPRESS
TABLESPACE pyddl_test_data
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
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION VALUES LESS THAN (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
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
  PARTITION VALUES LESS THAN (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
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
NOCACHE
RESULT_CACHE (MODE DEFAULT);


COMMENT ON TABLE pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" IS 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';

COMMENT ON COLUMN pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE".sale_date       IS 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';

COMMENT ON COLUMN pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" IS 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';


PROMPT Index pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
CREATE INDEX pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(sale_date, region)
LOGGING
TABLESPACE pyddl_test_index
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

PROMPT Index pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
CREATE INDEX pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(amount)
LOGGING
TABLESPACE pyddl_test_index
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


PROMPT Constraints for table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
ALTER TABLE pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" ADD (
  CONSTRAINT "ck_lowercase_T_RANGE_PART_INTERVAL_DATE"
  CHECK (amount BETWEEN 1 and 1000000 )
  DEFERRABLE INITIALLY DEFERRED
  ENABLE VALIDATE,
  CONSTRAINT "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  PRIMARY KEY (sale_date, region)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE,
  CONSTRAINT "uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  UNIQUE (amount)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE);


PROMPT Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_app_role
GRANT ALTER, DEBUG, DELETE, FLASHBACK, INSERT, ON COMMIT REFRESH, QUERY REWRITE, READ, SELECT, UPDATE ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" TO pyddl_test_app_role;

PROMPT Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_read_role
GRANT READ ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" TO pyddl_test_read_role;

PROMPT Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user
GRANT ALTER, DEBUG, FLASHBACK, INDEX, ON COMMIT REFRESH, QUERY REWRITE, READ, REFERENCES ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" TO pyddl_test_user;
GRANT DELETE, INSERT, SELECT, UPDATE ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" TO pyddl_test_user WITH GRANT OPTION;

PROMPT Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user_role
GRANT SELECT ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" TO pyddl_test_user_role;

PROMPT Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to "PYDDL_TEST_lowercase_Role"
GRANT DELETE, INSERT, UPDATE ON pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" TO "PYDDL_TEST_lowercase_Role";
