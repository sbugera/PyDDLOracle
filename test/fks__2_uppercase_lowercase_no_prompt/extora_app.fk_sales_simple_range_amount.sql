PROMPT Foreign key extora_app.fk_sales_simple_range_amount
ALTER TABLE extora_app.sales_simple_range ADD (
  CONSTRAINT fk_sales_simple_range_amount
  FOREIGN KEY (amount)
  REFERENCES extora_app.sales (sale_amount)
  ON DELETE SET NULL
  ENABLE VALIDATE);
