CREATE TABLE EXTORA_APP.T_STANDARD_DATATYPES
(
    C_VARCHAR2                          VARCHAR2(10 BYTE) NOT NULL,
    C_VARCHAR2_NOT_NULL                 VARCHAR2(11 BYTE) NOT NULL,
    C_VARCHAR2_DEF_Y_CHAR               VARCHAR2(12 CHAR) DEFAULT 'Y',
    C_VARCHAR2_DEF_ON_NULL_BYTE         VARCHAR2(13 BYTE) DEFAULT ON NULL 'N' NOT NULL,
    C_VARCHAR2_DEF_ON_NULL_NO_DEF       VARCHAR2(14 BYTE),
    C_VARCHAR2_COMMENT                  VARCHAR2(17 BYTE),
    C_VARCHAR2_COLLATION                VARCHAR2(18 BYTE) COLLATE USING_NLS_SORT_AI DEFAULT 'abc' NOT NULL,
    C_VARCHAR2_VIRTUAL_CONCAT           VARCHAR2(200 BYTE) GENERATED ALWAYS AS ("C_VARCHAR2"||':'||"C_VARCHAR2_NOT_NULL"),
    C_NVARCHAR2                         NVARCHAR2(21),
    C_VARCHAR                           VARCHAR2(21 BYTE),
    C_CHAR                              CHAR(19 BYTE),
    C_CHAR_VARYING                      VARCHAR2(22 BYTE),
    C_CHAR_NO_LENGTH                    CHAR(1 BYTE),
    C_NCHAR                             NCHAR(22),
    C_NCHAR_VARYING                     NVARCHAR2(22),
    C_NCHAR_NO_LENGTH                   NCHAR(1),
    C_CHARACTER                         CHAR(20 BYTE),
    C_CHARACTER_VARYING                 VARCHAR2(20 BYTE),
    C_NATIONAL_CHAR                     NCHAR(22),
    C_NATIONAL_CHAR_VARYING             NVARCHAR2(22),
    C_NATIONAL_CHARACTER                NCHAR(22),
    C_NATIONAL_CHARACTER_VARYING        NVARCHAR2(22),
    C_NUMBER                            NUMBER NOT NULL,
    C_NUMBER_PRECISION_38               NUMBER(38),
    C_NUMBER_PRECISION_20               NUMBER(20),
    C_NUMBER_PRECISION_38_SCALE         NUMBER(38,3),
    C_NUMBER_PRECISION_38_SCALE_38      NUMBER(38,38),
    C_INTEGER                           INTEGER,
    C_INT                               INTEGER,
    C_SMALLINT                          INTEGER,
    C_NUMBERIC                          INTEGER,
    C_DECIMAL                           INTEGER,
    C_DEC                               INTEGER,
    C_NUMBERIC_PRECISION                NUMBER(20),
    C_DECIMAL_PRECISION                 NUMBER(20),
    C_DEC_PRECISION                     NUMBER(20),
    C_NUMBERIC_PRECISION_SCALE          NUMBER(20,3),
    C_DECIMAL_PRECISION_SCALE           NUMBER(20,3),
    C_DEC_PRECISION_SCALE               NUMBER(20,3) NOT NULL,
    C_DATE_DAFAULT                      DATE DEFAULT sysdate,
    C_DATE                              DATE,
    C_DATE_NOT_NULL                     DATE NOT NULL,
    C_LONG                              LONG,
    C_RAW                               RAW(1),
    C_ROWID                             ROWID,
    C_UROWID                            UROWID(4000),
    C_UROWID_40                         UROWID(40),
    C_CLOB                              CLOB,
    C_CLOB_STORAGE                      CLOB,
    C_CLOB_LOB_PAR                      CLOB,
    C_NCLOB                             NCLOB,
    C_BLOB                              BLOB,
    C_BFILE                             BFILE,
    C_FLOAT                             FLOAT(126),
    C_FLOAT_PRECISION_22                FLOAT(22),
    C_FLOAT_PRECISION_3                 FLOAT(3),
    C_DOUBLE_PRECISION                  FLOAT(126),
    C_BINARY_DOUBLE                     BINARY_DOUBLE,
    C_BINARY_FLOAT                      BINARY_FLOAT,
    C_REAL                              FLOAT(63),
    C_XML                               SYS.XMLTYPE,
    C_INTERVAL_DAY_SEC                  INTERVAL DAY(2) TO SECOND(6),
    C_INTERVAL_DAY2_SEC6                INTERVAL DAY(2) TO SECOND(6),
    C_INTERVAL_DAY3_SEC9                INTERVAL DAY(3) TO SECOND(9),
    C_INTERVAL_YM                       INTERVAL YEAR(2) TO MONTH,
    C_INTERVAL_YM2                      INTERVAL YEAR(2) TO MONTH,
    C_INTERVAL_YM3                      INTERVAL YEAR(3) TO MONTH,
    C_TIMESTAMP                         TIMESTAMP(6),
    C_TIMESTAMP6                        TIMESTAMP(6),
    C_TIMESTAMP3                        TIMESTAMP(3),
    C_TIMESTAMP_TZ                      TIMESTAMP(6) WITH TIME ZONE,
    C_TIMESTAMP_TZ6                     TIMESTAMP(6) WITH TIME ZONE,
    C_TIMESTAMP_TZ9                     TIMESTAMP(9) WITH TIME ZONE,
    C_TIMESTAMP_LTZ6                    TIMESTAMP(6) WITH LOCAL TIME ZONE,
    C_TIMESTAMP_LTZ0                    TIMESTAMP(0) WITH LOCAL TIME ZONE,
    C_ANYDATA                           SYS.ANYDATA,
    C_JSON                              JSON,
    "c_Camel_Case_Name       32 Chars"  VARCHAR2(100 BYTE),
    C_VARCHAR2_NOT_VISIBLE              VARCHAR2(16 BYTE) INVISIBLE,
    C_DATE_INVISIBLE                    DATE INVISIBLE DEFAULT sysdate NOT NULL
)
LOGGING
NOCOMPRESS
NOCACHE
RESULT_CACHE (MODE DEFAULT);


