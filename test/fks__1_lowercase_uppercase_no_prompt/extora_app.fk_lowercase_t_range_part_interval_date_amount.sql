alter table EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
  foreign key (AMOUNT)
  references EXTORA_APP.SALES (SALE_AMOUNT)
  deferrable initially deferred
  disable novalidate);
