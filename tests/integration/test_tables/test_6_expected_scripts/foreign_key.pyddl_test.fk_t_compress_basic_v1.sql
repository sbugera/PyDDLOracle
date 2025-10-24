ALTER TABLE pyddl_test.t_compress_basic ADD (
  CONSTRAINT fk_t_compress_basic_v1
  FOREIGN KEY (v1)
  REFERENCES pyddl_test.t_compress_for_oltp (v1)
  DISABLE NOVALIDATE);
