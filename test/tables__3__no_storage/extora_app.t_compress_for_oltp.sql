CREATE TABLE EXTORA_APP.T_COMPRESS_FOR_OLTP
(
    ID  NUMBER,
    V1  VARCHAR2(100 BYTE) NOT NULL,
    V2  VARCHAR2(100 BYTE),
    V3  VARCHAR2(100 BYTE),
    V4  VARCHAR2(100 BYTE)
)
LOGGING
COMPRESS FOR OLTP
RESULT_CACHE (MODE DEFAULT);


ALTER TABLE EXTORA_APP.T_COMPRESS_FOR_OLTP ADD (
  CONSTRAINT CK_T_COMPRESS_FOR_OLTP
  CHECK ( V2 IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J') )
  DISABLE VALIDATE,
  CONSTRAINT PK_T_COMPRESS_FOR_OLTP
  PRIMARY KEY (V1)
  DISABLE VALIDATE,
  CONSTRAINT UK_T_COMPRESS_FOR_OLTP
  UNIQUE (V2)
  DISABLE VALIDATE);
