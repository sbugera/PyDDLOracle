"""Unit tests for pyddl_oracle.partitioning.Partitioning."""

from types import SimpleNamespace

import pandas as pd
import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.partitioning import Partitioning


@pytest.fixture(autouse=True)
def set_config_defaults():
    c.conf = {
        "case": {"keyword": "uppercase", "identifier": "uppercase"},
        "storage": {"partitions": "all", "storage": "with_storage"},
    }


def df_key_cols(*names):
    return pd.DataFrame({"column_name": list(names)})


def df_partitions(rows):
    return pd.DataFrame(rows)


def make_part_table(**overrides):
    defaults = dict(partitioning_type="RANGE", interval=None, autolist="NO")
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_get_list_of_key_columns_uppercase():
    part = Partitioning(
        make_part_table(), df_key_cols("COL1", "COL2"), df_partitions([])
    )
    assert part.get_list_of_key_columns() == "COL1, COL2"


def test_partitions_none_returns_empty():
    c.conf["storage"]["partitions"] = "none"
    part = Partitioning(
        make_part_table(), df_key_cols("COL"), df_partitions([])
    )
    assert part.get_partitioning() == ""


def test_range_all_no_interval_includes_all_partitions(monkeypatch):
    class FakePartition:
        def __init__(self, partitioning_type, tab_partition):
            self.name = tab_partition.partition_name

        def get_partition(self):
            return f"\n  PART {self.name}"

    monkeypatch.setattr("pyddl_oracle.partitioning.Partition", FakePartition)

    part = Partitioning(
        make_part_table(partitioning_type="RANGE", interval=None),
        df_key_cols("KEY1"),
        df_partitions(
            [
                {"partition_name": "P1", "partition_position": 1},
                {"partition_name": "P2", "partition_position": 2},
            ]
        ),
    )
    ddl = part.get_partitioning()
    assert "PARTITION BY RANGE (KEY1)" in ddl
    assert "\n(" in ddl and ddl.rstrip().endswith(")")
    assert "PART P1" in ddl and "PART P2" in ddl


def test_list_with_interval_and_automatic(monkeypatch):
    class FakePartition:
        def __init__(self, partitioning_type, tab_partition):
            self.name = tab_partition.partition_name

        def get_partition(self):
            return f"\n  PART {self.name}"

    monkeypatch.setattr("pyddl_oracle.partitioning.Partition", FakePartition)

    part = Partitioning(
        make_part_table(
            partitioning_type="LIST",
            interval="NUMTOYMINTERVAL(1,'MONTH')",
            autolist="YES",
        ),
        df_key_cols("K"),
        df_partitions([{"partition_name": "P1", "partition_position": 1}]),
    )
    ddl = part.get_partitioning()
    assert "PARTITION BY LIST (K)" in ddl
    assert "INTERVAL (NUMTOYMINTERVAL(1,'MONTH'))" in ddl
    assert " AUTOMATIC" in ddl
    assert "PART P1" in ddl


def test_compact_with_interval_keeps_only_first(monkeypatch):
    c.conf["storage"]["partitions"] = "compact"

    class FakePartition:
        def __init__(self, partitioning_type, tab_partition):
            self.name = tab_partition.partition_name

        def get_partition(self):
            return f"\n  PART {self.name}"

    monkeypatch.setattr("pyddl_oracle.partitioning.Partition", FakePartition)

    part = Partitioning(
        make_part_table(partitioning_type="RANGE", interval="SOME_INTERVAL"),
        df_key_cols("K1"),
        df_partitions(
            [
                {"partition_name": "P1", "partition_position": 1},
                {"partition_name": "P2", "partition_position": 2},
            ]
        ),
    )
    ddl = part.get_partitioning()
    assert "PART P1" in ddl and "PART P2" not in ddl


def test_compact_skips_sys_p_after_first(monkeypatch):
    c.conf["storage"]["partitions"] = "compact"

    class FakePartition:
        def __init__(self, partitioning_type, tab_partition):
            self.name = tab_partition.partition_name

        def get_partition(self):
            return f"\n  PART {self.name}"

    monkeypatch.setattr("pyddl_oracle.partitioning.Partition", FakePartition)

    part = Partitioning(
        make_part_table(partitioning_type="RANGE", interval=None),
        df_key_cols("K"),
        df_partitions(
            [
                {"partition_name": "P1", "partition_position": 1},
                {"partition_name": "SYS_P123", "partition_position": 2},
                {"partition_name": "P3", "partition_position": 3},
            ]
        ),
    )
    ddl = part.get_partitioning()
    assert "PART P1" in ddl and "SYS_P123" not in ddl and "PART P3" not in ddl


def test_hash_partitions_with_store_in_tablespaces():
    c.conf["storage"]["partitions"] = "all"
    # ensure either of these triggers STORE IN
    c.conf["storage"]["storage"] = "only_tablespace"

    part = Partitioning(
        make_part_table(partitioning_type="HASH"),
        df_key_cols("HKEY"),
        df_partitions(
            [
                {"tablespace_name": "TS1"},
                {"tablespace_name": "TS2"},
                {"tablespace_name": "TS3"},
            ]
        ),
    )
    ddl = part.get_partitioning()
    assert "PARTITION BY HASH (HKEY)" in ddl
    assert "PARTITIONS 3" in ddl
    assert "STORE IN (TS1, TS2, TS3)" in ddl


