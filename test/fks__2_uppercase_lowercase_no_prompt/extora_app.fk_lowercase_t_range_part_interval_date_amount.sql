PROMPT Foreign key extora_app."fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
ALTER TABLE extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" ADD (
  CONSTRAINT "fk_lowercase_T_RANGE_PART_INTERVAL_DATE_amount"
  FOREIGN KEY (amount)
  REFERENCES extora_app.sales (sale_amount)
  DEFERRABLE INITIALLY DEFERRED
  DISABLE NOVALIDATE);
