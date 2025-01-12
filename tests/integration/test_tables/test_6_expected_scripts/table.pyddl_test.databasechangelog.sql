CREATE TABLE pyddl_test.databasechangelog
(
    id             VARCHAR2(255 BYTE) NOT NULL,
    author         VARCHAR2(255 BYTE) NOT NULL,
    filename       VARCHAR2(255 BYTE) NOT NULL,
    dateexecuted   TIMESTAMP(6) NOT NULL,
    orderexecuted  INTEGER NOT NULL,
    exectype       VARCHAR2(10 BYTE) NOT NULL,
    md5sum         VARCHAR2(35 BYTE),
    description    VARCHAR2(255 BYTE),
    comments       VARCHAR2(255 BYTE),
    tag            VARCHAR2(255 BYTE),
    liquibase      VARCHAR2(20 BYTE),
    contexts       VARCHAR2(255 BYTE),
    labels         VARCHAR2(255 BYTE),
    deployment_id  VARCHAR2(10 BYTE)
)
TABLESPACE pyddl_test_data
LOGGING
NOCOMPRESS
NOCACHE
RESULT_CACHE (MODE DEFAULT);
