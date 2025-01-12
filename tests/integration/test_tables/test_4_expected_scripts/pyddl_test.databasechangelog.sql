prompt Table pyddl_test.databasechangelog
create table pyddl_test.databasechangelog
(
    id             varchar2(255 byte) not null,
    author         varchar2(255 byte) not null,
    filename       varchar2(255 byte) not null,
    dateexecuted   timestamp(6) not null,
    orderexecuted  integer not null,
    exectype       varchar2(10 byte) not null,
    md5sum         varchar2(35 byte),
    description    varchar2(255 byte),
    comments       varchar2(255 byte),
    tag            varchar2(255 byte),
    liquibase      varchar2(20 byte),
    contexts       varchar2(255 byte),
    labels         varchar2(255 byte),
    deployment_id  varchar2(10 byte)
)
tablespace pyddl_test_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            minextents       1
            maxextents       unlimited
            pctincrease      0
            buffer_pool      default
            )
logging
nocompress
nocache
result_cache (mode default);
