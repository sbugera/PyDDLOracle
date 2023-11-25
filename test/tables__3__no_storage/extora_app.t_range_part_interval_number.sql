CREATE TABLE EXTORA_APP.T_RANGE_PART_INTERVAL_NUMBER
(
    SALE_ID  NUMBER NOT NULL,
    REGION   VARCHAR2(50 BYTE),
    AMOUNT   NUMBER
)
NOCOMPRESS
PARTITION BY RANGE (SALE_ID)
INTERVAL (1000)
(
  PARTITION INITIAL_PARTITION VALUES LESS THAN (1000)
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (2000)
    LOGGING
    NOCOMPRESS
)
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
