"""Handles Oracle database metadata and DDL generation."""

import pandas as pd
from sqlalchemy import create_engine

import sql_queries as sql
from config import config as c


def get_db_schema_name() -> str:
    """Return DB schema name in uppercase."""
    if c.args.schema_name:
        schema_name = c.args.schema_name.upper()
    else:
        schema_name = c.conf_con["database"]["username"].upper()
    return schema_name


def get_db_engine():
    """Create and return a SQLAlchemy Engine for Oracle.

    Uses service_name if present; otherwise falls back to SID.
    """
    db_username = c.conf_con["database"]["username"]
    db_password = c.conf_con["database"]["password"]
    db_host = c.conf_con["database"]["host"]
    db_port = c.conf_con["database"]["port"]

    connection_string = "oracle+oracledb://"
    try:
        db_service_name = c.conf_con["database"]["service_name"]
        connection_string += (
            f"{db_username}:{db_password}@{db_host}:{db_port}/?service_name={db_service_name}"
        )
    except KeyError:
        db_sid = c.conf_con["database"]["sid"]
        connection_string += f"{db_username}:{db_password}@{db_host}:{db_port}/{db_sid}"

    return create_engine(connection_string, arraysize=1000)


def column_exists_in_view(
    column_exists_df: pd.DataFrame, view_name: str, column_name: str
) -> bool:
    """Check if a column exists in a given DBA view.

    Raises IndexError when the (view_name, column_name) pair is not found.
    """
    exists_value = column_exists_df.loc[
        (column_exists_df["view_name"] == view_name.upper())
        & (column_exists_df["column_name"] == column_name.upper()),
        "column_exists",
    ].values[0]
    return exists_value == "Y"


class DBMetadata:
    """Class to handle Oracle database metadata."""

    def __init__(self):
        self.schema_name = get_db_schema_name()
        self.engine = get_db_engine()
        self.column_exists = None

        # Database metadata attributes
        self.tables = None
        self.tab_columns = None
        self.part_tables = None
        self.part_key_columns = None
        self.tab_partitions = None
        self.comments = None
        self.indexes = None
        self.index_columns = None
        self.constraints = None
        self.constraint_columns = None
        self.grants = None

        self._get_db_metadata()
        self.engine.dispose()

    def __del__(self):
        self.engine.dispose()


    def _get_column_exists(self):
        """Returns DataFrame with column exists metadata."""
        return pd.read_sql_query(sql.SQL_COLUMN_EXISTS, self.engine)

    def _get_tables(self):
        """Returns DataFrame with tables metadata."""
        sql_tables = sql.SQL_TABLES
        if column_exists_in_view(self.column_exists, "DBA_TABLES", "DEFAULT_COLLATION"):
            sql_tables = sql_tables.replace(
                "CAST(NULL AS VARCHAR2(100)) AS default_collation",
                "t.default_collation",
            )
        return pd.read_sql_query(
            sql_tables, self.engine, params={"schema_name": self.schema_name}
        )

    def _get_tab_columns(self):
        """Returns DataFrame with columns metadata."""
        sql_tab_columns = sql.SQL_TAB_COLUMNS
        if column_exists_in_view(self.column_exists, "DBA_TAB_COLS", "COLLATION"):
            sql_tab_columns = sql_tab_columns.replace(
                "CAST(NULL AS VARCHAR2(100)) AS collation", "c.collation"
            )
        return pd.read_sql_query(
            sql_tab_columns,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_part_tables(self):
        """Returns DataFrame with partitioned tables metadata."""
        sql_part_tables = sql.SQL_PART_TABLES
        if column_exists_in_view(self.column_exists, "DBA_PART_TABLES", "AUTOLIST"):
            sql_part_tables = sql_part_tables.replace(
                "CAST('NO' AS VARCHAR2(3)) AS autolist", "pt.autolist"
            )
        if column_exists_in_view(self.column_exists, "DBA_PART_TABLES", "AUTOLIST_SUBPARTITION"):
            sql_part_tables = sql_part_tables.replace(
                "CAST('NO' AS VARCHAR2(3)) AS autolist_subpartition",
                "pt.autolist_subpartition",
            )
        return pd.read_sql_query(
            sql_part_tables,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_part_key_columns(self):
        """Returns DataFrame with partition key columns metadata."""
        return pd.read_sql_query(
            sql.SQL_PART_KEY_COLUMNS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_tab_partitions(self):
        """Returns DataFrame with table partitions metadata."""
        return pd.read_sql_query(
            sql.SQL_TAB_PARTITIONS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_comments(self):
        """Returns DataFrame with comments metadata."""
        return pd.read_sql_query(
            sql.SQL_COMMENTS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_indexes(self):
        """Returns DataFrame with indexes metadata."""
        return pd.read_sql_query(
            sql.SQL_INDEXES,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_index_columns(self):
        """Returns DataFrame with index columns metadata."""
        return pd.read_sql_query(
            sql.SQL_INDEX_COLUMNS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_constraints(self):
        """Returns DataFrame with constraints metadata."""
        return pd.read_sql_query(
            sql.SQL_CONSTRAINTS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_constraint_columns(self):
        """Returns DataFrame with constraint columns metadata."""
        return pd.read_sql_query(
            sql.SQL_CONSTRAINT_COLUMNS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_grants(self):
        """Returns DataFrame with grants metadata."""
        return pd.read_sql_query(
            sql.SQL_GRANTS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _get_db_metadata(self):
        """Returns dict with all database metadata DataFrames."""
        self.column_exists = self._get_column_exists()
        self.tables = self._get_tables()
        self.tab_columns = self._get_tab_columns()
        self.part_tables = self._get_part_tables()
        self.part_key_columns = self._get_part_key_columns()
        self.tab_partitions = self._get_tab_partitions()
        self.comments = self._get_comments()
        self.indexes = self._get_indexes()
        self.index_columns = self._get_index_columns()
        self.constraints = self._get_constraints()
        self.constraint_columns = self._get_constraint_columns()
        self.grants = self._get_grants()
