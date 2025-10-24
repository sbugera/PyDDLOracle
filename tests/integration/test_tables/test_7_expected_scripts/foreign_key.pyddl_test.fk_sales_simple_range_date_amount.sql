prompt Foreign key PYDDL_TEST.FK_SALES_SIMPLE_RANGE_DATE_AMOUNT
alter table PYDDL_TEST.SALES_SIMPLE_RANGE add (
  constraint FK_SALES_SIMPLE_RANGE_DATE_AMOUNT
  foreign key (SALE_DATE, AMOUNT)
  references PYDDL_TEST.SALES (SALE_DATE, SALE_AMOUNT)
  on delete cascade
  enable validate);
