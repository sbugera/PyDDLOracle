PROMPT Table extora_app.t_standard_datatypes
CREATE TABLE extora_app.t_standard_datatypes
(
    c_varchar2                          VARCHAR2(10 BYTE) NOT NULL,
    c_varchar2_not_null                 VARCHAR2(11 BYTE) NOT NULL,
    c_varchar2_def_y_char               VARCHAR2(12 CHAR) DEFAULT 'Y',
    c_varchar2_def_on_null_byte         VARCHAR2(13 BYTE) DEFAULT ON NULL 'N' NOT NULL,
    c_varchar2_def_on_null_no_def       VARCHAR2(14 BYTE),
    c_varchar2_comment                  VARCHAR2(17 BYTE),
    c_varchar2_collation                VARCHAR2(18 BYTE) COLLATE USING_NLS_SORT_AI DEFAULT 'abc' NOT NULL,
    c_varchar2_virtual_concat           VARCHAR2(200 BYTE) GENERATED ALWAYS AS ("C_VARCHAR2"||':'||"C_VARCHAR2_NOT_NULL"),
    c_nvarchar2                         NVARCHAR2(21),
    c_varchar                           VARCHAR2(21 BYTE),
    c_char                              CHAR(19 BYTE),
    c_char_varying                      VARCHAR2(22 BYTE),
    c_char_no_length                    CHAR(1 BYTE),
    c_nchar                             NCHAR(22),
    c_nchar_varying                     NVARCHAR2(22),
    c_nchar_no_length                   NCHAR(1),
    c_character                         CHAR(20 BYTE),
    c_character_varying                 VARCHAR2(20 BYTE),
    c_national_char                     NCHAR(22),
    c_national_char_varying             NVARCHAR2(22),
    c_national_character                NCHAR(22),
    c_national_character_varying        NVARCHAR2(22),
    c_number                            NUMBER NOT NULL,
    c_number_precision_38               NUMBER(38),
    c_number_precision_20               NUMBER(20),
    c_number_precision_38_scale         NUMBER(38,3),
    c_number_precision_38_scale_38      NUMBER(38,38),
    c_integer                           INTEGER,
    c_int                               INTEGER,
    c_smallint                          INTEGER,
    c_numberic                          INTEGER,
    c_decimal                           INTEGER,
    c_dec                               INTEGER,
    c_numberic_precision                NUMBER(20),
    c_decimal_precision                 NUMBER(20),
    c_dec_precision                     NUMBER(20),
    c_numberic_precision_scale          NUMBER(20,3),
    c_decimal_precision_scale           NUMBER(20,3),
    c_dec_precision_scale               NUMBER(20,3) NOT NULL,
    c_date_dafault                      DATE DEFAULT sysdate,
    c_date                              DATE,
    c_date_not_null                     DATE NOT NULL,
    c_long                              LONG,
    c_raw                               RAW(1),
    c_rowid                             ROWID,
    c_urowid                            UROWID(4000),
    c_urowid_40                         UROWID(40),
    c_clob                              CLOB,
    c_clob_storage                      CLOB,
    c_clob_lob_par                      CLOB,
    c_nclob                             NCLOB,
    c_blob                              BLOB,
    c_bfile                             BFILE,
    c_float                             FLOAT(126),
    c_float_precision_22                FLOAT(22),
    c_float_precision_3                 FLOAT(3),
    c_double_precision                  FLOAT(126),
    c_binary_double                     BINARY_DOUBLE,
    c_binary_float                      BINARY_FLOAT,
    c_real                              FLOAT(63),
    c_xml                               SYS.XMLTYPE,
    c_interval_day_sec                  INTERVAL DAY(2) TO SECOND(6),
    c_interval_day2_sec6                INTERVAL DAY(2) TO SECOND(6),
    c_interval_day3_sec9                INTERVAL DAY(3) TO SECOND(9),
    c_interval_ym                       INTERVAL YEAR(2) TO MONTH,
    c_interval_ym2                      INTERVAL YEAR(2) TO MONTH,
    c_interval_ym3                      INTERVAL YEAR(3) TO MONTH,
    c_timestamp                         TIMESTAMP(6),
    c_timestamp6                        TIMESTAMP(6),
    c_timestamp3                        TIMESTAMP(3),
    c_timestamp_tz                      TIMESTAMP(6) WITH TIME ZONE,
    c_timestamp_tz6                     TIMESTAMP(6) WITH TIME ZONE,
    c_timestamp_tz9                     TIMESTAMP(9) WITH TIME ZONE,
    c_timestamp_ltz6                    TIMESTAMP(6) WITH LOCAL TIME ZONE,
    c_timestamp_ltz0                    TIMESTAMP(0) WITH LOCAL TIME ZONE,
    c_anydata                           SYS.ANYDATA,
    c_json                              JSON,
    "c_Camel_Case_Name       32 Chars"  VARCHAR2(100 BYTE),
    c_varchar2_not_visible              VARCHAR2(16 BYTE) INVISIBLE,
    c_date_invisible                    DATE INVISIBLE DEFAULT sysdate NOT NULL
)
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
LOGGING
NOCOMPRESS
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX extora_app.idf_standard_datatypes_compress_low ON extora_app.t_standard_datatypes
(c_nvarchar2, c_varchar, c_char, c_char_varying)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
COMPRESS ADVANCED LOW;

