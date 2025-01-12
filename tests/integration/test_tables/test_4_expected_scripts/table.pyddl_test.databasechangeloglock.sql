prompt Table pyddl_test.databasechangeloglock
create table pyddl_test.databasechangeloglock
(
    id           integer not null,
    locked       number(1) not null,
    lockgranted  timestamp(6),
    lockedby     varchar2(255 byte)
)
tablespace pyddl_test_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      default
            )
logging
nocompress
nocache
result_cache (mode default);


prompt Index pyddl_test.pk_databasechangeloglock
create unique index pyddl_test.pk_databasechangeloglock on pyddl_test.databasechangeloglock
(id)
logging
tablespace pyddl_test_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            initial          64K
            next             1M
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      default
            );


prompt Constraints for table pyddl_test.databasechangeloglock
alter table pyddl_test.databasechangeloglock add (
  constraint pk_databasechangeloglock
  primary key (id)
  using index pyddl_test.pk_databasechangeloglock
  enable validate);
