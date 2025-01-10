prompt Table PYDDL_TEST.DATABASECHANGELOG
create table PYDDL_TEST.DATABASECHANGELOG
(
    ID             varchar2(255 byte) not null,
    AUTHOR         varchar2(255 byte) not null,
    FILENAME       varchar2(255 byte) not null,
    DATEEXECUTED   timestamp(6) not null,
    ORDEREXECUTED  integer not null,
    EXECTYPE       varchar2(10 byte) not null,
    MD5SUM         varchar2(35 byte),
    DESCRIPTION    varchar2(255 byte),
    COMMENTS       varchar2(255 byte),
    TAG            varchar2(255 byte),
    LIQUIBASE      varchar2(20 byte),
    CONTEXTS       varchar2(255 byte),
    LABELS         varchar2(255 byte),
    DEPLOYMENT_ID  varchar2(10 byte)
)
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      DEFAULT
            )
logging
nocompress
nocache
result_cache (mode default);
