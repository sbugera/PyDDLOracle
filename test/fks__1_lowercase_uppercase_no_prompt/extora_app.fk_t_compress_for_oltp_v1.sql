alter table EXTORA_APP.T_COMPRESS_FOR_OLTP add (
  constraint FK_T_COMPRESS_FOR_OLTP_V1
  foreign key (V1)
  references EXTORA_APP.T_COMPRESS_BASIC (V2)
  disable validate);
