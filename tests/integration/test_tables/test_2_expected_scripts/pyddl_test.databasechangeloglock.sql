prompt Table PYDDL_TEST.DATABASECHANGELOGLOCK
create table PYDDL_TEST.DATABASECHANGELOGLOCK
(
    ID           integer not null,
    LOCKED       number(1) not null,
    LOCKGRANTED  timestamp(6),
    LOCKEDBY     varchar2(255 byte)
)
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      DEFAULT
            )
logging
nocompress
nocache
result_cache (mode default);


prompt Index PYDDL_TEST.PK_DATABASECHANGELOGLOCK
create unique index PYDDL_TEST.PK_DATABASECHANGELOGLOCK on PYDDL_TEST.DATABASECHANGELOGLOCK
(ID)
logging
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   2
maxtrans   255
storage    (
            initial          64K
            next             1M
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      DEFAULT
            );


prompt Constraints for table PYDDL_TEST.DATABASECHANGELOGLOCK
alter table PYDDL_TEST.DATABASECHANGELOGLOCK add (
  constraint PK_DATABASECHANGELOGLOCK
  primary key (ID)
  using index PYDDL_TEST.PK_DATABASECHANGELOGLOCK
  enable validate);
