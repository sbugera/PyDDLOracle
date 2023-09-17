DROP TABLE EXTORA_APP.T_STANDARD_DATATYPES CASCADE CONSTRAINTS;

CREATE TABLE EXTORA_APP.t_standard_datatypes
(
  c_varchar2                      VARCHAR2(10),
  c_varchar2_not_null             VARCHAR2(11)  NOT NULL,
  c_varchar2_def_y_char           VARCHAR2(12 CHAR) DEFAULT 'Y',
  c_varchar2_def_on_null_byte     VARCHAR2(13 BYTE) DEFAULT ON NULL 'N',
  c_varchar2_def_on_null_no_def   VARCHAR2(14),
  c_varchar2_not_visible          VARCHAR2(16) INVISIBLE,
  c_varchar2_comment              VARCHAR2(17),
  c_varchar2_collation            VARCHAR2(18) COLLATE USING_NLS_SORT_AI,
  c_varchar2_virtual_concat       VARCHAR2(200) GENERATED ALWAYS AS (c_varchar2 || ':' || c_varchar2_not_null),
  c_nvarchar2                     NVARCHAR2(21),
  c_varchar                       VARCHAR(21),
  c_char                          CHAR(19 BYTE),
  c_char_varying                  CHAR VARYING(22),
  c_char_no_length                CHAR,
  c_nchar                         NCHAR(22),
  c_nchar_varying                 NCHAR VARYING(22),
  c_nchar_no_length               NCHAR,
  c_character                     CHARACTER(20),
  c_character_varying             CHARACTER VARYING(20),
  c_national_char                 NATIONAL CHAR(22),
  c_national_char_varying         NATIONAL CHAR VARYING(22),
  c_national_character            NATIONAL CHARACTER(22),
  c_national_character_varying    NATIONAL CHARACTER VARYING(22),
  c_number                        NUMBER,
  c_number_precision_38           NUMBER(38),
  c_number_precision_20           NUMBER(20),
  c_number_precision_38_scale     NUMBER(38,3),
  c_number_precision_38_scale_38  NUMBER(38,38),
  c_integer                       INTEGER,
  c_int                           INT,
  c_smallint                      SMALLINT,
  c_numberic                      NUMERIC,
  c_decimal                       DECIMAL,
  c_dec                           DEC,
  c_numberic_precision            NUMERIC(20),
  c_decimal_precision             DECIMAL(20),
  c_dec_precision                 DEC(20),
  c_numberic_precision_scale      NUMERIC(20,3),
  c_decimal_precision_scale       DECIMAL(20,3),
  c_dec_precision_scale           DEC(20,3),
  c_date                          DATE          DEFAULT systimestamp,
  c_long                          LONG,
  --c_long_raw                      LONG RAW,
  c_raw                           RAW(1),
  c_rowid                         ROWID,
  c_urowid                        UROWID,
  c_urowid_40                     UROWID(40),
  c_clob                          CLOB,
  c_clob_storage                  CLOB,
  c_clob_lob_par                  CLOB,
  c_nclob                         NCLOB,
  c_blob                          BLOB,
  c_bfile                         BFILE,
  c_float                         FLOAT,
  c_float_precision_22            FLOAT(22),
  c_float_precision_3             FLOAT(3),
  c_double_precision              DOUBLE PRECISION,
  c_binary_double                 BINARY_DOUBLE,
  c_binary_float                  BINARY_FLOAT,
  c_real                          REAL,
  c_xml                           SYS.XMLTYPE,
  c_interval_day_sec              INTERVAL DAY TO SECOND,
  c_interval_day2_sec6            INTERVAL DAY(2) TO SECOND(6),
  c_interval_day3_sec9            INTERVAL DAY(3) TO SECOND(9),
  c_interval_ym                   INTERVAL YEAR TO MONTH,
  c_interval_ym2                  INTERVAL YEAR(2) TO MONTH,
  c_interval_ym3                  INTERVAL YEAR(3) TO MONTH,
  c_timestamp                     TIMESTAMP,
  c_timestamp6                    TIMESTAMP(6),
  c_timestamp3                    TIMESTAMP(3),
  c_timestamp_tz                  TIMESTAMP WITH TIME ZONE,
  c_timestamp_tz6                 TIMESTAMP(6) WITH TIME ZONE,
  c_timestamp_tz9                 TIMESTAMP(9) WITH TIME ZONE,
  c_timestamp_ltz6                TIMESTAMP(6) WITH LOCAL TIME ZONE,
  c_timestamp_ltz0                TIMESTAMP(0) WITH LOCAL TIME ZONE,
  c_anydata                       SYS.ANYDATA,
  c_json                          JSON
)
LOB (c_clob) STORE AS SECUREFILE (
  ENABLE      STORAGE IN ROW
  RETENTION
  NOCACHE
  LOGGING)
LOB (c_clob_storage) STORE AS SECUREFILE c_clob_storage_segment (
  TABLESPACE  extora_app_data
  ENABLE      STORAGE IN ROW
  RETENTION
  NOCACHE
  LOGGING
  STORAGE    (
              INITIAL          10M
              NEXT             1M
              MAXSIZE          100G
              MINEXTENTS       15
              MAXEXTENTS       16
              PCTINCREASE      12
              FREELISTS        13
              FREELIST GROUPS  14
              BUFFER_POOL      RECYCLE
              FLASH_CACHE      KEEP
              CELL_FLASH_CACHE NONE
             ))
LOB (c_clob_lob_par) STORE AS SECUREFILE c_clob_lob_par_segment (
  DISABLE     STORAGE IN ROW
  --ENCRYPT USING 'AES128'
  CHUNK       7
  RETENTION   MIN 900
  DEDUPLICATE
  COMPRESS HIGH
  CACHE READS

  FILESYSTEM_LIKE_LOGGING
  INDEX       c_clob_lob_par_idx)
LOB (c_nclob) STORE AS SECUREFILE (
  ENABLE      STORAGE IN ROW
  RETENTION
  NOCACHE
  LOGGING)
LOB (c_blob) STORE AS SECUREFILE (
  ENABLE      STORAGE IN ROW
  RETENTION
  NOCACHE
  LOGGING)
XMLTYPE c_xml STORE AS CLOB (
  ENABLE      STORAGE IN ROW
  RETENTION
  NOCACHE
  LOGGING)
STORAGE    (
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOCOMPRESS 
NOCACHE
RESULT_CACHE (MODE DEFAULT)
NOPARALLEL;
