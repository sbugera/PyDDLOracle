prompt Foreign key pyddl_test.fk_t_compress_basic_v1
alter table pyddl_test.t_compress_basic add (
  constraint fk_t_compress_basic_v1
  foreign key (v1)
  references pyddl_test.t_compress_for_oltp (v1)
  disable novalidate);
