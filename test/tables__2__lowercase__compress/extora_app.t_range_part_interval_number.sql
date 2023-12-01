prompt Table extora_app.t_range_part_interval_number
create table extora_app.t_range_part_interval_number
(
    sale_id  number not null,
    region   varchar2(50 byte),
    amount   number
)
tablespace extora_app_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by range (sale_id)
interval (1000)
(
  partition initial_partition values less than (1000)
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
  partition values less than (2000)
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


prompt Index extora_app.uk_t_range_part_interval_number
create index extora_app.uk_t_range_part_interval_number on extora_app.t_range_part_interval_number
(region)
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

prompt Index extora_app.uq_t_range_part_interval_number
create unique index extora_app.uq_t_range_part_interval_number on extora_app.t_range_part_interval_number
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


alter table extora_app.t_range_part_interval_number add (
  constraint pk_t_range_part_interval_number
  primary key (sale_id)
  using index extora_app.uq_t_range_part_interval_number
  enable validate,
  constraint uk_t_range_part_interval_number
  unique (region)
  using index extora_app.uk_t_range_part_interval_number
  enable validate);
