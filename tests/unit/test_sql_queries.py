"""Unit tests for SQL query string constants in pyddl_oracle.sql_queries."""

import pyddl_oracle.sql_queries as q


def assert_contains(sql: str, view_name: str):
    assert view_name in sql, f"Missing view: {view_name}"


def test_sql_column_exists():
    sql = q.SQL_COLUMN_EXISTS
    assert_contains(sql, "sys.dba_tab_cols")


def test_sql_tables():
    sql = q.SQL_TABLES
    assert_contains(sql, "sys.dba_tables")


def test_sql_tab_columns():
    sql = q.SQL_TAB_COLUMNS
    assert_contains(sql, "sys.dba_tab_cols")


def test_sql_part_key_columns():
    sql = q.SQL_PART_KEY_COLUMNS
    assert_contains(sql, "sys.dba_part_key_columns")


def test_sql_tab_partitions():
    sql = q.SQL_TAB_PARTITIONS
    assert_contains(sql, "sys.dba_tab_partitions")


def test_sql_comments():
    sql = q.SQL_COMMENTS
    assert_contains(sql, "sys.dba_tab_comments")


def test_sql_indexes():
    sql = q.SQL_INDEXES
    assert_contains(sql, "sys.dba_indexes")


def test_sql_constraints():
    sql = q.SQL_CONSTRAINTS
    assert_contains(sql, "sys.dba_constraints")


def test_sql_grants():
    sql = q.SQL_GRANTS
    assert_contains(sql, "sys.dba_tab_privs")

