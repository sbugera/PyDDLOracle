ALTER TABLE pyddl_test.sales_simple_range ADD (
  CONSTRAINT fk_sales_simple_range_date
  FOREIGN KEY (sale_date)
  REFERENCES pyddl_test_user.sales (sale_date)
  ENABLE VALIDATE);
