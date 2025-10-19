"""Unit tests for pyddl_oracle.column.Column."""

from types import SimpleNamespace

import pytest

from pyddl_oracle.column import Column
from pyddl_oracle.config import config as c


@pytest.fixture(autouse=True)
def set_config_defaults():
    """Ensure config has required case settings for formatting."""
    c.conf = {"case": {"keyword": "uppercase", "identifier": "uppercase"}}


def make_row(**overrides):
    """Create a minimal row object with sensible defaults for Column."""
    defaults = dict(
        column_name="COL",
        data_type="VARCHAR2",
        data_length=10,
        data_precision=None,
        data_scale=0,
        data_type_owner=None,
        char_used="C",  # C = CHAR semantics, B = BYTE semantics
        hidden_column="NO",
        collation=None,
        data_default=None,
        virtual_column="NO",
        default_on_null="NO",
        nullable="Y",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_get_name_padding_uppercase():
    row = make_row(column_name="AMOUNT")
    col = Column(row, max_column_name_length=len("AMOUNT"))
    assert col.get_name() == "AMOUNT"


def test_get_name_quotes_for_mixedcase():
    row = make_row(column_name="Amount")
    # formatted becomes "Amount" and should be padded to length 10
    col = Column(row, max_column_name_length=10)
    assert col.get_name() == '"Amount"'.ljust(10)


def test_number_with_precision_and_scale():
    row = make_row(data_type="NUMBER", data_precision=12, data_scale=3)
    col = Column(row, 3)
    assert col.get_data_type() == "NUMBER(12,3)"


def test_number_with_precision_only():
    row = make_row(data_type="NUMBER", data_precision=8, data_scale=0)
    col = Column(row, 3)
    assert col.get_data_type() == "NUMBER(8)"


def test_number_integer_when_no_precision_and_zero_scale():
    row = make_row(data_type="NUMBER", data_precision=None, data_scale=0)
    col = Column(row, 3)
    assert col.get_data_type() == "INTEGER"


@pytest.mark.parametrize(
    "dtype,char_used,expected",
    [
        ("CHAR", "B", "CHAR(10 BYTE)"),
        ("CHAR", "C", "CHAR(10 CHAR)"),
        ("VARCHAR", "B", "VARCHAR(10 BYTE)"),
        ("VARCHAR2", "C", "VARCHAR2(10 CHAR)"),
        ("NVARCHAR", "C", "NVARCHAR(10 CHAR)"),
    ],
)
def test_char_and_varchar_variants(dtype, char_used, expected):
    row = make_row(data_type=dtype, data_length=10, char_used=char_used)
    col = Column(row, 3)
    assert col.get_data_type() == expected


@pytest.mark.parametrize(
    "dtype,expected",
    [("UROWID", "UROWID(16)"), ("RAW", "RAW(16)"), ("NCHAR", "NCHAR(16)"), ("NVARCHAR2", "NVARCHAR2(16)")],
)
def test_length_only_variants(dtype, expected):
    row = make_row(data_type=dtype, data_length=16)
    col = Column(row, 3)
    assert col.get_data_type() == expected


def test_float_with_precision():
    row = make_row(data_type="FLOAT", data_precision=63)
    col = Column(row, 3)
    assert col.get_data_type() == "FLOAT(63)"


def test_data_type_with_owner_qualified():
    row = make_row(data_type="MY_TYPE", data_type_owner="MY_SCHEMA")
    col = Column(row, 3)
    assert col.get_data_type() == "MY_SCHEMA.MY_TYPE"


def test_invisible_yes():
    row = make_row(hidden_column="YES")
    col = Column(row, 3)
    assert col.get_invisible() == " INVISIBLE"


def test_invisible_no():
    row = make_row(hidden_column="NO")
    col = Column(row, 3)
    assert col.get_invisible() == ""


def test_collation_present():
    row = make_row(collation="BINARY_CI")
    col = Column(row, 3)
    assert col.get_collation() == " COLLATE BINARY_CI"


def test_collation_ignored_for_using_nls_comp():
    row = make_row(collation="USING_NLS_COMP")
    col = Column(row, 3)
    assert col.get_collation() == ""


def test_default_generated_always_virtual():
    row = make_row(
        data_default="LOWER('X')", virtual_column="YES", default_on_null="NO"
    )
    col = Column(row, 3)
    assert col.get_default() == " GENERATED ALWAYS AS (LOWER('X'))"


def test_default_on_null():
    row = make_row(data_default="42", default_on_null="YES")
    col = Column(row, 3)
    assert col.get_default() == " DEFAULT ON NULL 42"


def test_default_plain():
    row = make_row(data_default="SYSDATE")
    col = Column(row, 3)
    assert col.get_default() == " DEFAULT SYSDATE"


def test_not_null_flag():
    row = make_row(nullable="N")
    col = Column(row, 3)
    assert col.get_not_null() == " NOT NULL"


def test_get_ddl_full_assembly():
    row = make_row(
        column_name="AMOUNT",
        data_type="NUMBER",
        data_precision=12,
        data_scale=2,
        hidden_column="YES",
        collation="BINARY_CI",
        data_default="0",
        nullable="N",
    )
    col = Column(row, max_column_name_length=len("AMOUNT"))
    # 4 spaces indentation + name + two spaces + data type + clauses
    assert (
        col.get_ddl()
        == "    AMOUNT  NUMBER(12,2) INVISIBLE COLLATE BINARY_CI DEFAULT 0 NOT NULL"
    )


