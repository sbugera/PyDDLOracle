CREATE TABLE EXTORA_APP.T_LIST_PART
(
    SALE_DATE  DATE NOT NULL,
    REGION     VARCHAR2(50 BYTE),
    AMOUNT     NUMBER
)
NOCOMPRESS
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE UNIQUE INDEX EXTORA_APP.PK_T_LIST_PART ON EXTORA_APP.T_LIST_PART
(SALE_DATE)
LOGGING;

ALTER TABLE EXTORA_APP.T_LIST_PART ADD (
  CONSTRAINT PK_T_LIST_PART
  PRIMARY KEY
  (SALE_DATE)
  USING INDEX EXTORA_APP.PK_T_LIST_PART
  ENABLE VALIDATE);