CREATE BITMAP INDEX extora_app.idx_standard_datatypes_bitmap ON extora_app.t_standard_datatypes
(c_integer, c_date)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

CREATE INDEX extora_app.idx_standard_datatypes_compressed_prefix ON extora_app.t_standard_datatypes
(c_varchar2, c_varchar2_not_null, c_varchar2_def_y_char, c_varchar2_def_on_null_byte)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
COMPRESS 2;

CREATE INDEX extora_app.idx_standard_datatypes_compress_high ON extora_app.t_standard_datatypes
(c_char_no_length, c_nchar)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
COMPRESS ADVANCED HIGH;

CREATE INDEX extora_app.idx_standard_datatypes_invisible ON extora_app.t_standard_datatypes
(c_varchar2_def_on_null_no_def)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
INVISIBLE;

CREATE INDEX extora_app.idx_standard_datatypes_reverse_nolog_parallel ON extora_app.t_standard_datatypes
(c_varchar2_comment, c_binary_float)
NOLOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            )
PARALLEL ( DEGREE 16 INSTANCES DEFAULT )
REVERSE;

CREATE UNIQUE INDEX extora_app.pk_t_standard_datatypes ON extora_app.t_standard_datatypes
(c_varchar2, c_number)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

CREATE UNIQUE INDEX extora_app."T_STANDARD_DATATYPES_uk_02" ON extora_app.t_standard_datatypes
("c_Camel_Case_Name       32 Chars")
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );

CREATE UNIQUE INDEX extora_app.uk_t_standard_datatypes ON extora_app.t_standard_datatypes
(c_char, c_number)
LOGGING
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            PCTINCREASE      0
            BUFFER_POOL      default
            );


ALTER TABLE extora_app.t_standard_datatypes ADD (
  CONSTRAINT pk_t_standard_datatypes
  PRIMARY KEY (c_varchar2, c_number)
  USING INDEX extora_app.pk_t_standard_datatypes
  ENABLE VALIDATE,
  CONSTRAINT "T_STANDARD_DATATYPES_uk_02"
  UNIQUE ("c_Camel_Case_Name       32 Chars")
  USING INDEX extora_app."T_STANDARD_DATATYPES_uk_02"
  ENABLE VALIDATE,
  CONSTRAINT uk_t_standard_datatypes
  UNIQUE (c_char, c_number)
  USING INDEX extora_app.uk_t_standard_datatypes
  ENABLE VALIDATE);
