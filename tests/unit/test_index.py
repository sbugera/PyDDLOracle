"""Unit tests for pyddl_oracle.index.Index generation."""

from types import SimpleNamespace

import pandas as pd
import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.index import Index


@pytest.fixture(autouse=True)
def set_config_defaults():
    """Ensure config has required settings for formatting and storage."""
    c.conf = {
        "case": {"keyword": "uppercase", "identifier": "uppercase"},
        "prompts": "yes",
        "storage": {
            "storage": "with_storage",
            "logging": "yes",
            "compression": "yes",
        },
    }


def df_cols(*names):
    return pd.DataFrame({"column_name": list(names)})


def make_index_row(**overrides):
    defaults = dict(
        owner="SCHEMA",
        index_name="IDX",
        index_type="NORMAL",
        table_owner="SCHEMA",
        table_name="T",
        uniqueness="NONUNIQUE",
        compression="DISABLED",
        prefix_length=None,
        tablespace_name="TS",
        ini_trans=2,
        max_trans=255,
        initial_extent=0,
        next_extent=0,
        min_extents=1,
        max_extents=2147483645,
        pct_increase=0,
        pct_threshold=None,
        include_column=None,
        freelists=None,
        freelist_groups=None,
        pct_free=10,
        logging="YES",
        instances=1,
        partitioned="NO",
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
        visibility="VISIBLE",
        monitoring="NO",
        degree=1,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_prompt_and_basic_create_with_columns_and_names():
    row = make_index_row()
    idx = Index(row, index_columns=df_cols("C1", "C2"))
    ddl = idx.get_index()
    assert ddl.startswith("PROMPT Index SCHEMA.IDX\n")
    assert "CREATE INDEX SCHEMA.IDX ON SCHEMA.T\n(C1, C2)" in ddl


def test_bitmap_and_unique_flags():
    row = make_index_row(index_type="BITMAP", uniqueness="UNIQUE")
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert "CREATE BITMAP UNIQUE INDEX" in ddl


def test_logging_variants_yes_and_no():
    row_yes = make_index_row(logging="YES")
    idx_yes = Index(row_yes, index_columns=df_cols("C1"))
    ddl_yes = idx_yes.get_index()
    assert "\nLOGGING" in ddl_yes

    row_no = make_index_row(logging="NO")
    idx_no = Index(row_no, index_columns=df_cols("C1"))
    ddl_no = idx_no.get_index()
    assert "\nNOLOGGING" in ddl_no


def test_only_tablespace_when_not_partitioned(monkeypatch):
    c.conf["storage"]["storage"] = "only_tablespace"
    row = make_index_row(partitioned="NO", tablespace_name="TS1")
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert "\nTABLESPACE TS1" in ddl


def test_with_storage_calls_storage_helper(monkeypatch):
    calls = {}
    
    def fake_build(self, *_args, **_kwargs):
        calls["called"] = True
        return f"\n{self.indentation}-- STORAGE --"
    monkeypatch.setattr("pyddl_oracle.index.Storage.build", fake_build)

    c.conf["storage"]["storage"] = "with_storage"
    row = make_index_row()
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert calls.get("called") is True
    assert "-- STORAGE --" in ddl


def test_compression_enabled_with_prefix_length():
    row = make_index_row(compression="ENABLED", prefix_length=2)
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert "\nCOMPRESS 2" in ddl


def test_compression_custom_mode_string():
    row = make_index_row(compression="ADVANCED LOW")
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert "\nCOMPRESS ADVANCED LOW" in ddl


def test_partition_local_and_visibility_and_reverse():
    row = make_index_row(partitioned="YES", visibility="INVISIBLE", index_type="NORMAL/REV")
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert "\nLOCAL" in ddl
    assert "\nINVISIBLE" in ddl
    assert "\nREVERSE" in ddl


def test_parallel_clause_when_degree_gt_1():
    row = make_index_row(degree=4, instances=2)
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert "\nPARALLEL ( DEGREE 4 INSTANCES 2 )" in ddl


def test_monitoring_usage_block_appended():
    row = make_index_row(monitoring="YES")
    idx = Index(row, index_columns=df_cols("C1"))
    ddl = idx.get_index()
    assert ddl.strip().endswith("ALTER INDEX SCHEMA.IDX\n  MONITORING USAGE;")


