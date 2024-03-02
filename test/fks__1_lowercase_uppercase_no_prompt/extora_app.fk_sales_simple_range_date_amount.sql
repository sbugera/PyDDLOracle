alter table EXTORA_APP.SALES_SIMPLE_RANGE add (
  constraint FK_SALES_SIMPLE_RANGE_DATE_AMOUNT
  foreign key (SALE_DATE, AMOUNT)
  references EXTORA_APP.SALES (SALE_DATE, SALE_AMOUNT)
  on delete cascade
  enable validate);
