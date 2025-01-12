CREATE TABLE pyddl_test.t_hash_part
(
    employee_id  NUMBER,
    first_name   VARCHAR2(50 BYTE),
    last_name    VARCHAR2(50 BYTE),
    hire_date    DATE
)
NOCOMPRESS
PARTITION BY HASH (employee_id)
    PARTITIONS 4
NOCACHE
RESULT_CACHE (MODE DEFAULT);
