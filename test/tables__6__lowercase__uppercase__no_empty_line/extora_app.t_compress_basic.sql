prompt Table EXTORA_APP.T_COMPRESS_BASIC
create table EXTORA_APP.T_COMPRESS_BASIC
(
    ID  number,
    V1  varchar2(100 byte),
    V2  varchar2(100 byte),
    V3  varchar2(100 byte),
    V4  varchar2(100 byte)
)
tablespace EXTORA_APP_DATA
pctfree    0
initrans   1
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      DEFAULT
            )
logging
compress basic
nocache
result_cache (mode default);
