prompt Foreign key pyddl_test."fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
alter table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
  foreign key (amount)
  references pyddl_test.sales (sale_amount)
  deferrable initially deferred
  disable novalidate);
