"""Tests for column existence check functionality."""

# pylint: disable=redefined-outer-name
import pandas as pd
import pytest

from db_metadata import column_exists_in_view


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
        column_exists_in_view(
            df_test_columns, "DBA_TABLES", "NON_EXISTENT_COLUMN"
        )


def test_case_sensitivity(df_test_columns):
    """Test case sensitivity of view and column names."""
    result = column_exists_in_view(df_test_columns, "dba_tables", "Column1")
    assert result is True
