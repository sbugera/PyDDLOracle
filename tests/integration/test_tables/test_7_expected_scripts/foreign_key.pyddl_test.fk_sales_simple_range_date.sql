prompt Foreign key PYDDL_TEST.FK_SALES_SIMPLE_RANGE_DATE
alter table PYDDL_TEST.SALES_SIMPLE_RANGE add (
  constraint FK_SALES_SIMPLE_RANGE_DATE
  foreign key (SALE_DATE)
  references PYDDL_TEST_USER.SALES (SALE_DATE)
  enable validate);
