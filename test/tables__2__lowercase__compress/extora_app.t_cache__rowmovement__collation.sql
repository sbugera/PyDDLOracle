create table extora_app.t_cache__rowmovement__collation
(
    id  number not null
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


create unique index extora_app.pk_t_cache__rowmovement__collation on extora_app.t_cache__rowmovement__collation
(id)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );


alter table extora_app.t_cache__rowmovement__collation add (
  constraint pk_t_cache__rowmovement__collation
  primary key (id)
  using index extora_app.pk_t_cache__rowmovement__collation
  enable validate);
