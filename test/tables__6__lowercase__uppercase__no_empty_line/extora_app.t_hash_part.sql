create table EXTORA_APP.T_HASH_PART
(
    EMPLOYEE_ID  number,
    FIRST_NAME   varchar2(50 byte),
    LAST_NAME    varchar2(50 byte),
    HIRE_DATE    date
)
nocompress
tablespace EXTORA_APP_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by hash (EMPLOYEE_ID)
    partitions 4
    store in (EXTORA_APP_DATA, EXTORA_APP_DATA, EXTORA_APP_DATA, EXTORA_APP_DATA)
nocache
result_cache (mode default);
