CREATE TABLE EXTORA_APP.T_COMPRESS_BASIC
(
    ID  NUMBER,
    V1  VARCHAR2(100 BYTE),
    V2  VARCHAR2(100 BYTE),
    V3  VARCHAR2(100 BYTE),
    V4  VARCHAR2(100 BYTE)
)
LOGGING
COMPRESS BASIC
RESULT_CACHE (MODE DEFAULT);
