prompt Foreign key PYDDL_TEST.FK_T_COMPRESS_FOR_OLTP_V1
alter table PYDDL_TEST.T_COMPRESS_FOR_OLTP add (
  constraint FK_T_COMPRESS_FOR_OLTP_V1
  foreign key (V1)
  references PYDDL_TEST.T_COMPRESS_BASIC (V2)
  disable validate);
