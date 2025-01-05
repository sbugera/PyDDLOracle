prompt Table extora_app.sales
create table extora_app.sales
(
    sale_id      number,
    sale_date    date,
    sale_amount  number
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
  partition p1 values less than (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition p2 values less than (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  partition p3 values less than (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  partition p4 values less than (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  partition values less than (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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
  partition values less than (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
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


comment on table extora_app.sales is 'Sales';

comment on column extora_app.sales.sale_id     is 'Sale ID';

comment on column extora_app.sales.sale_date   is 'Sale Date';

comment on column extora_app.sales.sale_amount is 'Sale Ammount';


prompt Index extora_app.pk_sales
create index extora_app.pk_sales on extora_app.sales
(sale_id)
logging
tablespace extora_app_data
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

prompt Index extora_app.uk_sales
create index extora_app.uk_sales on extora_app.sales
(sale_amount)
logging
tablespace extora_app_data
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

prompt Index extora_app.uk_sales_02
create index extora_app.uk_sales_02 on extora_app.sales
(sale_date, sale_amount)
logging
tablespace extora_app_data
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


prompt Constraints for table extora_app.sales
alter table extora_app.sales add (
  constraint ck_sales
  check (sale_amount > 0)
  deferrable initially immediate
  enable validate,
  constraint pk_sales
  primary key (sale_id)
  deferrable initially immediate
  using index extora_app.pk_sales
  enable validate,
  constraint uk_sales
  unique (sale_amount)
  deferrable initially immediate
  using index extora_app.uk_sales
  enable validate,
  constraint uk_sales_02
  unique (sale_date, sale_amount)
  deferrable initially immediate
  using index extora_app.uk_sales_02
  enable validate);


prompt Grants on table extora_app.sales to app_role
grant alter, debug, delete, flashback, insert, on commit refresh, query rewrite, read, select, update on extora_app.sales to app_role;

prompt Grants on table extora_app.sales to extora_usr
grant alter, debug, flashback, index, on commit refresh, query rewrite, read, references on extora_app.sales to extora_usr;
grant delete, insert, select, update on extora_app.sales to extora_usr with grant option;

prompt Grants on table extora_app.sales to read_role
grant read on extora_app.sales to read_role;

prompt Grants on table extora_app.sales to user_role
grant select on extora_app.sales to user_role;

prompt Grants on table extora_app.sales to "lowercase_Role"
grant delete, insert, update on extora_app.sales to "lowercase_Role";
