create table extora_app.t_hash_part
(
    employee_id  number,
    first_name   varchar2(50 byte),
    last_name    varchar2(50 byte),
    hire_date    date
)
tablespace extora_app_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by hash (employee_id)
    partitions 4
    store in (extora_app_data, extora_app_data, extora_app_data, extora_app_data)
nocache
result_cache (mode default);
