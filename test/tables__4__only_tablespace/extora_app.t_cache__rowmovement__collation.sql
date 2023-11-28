PROMPT Table EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
CREATE TABLE EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
(
    ID  NUMBER NOT NULL
)
DEFAULT COLLATION USING_NLS_SORT_CI
TABLESPACE EXTORA_APP_DATA
LOGGING
NOCOMPRESS
CACHE
ENABLE ROW MOVEMENT;


CREATE UNIQUE INDEX EXTORA_APP.PK_T_CACHE__ROWMOVEMENT__COLLATION ON EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
(ID)
LOGGING
TABLESPACE EXTORA_APP_DATA;


ALTER TABLE EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION ADD (
  CONSTRAINT PK_T_CACHE__ROWMOVEMENT__COLLATION
  PRIMARY KEY (ID)
  USING INDEX EXTORA_APP.PK_T_CACHE__ROWMOVEMENT__COLLATION
  ENABLE VALIDATE);
