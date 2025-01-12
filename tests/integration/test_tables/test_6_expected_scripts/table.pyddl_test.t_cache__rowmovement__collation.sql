CREATE TABLE pyddl_test.t_cache__rowmovement__collation
(
    id  NUMBER NOT NULL
)
TABLESPACE pyddl_test_data
LOGGING
NOCOMPRESS
CACHE
RESULT_CACHE (MODE FORCE)
ENABLE ROW MOVEMENT;


CREATE UNIQUE INDEX pyddl_test.pk_t_cache__rowmovement__collation ON pyddl_test.t_cache__rowmovement__collation
(id)
LOGGING
TABLESPACE pyddl_test_data;


ALTER TABLE pyddl_test.t_cache__rowmovement__collation ADD (
  CONSTRAINT pk_t_cache__rowmovement__collation
  PRIMARY KEY (id)
  USING INDEX pyddl_test.pk_t_cache__rowmovement__collation
  ENABLE VALIDATE);
