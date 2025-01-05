prompt Table EXTORA_APP.SALES
create table EXTORA_APP.SALES
(
    SALE_ID      number,
    SALE_DATE    date,
    SALE_AMOUNT  number
)
nocompress
tablespace EXTORA_APP_DATA
pctfree    10
initrans   1
maxtrans   255
storage    (
            buffer_pool      DEFAULT
            )
partition by range (SALE_DATE)
interval (NUMTOYMINTERVAL(1, 'MONTH'))
(
  partition P1 values less than (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                buffer_pool      DEFAULT
                ),
  partition P2 values less than (TO_DATE(' 2020-02-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition P3 values less than (TO_DATE(' 2020-03-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition P4 values less than (TO_DATE(' 2020-04-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition values less than (TO_DATE(' 2020-05-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                ),
  partition values less than (TO_DATE(' 2020-06-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    logging
    nocompress
    tablespace EXTORA_APP_DATA
    pctfree    10
    initrans   1
    maxtrans   255
    storage    (
                initial          8M
                next             1M
                minextents       1
                maxextents       unlimited
                buffer_pool      DEFAULT
                )
)
nocache;


comment on table EXTORA_APP.SALES is 'Sales';
comment on column EXTORA_APP.SALES.SALE_ID     is 'Sale ID';
comment on column EXTORA_APP.SALES.SALE_DATE   is 'Sale Date';
comment on column EXTORA_APP.SALES.SALE_AMOUNT is 'Sale Ammount';


prompt Grants on table EXTORA_APP.SALES to APP_ROLE
grant alter, debug, delete, flashback, insert, on commit refresh, query rewrite, read, select, update on EXTORA_APP.SALES to APP_ROLE;

prompt Grants on table EXTORA_APP.SALES to EXTORA_USR
grant alter, debug, flashback, index, on commit refresh, query rewrite, read, references on EXTORA_APP.SALES to EXTORA_USR;
grant delete, insert, select, update on EXTORA_APP.SALES to EXTORA_USR with grant option;

prompt Grants on table EXTORA_APP.SALES to READ_ROLE
grant read on EXTORA_APP.SALES to READ_ROLE;

prompt Grants on table EXTORA_APP.SALES to USER_ROLE
grant select on EXTORA_APP.SALES to USER_ROLE;

prompt Grants on table EXTORA_APP.SALES to "lowercase_Role"
grant delete, insert, update on EXTORA_APP.SALES to "lowercase_Role";
