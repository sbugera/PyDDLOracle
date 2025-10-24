PROMPT Foreign key pyddl_test."fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
ALTER TABLE pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" ADD (
  CONSTRAINT "fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
  FOREIGN KEY (amount)
  REFERENCES pyddl_test.sales (sale_amount)
  DEFERRABLE INITIALLY DEFERRED
  DISABLE NOVALIDATE);
