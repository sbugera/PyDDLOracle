prompt Foreign key PYDDL_TEST.FK_SALES_SIMPLE_RANGE_AMOUNT
alter table PYDDL_TEST.SALES_SIMPLE_RANGE add (
  constraint FK_SALES_SIMPLE_RANGE_AMOUNT
  foreign key (AMOUNT)
  references PYDDL_TEST.SALES (SALE_AMOUNT)
  on delete set null
  enable validate);
