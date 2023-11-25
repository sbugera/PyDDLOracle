CREATE TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(
    SALE_ID  NUMBER NOT NULL,
    REGION   VARCHAR2(50 BYTE),
    AMOUNT   NUMBER
)
NOCOMPRESS
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX EXTORA_APP.UK_T_RANGE_PART_INTERVAL_NUMBER ON EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(REGION)
LOGGING;
CREATE UNIQUE INDEX EXTORA_APP.UQ_T_RANGE_PART_INTERVAL_NUMBER ON EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(SALE_ID)
LOGGING;

ALTER TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER ADD (
  CONSTRAINT PK_T_RANGE_PART_INTERVAL_NUMBER
  PRIMARY KEY
  (SALE_ID)
  USING INDEX EXTORA_APP.UQ_T_RANGE_PART_INTERVAL_NUMBER
  ENABLE VALIDATE,
  CONSTRAINT UK_T_RANGE_PART_INTERVAL_NUMBER
  UNIQUE
  (REGION)
  USING INDEX EXTORA_APP.UK_T_RANGE_PART_INTERVAL_NUMBER
  ENABLE VALIDATE);
