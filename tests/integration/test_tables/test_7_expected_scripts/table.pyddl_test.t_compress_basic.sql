prompt Table PYDDL_TEST.T_COMPRESS_BASIC
create table PYDDL_TEST.T_COMPRESS_BASIC
(
    ID  number,
    V1  varchar2(100 byte),
    V2  varchar2(100 byte),
    V3  varchar2(100 byte),
    V4  varchar2(100 byte)
)
tablespace PYDDL_TEST_DATA
logging
compress basic
nocache
result_cache (mode default);
