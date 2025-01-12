ALTER TABLE pyddl_test.sales_simple_range ADD (
  CONSTRAINT fk_sales_simple_range_date_amount
  FOREIGN KEY (sale_date, amount)
  REFERENCES pyddl_test.sales (sale_date, sale_amount)
  ON DELETE CASCADE
  ENABLE VALIDATE);
