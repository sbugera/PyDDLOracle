PROMPT Foreign key pyddl_test.fk_t_compress_for_oltp_v1
ALTER TABLE pyddl_test.t_compress_for_oltp ADD (
  CONSTRAINT fk_t_compress_for_oltp_v1
  FOREIGN KEY (v1)
  REFERENCES pyddl_test.t_compress_basic (v2)
  DISABLE VALIDATE);
