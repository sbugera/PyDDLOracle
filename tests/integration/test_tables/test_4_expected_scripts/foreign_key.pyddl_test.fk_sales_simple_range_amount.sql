prompt Foreign key pyddl_test.fk_sales_simple_range_amount
alter table pyddl_test.sales_simple_range add (
  constraint fk_sales_simple_range_amount
  foreign key (amount)
  references pyddl_test.sales (sale_amount)
  on delete set null
  enable validate);
