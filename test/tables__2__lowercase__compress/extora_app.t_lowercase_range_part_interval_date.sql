prompt Table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
create table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    sale_date        date,
    region           varchar2(50 byte),
    amount           number,
    "Col_lowercase"  varchar2(10 byte) default 'test' not null
)
tablespace extora_app_data
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
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition values less than (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    tablespace extora_app_data
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
    tablespace extora_app_data
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


comment on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" is 'Comment for table t_lowercase_RANGE_PART_INTERVAL_DATE';

comment on column extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE".sale_date       is 'Column comment for SALES_DATE in t_lowercase_RANGE_PART_INTERVAL_DATE';

comment on column extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"."Col_lowercase" is 'Column comment for "Col_lowercase" in t_lowercase_RANGE_PART_INTERVAL_DATE';


prompt Index extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
(sale_date, region)
logging
tablespace extora_app_index
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

prompt Index extora_app."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
create index extora_app."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
(amount)
logging
tablespace extora_app_index
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


prompt Constraints for table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE"
alter table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "ck_lowercase_T_RANGE_PART_INTERVAL_DATE"
  check (amount BETWEEN 1 and 1000000 )
  deferrable initially deferred
  enable validate,
  constraint "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  primary key (sale_date, region)
  deferrable initially deferred
  using index extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate,
  constraint "uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  unique (amount)
  deferrable initially deferred
  using index extora_app."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate);


prompt Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to app_role
grant alter, debug, delete, flashback, insert, on commit refresh, query rewrite, read, select, update on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to app_role;

prompt Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to extora_usr
grant alter, debug, flashback, index, on commit refresh, query rewrite, read, references on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to extora_usr;
grant delete, insert, select, update on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to extora_usr with grant option;

prompt Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to read_role
grant read on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to read_role;

prompt Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to user_role
grant select on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to user_role;

prompt Grants on table extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to "lowercase_Role"
grant delete, insert, update on extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" to "lowercase_Role";
