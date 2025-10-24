prompt Table PYDDL_TEST.T_COMPRESS_FOR_OLTP
create table PYDDL_TEST.T_COMPRESS_FOR_OLTP
(
    ID  number,
    V1  varchar2(100 byte) not null,
    V2  varchar2(100 byte),
    V3  varchar2(100 byte),
    V4  varchar2(100 byte)
)
tablespace PYDDL_TEST_DATA
logging
compress for oltp
nocache
result_cache (mode default);
