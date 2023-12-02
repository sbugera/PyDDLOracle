prompt Table extora_app.t_standard_datatypes
create table extora_app.t_standard_datatypes
(
    c_varchar2                          varchar2(10 byte) not null,
    c_varchar2_not_null                 varchar2(11 byte) not null,
    c_varchar2_def_y_char               varchar2(12 char) default 'Y',
    c_varchar2_def_on_null_byte         varchar2(13 byte) default on null 'N' not null,
    c_varchar2_def_on_null_no_def       varchar2(14 byte),
    c_varchar2_comment                  varchar2(17 byte),
    c_varchar2_collation                varchar2(18 byte) collate using_nls_sort_ai default 'abc' not null,
    c_varchar2_virtual_concat           varchar2(200 byte) generated always as ("C_VARCHAR2"||':'||"C_VARCHAR2_NOT_NULL"),
    c_nvarchar2                         nvarchar2(21),
    c_varchar                           varchar2(21 byte),
    c_char                              char(19 byte),
    c_char_varying                      varchar2(22 byte),
    c_char_no_length                    char(1 byte),
    c_nchar                             nchar(22),
    c_nchar_varying                     nvarchar2(22),
    c_nchar_no_length                   nchar(1),
    c_character                         char(20 byte),
    c_character_varying                 varchar2(20 byte),
    c_national_char                     nchar(22),
    c_national_char_varying             nvarchar2(22),
    c_national_character                nchar(22),
    c_national_character_varying        nvarchar2(22),
    c_number                            number not null,
    c_number_precision_38               number(38),
    c_number_precision_20               number(20),
    c_number_precision_38_scale         number(38,3),
    c_number_precision_38_scale_38      number(38,38),
    c_integer                           integer,
    c_int                               integer,
    c_smallint                          integer,
    c_numberic                          integer,
    c_decimal                           integer,
    c_dec                               integer,
    c_numberic_precision                number(20),
    c_decimal_precision                 number(20),
    c_dec_precision                     number(20),
    c_numberic_precision_scale          number(20,3),
    c_decimal_precision_scale           number(20,3),
    c_dec_precision_scale               number(20,3) not null,
    c_date_dafault                      date default sysdate,
    c_date                              date,
    c_date_not_null                     date not null,
    c_long                              long,
    c_raw                               raw(1),
    c_rowid                             rowid,
    c_urowid                            urowid(4000),
    c_urowid_40                         urowid(40),
    c_clob                              clob,
    c_clob_storage                      clob,
    c_clob_lob_par                      clob,
    c_nclob                             nclob,
    c_blob                              blob,
    c_bfile                             bfile,
    c_float                             float(126),
    c_float_precision_22                float(22),
    c_float_precision_3                 float(3),
    c_double_precision                  float(126),
    c_binary_double                     binary_double,
    c_binary_float                      binary_float,
    c_real                              float(63),
    c_xml                               sys.xmltype,
    c_interval_day_sec                  interval day(2) to second(6),
    c_interval_day2_sec6                interval day(2) to second(6),
    c_interval_day3_sec9                interval day(3) to second(9),
    c_interval_ym                       interval year(2) to month,
    c_interval_ym2                      interval year(2) to month,
    c_interval_ym3                      interval year(3) to month,
    c_timestamp                         timestamp(6),
    c_timestamp6                        timestamp(6),
    c_timestamp3                        timestamp(3),
    c_timestamp_tz                      timestamp(6) with time zone,
    c_timestamp_tz6                     timestamp(6) with time zone,
    c_timestamp_tz9                     timestamp(9) with time zone,
    c_timestamp_ltz6                    timestamp(6) with local time zone,
    c_timestamp_ltz0                    timestamp(0) with local time zone,
    c_anydata                           sys.anydata,
    "c_Camel_Case_Name       32 Chars"  varchar2(100 byte),
    c_varchar2_not_visible              varchar2(16 byte) invisible,
    c_date_invisible                    date invisible default sysdate not null
)
tablespace extora_app_data
pctfree    10
initrans   1
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            )
logging
nocache
result_cache (mode default);


prompt Index extora_app.idf_standard_datatypes_compress_low
create index extora_app.idf_standard_datatypes_compress_low on extora_app.t_standard_datatypes
(c_nvarchar2, c_varchar, c_char, c_char_varying)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

prompt Index extora_app.idx_standard_datatypes_bitmap
create bitmap index extora_app.idx_standard_datatypes_bitmap on extora_app.t_standard_datatypes
(c_integer, c_date)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

prompt Index extora_app.idx_standard_datatypes_compressed_prefix
create index extora_app.idx_standard_datatypes_compressed_prefix on extora_app.t_standard_datatypes
(c_varchar2, c_varchar2_not_null, c_varchar2_def_y_char, c_varchar2_def_on_null_byte)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

prompt Index extora_app.idx_standard_datatypes_compress_high
create index extora_app.idx_standard_datatypes_compress_high on extora_app.t_standard_datatypes
(c_char_no_length, c_nchar)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

prompt Index extora_app.idx_standard_datatypes_invisible
create index extora_app.idx_standard_datatypes_invisible on extora_app.t_standard_datatypes
(c_varchar2_def_on_null_no_def)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            )
invisible;

prompt Index extora_app.idx_standard_datatypes_reverse_nolog_parallel
create index extora_app.idx_standard_datatypes_reverse_nolog_parallel on extora_app.t_standard_datatypes
(c_varchar2_comment, c_binary_float)
nologging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            )
parallel ( degree 16 instances default )
reverse;

prompt Index extora_app.pk_t_standard_datatypes
create unique index extora_app.pk_t_standard_datatypes on extora_app.t_standard_datatypes
(c_varchar2, c_number)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

prompt Index extora_app."T_STANDARD_DATATYPES_uk_02"
create unique index extora_app."T_STANDARD_DATATYPES_uk_02" on extora_app.t_standard_datatypes
("c_Camel_Case_Name       32 Chars")
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );

prompt Index extora_app.uk_t_standard_datatypes
create unique index extora_app.uk_t_standard_datatypes on extora_app.t_standard_datatypes
(c_char, c_number)
logging
tablespace extora_app_data
pctfree    10
initrans   2
maxtrans   255
storage    (
            pctincrease      0
            buffer_pool      default
            );


prompt Constraints for table extora_app.t_standard_datatypes
alter table extora_app.t_standard_datatypes add (
  constraint pk_t_standard_datatypes
  primary key (c_varchar2, c_number)
  using index extora_app.pk_t_standard_datatypes
  enable validate,
  constraint "T_STANDARD_DATATYPES_uk_02"
  unique ("c_Camel_Case_Name       32 Chars")
  using index extora_app."T_STANDARD_DATATYPES_uk_02"
  enable validate,
  constraint uk_t_standard_datatypes
  unique (c_char, c_number)
  using index extora_app.uk_t_standard_datatypes
  enable validate);
