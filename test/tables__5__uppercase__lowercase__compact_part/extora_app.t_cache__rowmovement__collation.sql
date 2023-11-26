CREATE TABLE extora_app.t_cache__rowmovement__collation
(
    id  NUMBER NOT NULL
)
DEFAULT COLLATION USING_NLS_SORT_CI
TABLESPACE extora_app_data
PCTFREE    19
INITRANS   21
MAXTRANS   255
STORAGE    (
            MINEXTENTS       17
            MAXEXTENTS       18
            PCTINCREASE      0
            BUFFER_POOL      recycle
            FLASH_CACHE      keep
            CELL_FLASH_CACHE keep
            )
LOGGING
NOCOMPRESS
CACHE
RESULT_CACHE (MODE FORCE)
ENABLE ROW MOVEMENT;


CREATE UNIQUE INDEX extora_app.pk_t_cache__rowmovement__collation ON extora_app.t_cache__rowmovement__collation
(id)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );


ALTER TABLE extora_app.t_cache__rowmovement__collation ADD (
  CONSTRAINT pk_t_cache__rowmovement__collation
  PRIMARY KEY (id)
  USING INDEX extora_app.pk_t_cache__rowmovement__collation
  ENABLE VALIDATE);
