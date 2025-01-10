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
pctfree    0
initrans   1
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      DEFAULT
            )
logging
compress for oltp
nocache
result_cache (mode default);


prompt Constraints for table PYDDL_TEST.T_COMPRESS_FOR_OLTP
alter table PYDDL_TEST.T_COMPRESS_FOR_OLTP add (
  constraint CK_T_COMPRESS_FOR_OLTP
  check ( V2 IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J') )
  disable validate,
  constraint PK_T_COMPRESS_FOR_OLTP
  primary key (V1)
  disable validate,
  constraint UK_T_COMPRESS_FOR_OLTP
  unique (V2)
  disable validate);
