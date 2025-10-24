"""Handles Oracle database metadata and DDL generation."""

import pandas as pd
from sqlalchemy import create_engine

from pyddl_oracle import sql_queries as sql
from pyddl_oracle.config import config as c


class DBMetadata:  # pylint: disable=too-many-instance-attributes
    """Class to handle Oracle database metadata."""

    def __init__(self):
        self.schema_name = None
        self.engine = None

        # Database metadata attributes
        self.column_exists = None
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

    def _set_db_schema_name(self) -> str:
        if c.args.schema_name:
            self.schema_name = c.args.schema_name.upper()
        else:
            self.schema_name = c.conf_con["database"]["username"].upper()

    def _get_db_engine(self):
        """Create and return a SQLAlchemy Engine for Oracle.

        Uses service_name if present; otherwise falls back to SID.
        """
        db_username = c.conf_con["database"]["username"]
        db_password = c.conf_con["database"]["password"]
        db_host = c.conf_con["database"]["host"]
        db_port = c.conf_con["database"]["port"]

        connection_string = "oracle+oracledb://"
        connection_string += f"{db_username}:{db_password}@{db_host}:{db_port}"
        try:
            db_service_name = c.conf_con["database"]["service_name"]
            connection_string += f"/?service_name={db_service_name}"
        except KeyError:
            db_sid = c.conf_con["database"]["sid"]
            connection_string += f"/{db_sid}"

        return create_engine(connection_string, arraysize=1000)

    def _column_exists_in_view(
        self, view_name: str, column_name: str
    ) -> bool:
        """Check if a column exists in a given DBA view.

        Raises IndexError when the (view_name, column_name) pair is not found.
        """
        exists_value = self.column_exists.loc[
            (self.column_exists["view_name"] == view_name.upper())
            & (self.column_exists["column_name"] == column_name.upper()),
            "column_exists",
        ].values[0]
        return exists_value == "Y"

    def _set_column_exists(self):
        """Returns DataFrame with column exists metadata."""
        self.column_exists = pd.read_sql_query(
            sql.SQL_COLUMN_EXISTS,
            self.engine,
        )

    def _set_tables(self):
        """Returns DataFrame with tables metadata."""
        sql_tables = sql.SQL_TABLES
        if self._column_exists_in_view("DBA_TABLES", "DEFAULT_COLLATION"):
            sql_tables = sql_tables.replace(
                "CAST(NULL AS VARCHAR2(100)) AS default_collation,",
                "t.default_collation,",
            )
        self.tables = pd.read_sql_query(
            sql_tables, self.engine, params={"schema_name": self.schema_name}
        )

    def _set_tab_columns(self):
        """Returns DataFrame with columns metadata."""
        sql_tab_columns = sql.SQL_TAB_COLUMNS
        if self._column_exists_in_view("DBA_TAB_COLS", "COLLATION"):
            sql_tab_columns = sql_tab_columns.replace(
                "CAST(NULL AS VARCHAR2(100)) AS collation,", "c.collation,"
            )
        self.tab_columns = pd.read_sql_query(
            sql_tab_columns,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_part_tables(self):
        """Returns DataFrame with partitioned tables metadata."""
        sql_part_tables = sql.SQL_PART_TABLES
        if self._column_exists_in_view("DBA_PART_TABLES", "AUTOLIST"):
            sql_part_tables = sql_part_tables.replace(
                "CAST('NO' AS VARCHAR2(3)) AS autolist,", "pt.autolist,"
            )
        if self._column_exists_in_view("DBA_PART_TABLES",
                                       "AUTOLIST_SUBPARTITION"):
            sql_part_tables = sql_part_tables.replace(
                "CAST('NO' AS VARCHAR2(3)) AS autolist_subpartition,",
                "pt.autolist_subpartition,",
            )
        self.part_tables = pd.read_sql_query(
            sql_part_tables,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_part_key_columns(self):
        """Returns DataFrame with partition key columns metadata."""
        self.part_key_columns = pd.read_sql_query(
            sql.SQL_PART_KEY_COLUMNS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_tab_partitions(self):
        """Returns DataFrame with table partitions metadata."""
        self.tab_partitions = pd.read_sql_query(
            sql.SQL_TAB_PARTITIONS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_comments(self):
        """Returns DataFrame with comments metadata."""
        self.comments = pd.read_sql_query(
            sql.SQL_COMMENTS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_indexes(self):
        """Returns DataFrame with indexes metadata."""
        self.indexes = pd.read_sql_query(
            sql.SQL_INDEXES,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_index_columns(self):
        """Returns DataFrame with index columns metadata."""
        self.index_columns = pd.read_sql_query(
            sql.SQL_INDEX_COLUMNS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_constraints(self):
        """Returns DataFrame with constraints metadata."""
        self.constraints = pd.read_sql_query(
            sql.SQL_CONSTRAINTS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_constraint_columns(self):
        """Returns DataFrame with constraint columns metadata."""
        self.constraint_columns = pd.read_sql_query(
            sql.SQL_CONSTRAINT_COLUMNS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def _set_grants(self):
        """Returns DataFrame with grants metadata."""
        self.grants = pd.read_sql_query(
            sql.SQL_GRANTS,
            self.engine,
            params={"schema_name": self.schema_name},
        )

    def load_db_metadata(self):
        """Loads database metadata into the class attributes."""
        self._set_db_schema_name()
        self.engine = self._get_db_engine()
        self._set_column_exists()
        self._set_tables()
        self._set_tab_columns()
        self._set_part_tables()
        self._set_part_key_columns()
        self._set_tab_partitions()
        self._set_comments()
        self._set_indexes()
        self._set_index_columns()
        self._set_constraints()
        self._set_constraint_columns()
        self._set_grants()
        self.engine.dispose()
        print(self.column_exists)

    def get_db_metadata(self):
        """Returns dict with all database metadata DataFrames."""
        return {
            "column_exists": self.column_exists,
            "tables": self.tables,
            "tab_columns": self.tab_columns,
            "part_tables": self.part_tables,
            "part_key_columns": self.part_key_columns,
            "tab_partitions": self.tab_partitions,
            "comments": self.comments,
            "indexes": self.indexes,
            "index_columns": self.index_columns,
            "constraints": self.constraints,
            "constraint_columns": self.constraint_columns,
            "grants": self.grants,
        }
