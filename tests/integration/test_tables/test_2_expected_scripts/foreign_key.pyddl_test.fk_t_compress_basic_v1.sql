prompt Foreign key PYDDL_TEST.FK_T_COMPRESS_BASIC_V1
alter table PYDDL_TEST.T_COMPRESS_BASIC add (
  constraint FK_T_COMPRESS_BASIC_V1
  foreign key (V1)
  references PYDDL_TEST.T_COMPRESS_FOR_OLTP (V1)
  disable novalidate);
