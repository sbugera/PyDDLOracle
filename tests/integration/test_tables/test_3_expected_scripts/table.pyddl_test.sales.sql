PROMPT Table pyddl_test.sales
CREATE TABLE pyddl_test.sales
(
    sale_id      NUMBER,
    sale_date    DATE,
    sale_amount  NUMBER
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
  PARTITION p1 VALUES LESS THAN (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION p2 VALUES LESS THAN (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION p3 VALUES LESS THAN (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION p4 VALUES LESS THAN (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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


COMMENT ON TABLE pyddl_test.sales IS 'Sales';

COMMENT ON COLUMN pyddl_test.sales.sale_id     IS 'Sale ID';

COMMENT ON COLUMN pyddl_test.sales.sale_date   IS 'Sale Date';

COMMENT ON COLUMN pyddl_test.sales.sale_amount IS 'Sale Ammount';


PROMPT Index pyddl_test.pk_sales
CREATE INDEX pyddl_test.pk_sales ON pyddl_test.sales
(sale_id)
LOGGING
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

PROMPT Index pyddl_test.uk_sales
CREATE INDEX pyddl_test.uk_sales ON pyddl_test.sales
(sale_amount)
LOGGING
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

PROMPT Index pyddl_test.uk_sales_02
CREATE INDEX pyddl_test.uk_sales_02 ON pyddl_test.sales
(sale_date, sale_amount)
LOGGING
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


PROMPT Constraints for table pyddl_test.sales
ALTER TABLE pyddl_test.sales ADD (
  CONSTRAINT ck_sales
  CHECK (sale_amount > 0)
  DEFERRABLE INITIALLY IMMEDIATE
  ENABLE VALIDATE,
  CONSTRAINT pk_sales
  PRIMARY KEY (sale_id)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX pyddl_test.pk_sales
  ENABLE VALIDATE,
  CONSTRAINT uk_sales
  UNIQUE (sale_amount)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX pyddl_test.uk_sales
  ENABLE VALIDATE,
  CONSTRAINT uk_sales_02
  UNIQUE (sale_date, sale_amount)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX pyddl_test.uk_sales_02
  ENABLE VALIDATE);


PROMPT Grants on table pyddl_test.sales to pyddl_test_app_role
GRANT ALTER, DEBUG, DELETE, FLASHBACK, INSERT, ON COMMIT REFRESH, QUERY REWRITE, READ, SELECT, UPDATE ON pyddl_test.sales TO pyddl_test_app_role;

PROMPT Grants on table pyddl_test.sales to pyddl_test_read_role
GRANT READ ON pyddl_test.sales TO pyddl_test_read_role;

PROMPT Grants on table pyddl_test.sales to pyddl_test_user
GRANT ALTER, DEBUG, FLASHBACK, ON COMMIT REFRESH, QUERY REWRITE, READ ON pyddl_test.sales TO pyddl_test_user;
GRANT DELETE, INSERT, SELECT, UPDATE ON pyddl_test.sales TO pyddl_test_user WITH GRANT OPTION;

PROMPT Grants on table pyddl_test.sales to pyddl_test_user_role
GRANT SELECT ON pyddl_test.sales TO pyddl_test_user_role;

PROMPT Grants on table pyddl_test.sales to "PYDDL_TEST_lowercase_Role"
GRANT DELETE, INSERT, UPDATE ON pyddl_test.sales TO "PYDDL_TEST_lowercase_Role";
