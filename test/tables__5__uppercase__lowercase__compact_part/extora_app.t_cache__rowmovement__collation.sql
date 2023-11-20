CREATE TABLE extora_app.t_cache__rowmovement__collation
(
    id  NUMBER
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
