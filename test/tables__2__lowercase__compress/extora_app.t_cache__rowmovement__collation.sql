create table extora_app.t_cache__rowmovement__collation
(
    id  number
)
default collation using_nls_sort_ci
tablespace extora_app_data
pctfree    19
initrans   21
maxtrans   255
storage    (
            minextents       17
            maxextents       18
            pctincrease      0
            buffer_pool      recycle
            flash_cache      keep
            cell_flash_cache keep
            )
logging
cache
result_cache (mode force)
enable row movement;
