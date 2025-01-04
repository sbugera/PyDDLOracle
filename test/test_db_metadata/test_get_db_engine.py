"""Tests for database engine creation functionality."""

from unittest.mock import patch
from sqlalchemy import Engine

from db_metadata import get_db_engine
from utils import conf_con


def test_with_service_name():
    """Test engine creation using service name connection."""
    with patch.dict(
        conf_con,
        {
            "database": {
                "username": "test_user",
                "password": "test_pass",
                "host": "localhost",
                "port": "1521",
                "service_name": "test_service",
            }
        },
    ):
        engine = get_db_engine()
        assert isinstance(engine, Engine)
        assert "service_name=test_service" in str(engine.url)
        engine.dispose()


def test_with_sid():
    """Test engine creation using SID connection."""
    with patch.dict(
        conf_con,
        {
            "database": {
                "username": "test_user",
                "password": "test_pass",
                "host": "localhost",
                "port": "1521",
                "sid": "test_sid",
            }
        },
    ):
        engine = get_db_engine()
        assert isinstance(engine, Engine)
        assert "test_sid" in str(engine.url)
        engine.dispose()


def test_connection_string_format():
    """Test correct format of connection string."""
    with patch.dict(
        conf_con,
        {
            "database": {
                "username": "test_user",
                "password": "test_pass",
                "host": "localhost",
                "port": "1521",
                "service_name": "test_service",
            }
        },
    ):
        engine = get_db_engine()
        expected = (
            "oracle+cx_oracle://test_user:***@localhost:1521/"
            "?service_name=test_service"
        )
        assert str(engine.url) == expected
        engine.dispose()


def test_arraysize_setting():
    """Test if engine is created with correct arraysize."""
    with patch.dict(
        conf_con,
        {
            "database": {
                "username": "test_user",
                "password": "test_pass",
                "host": "localhost",
                "port": "1521",
                "sid": "test_sid",
            }
        },
    ):
        engine = get_db_engine()
        assert engine.dialect.arraysize == 1000
        engine.dispose()
