"""Merged unit tests for db metadata and related helpers."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from sqlalchemy import Engine

from pyddl_oracle import sql_queries as sql
from pyddl_oracle.config import config as c
from pyddl_oracle.db_metadata import (
    DBMetadata,
    column_exists_in_view,
    get_db_engine,
    get_db_schema_name,
)


# =============================
# column_exists_in_view tests
# =============================


@pytest.fixture
def df_test_columns():
    """Fixture providing test DataFrame with column existence data."""
    return pd.DataFrame(
        {
            "view_name": ["DBA_TABLES", "DBA_TAB_COLS", "DBA_TABLES"],
            "column_name": ["COLUMN1", "COLUMN2", "COLUMN3"],
            "column_exists": ["Y", "N", "Y"],
        }
    )


def test_existing_column(df_test_columns):
    """Test when column exists in view."""
    result = column_exists_in_view(df_test_columns, "DBA_TABLES", "COLUMN1")
    assert result is True


def test_non_existing_column(df_test_columns):
    """Test when column doesn't exist in view."""
    result = column_exists_in_view(df_test_columns, "DBA_TAB_COLS", "COLUMN2")
    assert result is False


def test_missing_view(df_test_columns):
    """Test with non-existent view."""
    with pytest.raises(IndexError):
        column_exists_in_view(df_test_columns, "NON_EXISTENT_VIEW", "COLUMN1")


def test_missing_column(df_test_columns):
    """Test with non-existent column in existing view."""
    with pytest.raises(IndexError):
        column_exists_in_view(df_test_columns, "DBA_TABLES", "NON_EXISTENT_COLUMN")


def test_case_sensitivity(df_test_columns):
    """Test case sensitivity of view and column names."""
    result = column_exists_in_view(df_test_columns, "dba_tables", "Column1")
    assert result is True


# =============================
# get_db_engine tests
# =============================


def test_with_service_name():
    """Test engine creation using service name connection."""
    c.conf_con = {
        "database": {
            "username": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "1521",
            "service_name": "test_service",
        }
    }
    engine = get_db_engine()
    assert isinstance(engine, Engine)
    assert "service_name=test_service" in str(engine.url)
    engine.dispose()


def test_with_sid():
    """Test engine creation using SID connection."""
    c.conf_con = {
        "database": {
            "username": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "1521",
            "sid": "test_sid",
        }
    }
    engine = get_db_engine()
    assert isinstance(engine, Engine)
    assert "test_sid" in str(engine.url)
    engine.dispose()


def test_connection_string_format():
    """Test correct format of connection string."""
    c.conf_con = {
        "database": {
            "username": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "1521",
            "service_name": "test_service",
        }
    }
    engine = get_db_engine()
    expected = (
        "oracle+oracledb://test_user:***@localhost:1521/" "?service_name=test_service"
    )
    assert str(engine.url) == expected
    engine.dispose()


def test_arraysize_setting():
    """Test if engine is created with correct arraysize."""
    c.conf_con = {
        "database": {
            "username": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "1521",
            "sid": "test_sid",
        }
    }
    engine = get_db_engine()
    assert engine.dialect.arraysize == 1000
    engine.dispose()


# =============================
# get_db_schema_name tests
# =============================


def test_with_provided_arg():
    """Test schema name retrieval when argument is provided."""
    c.args = MagicMock(schema_name="test_schema")
    c.args.schema_name = "test_schema"
    schema_name = get_db_schema_name()
    assert schema_name == "TEST_SCHEMA"


def test_with_config():
    """Test schema name retrieval from configuration when no argument."""
    c.args = MagicMock(schema_name=None)
    c.conf_con = {"database": {"username": "db_user"}}
    schema_name = get_db_schema_name()
    assert schema_name == "DB_USER"


def test_with_mixed_case():
    """Test if mixed case schema name is properly converted."""
    c.args = MagicMock(schema_name="TeSt_ScHeMa")
    schema_name = get_db_schema_name()
    assert schema_name == "TEST_SCHEMA"
    assert schema_name.isupper()


def test_with_missing_config():
    """Test behavior when configuration is missing."""
    c.args = MagicMock(schema_name=None)
    c.conf_con = {}
    with pytest.raises(KeyError) as err:
        get_db_schema_name()
    assert str(err.value) == "'database'"


# =============================
# DBMetadata initialization tests
# =============================


@pytest.fixture
def mock_config():
    """Mock the configuration object."""
    with patch("pyddl_oracle.db_metadata.c") as mock_config:
        mock_config.conf_con = {
            "database": {
                "username": "test_user",
                "password": "test_pass",
                "host": "localhost",
                "port": "1521",
                "service_name": "test_service",
            }
        }
        mock_config.args = MagicMock()
        mock_config.args.schema_name = "test_schema"
        yield mock_config


@pytest.fixture
def mock_read_sql_query():
    """
    Replaces pd.read_sql_query with a mock that returns
    different DataFrame objects depending on the SQL query or parameters.
    """

    def _mock_side_effect(query, *args, params=None, **kwargs):
        """Inspects 'query' (and/or 'params') and returns different DataFrames."""
        if query == sql.SQL_COLUMN_EXISTS:
            return pd.DataFrame(
                {
                    "view_name": [
                        "DBA_TABLES",
                        "DBA_TAB_COLS",
                        "DBA_PART_TABLES",
                        "DBA_PART_TABLES",
                    ],
                    "column_name": [
                        "DEFAULT_COLLATION",
                        "COLLATION",
                        "AUTOLIST",
                        "AUTOLIST_SUBPARTITION",
                    ],
                    "column_exists": ["N", "Y", "Y", "N"],
                }
            )

        if query == sql.SQL_TABLES:
            if params and params.get("schema_name") == "TEST_SCHEMA":
                return pd.DataFrame(
                    {
                        "table_name": ["TABLE_1", "TABLE_2"],
                        "default_collation": [None, None],
                    }
                )
            return pd.DataFrame(
                {"table_name": ["TABLE_3"], "default_collation": [None]}
            )

        if query == sql.SQL_TAB_COLUMNS:
            return pd.DataFrame(
                {
                    "table_name": ["TABLE_1", "TABLE_2"],
                    "column_name": ["COL1", "COL2"],
                    "collation": [None, "USING_NLS_COMP"],
                }
            )

        return pd.DataFrame()

    with patch("pandas.read_sql_query", side_effect=_mock_side_effect) as mock:
        yield mock


def test_dbmetadata_initialization(mock_read_sql_query, mock_config):
    """Test if DBMetadata initializes with correct attributes."""
    dbm = DBMetadata()
    assert hasattr(dbm, "schema_name")
    assert hasattr(dbm, "engine")
    assert hasattr(dbm, "column_exists")
    assert hasattr(dbm, "tables")
    assert hasattr(dbm, "tab_columns")
    assert hasattr(dbm, "part_tables")
    assert hasattr(dbm, "part_key_columns")
    assert hasattr(dbm, "tab_partitions")
    assert hasattr(dbm, "comments")
    assert hasattr(dbm, "indexes")
    assert hasattr(dbm, "index_columns")
    assert hasattr(dbm, "constraints")
    assert hasattr(dbm, "constraint_columns")
    assert hasattr(dbm, "grants")

    assert mock_read_sql_query.call_count >= 1

    assert not dbm.column_exists.empty
    assert "view_name" in dbm.column_exists.columns
    assert "column_exists" in dbm.column_exists.columns

    assert not dbm.tables.empty
    assert "table_name" in dbm.tables.columns


