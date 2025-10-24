prompt Foreign key pyddl_test.fk_sales_simple_range_date_amount
alter table pyddl_test.sales_simple_range add (
  constraint fk_sales_simple_range_date_amount
  foreign key (sale_date, amount)
  references pyddl_test.sales (sale_date, sale_amount)
  on delete cascade
  enable validate);
