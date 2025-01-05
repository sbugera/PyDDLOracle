alter table EXTORA_APP.SALES_SIMPLE_RANGE add (
  constraint FK_SALES_SIMPLE_RANGE_DATE
  foreign key (SALE_DATE)
  references EXTORA_USR.SALES (SALE_DATE)
  enable validate);
