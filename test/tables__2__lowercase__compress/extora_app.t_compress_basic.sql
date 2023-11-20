create table extora_app.t_compress_basic
(
    id  number,
    v1  varchar2(100 byte),
    v2  varchar2(100 byte),
    v3  varchar2(100 byte),
    v4  varchar2(100 byte)
)
tablespace extora_app_data
pctfree    0
initrans   1
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            )
logging
nocache
result_cache (mode default);