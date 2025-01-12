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


prompt Constraints for table PYDDL_TEST.T_COMPRESS_BASIC
alter table PYDDL_TEST.T_COMPRESS_BASIC add (
  constraint CK_T_COMPRESS_BASIC
  check (v2 = upper(v2))
  disable novalidate,
  constraint PK_T_COMPRESS_BASIC
  primary key (ID, V1)
  disable novalidate,
  constraint UK_T_COMPRESS_BASIC
  unique (V2)
  disable novalidate);
