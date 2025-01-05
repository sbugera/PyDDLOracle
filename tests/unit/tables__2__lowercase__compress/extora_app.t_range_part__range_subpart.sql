prompt Table extora_app.t_range_part__range_subpart
create table extora_app.t_range_part__range_subpart
(
    id      number,
    sub_id  number
)
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
    nologging
    tablespace extora_app_data
    pctfree    0
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      default
                )
)
nocache
result_cache (mode default);
