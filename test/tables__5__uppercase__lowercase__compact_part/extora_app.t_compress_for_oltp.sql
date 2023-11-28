PROMPT Table extora_app.t_compress_for_oltp
CREATE TABLE extora_app.t_compress_for_oltp
(
    id  NUMBER,
    v1  VARCHAR2(100 BYTE) NOT NULL,
    v2  VARCHAR2(100 BYTE),
    v3  VARCHAR2(100 BYTE),
    v4  VARCHAR2(100 BYTE)
)
TABLESPACE extora_app_data
PCTFREE    0
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
LOGGING
COMPRESS FOR OLTP
NOCACHE
RESULT_CACHE (MODE DEFAULT);


ALTER TABLE extora_app.t_compress_for_oltp ADD (
  CONSTRAINT ck_t_compress_for_oltp
  CHECK ( V2 IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J') )
  DISABLE VALIDATE,
  CONSTRAINT pk_t_compress_for_oltp
  PRIMARY KEY (v1)
  DISABLE VALIDATE,
  CONSTRAINT uk_t_compress_for_oltp
  UNIQUE (v2)
  DISABLE VALIDATE);
