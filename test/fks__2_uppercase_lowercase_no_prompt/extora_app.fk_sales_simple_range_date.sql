PROMPT Foreign key extora_app.fk_sales_simple_range_date
ALTER TABLE extora_app.sales_simple_range ADD (
  CONSTRAINT fk_sales_simple_range_date
  FOREIGN KEY (sale_date)
  REFERENCES extora_usr.sales (sale_date)
  ENABLE VALIDATE);
