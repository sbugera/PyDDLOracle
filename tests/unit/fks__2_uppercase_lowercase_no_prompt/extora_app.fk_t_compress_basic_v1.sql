PROMPT Foreign key extora_app.fk_t_compress_basic_v1
ALTER TABLE extora_app.t_compress_basic ADD (
  CONSTRAINT fk_t_compress_basic_v1
  FOREIGN KEY (v1)
  REFERENCES extora_app.t_compress_for_oltp (v1)
  DISABLE NOVALIDATE);
