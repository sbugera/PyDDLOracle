create table extora_app.t_list_part__multicolumn
(
    sale_date         date,
    region            varchar2(50 byte),
    product_category  varchar2(50 byte),
    amount            number
)
tablespace extora_app_data
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
  partition north_clothing values (( 'North', 'Clothing' ))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition south_electronics values (( 'South', 'Electronics' ))
    logging
    tablespace extora_app_data
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                ),
  partition south_clothing values (( 'South', 'Clothing' ))
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
