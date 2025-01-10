PROMPT Dropping tables

BEGIN
    FOR i IN (SELECT table_name FROM user_tables WHERE table_name NOT IN ('DATABASECHANGELOG', 'DATABASECHANGELOGLOCK')) LOOP
        dbms_output.put_line('Table "' || i.table_name || '"');
        EXECUTE IMMEDIATE 'DROP TABLE "' || i.table_name || '" CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

PROMPT Tables dropped
