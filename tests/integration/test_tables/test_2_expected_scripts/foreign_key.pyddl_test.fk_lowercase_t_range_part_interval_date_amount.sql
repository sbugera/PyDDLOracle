prompt Foreign key PYDDL_TEST."fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
alter table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
  foreign key (AMOUNT)
  references PYDDL_TEST.SALES (SALE_AMOUNT)
  deferrable initially deferred
  disable novalidate);
