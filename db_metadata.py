"""Handles Oracle database metadata and DDL generation."""

import pandas as pd
from sqlalchemy import create_engine

import sql_queries as sql
from utils import conf_con


def get_db_engine():
    """Returns SQLAlchemy engine for Oracle database."""
    db_username = conf_con["database"]["username"]
    db_password = conf_con["database"]["password"]
    db_host = conf_con["database"]["host"]
    db_port = conf_con["database"]["port"]
    connection_string = "oracle+cx_oracle://"
    try:
        db_service_name = conf_con["database"]["service_name"]
        connection_string += (
            f"{db_username}:{db_password}@{db_host}:{db_port}"
            f"/?service_name={db_service_name}"
        )
    except KeyError:
        db_sid = conf_con["database"]["sid"]
        connection_string += (
            f"{db_username}:{db_password}@{db_host}:{db_port}/{db_sid}"
        )
    return create_engine(connection_string, arraysize=1000)


def get_db_schema_name(arg_schema_name=None):
    """Returns DB schema name for which DDL scripts need to be generated."""
    if arg_schema_name:
        username = arg_schema_name.upper()
    else:
        username = conf_con["database"]["username"].upper()
    return username


def get_column_exists(df_column_exists, view_name, column_name):
    """Checks if a column exists in a view."""
    return df_column_exists.loc[
        (df_column_exists["view_name"] == view_name)
        & (df_column_exists["column_name"] == column_name),
        "column_exists",
    ].values[0]


def get_df_tables(engine, schema_name, df_column_exists):
    """Returns DataFrame with tables metadata."""
    sql_tables = sql.SQL_TABLES
    if (
        get_column_exists(df_column_exists, "DBA_TABLES", "DEFAULT_COLLATION")
        == "Y"
    ):
        sql_tables = sql_tables.replace(
            "CAST(NULL AS VARCHAR2(100)) AS default_collation",
            "t.default_collation",
        )
    return pd.read_sql_query(
        sql_tables, engine, params={"schema_name": schema_name}
    )


def get_df_tab_columns(engine, schema_name, df_column_exists):
    """Returns DataFrame with columns metadata."""
    sql_tab_columns = sql.SQL_TAB_COLUMNS
    if get_column_exists(df_column_exists, "DBA_TAB_COLS", "COLLATION") == "Y":
        sql_tab_columns = sql_tab_columns.replace(
            "CAST(NULL AS VARCHAR2(100)) AS collation", "c.collation"
        )
    return pd.read_sql_query(
        sql_tab_columns, engine, params={"schema_name": schema_name}
    )


def get_df_part_tables(engine, schema_name, df_column_exists):
    """Returns DataFrame with partitioned tables metadata."""
    sql_part_tables = sql.SQL_PART_TABLES
    if (
        get_column_exists(df_column_exists, "DBA_PART_TABLES", "AUTOLIST")
        == "Y"
    ):
        sql_part_tables = sql_part_tables.replace(
            "CAST('NO' AS VARCHAR2(3)) AS autolist", "pt.autolist"
        )
    if (
        get_column_exists(
            df_column_exists, "DBA_PART_TABLES", "AUTOLIST_SUBPARTITION"
        )
        == "Y"
    ):
        sql_part_tables = sql_part_tables.replace(
            "CAST('NO' AS VARCHAR2(3)) AS autolist_subpartition",
            "pt.autolist_subpartition",
        )
    return pd.read_sql_query(
        sql_part_tables, engine, params={"schema_name": schema_name}
    )


def get_df_part_key_columns(engine, schema_name):
    """Returns DataFrame with partition key columns metadata."""
    return pd.read_sql_query(
        sql.SQL_PART_KEY_COLUMNS, engine, params={"schema_name": schema_name}
    )


def get_df_comments(engine, schema_name):
    """Returns DataFrame with comments metadata."""
    return pd.read_sql_query(
        sql.SQL_COMMENTS, engine, params={"schema_name": schema_name}
    )


def get_df_tab_partitions(engine, schema_name):
    """Returns DataFrame with table partitions metadata."""
    return pd.read_sql_query(
        sql.SQL_TAB_PARTITIONS, engine, params={"schema_name": schema_name}
    )


def get_df_indexes(engine, schema_name):
    """Returns DataFrame with indexes metadata."""
    return pd.read_sql_query(
        sql.SQL_INDEXES, engine, params={"schema_name": schema_name}
    )


def get_df_index_columns(engine, schema_name):
    """Returns DataFrame with index columns metadata."""
    return pd.read_sql_query(
        sql.SQL_INDEX_COLUMNS, engine, params={"schema_name": schema_name}
    )


def get_df_constraints(engine, schema_name):
    """Returns DataFrame with constraints metadata."""
    return pd.read_sql_query(
        sql.SQL_CONSTRAINTS, engine, params={"schema_name": schema_name}
    )


def get_df_constraint_columns(engine, schema_name):
    """Returns DataFrame with constraint columns metadata."""
    return pd.read_sql_query(
        sql.SQL_CONSTRAINT_COLUMNS, engine, params={"schema_name": schema_name}
    )


def get_df_grants(engine, schema_name):
    """Returns DataFrame with grants metadata."""
    return pd.read_sql_query(
        sql.SQL_GRANTS, engine, params={"schema_name": schema_name}
    )


def get_df_column_exists(engine):
    """Returns DataFrame with column exists metadata."""
    return pd.read_sql_query(sql.SQL_COLUMN_EXISTS, engine)


def get_db_metadata(schema_name):
    """Returns dict with all database metadata DataFrames."""
    engine = get_db_engine()
    df_column_exists = get_df_column_exists(engine)
    metadata = {
        "tables": get_df_tables(engine, schema_name, df_column_exists),
        "tab_columns": get_df_tab_columns(
            engine, schema_name, df_column_exists
        ),
        "part_tables": get_df_part_tables(
            engine, schema_name, df_column_exists
        ),
        "part_key_columns": get_df_part_key_columns(engine, schema_name),
        "tab_partitions": get_df_tab_partitions(engine, schema_name),
        "comments": get_df_comments(engine, schema_name),
        "indexes": get_df_indexes(engine, schema_name),
        "index_columns": get_df_index_columns(engine, schema_name),
        "constraints": get_df_constraints(engine, schema_name),
        "constraint_columns": get_df_constraint_columns(engine, schema_name),
        "grants": get_df_grants(engine, schema_name),
    }
    engine.dispose()
    return metadata
