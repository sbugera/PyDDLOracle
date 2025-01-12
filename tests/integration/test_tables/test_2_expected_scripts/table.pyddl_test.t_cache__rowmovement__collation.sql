prompt Table PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
create table PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
(
    ID  number not null
)
tablespace PYDDL_TEST_DATA
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


prompt Index PYDDL_TEST.PK_T_CACHE__ROWMOVEMENT__COLLATION
create unique index PYDDL_TEST.PK_T_CACHE__ROWMOVEMENT__COLLATION on PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
(ID)
logging
tablespace PYDDL_TEST_DATA
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      DEFAULT
            );


prompt Constraints for table PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
alter table PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION add (
  constraint PK_T_CACHE__ROWMOVEMENT__COLLATION
  primary key (ID)
  using index PYDDL_TEST.PK_T_CACHE__ROWMOVEMENT__COLLATION
  enable validate);
