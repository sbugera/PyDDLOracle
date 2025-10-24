CREATE TABLE pyddl_test.t_compress_basic
(
    id  NUMBER,
    v1  VARCHAR2(100 BYTE),
    v2  VARCHAR2(100 BYTE),
    v3  VARCHAR2(100 BYTE),
    v4  VARCHAR2(100 BYTE)
)
LOGGING
COMPRESS BASIC
NOCACHE
RESULT_CACHE (MODE DEFAULT);


ALTER TABLE pyddl_test.t_compress_basic ADD (
  CONSTRAINT ck_t_compress_basic
  CHECK (v2 = upper(v2))
  DISABLE NOVALIDATE,
  CONSTRAINT pk_t_compress_basic
  PRIMARY KEY (id, v1)
  DISABLE NOVALIDATE,
  CONSTRAINT uk_t_compress_basic
  UNIQUE (v2)
  DISABLE NOVALIDATE);
