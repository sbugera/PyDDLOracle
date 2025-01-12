prompt Table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
create table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    sale_date        date,
    region           varchar2(50 byte),
    amount           number,
    "Col_lowercase"  varchar2(10 byte) default 'test' not null
)
nocompress
tablespace pyddl_test_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by range (sale_date)
interval (NUMTOYMINTERVAL(1, 'MONTH'))
(
  partition sales_data_initial values less than (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace pyddl_test_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition values less than (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace pyddl_test_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      default
                ),
  partition values less than (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace pyddl_test_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      default
                )
)
nocache
result_cache (mode default);


comment on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" is 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';

comment on column pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE".sale_date       is 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';

comment on column pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" is 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';


prompt Index pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(sale_date, region)
logging
tablespace pyddl_test_index
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

prompt Index pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
(amount)
logging
tablespace pyddl_test_index
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


prompt Constraints for table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE"
alter table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "ck_lowercase_T_RANGE_PART_INTERVAL_DATE"
  check (amount BETWEEN 1 and 1000000 )
  deferrable initially deferred
  enable validate,
  constraint "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  primary key (sale_date, region)
  deferrable initially deferred
  using index pyddl_test."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate,
  constraint "uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  unique (amount)
  deferrable initially deferred
  using index pyddl_test."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate);


prompt Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_app_role
grant alter, debug, delete, flashback, insert, on commit refresh, query rewrite, read, select, update on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_app_role;

prompt Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_read_role
grant read on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_read_role;

prompt Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user
grant alter, debug, flashback, index, on commit refresh, query rewrite, read, references on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user;
grant delete, insert, select, update on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user with grant option;

prompt Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user_role
grant select on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to pyddl_test_user_role;

prompt Grants on table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to "PYDDL_TEST_lowercase_Role"
grant delete, insert, update on pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" to "PYDDL_TEST_lowercase_Role";
