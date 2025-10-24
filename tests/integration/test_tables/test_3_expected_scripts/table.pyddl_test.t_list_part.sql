PROMPT Table pyddl_test.t_list_part
CREATE TABLE pyddl_test.t_list_part
(
    sale_date  DATE NOT NULL,
    region     VARCHAR2(50 BYTE),
    amount     NUMBER
)
NOCOMPRESS
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY LIST (region)
(
  PARTITION north_sales VALUES ('North')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      default
                ),
  PARTITION south_sales VALUES ('South')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                INITIAL          8M
                NEXT             1M
                MINEXTENTS       1
                MAXEXTENTS       UNLIMITED
                BUFFER_POOL      default
                ),
  PARTITION west_sales VALUES ('West')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION east_sales VALUES ('East')
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                ),
  PARTITION other_sales VALUES (DEFAULT)
    LOGGING
    NOCOMPRESS
    TABLESPACE pyddl_test_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


PROMPT Index pyddl_test.pk_t_list_part
CREATE UNIQUE INDEX pyddl_test.pk_t_list_part ON pyddl_test.t_list_part
(sale_date)
LOGGING
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          64K
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      default
            );


PROMPT Constraints for table pyddl_test.t_list_part
ALTER TABLE pyddl_test.t_list_part ADD (
  CONSTRAINT pk_t_list_part
  PRIMARY KEY (sale_date)
  USING INDEX pyddl_test.pk_t_list_part
  ENABLE VALIDATE);
