prompt Table PYDDL_TEST.T_RANGE_PART__RANGE_SUBPART
create table PYDDL_TEST.T_RANGE_PART__RANGE_SUBPART
(
    ID      number,
    SUB_ID  number
)
nocompress
tablespace USERS
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by range (ID)
interval (10)
(
  partition P_0 values less than (0)
    logging
    compress basic
    tablespace PYDDL_TEST_DATA
    pctfree    0
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                )
)
nocache
result_cache (mode default);
