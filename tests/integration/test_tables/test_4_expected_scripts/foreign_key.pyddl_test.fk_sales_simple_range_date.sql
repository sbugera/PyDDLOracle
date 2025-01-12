prompt Foreign key pyddl_test.fk_sales_simple_range_date
alter table pyddl_test.sales_simple_range add (
  constraint fk_sales_simple_range_date
  foreign key (sale_date)
  references pyddl_test_user.sales (sale_date)
  enable validate);
