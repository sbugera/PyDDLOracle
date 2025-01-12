CREATE TABLE pyddl_test.databasechangeloglock
(
    id           INTEGER NOT NULL,
    locked       NUMBER(1) NOT NULL,
    lockgranted  TIMESTAMP(6),
    lockedby     VARCHAR2(255 BYTE)
)
TABLESPACE pyddl_test_data
LOGGING
NOCOMPRESS
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE UNIQUE INDEX pyddl_test.pk_databasechangeloglock ON pyddl_test.databasechangeloglock
(id)
LOGGING
TABLESPACE pyddl_test_data;


ALTER TABLE pyddl_test.databasechangeloglock ADD (
  CONSTRAINT pk_databasechangeloglock
  PRIMARY KEY (id)
  USING INDEX pyddl_test.pk_databasechangeloglock
  ENABLE VALIDATE);
