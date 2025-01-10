prompt Table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
create table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    SALE_DATE        date,
    REGION           varchar2(50 byte),
    AMOUNT           number,
    "Col_lowercase"  varchar2(10 byte) default 'test' not null
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
  partition SALES_DATA_INITIAL values less than (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace PYDDL_TEST_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition values less than (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  partition values less than (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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


comment on table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" is 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';

comment on column PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE".SALE_DATE       is 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';

comment on column PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" is 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';


prompt Index PYDDL_TEST."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index PYDDL_TEST."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
(SALE_DATE, REGION)
logging
tablespace PYDDL_TEST_INDEX
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

prompt Index PYDDL_TEST."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index PYDDL_TEST."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
(AMOUNT)
logging
tablespace PYDDL_TEST_INDEX
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


prompt Constraints for table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE"
alter table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "ck_lowercase_T_RANGE_PART_INTERVAL_DATE"
  check (amount BETWEEN 1 and 1000000 )
  deferrable initially deferred
  enable validate,
  constraint "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  primary key (SALE_DATE, REGION)
  deferrable initially deferred
  using index PYDDL_TEST."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate,
  constraint "uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  unique (AMOUNT)
  deferrable initially deferred
  using index PYDDL_TEST."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate);


prompt Grants on table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_APP_ROLE
grant alter, debug, delete, flashback, insert, on commit refresh, query rewrite, read, select, update on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_APP_ROLE;

prompt Grants on table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_READ_ROLE
grant read on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_READ_ROLE;

prompt Grants on table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_USER
grant alter, debug, flashback, index, on commit refresh, query rewrite, read, references on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_USER;
grant delete, insert, select, update on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_USER with grant option;

prompt Grants on table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_USER_ROLE
grant select on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to PYDDL_TEST_USER_ROLE;

prompt Grants on table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to "PYDDL_TEST_lowercase_Role"
grant delete, insert, update on PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" to "PYDDL_TEST_lowercase_Role";