CREATE INDEX EXTORA_APP.IDF_STANDARD_DATATYPES_COMPRESS_LOW ON EXTORA_APP.T_STANDARD_DATATYPES
(C_NVARCHAR2, C_VARCHAR, C_CHAR, C_CHAR_VARYING)
LOGGING
COMPRESS ADVANCED LOW;
CREATE BITMAP INDEX EXTORA_APP.IDX_STANDARD_DATATYPES_BITMAP ON EXTORA_APP.T_STANDARD_DATATYPES
(C_INTEGER, C_DATE)
LOGGING;
CREATE INDEX EXTORA_APP.IDX_STANDARD_DATATYPES_COMPRESSED_PREFIX ON EXTORA_APP.T_STANDARD_DATATYPES
(C_VARCHAR2, C_VARCHAR2_NOT_NULL, C_VARCHAR2_DEF_Y_CHAR, C_VARCHAR2_DEF_ON_NULL_BYTE)
LOGGING
COMPRESS 2;
CREATE INDEX EXTORA_APP.IDX_STANDARD_DATATYPES_COMPRESS_HIGH ON EXTORA_APP.T_STANDARD_DATATYPES
(C_CHAR_NO_LENGTH, C_NCHAR)
LOGGING
COMPRESS ADVANCED HIGH;
CREATE INDEX EXTORA_APP.IDX_STANDARD_DATATYPES_INVISIBLE ON EXTORA_APP.T_STANDARD_DATATYPES
(C_VARCHAR2_DEF_ON_NULL_NO_DEF)
LOGGING
INVISIBLE;
CREATE INDEX EXTORA_APP.IDX_STANDARD_DATATYPES_REVERSE_NOLOG_PARALLEL ON EXTORA_APP.T_STANDARD_DATATYPES
(C_VARCHAR2_COMMENT, C_BINARY_FLOAT)
NOLOGGING
PARALLEL ( DEGREE 16 INSTANCES DEFAULT )
REVERSE;
CREATE UNIQUE INDEX EXTORA_APP.PK_T_STANDARD_DATATYPES ON EXTORA_APP.T_STANDARD_DATATYPES
(C_VARCHAR2, C_NUMBER)
LOGGING;
CREATE UNIQUE INDEX EXTORA_APP."T_STANDARD_DATATYPES_uk_02" ON EXTORA_APP.T_STANDARD_DATATYPES
("c_Camel_Case_Name       32 Chars")
LOGGING;
CREATE UNIQUE INDEX EXTORA_APP.UK_T_STANDARD_DATATYPES ON EXTORA_APP.T_STANDARD_DATATYPES
(C_CHAR, C_NUMBER)
LOGGING;

ALTER TABLE EXTORA_APP.T_STANDARD_DATATYPES ADD (
  CONSTRAINT PK_T_STANDARD_DATATYPES
  PRIMARY KEY (C_VARCHAR2, C_NUMBER)
  USING INDEX EXTORA_APP.PK_T_STANDARD_DATATYPES
  ENABLE VALIDATE,
  CONSTRAINT "T_STANDARD_DATATYPES_uk_02"
  UNIQUE ("c_Camel_Case_Name       32 Chars")
  USING INDEX EXTORA_APP."T_STANDARD_DATATYPES_uk_02"
  ENABLE VALIDATE,
  CONSTRAINT UK_T_STANDARD_DATATYPES
  UNIQUE (C_CHAR, C_NUMBER)
  USING INDEX EXTORA_APP.UK_T_STANDARD_DATATYPES
  ENABLE VALIDATE);
