prompt Table PYDDL_TEST.DATABASECHANGELOGLOCK
create table PYDDL_TEST.DATABASECHANGELOGLOCK
(
    ID           integer not null,
    LOCKED       number(1) not null,
    LOCKGRANTED  timestamp(6),
    LOCKEDBY     varchar2(255 byte)
)
tablespace PYDDL_TEST_DATA
logging
nocompress
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.PK_DATABASECHANGELOGLOCK
create unique index PYDDL_TEST.PK_DATABASECHANGELOGLOCK on PYDDL_TEST.DATABASECHANGELOGLOCK
(ID)
logging
tablespace PYDDL_TEST_DATA;
