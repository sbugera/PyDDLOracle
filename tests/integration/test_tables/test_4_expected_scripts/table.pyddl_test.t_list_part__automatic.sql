prompt Table pyddl_test.t_list_part__automatic
create table pyddl_test.t_list_part__automatic
(
    id            number,
    country_code  varchar2(5 byte),
    customer_id   number,
    order_date    date,
    order_total   number(8,2)
)
nocompress
tablespace pyddl_test_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by list (country_code) automatic
(
  partition part_usa values ('USA')
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
  partition part_uk_and_ireland values ('GBR', 'IRL')
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
  partition values ('BGR')
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
  partition values ('POL')
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
