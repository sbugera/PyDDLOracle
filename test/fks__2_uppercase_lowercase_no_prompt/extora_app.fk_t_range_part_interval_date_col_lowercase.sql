PROMPT Foreign key extora_app."fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
ALTER TABLE extora_app."t_lowercase_RANGE_PART_INTERVAL_DATE" ADD (
  CONSTRAINT "fk_T_RANGE_PART_INTERVAL_DATE_Col_lowercase"
  FOREIGN KEY ("Col_lowercase")
  REFERENCES extora_app.t_standard_datatypes ("c_Camel_Case_Name       32 Chars")
  DEFERRABLE INITIALLY DEFERRED
  DISABLE NOVALIDATE);
