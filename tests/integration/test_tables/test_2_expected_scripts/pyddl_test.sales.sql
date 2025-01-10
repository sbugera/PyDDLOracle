prompt Table PYDDL_TEST.SALES
create table PYDDL_TEST.SALES
(
    SALE_ID      number,
    SALE_DATE    date,
    SALE_AMOUNT  number
)
nocompress
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by range (SALE_DATE)
interval (NUMTOYMINTERVAL(1, 'MONTH'))
(
  partition P1 values less than (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition P2 values less than (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition P3 values less than (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition P4 values less than (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition values less than (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition values less than (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                )
)
nocache
result_cache (mode default);


comment on table PYDDL_TEST.SALES is 'Sales';

comment on column PYDDL_TEST.SALES.SALE_ID     is 'Sale ID';

comment on column PYDDL_TEST.SALES.SALE_DATE   is 'Sale Date';

comment on column PYDDL_TEST.SALES.SALE_AMOUNT is 'Sale Ammount';


prompt Index PYDDL_TEST.PK_SALES
create index PYDDL_TEST.PK_SALES on PYDDL_TEST.SALES
(SALE_ID)
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

prompt Index PYDDL_TEST.UK_SALES
create index PYDDL_TEST.UK_SALES on PYDDL_TEST.SALES
(SALE_AMOUNT)
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

prompt Index PYDDL_TEST.UK_SALES_02
create index PYDDL_TEST.UK_SALES_02 on PYDDL_TEST.SALES
(SALE_DATE, SALE_AMOUNT)
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


prompt Constraints for table PYDDL_TEST.SALES
alter table PYDDL_TEST.SALES add (
  constraint CK_SALES
  check (sale_amount > 0)
  deferrable initially immediate
  enable validate,
  constraint PK_SALES
  primary key (SALE_ID)
  deferrable initially immediate
  using index PYDDL_TEST.PK_SALES
  enable validate,
  constraint UK_SALES
  unique (SALE_AMOUNT)
  deferrable initially immediate
  using index PYDDL_TEST.UK_SALES
  enable validate,
  constraint UK_SALES_02
  unique (SALE_DATE, SALE_AMOUNT)
  deferrable initially immediate
  using index PYDDL_TEST.UK_SALES_02
  enable validate);


prompt Grants on table PYDDL_TEST.SALES to PYDDL_TEST_APP_ROLE
grant alter, debug, delete, flashback, insert, on commit refresh, query rewrite, read, select, update on PYDDL_TEST.SALES to PYDDL_TEST_APP_ROLE;

prompt Grants on table PYDDL_TEST.SALES to PYDDL_TEST_READ_ROLE
grant read on PYDDL_TEST.SALES to PYDDL_TEST_READ_ROLE;

prompt Grants on table PYDDL_TEST.SALES to PYDDL_TEST_USER
grant alter, debug, flashback, on commit refresh, query rewrite, read on PYDDL_TEST.SALES to PYDDL_TEST_USER;
grant delete, insert, select, update on PYDDL_TEST.SALES to PYDDL_TEST_USER with grant option;

prompt Grants on table PYDDL_TEST.SALES to PYDDL_TEST_USER_ROLE
grant select on PYDDL_TEST.SALES to PYDDL_TEST_USER_ROLE;

prompt Grants on table PYDDL_TEST.SALES to "PYDDL_TEST_lowercase_Role"
grant delete, insert, update on PYDDL_TEST.SALES to "PYDDL_TEST_lowercase_Role";
