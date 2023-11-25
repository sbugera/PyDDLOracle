create table extora_app.t_range_part_interval_date
(
    sale_date  date,
    region     varchar2(50 byte),
    amount     number
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


create index extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" on extora_app.t_range_part_interval_date
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


alter table extora_app.t_range_part_interval_date add (
  constraint "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  primary key
  (sale_date, region)
  deferrable initially deferred
  using index extora_app."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  enable validate);
