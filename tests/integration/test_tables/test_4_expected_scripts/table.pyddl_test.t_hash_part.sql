prompt Table pyddl_test.t_hash_part
create table pyddl_test.t_hash_part
(
    employee_id  number,
    first_name   varchar2(50 byte),
    last_name    varchar2(50 byte),
    hire_date    date
)
nocompress
tablespace pyddl_test_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      default
            )
partition by hash (employee_id)
    partitions 4
    store in (pyddl_test_data, pyddl_test_data, pyddl_test_data, pyddl_test_data)
nocache
result_cache (mode default);
