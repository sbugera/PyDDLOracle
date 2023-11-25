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
SELECT c.table_name,
       c.column_name,
       c.column_id,
       c.data_type,
       c.data_type_mod,
       c.data_type_owner,
       DECODE(data_type,
              'CHAR', c.char_length,
              'VARCHAR', c.char_length,
              'VARCHAR2', c.char_length,
              'NCHAR', c.char_length,
              'NVARCHAR', c.char_length,
              'NVARCHAR2', c.char_length,
              c.data_length) AS data_length,
       c.data_precision,
       c.data_scale,
       c.nullable,
       c.char_used,
       c.default_length,
       c.data_default,
       c.virtual_column,
       c.identity_column,
       c.hidden_column,
       c.default_on_null,
       c.evaluation_edition,
       c.unusable_before,
       c.unusable_beginning,
       c.collation
  FROM sys.dba_tab_cols   c
  JOIN sys.dba_all_tables t
    ON c.table_name = t.table_name
   AND c.owner = t.owner
 WHERE c.owner = :schema_name
   AND NOT (c.column_name LIKE 'SYS\\_%' ESCAPE '\\' AND c.hidden_column = 'YES')
 ORDER BY c.table_name, c.column_id, c.internal_column_id
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

sql_comments = """
SELECT table_name,
       NULL column_name,
       comments,
       0 order_num
  FROM sys.dba_tab_comments
 WHERE owner = :schema_name
   AND comments IS NOT NULL
   AND origin_con_id = TO_NUMBER (SYS_CONTEXT ('USERENV', 'CON_ID'))
 UNION ALL
SELECT cc.table_name,
       cc.column_name,
       cc.comments,
       tc.internal_column_id
  FROM sys.dba_col_comments cc
  JOIN sys.dba_tab_cols tc
    ON cc.column_name = tc.column_name
   AND cc.table_name = tc.table_name
   AND cc.owner = tc.owner
 WHERE cc.owner = :schema_name
   AND cc.comments IS NOT NULL
   AND cc.origin_con_id = TO_NUMBER (SYS_CONTEXT ('USERENV', 'CON_ID'))
 ORDER BY table_name, order_num
"""

sql_indexes = """
SELECT i.owner,
       i.index_name,
       i.index_type,
       i.table_owner,
       i.table_name,
       i.uniqueness,
       i.compression,
       i.prefix_length,
       i.tablespace_name,
       i.ini_trans,
       i.max_trans,
       i.initial_extent,
       i.next_extent,
       i.min_extents,
       i.max_extents,
       i.pct_increase,
       i.pct_threshold,
       i.include_column,
       i.freelists,
       i.freelist_groups,
       i.pct_free,
       i.logging,
       i.instances,
       i.partitioned,
       i.buffer_pool,
       i.flash_cache,
       i.cell_flash_cache,
       i.visibility,
       u.monitoring,
       i.degree,
       i.instances
  FROM sys.dba_indexes i
  LEFT JOIN sys.dba_object_usage u
    ON i.owner = u.owner
   AND i.index_name = u.index_name
   AND u.monitoring = 'YES'
 WHERE i.owner = :schema_name
   AND i.index_type <> 'LOB'
 ORDER BY i.owner, i.index_name
"""

sql_index_columns = """
SELECT ic.index_owner,
       ic.index_name,
       ic.column_name,
       ic.table_owner,
       ic.table_name,
       ic.column_position
  FROM sys.dba_ind_columns ic
  JOIN sys.dba_indexes i
    ON ic.index_owner = i.owner
   AND ic.index_name = i.index_name
   AND i.index_type <> 'LOB'
 WHERE ic.index_owner = :schema_name
 ORDER BY ic.index_owner, ic.index_name, ic.column_position
"""

sql_constraints = """
SELECT c.table_name,
       c.constraint_name,
       c.status,
       c.deferrable,
       c.deferred,
       c.validated,
       c.index_name,
       c.index_owner
  FROM sys.dba_constraints c
  LEFT JOIN sys.dba_recyclebin b
    ON c.table_name = b.object_name
   AND c.owner = b.owner
   AND b.type = 'TABLE'
 WHERE c.owner = :schema_name
   AND b.object_name IS NULL
   AND c.constraint_type = 'P'
 ORDER BY c.table_name, c.constraint_type, c.constraint_name
"""

sql_constraint_columns = """
SELECT cc.table_name,
       cc.constraint_name,
       cc.column_name
  FROM sys.dba_constraints c
  JOIN sys.dba_cons_columns cc
    ON c.constraint_name = cc.constraint_name
   AND c.owner = cc.owner
  LEFT JOIN sys.dba_recyclebin b
    ON c.table_name = b.object_name
   AND c.owner = b.owner
   AND b.type = 'TABLE'
 WHERE c.owner = :schema_name
   AND b.object_name IS NULL
   AND c.constraint_type = 'P'
 ORDER BY cc.table_name, cc.constraint_name, cc.position
"""