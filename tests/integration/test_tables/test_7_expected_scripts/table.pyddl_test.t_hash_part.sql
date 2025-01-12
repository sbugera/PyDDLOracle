prompt Table PYDDL_TEST.T_HASH_PART
create table PYDDL_TEST.T_HASH_PART
(
    EMPLOYEE_ID  number,
    FIRST_NAME   varchar2(50 byte),
    LAST_NAME    varchar2(50 byte),
    HIRE_DATE    date
)
nocompress
tablespace PYDDL_TEST_DATA
partition by hash (EMPLOYEE_ID)
    partitions 4
    store in (PYDDL_TEST_DATA, PYDDL_TEST_DATA, PYDDL_TEST_DATA, PYDDL_TEST_DATA)
nocache
result_cache (mode default);
