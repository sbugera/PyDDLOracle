sql_column_exists = """
WITH f(view_name, column_name) AS (
    SELECT 'DBA_TABLES'     , 'DEFAULT_COLLATION'     FROM dual UNION ALL
    SELECT 'DBA_TAB_COLS'   , 'COLLATION'             FROM dual UNION ALL
    SELECT 'DBA_PART_TABLES', 'AUTOLIST'              FROM dual UNION ALL
    SELECT 'DBA_PART_TABLES', 'AUTOLIST_SUBPARTITION' FROM dual
)
SELECT f.view_name,
       f.column_name,
       decode(c.column_name, NULL, 'N', 'Y') AS column_exists,
       c.data_type,
       c.char_length
  FROM f
  LEFT JOIN sys.dba_tab_cols c
    ON f.view_name = c.table_name
   AND f.column_name = c.column_name
"""

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
       CAST(NULL AS VARCHAR2(100)) AS default_collation
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
       CAST(NULL AS VARCHAR2(100)) AS collation
  FROM sys.dba_tab_cols   c
  JOIN sys.dba_all_tables t
    ON c.table_name = t.table_name
   AND c.owner = t.owner
 WHERE c.owner = :schema_name
   AND NOT (c.column_name LIKE 'SYS\\_%' ESCAPE '\\' AND c.hidden_column = 'YES')
 ORDER BY c.table_name, c.column_id, c.internal_column_id
"""

sql_part_tables = """
SELECT pt.owner,
       pt.table_name,
       pt.partitioning_type,
       pt.subpartitioning_type,
       pt.interval,
       CAST('NO' AS VARCHAR2(3)) AS autolist,
       CAST('NO' AS VARCHAR2(3)) AS autolist_subpartition,
       pt.is_nested,
       pt.def_tablespace_name,
       pt.def_pct_free,
       pt.def_pct_used,
       pt.def_ini_trans,
       pt.def_max_trans,
       pt.def_initial_extent,
       pt.def_next_extent,
       pt.def_min_extents,
       pt.def_max_extents,
       pt.def_max_size,
       pt.def_pct_increase,
       pt.def_freelists,
       pt.def_freelist_groups,
       pt.def_logging,
       pt.def_compression,
       pt.def_compress_for,
       pt.def_buffer_pool,
       pt.def_flash_cache,
       pt.def_cell_flash_cache,
       pt.ref_ptn_constraint_name,
       pt.def_segment_creation,
       pt.def_indexing
  FROM sys.dba_part_tables pt
 WHERE pt.owner = :schema_name
 ORDER BY pt.table_name
"""

sql_part_key_columns = """
SELECT name,
       column_name
  FROM sys.dba_part_key_columns
 WHERE owner = :schema_name
   AND object_type = 'TABLE'
 ORDER BY name, column_position
"""

sql_tab_partitions = """
SELECT table_name,
       partition_name,
       high_value,
       high_value_length,
       partition_position,
       tablespace_name,
       logging,
       nvl(ini_trans, -1)       AS ini_trans,
       nvl(max_trans, -1)       AS max_trans,
       nvl(initial_extent, -1)  AS initial_extent,
       nvl(next_extent, -1)     AS next_extent,
       nvl(min_extent, -1)      AS min_extent,
       nvl(max_extent, -1)      AS max_extent,
       nvl(pct_increase, -1)    AS pct_increase,
       nvl(pct_free, -1)        AS pct_free,
       nvl(pct_used, -1)        AS pct_used,
       nvl(freelists, -1)       AS freelists,
       nvl(freelist_groups, -1) AS freelist_groups,
       buffer_pool,
       subpartition_count,
       compression,
       compress_for,
       flash_cache,
       cell_flash_cache,
       indexing
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
       c.constraint_type,
       c.search_condition,
       c.status,
       c.deferrable,
       c.deferred,
       c.validated,
       c.index_name,
       c.index_owner,
       c.r_owner,
       rc.table_name AS r_table_name,
       c.r_constraint_name,
       c.delete_rule
  FROM sys.dba_constraints c
  LEFT JOIN sys.dba_constraints rc
    ON c.r_owner = rc.owner
   AND c.r_constraint_name = rc.constraint_name
  LEFT JOIN sys.dba_recyclebin b
    ON c.table_name = b.object_name
   AND c.owner = b.owner
   AND b.type = 'TABLE'
 WHERE c.owner = :schema_name
   AND b.object_name IS NULL
   AND c.constraint_type IN ('P', 'U', 'C', 'R')
   AND (c.search_condition_vc IS NULL OR c.search_condition_vc NOT LIKE '"%" IS NOT NULL')
 ORDER BY c.table_name, c.constraint_type, c.constraint_name
"""

sql_constraint_columns = """
SELECT c.owner,
       cc.table_name,
       cc.constraint_name,
       cc.column_name,
       cc.position
  FROM sys.dba_constraints c
  JOIN sys.dba_cons_columns cc
    ON c.constraint_name = cc.constraint_name
   AND c.owner = cc.owner
  LEFT JOIN sys.dba_recyclebin b
    ON c.table_name = b.object_name
   AND c.owner = b.owner
   AND b.type = 'TABLE'
 WHERE b.object_name IS NULL
   AND c.owner = :schema_name
   AND c.constraint_type IN ('P', 'U', 'R')
 UNION
SELECT cc.owner,
       cc.table_name,
       cc.constraint_name,
       cc.column_name,
       cc.position
  FROM sys.dba_constraints c
  JOIN sys.dba_cons_columns cc
    ON c.constraint_name = cc.constraint_name
   AND c.owner = cc.owner
 WHERE EXISTS (SELECT NULL
                 FROM sys.dba_constraints sc
                WHERE sc.constraint_type = 'R'
                  AND sc.r_constraint_name = c.constraint_name
                  AND sc.r_owner = c.owner
                  AND sc.owner = :schema_name
                  AND sc.owner != c.owner)
 ORDER BY owner, table_name, constraint_name, position   
"""

sql_grants = """
SELECT tp.grantee,
       tp.owner,
       tp.table_name,
       tp.privilege,
       tp.grantable
  FROM sys.dba_tab_privs tp
 WHERE tp.owner = :schema_name
 ORDER BY tp.owner,
          tp.table_name,
          tp.grantee,
          tp.grantable,
          tp.privilege
"""