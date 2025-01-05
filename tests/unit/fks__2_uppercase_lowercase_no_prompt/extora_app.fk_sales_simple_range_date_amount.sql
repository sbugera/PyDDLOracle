PROMPT Foreign key extora_app.fk_sales_simple_range_date_amount
ALTER TABLE extora_app.sales_simple_range ADD (
  CONSTRAINT fk_sales_simple_range_date_amount
  FOREIGN KEY (sale_date, amount)
  REFERENCES extora_app.sales (sale_date, sale_amount)
  ON DELETE CASCADE
  ENABLE VALIDATE);
