prompt Foreign key PYDDL_TEST."fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
alter table PYDDL_TEST."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
  foreign key ("Col_lowercase")
  references PYDDL_TEST.T_STANDARD_DATATYPES ("c_Camel_Case_Name       32 Chars")
  deferrable initially deferred
  disable novalidate);
