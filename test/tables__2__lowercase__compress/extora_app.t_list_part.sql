prompt Table extora_app.t_list_part
create table extora_app.t_list_part
(
    sale_date  date not null,
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
partition by list (region)
(
  partition north_sales values ('North')
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
  partition south_sales values ('South')
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
  partition west_sales values ('West')
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition east_sales values ('East')
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition other_sales values (DEFAULT)
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


create unique index extora_app.pk_t_list_part on extora_app.t_list_part
(sale_date)
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


alter table extora_app.t_list_part add (
  constraint pk_t_list_part
  primary key (sale_date)
  using index extora_app.pk_t_list_part
  enable validate);
