alter table EXTORA_APP.T_COMPRESS_BASIC add (
  constraint FK_T_COMPRESS_BASIC_V1
  foreign key (V1)
  references EXTORA_APP.T_COMPRESS_FOR_OLTP (V1)
  disable novalidate);
