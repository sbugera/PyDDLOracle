PROMPT Table pyddl_test.t_compress_basic
CREATE TABLE pyddl_test.t_compress_basic
(
    id  NUMBER,
    v1  VARCHAR2(100 BYTE),
    v2  VARCHAR2(100 BYTE),
    v3  VARCHAR2(100 BYTE),
    v4  VARCHAR2(100 BYTE)
)
TABLESPACE pyddl_test_data
PCTFREE    0
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
LOGGING
COMPRESS BASIC
NOCACHE
RESULT_CACHE (MODE DEFAULT);
