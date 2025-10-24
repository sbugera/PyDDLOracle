prompt Table pyddl_test.t_list_part__multicolumn
create table pyddl_test.t_list_part__multicolumn
(
    sale_date         date,
    region            varchar2(50 byte),
    product_category  varchar2(50 byte),
    amount            number
)
nocompress
tablespace pyddl_test_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by list (region, product_category)
(
  partition north_electronics values (( 'North', 'Electronics' ))
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
  partition north_clothing values (( 'North', 'Clothing' ))
    logging
    nocompress
    tablespace pyddl_test_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition south_electronics values (( 'South', 'Electronics' ))
    logging
    nocompress
    tablespace pyddl_test_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition south_clothing values (( 'South', 'Clothing' ))
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
  partition other_sales values (DEFAULT)
    logging
    nocompress
    tablespace pyddl_test_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                )
)
nocache
result_cache (mode default);
