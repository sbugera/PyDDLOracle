prompt Foreign key pyddl_test."fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
alter table pyddl_test."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
  foreign key ("Col_lowercase")
  references pyddl_test.t_standard_datatypes ("c_Camel_Case_Name       32 Chars")
  deferrable initially deferred
  disable novalidate);
