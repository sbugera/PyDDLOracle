PROMPT Table pyddl_test.t_cache__rowmovement__collation
CREATE TABLE pyddl_test.t_cache__rowmovement__collation
(
    id  NUMBER NOT NULL
)
TABLESPACE pyddl_test_data
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


PROMPT Index pyddl_test.pk_t_cache__rowmovement__collation
CREATE UNIQUE INDEX pyddl_test.pk_t_cache__rowmovement__collation ON pyddl_test.t_cache__rowmovement__collation
(id)
LOGGING
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );
