prompt Table pyddl_test.t_cache__rowmovement__collation
create table pyddl_test.t_cache__rowmovement__collation
(
    id  number not null
)
tablespace pyddl_test_data
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
nocompress
cache
result_cache (mode force)
enable row movement;


prompt Index pyddl_test.pk_t_cache__rowmovement__collation
create unique index pyddl_test.pk_t_cache__rowmovement__collation on pyddl_test.t_cache__rowmovement__collation
(id)
logging
tablespace pyddl_test_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );


prompt Constraints for table pyddl_test.t_cache__rowmovement__collation
alter table pyddl_test.t_cache__rowmovement__collation add (
  constraint pk_t_cache__rowmovement__collation
  primary key (id)
  using index pyddl_test.pk_t_cache__rowmovement__collation
  enable validate);
