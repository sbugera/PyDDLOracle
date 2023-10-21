sql_tables = """
SELECT t.owner,
       t.table_name,
       t.tablespace_name,
       t.buffer_pool,
       t.iot_name,
       t.iot_type,
       t.min_extents,
       t.next_extent,
       t.max_extents,
       t.ini_trans,
       t.max_trans,
       t.initial_extent,
       t.pct_increase,
       t.freelists,
       t.freelist_groups,
       t.pct_free,
       t.pct_used,
       t.instances,
       t.cluster_name,
       t.degree,
       t.num_rows,
       t.avg_row_len,
       t.temporary,
       t.logging,
       t.partitioned,
       t.nested,
       t.row_movement,
       t.monitoring,
       t.duration,
       t.dependencies,
       t.compression,
       t.compress_for,
       t.read_only,
       t.cache,
       t.flash_cache,
       t.cell_flash_cache,
       t.result_cache,
       t.segment_created,
       t.inmemory,
       t.inmemory_priority,
       t.inmemory_distribute,
       t.inmemory_compression,
       t.inmemory_duplicate,
       t.clustering,
       t.inmemory_service,
       t.inmemory_service_name,
       t.default_collation,
       t.sharded,
       t.duplicated,
       t.external,
       t.memoptimize_read,
       t.memoptimize_write,
       t.hybrid
  FROM sys.dba_tables t
 WHERE t.owner = :schema_name
 ORDER BY t.table_name
"""

sql_tab_columns = """
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
       collation
  FROM sys.dba_tab_cols   c
 WHERE owner = :schema_name
   AND ((user_generated = 'YES') OR (column_name = 'ORA_ARCHIVE_STATE'))
   AND EXISTS (SELECT NULL
                 FROM sys.dba_all_tables t
                WHERE t.table_name = c.table_name
                  AND t.owner = c.owner)
 ORDER BY table_name, column_id, internal_column_id
"""

sql_part_tables = """
SELECT owner,
       table_name,
       partitioning_type,
       subpartitioning_type,
       interval,
       autolist,
       interval_subpartition,
       autolist_subpartition,
       is_nested,
       auto,
       def_tablespace_name,
       def_pct_free,
       def_pct_used,
       def_ini_trans,
       def_max_trans,
       def_initial_extent,
       def_next_extent,
       def_min_extents,
       def_max_extents,
       def_max_size,
       def_pct_increase,
       def_freelists,
       def_freelist_groups,
       def_logging,
       def_compression,
       def_compress_for,
       def_buffer_pool,
       def_flash_cache,
       def_cell_flash_cache,
       ref_ptn_constraint_name,
       def_segment_creation,
       def_indexing,
       def_inmemory,
       def_inmemory_priority,
       def_inmemory_distribute,
       def_inmemory_compression,
       def_inmemory_duplicate,
       def_read_only,
       def_cellmemory,
       def_inmemory_service,
       def_inmemory_service_name
  FROM sys.dba_part_tables
 WHERE owner = :schema_name
 ORDER BY table_name
"""

sql_part_key_columns = """
SELECT name,
       column_name
  FROM sys.dba_part_key_columns
 WHERE owner = :schema_name
   AND object_type = 'TABLE'
"""

sql_tab_partitions = """
SELECT table_name,
       partition_name,
       high_value,
       high_value_length,
       partition_position,
       tablespace_name,
       logging,
       nvl(ini_trans, -1)       ini_trans,
       nvl(max_trans, -1)       max_trans,
       nvl(initial_extent, -1) initial_extent,
       nvl(next_extent, -1)     next_extent,
       nvl(min_extent, -1)      min_extent,
       nvl(max_extent, -1)      max_extent,
       nvl(pct_increase, -1)    pct_increase,
       nvl(pct_free, -1)        pct_free,
       nvl(pct_used, -1)        pct_used,
       nvl(freelists, -1)       freelists,
       nvl(freelist_groups, -1) freelist_groups,
       buffer_pool,
       last_analyzed,
       nvl(num_rows, -1)        num_rows,
       nvl(blocks, -1)          blocks,
       nvl(empty_blocks, -1)    empty_blocks,
       nvl(avg_space, -1)       avg_space,
       subpartition_count,
       compression,
       compress_for,
       flash_cache,
       cell_flash_cache,
       indexing,
       inmemory,
       inmemory_priority,
       inmemory_distribute,
       inmemory_compression,
       inmemory_duplicate,
       read_only,
       inmemory_service,
       inmemory_service_name
  FROM sys.dba_tab_partitions
 WHERE table_owner = :schema_name
 ORDER BY table_name, partition_position
"""