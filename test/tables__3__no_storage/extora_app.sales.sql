CREATE TABLE EXTORA_APP.SALES
(
    SALE_ID      NUMBER,
    SALE_DATE    DATE,
    SALE_AMOUNT  NUMBER
)
NOCOMPRESS
PARTITION BY RANGE (SALE_DATE)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION P1 VALUES LESS THAN (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION P2 VALUES LESS THAN (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION P3 VALUES LESS THAN (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION P4 VALUES LESS THAN (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS,
  PARTITION VALUES LESS THAN (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
)
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX EXTORA_APP.PK_SALES ON EXTORA_APP.SALES
(SALE_ID)
LOGGING;

CREATE INDEX EXTORA_APP.UK_SALES ON EXTORA_APP.SALES
(SALE_AMOUNT)
LOGGING;

CREATE INDEX EXTORA_APP.UK_SALES_02 ON EXTORA_APP.SALES
(SALE_DATE, SALE_AMOUNT)
LOGGING;


ALTER TABLE EXTORA_APP.SALES ADD (
  CONSTRAINT CK_SALES
  CHECK (sale_amount > 0)
  DEFERRABLE INITIALLY IMMEDIATE
  ENABLE VALIDATE,
  CONSTRAINT PK_SALES
  PRIMARY KEY (SALE_ID)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX EXTORA_APP.PK_SALES
  ENABLE VALIDATE,
  CONSTRAINT UK_SALES
  UNIQUE (SALE_AMOUNT)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX EXTORA_APP.UK_SALES
  ENABLE VALIDATE,
  CONSTRAINT UK_SALES_02
  UNIQUE (SALE_DATE, SALE_AMOUNT)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX EXTORA_APP.UK_SALES_02
  ENABLE VALIDATE);


GRANT ALTER, DEBUG, DELETE, FLASHBACK, INSERT, ON COMMIT REFRESH, QUERY REWRITE, READ, SELECT, UPDATE ON EXTORA_APP.SALES TO APP_ROLE;

GRANT ALTER, DEBUG, FLASHBACK, INDEX, ON COMMIT REFRESH, QUERY REWRITE, READ, REFERENCES ON EXTORA_APP.SALES TO EXTORA_USR;
GRANT DELETE, INSERT, SELECT, UPDATE ON EXTORA_APP.SALES TO EXTORA_USR WITH GRANT OPTION;

GRANT READ ON EXTORA_APP.SALES TO READ_ROLE;

GRANT SELECT ON EXTORA_APP.SALES TO USER_ROLE;

GRANT DELETE, INSERT, UPDATE ON EXTORA_APP.SALES TO "lowercase_Role";
