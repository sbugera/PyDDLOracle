create table EXTORA_APP.T_CACHE__ROWMOVEMENT__COLLATION
(
    ID  number
)
default collation using_nls_sort_ci
tablespace EXTORA_APP_DATA
pctfree    19
initrans   21
maxtrans   255
storage    (
            minextents       17
            maxextents       18
            pctincrease      0
            buffer_pool      RECYCLE
            flash_cache      KEEP
            cell_flash_cache KEEP
            )
logging
nocompress
cache
result_cache (mode force)
enable row movement;
