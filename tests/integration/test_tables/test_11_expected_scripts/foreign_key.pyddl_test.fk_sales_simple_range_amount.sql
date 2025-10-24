ALTER TABLE pyddl_test.sales_simple_range ADD (
  CONSTRAINT fk_sales_simple_range_amount
  FOREIGN KEY (amount)
  REFERENCES pyddl_test.sales (sale_amount)
  ON DELETE SET NULL
  ENABLE VALIDATE);
