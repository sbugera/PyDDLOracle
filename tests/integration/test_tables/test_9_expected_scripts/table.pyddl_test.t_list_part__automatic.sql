PROMPT Table pyddl_test.t_list_part__automatic
CREATE TABLE pyddl_test.t_list_part__automatic
(
    id            NUMBER,
    country_code  VARCHAR2(5 BYTE),
    customer_id   NUMBER,
    order_date    DATE,
    order_total   NUMBER(8,2)
)
TABLESPACE pyddl_test_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY LIST (country_code) AUTOMATIC
(
  PARTITION part_usa VALUES ('USA')
    LOGGING
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
  PARTITION part_uk_and_ireland VALUES ('GBR', 'IRL')
    LOGGING
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
  PARTITION VALUES ('BGR')
    LOGGING
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
  PARTITION VALUES ('POL')
    LOGGING
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
                )
)
RESULT_CACHE (MODE DEFAULT);
