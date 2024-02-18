from sqlalchemy import create_engine
import pandas as pd
import argparse
import sql_queries as sql
from table import Table
from utils import conf_con, get_dataframe_namedtuple


pd.options.mode.chained_assignment = None  # type: ignore # default='warn'
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


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


def get_args():
    arg_parser = argparse.ArgumentParser(description='Generate DDL scripts for Oracle database objects')
    arg_parser.add_argument('--schema_name', '-s', type=str,
                            help='DB schema name for which DDL scripts need to be generated')
    return arg_parser.parse_args()


def get_df_column_exists(engine):
    return pd.read_sql_query(sql.sql_column_exists, engine)


def get_db_metadata(schema_name):
    engine = get_db_engine()
    df_column_exists = get_df_column_exists(engine)
    metadata = (get_df_tables(engine, schema_name, df_column_exists),
                get_df_tab_columns(engine, schema_name, df_column_exists),
                get_df_part_tables(engine, schema_name, df_column_exists),
                get_df_part_key_columns(engine, schema_name),
                get_df_tab_partitions(engine, schema_name),
                get_df_comments(engine, schema_name),
                get_df_indexes(engine, schema_name),
                get_df_index_columns(engine, schema_name),
                get_df_constraints(engine, schema_name),
                get_df_constraint_columns(engine, schema_name),
                get_df_grants(engine, schema_name))
    engine.dispose()
    return metadata


def get_table_dfs(table_row, metadata):
    (df_all_tab_columns,
     df_all_part_tables,
     df_all_part_key_columns,
     df_all_tab_partitions,
     df_all_comments,
     df_all_indexes,
     df_all_index_columns,
     df_all_constraints,
     df_all_constraint_columns,
     df_all_grants) = metadata

    df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table_row.table_name]
    df_part_tables = df_all_part_tables[df_all_part_tables["table_name"] == table_row.table_name]
    df_part_key_columns = df_all_part_key_columns[df_all_part_key_columns["name"] == table_row.table_name]
    df_tab_partitions = df_all_tab_partitions[df_all_tab_partitions["table_name"] == table_row.table_name]
    df_tab_comments = df_all_comments[df_all_comments["table_name"] == table_row.table_name]
    df_tab_indexes = df_all_indexes[df_all_indexes["table_name"] == table_row.table_name]
    df_tab_index_columns = df_all_index_columns[df_all_index_columns["table_name"] == table_row.table_name]
    df_tab_constraints = df_all_constraints[df_all_constraints["table_name"] == table_row.table_name]
    df_tab_constraint_columns = df_all_constraint_columns[
        df_all_constraint_columns["table_name"] == table_row.table_name
    ]
    df_tab_grants = df_all_grants[df_all_grants["table_name"] == table_row.table_name]
    part_table_row = get_dataframe_namedtuple(df_part_tables, 0)

    return (table_row,
            part_table_row,
            df_tab_columns,
            df_tab_comments,
            df_part_key_columns,
            df_tab_partitions,
            df_tab_indexes,
            df_tab_index_columns,
            df_tab_constraints,
            df_tab_constraint_columns,
            df_tab_grants)


if __name__ == "__main__":
    args = get_args()

    db_schema_name = get_db_schema_name(args.schema_name)
    df_tables, *db_metadata = get_db_metadata(db_schema_name)

    for db_table_row in df_tables.itertuples():
        print(db_table_row.table_name)
        tabel_dfs = get_table_dfs(db_table_row, db_metadata)
        table = Table(*tabel_dfs)
        table.generate_ddl()
        table.store_ddl_into_file()
