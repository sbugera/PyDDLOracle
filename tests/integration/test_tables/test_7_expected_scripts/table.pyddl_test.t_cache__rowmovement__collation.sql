prompt Table PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
create table PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
(
    ID  number not null
)
tablespace PYDDL_TEST_DATA
logging
nocompress
cache
result_cache (mode force)
enable row movement;


prompt Index PYDDL_TEST.PK_T_CACHE__ROWMOVEMENT__COLLATION
create unique index PYDDL_TEST.PK_T_CACHE__ROWMOVEMENT__COLLATION on PYDDL_TEST.T_CACHE__ROWMOVEMENT__COLLATION
(ID)
logging
tablespace PYDDL_TEST_DATA;
