prompt Table EXTORA_APP.T_COMPRESS_FOR_OLTP
create table EXTORA_APP.T_COMPRESS_FOR_OLTP
(
    ID  number,
    V1  varchar2(100 byte) not null,
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
compress for oltp
nocache;
