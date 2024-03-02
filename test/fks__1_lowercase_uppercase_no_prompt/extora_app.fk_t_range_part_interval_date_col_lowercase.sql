alter table EXTORA_APP."t_lowercase_RANGE_PART_INTERVAL_DATE" add (
  constraint "fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
  foreign key ("Col_lowercase")
  references EXTORA_APP.T_STANDARD_DATATYPES ("c_Camel_Case_Name       32 Chars")
  deferrable initially deferred
  disable novalidate);
