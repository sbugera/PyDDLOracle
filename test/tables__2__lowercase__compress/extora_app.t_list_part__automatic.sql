prompt Table extora_app.t_list_part__automatic
create table extora_app.t_list_part__automatic
(
    id            number,
    country_code  varchar2(5 byte),
    customer_id   number,
    order_date    date,
    order_total   number(8,2)
)
tablespace extora_app_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by list (country_code)
(
  partition part_usa values ('USA') automatic
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
  partition part_uk_and_ireland values ('GBR', 'IRL') automatic
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
  partition values ('BGR') automatic
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
  partition values ('POL') automatic
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
