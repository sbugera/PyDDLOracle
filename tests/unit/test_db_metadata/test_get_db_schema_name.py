"""Tests for database schema name retrieval functionality."""

from unittest.mock import MagicMock

import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.db_metadata import get_db_schema_name


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
