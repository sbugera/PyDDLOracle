CREATE TABLE extora_app.sales
(
    sale_id      NUMBER,
    sale_date    DATE,
    sale_amount  NUMBER
)
NOCOMPRESS
TABLESPACE extora_app_data
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            BUFFER_POOL      default
            )
PARTITION BY RANGE (sale_date)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
  PARTITION p1 VALUES LESS THAN (TO_DATE(' 2020-01-01 00:00:00', 'SYYYY-MM-DD HH24:MI:SS', 'NLS_CALENDAR=GREGORIAN'))
    LOGGING
    NOCOMPRESS
    TABLESPACE extora_app_data
    PCTFREE    10
    INITRANS   1
    MAXTRANS   255
    STORAGE    (
                BUFFER_POOL      default
                )
)
NOCACHE
RESULT_CACHE (MODE DEFAULT);


COMMENT ON TABLE extora_app.sales IS 'Sales';

COMMENT ON COLUMN extora_app.sales.sale_id IS 'Sale ID';

COMMENT ON COLUMN extora_app.sales.sale_date IS 'Sale Date';

COMMENT ON COLUMN extora_app.sales.sale_amount IS 'Sale Ammount';


CREATE INDEX extora_app.pk_sales ON extora_app.sales
(sale_id)
LOGGING
TABLESPACE extora_app_data
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

CREATE INDEX extora_app.uk_sales ON extora_app.sales
(sale_amount)
LOGGING
TABLESPACE extora_app_data
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


ALTER TABLE extora_app.sales ADD (
  CONSTRAINT ck_sales
  CHECK (sale_amount > 0)
  DEFERRABLE INITIALLY IMMEDIATE
  ENABLE VALIDATE,
  CONSTRAINT pk_sales
  PRIMARY KEY (sale_id)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX extora_app.pk_sales
  ENABLE VALIDATE,
  CONSTRAINT uk_sales
  UNIQUE (sale_amount)
  DEFERRABLE INITIALLY IMMEDIATE
  USING INDEX extora_app.uk_sales
  ENABLE VALIDATE);
