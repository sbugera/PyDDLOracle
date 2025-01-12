CREATE TABLE pyddl_test.databasechangeloglock
(
    id           INTEGER NOT NULL,
    locked       NUMBER(1) NOT NULL,
    lockgranted  TIMESTAMP(6),
    lockedby     VARCHAR2(255 BYTE)
);
