-- Lock Database
UPDATE PYDDL_TEST.DATABASECHANGELOGLOCK SET LOCKED = 1, LOCKEDBY = 'Sergiis-Laptop.local (192.168.100.24)', LOCKGRANTED = SYSTIMESTAMP WHERE ID = 1 AND LOCKED = 0;

-- *********************************************************************
-- Update Database Script
-- *********************************************************************
-- Change Log: ./tests/integration/test_tables/test_1_expected_scripts/changelog.xml
-- Ran at: 1/7/25, 11:32 PM
-- Against: PYDDL_TEST@jdbc:oracle:thin:@bhouse:1521/ORCLPDB1
-- Liquibase version: 4.30.0
-- *********************************************************************

-- Changeset tests/integration/test_tables/test_1_expected_scripts/changelog.xml::001_001_drop_objects::sit
PROMPT Dropping tables

BEGIN
    FOR i IN (SELECT table_name FROM user_tables WHERE table_name NOT IN ('DATABASECHANGELOG', 'DATABASECHANGELOGLOCK')) LOOP
        dbms_output.put_line('Table "' || i.table_name || '"');
        EXECUTE IMMEDIATE 'DROP TABLE "' || i.table_name || '" CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

PROMPT Tables dropped;

UPDATE PYDDL_TEST.DATABASECHANGELOG SET COMMENTS = '', CONTEXTS = NULL, DATEEXECUTED = SYSTIMESTAMP, DEPLOYMENT_ID = '6289147105', DESCRIPTION = 'sqlFile path=drop_tables.sql', EXECTYPE = 'RERAN', LABELS = NULL, LIQUIBASE = '4.30.0', MD5SUM = '9:43bad6e31a90753bb5dd6730d550b9dd', ORDEREXECUTED = 6 WHERE ID = '001_001_drop_objects' AND AUTHOR = 'sit' AND FILENAME = 'tests/integration/test_tables/test_1_expected_scripts/changelog.xml';

-- Release Database Lock
UPDATE PYDDL_TEST.DATABASECHANGELOGLOCK SET LOCKED = 0, LOCKEDBY = NULL, LOCKGRANTED = NULL WHERE ID = 1;

