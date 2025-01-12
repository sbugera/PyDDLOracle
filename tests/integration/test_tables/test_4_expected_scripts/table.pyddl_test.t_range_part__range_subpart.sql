prompt Table pyddl_test.t_range_part__range_subpart
create table pyddl_test.t_range_part__range_subpart
(
    id      number,
    sub_id  number
)
nocompress
tablespace users
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by range (id)
interval (10)
(
  partition p_0 values less than (0)
    logging
    compress basic
    tablespace pyddl_test_data
    pctfree    0
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                )
)
nocache
result_cache (mode default);
