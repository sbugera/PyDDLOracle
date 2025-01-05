alter table EXTORA_APP.SALES_SIMPLE_RANGE add (
  constraint FK_SALES_SIMPLE_RANGE_AMOUNT
  foreign key (AMOUNT)
  references EXTORA_APP.SALES (SALE_AMOUNT)
  on delete set null
  enable validate);
