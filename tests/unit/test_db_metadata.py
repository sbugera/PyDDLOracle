"""Merged unit tests for db metadata and related helpers."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from pyddl_oracle import sql_queries as sql
from pyddl_oracle.config import config as c
from pyddl_oracle.db_metadata import DBMetadata


@pytest.fixture(autouse=True)
def reset_config():
    # Ensure a clean config between tests
    c.args = None
    c.conf = {}
    c.conf_con = {}
    yield
    c.args = None
    c.conf = {}
    c.conf_con = {}


def df_column_exists(values):
    return pd.DataFrame(
        values,
        columns=[
            "view_name",
            "column_name",
            "column_exists",
            "data_type",
            "char_length",
        ],
    )


def test_set_db_schema_name_uses_cli_over_config():
    c.args = SimpleNamespace(schema_name="my_schema")
    c.conf_con = {"database": {"username": "other"}}
    dbm = DBMetadata()
    dbm._set_db_schema_name()  # pylint: disable=protected-access
    assert dbm.schema_name == "MY_SCHEMA"


def test_set_db_schema_name_falls_back_to_username_upper():
    c.args = SimpleNamespace(schema_name=None)
    c.conf_con = {"database": {"username": "lowercase"}}
    dbm = DBMetadata()
    dbm._set_db_schema_name()  # pylint: disable=protected-access
    assert dbm.schema_name == "LOWERCASE"


@patch("pyddl_oracle.db_metadata.create_engine")
def test_engine_with_service_name(mock_create_engine: MagicMock):
    c.conf_con = {
        "database": {
            "username": "u",
            "password": "p",
            "host": "h",
            "port": 1521,
            "service_name": "XEPDB1",
        }
    }
    dbm = DBMetadata()
    eng = dbm._get_db_engine()  # pylint: disable=protected-access

    expected = "oracle+oracledb://u:p@h:1521/?service_name=XEPDB1"
    mock_create_engine.assert_called_once_with(expected, arraysize=1000)
    assert eng == mock_create_engine.return_value


@patch("pyddl_oracle.db_metadata.create_engine")
def test_engine_with_sid(mock_create_engine: MagicMock):
    c.conf_con = {
        "database": {
            "username": "u",
            "password": "p",
            "host": "h",
            "port": 1521,
            "sid": "ORCLCDB",
        }
    }
    dbm = DBMetadata()
    _ = dbm._get_db_engine()  # pylint: disable=protected-access

    expected = "oracle+oracledb://u:p@h:1521/ORCLCDB"
    mock_create_engine.assert_called_once_with(expected, arraysize=1000)


def test_column_exists_in_view_true_false_and_index_error():
    dbm = DBMetadata()
    dbm.column_exists = df_column_exists(
        [
            ["DBA_TABLES", "DEFAULT_COLLATION", "Y", None, None],
            ["DBA_TAB_COLS", "COLLATION", "N", None, None],
        ]
    )

    assert dbm._column_exists_in_view(
        "DBA_TABLES",
        "DEFAULT_COLLATION",
    )  # pylint: disable=protected-access
    assert dbm._column_exists_in_view(
        "dba_tab_cols",
        "collation",
    ) is False  # pylint: disable=protected-access

    with pytest.raises(IndexError):
        _ = dbm._column_exists_in_view(
            "DBA_PART_TABLES",
            "AUTOLIST",
        )  # pylint: disable=protected-access


@patch("pandas.read_sql_query")
def test_tables_replace_default_collation(mock_read_sql: MagicMock):
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"
    # emulate column exists containing DEFAULT_COLLATION=Y
    dbm.column_exists = df_column_exists(
        [["DBA_TABLES", "DEFAULT_COLLATION", "Y", None, None]]
    )

    dbm._set_tables()  # pylint: disable=protected-access

    # verify SQL got replaced
    args, kwargs = mock_read_sql.call_args
    sent_sql = args[0]
    assert "t.default_collation" in sent_sql
    assert kwargs["params"] == {"schema_name": "SCHEMA"}


@patch("pandas.read_sql_query")
def test_tables_keep_cast_when_not_exists(mock_read_sql: MagicMock):
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"
    dbm.column_exists = df_column_exists(
        [["DBA_TABLES", "DEFAULT_COLLATION", "N", None, None]]
    )

    dbm._set_tables()  # pylint: disable=protected-access

    args, _ = mock_read_sql.call_args
    sent_sql = args[0]
    assert "CAST(NULL AS VARCHAR2(100)) AS default_collation" in sent_sql


@patch("pandas.read_sql_query")
def test_tab_cols_replace_collation(mock_read_sql: MagicMock):
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"
    dbm.column_exists = df_column_exists(
        [["DBA_TAB_COLS", "COLLATION", "Y", None, None]]
    )

    dbm._set_tab_columns()  # pylint: disable=protected-access

    sent_sql = mock_read_sql.call_args[0][0]
    assert "c.collation" in sent_sql


@patch("pandas.read_sql_query")
def test_tab_cols_keep_cast_when_not_exists(mock_read_sql: MagicMock):
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"
    dbm.column_exists = df_column_exists(
        [["DBA_TAB_COLS", "COLLATION", "N", None, None]]
    )

    dbm._set_tab_columns()  # pylint: disable=protected-access

    sent_sql = mock_read_sql.call_args[0][0]
    assert "CAST(NULL AS VARCHAR2(100)) AS collation" in sent_sql


@patch("pandas.read_sql_query")
def test_part_tables_replace_autolist(mock_read_sql: MagicMock):
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"
    dbm.column_exists = df_column_exists(
        [
            ["DBA_PART_TABLES", "AUTOLIST", "Y", None, None],
            ["DBA_PART_TABLES", "AUTOLIST_SUBPARTITION", "Y", None, None],
        ]
    )

    dbm._set_part_tables()  # pylint: disable=protected-access

    sent_sql = mock_read_sql.call_args[0][0]
    assert "pt.autolist" in sent_sql
    assert "pt.autolist_subpartition" in sent_sql


@patch("pandas.read_sql_query")
def test_part_tables_partial_replacements(mock_read_sql: MagicMock):
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"
    dbm.column_exists = df_column_exists(
        [
            ["DBA_PART_TABLES", "AUTOLIST", "Y", None, None],
            ["DBA_PART_TABLES", "AUTOLIST_SUBPARTITION", "N", None, None],
        ]
    )

    dbm._set_part_tables()  # pylint: disable=protected-access

    sent_sql = mock_read_sql.call_args[0][0]
    assert "pt.autolist" in sent_sql
    assert (
        "CAST('NO' AS VARCHAR2(3)) AS autolist_subpartition" in sent_sql
    )


@patch("pandas.read_sql_query")
def test_setters_call_read_sql_with_params(mock_read_sql: MagicMock):
    # Sanity: other setters pass schema param and engine
    dbm = DBMetadata()
    dbm.engine = MagicMock()
    dbm.schema_name = "SCHEMA"

    mock_read_sql.return_value = pd.DataFrame()

    dbm._set_part_key_columns()  # pylint: disable=protected-access
    dbm._set_tab_partitions()  # pylint: disable=protected-access
    dbm._set_comments()  # pylint: disable=protected-access
    dbm._set_indexes()  # pylint: disable=protected-access
    dbm._set_index_columns()  # pylint: disable=protected-access
    dbm._set_constraints()  # pylint: disable=protected-access
    dbm._set_constraint_columns()  # pylint: disable=protected-access
    dbm._set_grants()  # pylint: disable=protected-access

    # Expect eight calls with params carrying schema_name
    assert mock_read_sql.call_count == 8
    for _args, kwargs in mock_read_sql.call_args_list:
        assert kwargs["params"] == {"schema_name": "SCHEMA"}


@patch("pandas.read_sql_query")
@patch("pyddl_oracle.db_metadata.create_engine")
def test_load_orchestrates_and_disposes(
    mock_ce: MagicMock, mock_read_sql: MagicMock
):
    # Arrange minimal config and column_exists to drive replacements
    c.args = SimpleNamespace(schema_name=None)
    c.conf_con = {
        "database": {
            "username": "SCHEMA",
            "password": "p",
            "host": "h",
            "port": 1521,
            "service_name": "XEPDB1",
        }
    }

    # column_exists returned on first setter
    def read_sql_side_effect(query, con, params=None):
        # avoid unused-argument lint
        _ = con, params
        if query is sql.SQL_COLUMN_EXISTS:
            return df_column_exists(
                [
                    ["DBA_TABLES", "DEFAULT_COLLATION", "N", None, None],
                    ["DBA_TAB_COLS", "COLLATION", "N", None, None],
                    ["DBA_PART_TABLES", "AUTOLIST", "N", None, None],
                    [
                        "DBA_PART_TABLES",
                        "AUTOLIST_SUBPARTITION",
                        "N",
                        None,
                        None,
                    ],
                ]
            )
        return pd.DataFrame()

    mock_read_sql.side_effect = read_sql_side_effect

    dbm = DBMetadata()
    dbm.load_db_metadata()

    # Engine created and disposed
    mock_ce.assert_called_once()
    dbm.engine.dispose.assert_called_once()  # type: ignore[attr-defined]

    # After load, get_db_metadata returns dict with DataFrames
    md = dbm.get_db_metadata()
    expected_keys = {
        "column_exists",
        "tables",
        "tab_columns",
        "part_tables",
        "part_key_columns",
        "tab_partitions",
        "comments",
        "indexes",
        "index_columns",
        "constraints",
        "constraint_columns",
        "grants",
    }
    assert set(md.keys()) == expected_keys
    for v in md.values():
        assert isinstance(v, pd.DataFrame)
