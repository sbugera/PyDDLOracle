"""Test cases for DBMetadata class initialization."""

from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from db_metadata import DBMetadata
import sql_queries as sql

# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument


@pytest.fixture
def mock_config():
    """Mock the configuration object."""
    with patch("db_metadata.c") as mock_config:
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
                        "default_collation": [None, None],  # or real data
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
