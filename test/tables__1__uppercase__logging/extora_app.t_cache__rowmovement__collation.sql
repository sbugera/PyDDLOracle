PROMPT Table EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
CREATE TABLE EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
(
    ID  NUMBER NOT NULL
)
DEFAULT COLLATION USING_NLS_SORT_CI
TABLESPACE EXTORA_APP_DATA
PCTFREE    19
INITRANS   21
MAXTRANS   255
STORAGE    (
            MINEXTENTS       17
            MAXEXTENTS       18
            PCTINCREASE      0
            BUFFER_POOL      RECYCLE
            FLASH_CACHE      KEEP
            CELL_FLASH_CACHE KEEP
            )
NOCOMPRESS
CACHE
RESULT_CACHE (MODE FORCE)
ENABLE ROW MOVEMENT;


CREATE UNIQUE INDEX EXTORA_APP.PK_T_CACHE__ROWMOVEMENT__COLLATION ON EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
(ID)
TABLESPACE EXTORA_APP_DATA
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            );


ALTER TABLE EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION ADD (
  CONSTRAINT PK_T_CACHE__ROWMOVEMENT__COLLATION
  PRIMARY KEY (ID)
  USING INDEX EXTORA_APP.PK_T_CACHE__ROWMOVEMENT__COLLATION
  ENABLE VALIDATE);
