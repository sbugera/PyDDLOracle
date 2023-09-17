SELECT table_name,
       column_name,
       column_id,
       data_type,
       data_type_mod,
       data_type_owner,
       DECODE(data_type, 
              'CHAR', char_length, 
              'VARCHAR', char_length, 
              'VARCHAR2', char_length, 
              'NCHAR', char_length, 
              'NVARCHAR', char_length, 
              'NVARCHAR2', char_length, 
              data_length) AS data_length,
       data_precision,
       data_scale,
       nullable,
       char_used,
       default_length,
       data_default,
       virtual_column,
       identity_column,
       hidden_column,
       default_on_null,
       evaluation_edition,
       unusable_before,
       unusable_beginning,
       collation,
       internal_column_id
  FROM sys.dba_tab_cols   c
 WHERE owner = 'EXTORA_APP'
   AND ((user_generated = 'YES') OR (column_name = 'ORA_ARCHIVE_STATE'))
   and c.DATA_PRECISION is not NULL
   and c.DATA_TYPE != 'NUMBER'
   AND EXISTS (SELECT NULL
                 FROM sys.dba_all_tables t
                WHERE t.table_name = c.table_name
                  AND t.owner = c.owner)
 ORDER BY table_name, column_id, internal_column_id;