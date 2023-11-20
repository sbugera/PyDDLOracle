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
