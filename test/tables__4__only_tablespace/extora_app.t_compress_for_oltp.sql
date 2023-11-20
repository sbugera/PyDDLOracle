CREATE TABLE EXTORA_APP.T_COMPRESS_FOR_OLTP
(
    ID  NUMBER,
    V1  VARCHAR2(100 BYTE),
    V2  VARCHAR2(100 BYTE),
    V3  VARCHAR2(100 BYTE),
    V4  VARCHAR2(100 BYTE)
)
TABLESPACE EXTORA_APP_DATA
LOGGING
COMPRESS FOR OLTP
NOCACHE;
