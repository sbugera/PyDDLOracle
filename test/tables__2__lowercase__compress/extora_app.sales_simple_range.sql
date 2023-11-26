create table extora_app.sales_simple_range
(
    sale_date  date not null,
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
(
  partition sales_q1 values less than (TO_DATE(' 2022-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition sales_q2 values less than (TO_DATE(' 2022-07-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition sales_q3 values less than (TO_DATE(' 2022-10-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition sales_q4 values less than (TO_DATE(' 2023-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition sales_data_future values less than (MAXVALUE)
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                )
)
nocache
result_cache (mode default);


create unique index extora_app.idx_sales_simple_range_01 on extora_app.sales_simple_range
(sale_date)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

create index extora_app.idx_sales_simple_range_local on extora_app.sales_simple_range
(amount)
storage    (
            buffer_pool      default
            )
local;

create index extora_app.idx_sales_simple_range_monitored on extora_app.sales_simple_range
(sale_date, amount)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

alter index extora_app.idx_sales_simple_range_monitored
  monitoring usage;


alter table extora_app.sales_simple_range add (
  constraint ck_sales_simple_range
  check (SALE_DATE = trunc(SALE_DATE))
  enable validate,
  constraint pk_sales_simple_range
  primary key (sale_date)
  using index extora_app.idx_sales_simple_range_01
  enable validate,
  constraint uk_sales_simple_range
  unique (sale_date, amount)
  using index extora_app.idx_sales_simple_range_monitored
  enable validate);
