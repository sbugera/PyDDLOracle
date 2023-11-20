CREATE TABLE extora_app.t_hash_part
(
    employee_id  NUMBER,
    first_name   VARCHAR2(50 BYTE),
    last_name    VARCHAR2(50 BYTE),
    hire_date    DATE
)
NOCOMPRESS
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY HASH (employee_id)
    PARTITIONS 4
    STORE IN (extora_app_data, extora_app_data, extora_app_data, extora_app_data)
NOCACHE
RESULT_CACHE (MODE DEFAULT);
