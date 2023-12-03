CREATE TABLE EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE"
(
    SALE_DATE        DATE,
    REGION           VARCHAR2(50 BYTE),
    AMOUNT           NUMBER,
    "Col_lowercase"  VARCHAR2(10 BYTE) DEFAULT 'test' NOT NULL
)
NOCOMPRESS
PARTITION BY RANGE (SALE_DATE)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION SALES_DATA_INITIAL VALUES LESS THAN (TO_DATE(' 2022-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (TO_DATE(' 2022-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (TO_DATE(' 2022-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
)
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX EXTORA_APP."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE"
(SALE_DATE, REGION)
LOGGING;

CREATE INDEX EXTORA_APP."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk" ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE"
(AMOUNT)
LOGGING;


ALTER TABLE EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" ADD (
  CONSTRAINT "ck_lowercase_T_RANGE_PART_INTERVAL_DATE"
  CHECK (amount BETWEEN 1 and 1000000 )
  DEFERRABLE INITIALLY DEFERRED
  ENABLE VALIDATE,
  CONSTRAINT "pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  PRIMARY KEY (SALE_DATE, REGION)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX EXTORA_APP."pk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE,
  CONSTRAINT "uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  UNIQUE (AMOUNT)
  DEFERRABLE INITIALLY DEFERRED
  USING INDEX EXTORA_APP."uk_lowercase_T_RANGE_PART_INTERVAL_DATE_pk"
  ENABLE VALIDATE);


GRANT ALTER, DEBUG, DELETE, FLASHBACK, INSERT, ON COMMIT REFRESH, QUERY REWRITE, READ, SELECT, UPDATE ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" TO APP_ROLE;

GRANT ALTER, DEBUG, FLASHBACK, INDEX, ON COMMIT REFRESH, QUERY REWRITE, READ, REFERENCES ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" TO EXTORA_USR;
GRANT DELETE, INSERT, SELECT, UPDATE ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" TO EXTORA_USR WITH GRANT OPTION;

GRANT READ ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" TO READ_ROLE;

GRANT SELECT ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" TO USER_ROLE;

GRANT DELETE, INSERT, UPDATE ON EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" TO "lowercase_Role";
