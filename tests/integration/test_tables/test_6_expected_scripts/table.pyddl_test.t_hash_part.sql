CREATE TABLE pyddl_test.t_hash_part
(
    employee_id  NUMBER,
    first_name   VARCHAR2(50 BYTE),
    last_name    VARCHAR2(50 BYTE),
    hire_date    DATE
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PARTITION BY HASH (employee_id)
    PARTITIONS 4
    STORE IN (pyddl_test_data, pyddl_test_data, pyddl_test_data, pyddl_test_data)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
