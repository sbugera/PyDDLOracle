import pandas as pd
from sqlalchemy import create_engine

import sql_queries as sql
from utils import conf_con


def get_db_engine():
    db_username = conf_con['database']['username']
    db_password = conf_con['database']['password']
    db_host = conf_con['database']['host']
    db_port = conf_con['database']['port']
    try:
        db_service_name = conf_con['database']['service_name']
        connection_string = (f"oracle+cx_oracle://{db_username}:{db_password}@{db_host}:{db_port}"
                             f"/?service_name={db_service_name}")
    except KeyError:
        db_sid = conf_con['database']['sid']
        connection_string = f"oracle+cx_oracle://{db_username}:{db_password}@{db_host}:{db_port}/{db_sid}"
    return create_engine(connection_string, arraysize=1000)


def get_db_schema_name(arg_schema_name=None):
    if arg_schema_name:
        username = arg_schema_name.upper()
    else:
        username = conf_con['database']['username'].upper()
    return username


def get_column_exists(df_column_exists, view_name, column_name):
    return df_column_exists.loc[(df_column_exists['view_name'] == view_name) &
                                (df_column_exists['column_name'] == column_name), 'column_exists'].values[0]


def get_df_tables(engine, schema_name, df_column_exists):
    sql_tables = sql.sql_tables
    if get_column_exists(df_column_exists, 'DBA_TABLES', 'DEFAULT_COLLATION') == "Y":
        sql_tables = sql_tables.replace("CAST(NULL AS VARCHAR2(100)) AS default_collation", "t.default_collation")
    return pd.read_sql_query(sql_tables, engine, params={'schema_name': schema_name})


def get_df_tab_columns(engine, schema_name, df_column_exists):
    sql_tab_columns = sql.sql_tab_columns
    if get_column_exists(df_column_exists, 'DBA_TAB_COLS', 'COLLATION') == "Y":
        sql_tab_columns = sql_tab_columns.replace("CAST(NULL AS VARCHAR2(100)) AS collation", "c.collation")
    return pd.read_sql_query(sql_tab_columns, engine, params={'schema_name': schema_name})


def get_df_part_tables(engine, schema_name, df_column_exists):
    sql_part_tables = sql.sql_part_tables
    if get_column_exists(df_column_exists, 'DBA_PART_TABLES', 'AUTOLIST') == "Y":
        sql_part_tables = sql_part_tables.replace("CAST('NO' AS VARCHAR2(3)) AS autolist", "pt.autolist")
    if get_column_exists(df_column_exists, 'DBA_PART_TABLES', 'AUTOLIST_SUBPARTITION') == "Y":
        sql_part_tables = sql_part_tables.replace("CAST('NO' AS VARCHAR2(3)) AS autolist_subpartition",
                                                  "pt.autolist_subpartition")
    return pd.read_sql_query(sql_part_tables, engine, params={'schema_name': schema_name})


def get_df_part_key_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_part_key_columns, engine, params={'schema_name': schema_name})


def get_df_comments(engine, schema_name):
    return pd.read_sql_query(sql.sql_comments, engine, params={'schema_name': schema_name})


def get_df_tab_partitions(engine, schema_name):
    return pd.read_sql_query(sql.sql_tab_partitions, engine, params={'schema_name': schema_name})


def get_df_indexes(engine, schema_name):
    return pd.read_sql_query(sql.sql_indexes, engine, params={'schema_name': schema_name})


def get_df_index_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_index_columns, engine, params={'schema_name': schema_name})


def get_df_constraints(engine, schema_name):
    return pd.read_sql_query(sql.sql_constraints, engine, params={'schema_name': schema_name})


def get_df_constraint_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_constraint_columns, engine, params={'schema_name': schema_name})


def get_df_grants(engine, schema_name):
    return pd.read_sql_query(sql.sql_grants, engine, params={'schema_name': schema_name})


def get_df_column_exists(engine):
    return pd.read_sql_query(sql.sql_column_exists, engine)


def get_db_metadata(schema_name):
    engine = get_db_engine()
    df_column_exists = get_df_column_exists(engine)
    metadata = {"tables": get_df_tables(engine, schema_name, df_column_exists),
                "tab_columns": get_df_tab_columns(engine, schema_name, df_column_exists),
                "part_tables": get_df_part_tables(engine, schema_name, df_column_exists),
                "part_key_columns": get_df_part_key_columns(engine, schema_name),
                "tab_partitions": get_df_tab_partitions(engine, schema_name),
                "comments": get_df_comments(engine, schema_name),
                "indexes": get_df_indexes(engine, schema_name),
                "index_columns": get_df_index_columns(engine, schema_name),
                "constraints": get_df_constraints(engine, schema_name),
                "constraint_columns": get_df_constraint_columns(engine, schema_name),
                "grants": get_df_grants(engine, schema_name)}
    engine.dispose()
    return metadata
