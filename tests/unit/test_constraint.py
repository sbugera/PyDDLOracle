"""Unit tests for pyddl_oracle.constraint.Constraint and helpers."""

from types import SimpleNamespace

import pandas as pd
import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.constraint import Constraint, get_foreign_key_dfs


@pytest.fixture(autouse=True)
def set_config_defaults():
    """Ensure config has required settings for formatting and prompts."""
    c.conf = {
        "case": {"keyword": "uppercase", "identifier": "uppercase"},
        "prompts": "yes",
        "file_path": {
            # Not used directly except in store_ddl test (patched there)
            "foreign_key": "./ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql",
        },
    }


def make_constraint_row(**overrides):
    """Create a minimal constraint row object with sensible defaults."""
    defaults = dict(
        owner="SCHEMA",
        table_name="T",
        constraint_name="CN",
        constraint_type="P",
        search_condition="",
        status="ENABLED",
        deferrable="NOT DEFERRABLE",
        deferred="IMMEDIATE",
        validated="VALIDATED",
        index_owner="SCHEMA",
        index_name=None,
        r_owner=None,
        r_table_name=None,
        r_constraint_name=None,
        delete_rule="NO ACTION",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def df_cols(*names):
    return pd.DataFrame({"column_name": list(names)})


def test_get_constraint_primary_key_with_index_and_flags():
    row = make_constraint_row(
        constraint_type="P",
        index_name="IDX_PK",
        deferrable="DEFERRABLE",
        deferred="DEFERRED",
        status="ENABLED",
        validated="VALIDATED",
    )
    cons = Constraint(row, constraint_columns=df_cols("C1", "C2"))
    ddl = cons.get_constraint(standalone=False)
    assert "CONSTRAINT CN" in ddl
    assert "PRIMARY KEY (C1, C2)" in ddl
    assert "USING INDEX SCHEMA.IDX_PK" in ddl
    assert "DEFERRABLE INITIALLY DEFERRED" in ddl
    assert ddl.strip().endswith("ENABLE VALIDATE")


def test_get_constraint_unique_no_index_disabled_novalidate():
    row = make_constraint_row(
        constraint_type="U",
        status="DISABLED",
        validated="NOT VALIDATED",
    )
    cons = Constraint(row, constraint_columns=df_cols("U1"))
    ddl = cons.get_constraint()
    assert "UNIQUE (U1)" in ddl
    assert ddl.strip().endswith("DISABLE NOVALIDATE")


def test_get_constraint_check_uses_search_condition():
    row = make_constraint_row(constraint_type="C", search_condition="X > 0")
    cons = Constraint(row, constraint_columns=df_cols("IGNORED"))
    ddl = cons.get_constraint()
    assert "CHECK (X > 0)" in ddl


def test_get_constraint_foreign_key_with_ref_columns_delete_rule_and_index():
    row = make_constraint_row(
        constraint_type="R",
        r_owner="SCHEMA2",
        r_table_name="T2",
        index_name="IDX_FK",
        delete_rule="CASCADE",
    )
    cons = Constraint(
        row,
        constraint_columns=df_cols("C1", "C2"),
        constraint_columns_remote=df_cols("R1", "R2"),
    )
    ddl = cons.get_constraint()
    assert "FOREIGN KEY (C1, C2)" in ddl
    assert "REFERENCES SCHEMA2.T2 (R1, R2)" in ddl
    assert "USING INDEX SCHEMA.IDX_FK" in ddl
    assert "ON DELETE CASCADE" in ddl


def test_get_constraint_with_standalone_preamble():
    row = make_constraint_row(constraint_type="U")
    cons = Constraint(row, constraint_columns=df_cols("U1"))
    ddl = cons.get_constraint(standalone=True)
    assert ddl.startswith("ALTER TABLE SCHEMA.T ADD (")
    assert "UNIQUE (U1)" in ddl


def test_generate_ddl_adds_prompt_and_closes_paren():
    row = make_constraint_row(constraint_type="U")
    cons = Constraint(row, constraint_columns=df_cols("U1"))
    cons.generate_ddl()
    assert cons.ddl.startswith("PROMPT Foreign key SCHEMA.CN\n")
    assert cons.ddl.rstrip().endswith(");")


def test_store_ddl_into_file_writes(tmp_path, monkeypatch):
    target_file = tmp_path / "fk.sql"

    def fake_get_file_path(object_type, owner, name):
        return str(target_file)

    def fake_prepare_directories(_path):
        return None

    monkeypatch.setattr(
        "pyddl_oracle.constraint.get_file_path", fake_get_file_path
    )
    monkeypatch.setattr(
        "pyddl_oracle.constraint.prepare_directories",
        fake_prepare_directories,
    )

    row = make_constraint_row(constraint_type="U")
    cons = Constraint(row, constraint_columns=df_cols("U1"))
    cons.ddl = "SOME DDL CONTENT"  # pre-set content
    cons.store_ddl_into_file()

    assert target_file.exists()
    assert target_file.read_text(encoding="utf-8") == "SOME DDL CONTENT"


def test_get_foreign_key_dfs_filters_rows():
    fk_row = SimpleNamespace(
        constraint_name="FK1", owner="SCHEMA", r_constraint_name="PK2", r_owner="SCHEMA2"
    )
    metadata = SimpleNamespace(
        constraint_columns=pd.DataFrame(
            {
                "constraint_name": ["FK1", "FK1", "PK2", "PK2", "OTHER"],
                "owner": ["SCHEMA", "SCHEMA", "SCHEMA2", "SCHEMA2", "SCHEMA"],
                "column_name": ["C1", "C2", "R1", "R2", "X"],
            }
        )
    )

    fk_row_out, df_fk_cols, df_remote_cols = get_foreign_key_dfs(
        fk_row, metadata
    )
    assert fk_row_out is fk_row
    assert list(df_fk_cols["column_name"]) == ["C1", "C2"]
    assert list(df_remote_cols["column_name"]) == ["R1", "R2"]


