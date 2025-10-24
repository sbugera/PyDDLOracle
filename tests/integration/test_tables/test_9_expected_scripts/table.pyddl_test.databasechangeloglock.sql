PROMPT Table pyddl_test.databasechangeloglock
CREATE TABLE pyddl_test.databasechangeloglock
(
    id           INTEGER NOT NULL,
    locked       NUMBER(1) NOT NULL,
    lockgranted  TIMESTAMP(6),
    lockedby     VARCHAR2(255 BYTE)
)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      default
            )
LOGGING
RESULT_CACHE (MODE DEFAULT);


PROMPT Index pyddl_test.pk_databasechangeloglock
CREATE UNIQUE INDEX pyddl_test.pk_databasechangeloglock ON pyddl_test.databasechangeloglock
(id)
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
