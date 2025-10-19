"""Unit tests for pyddl_oracle.partition.Partition generation."""

from types import SimpleNamespace

import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.partition import Partition


@pytest.fixture(autouse=True)
def set_config_defaults():
    c.conf = {
        "case": {"keyword": "uppercase", "identifier": "uppercase"},
        "storage": {
            "storage": "with_storage",
            "logging": "yes",
            "compression": "yes",
        },
    }


def make_tab_partition(**overrides):
    defaults = dict(
        partition_name="P_202401",
        high_value="TO_DATE('2024-02-01','YYYY-MM-DD')",
        partition_position=1,
        tablespace_name="TS",
        pct_free=10,
        ini_trans=2,
        max_trans=255,
        min_extent=1,
        max_extent=2147483645,
        pct_increase=0,
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
        initial_extent=0,
        next_extent=0,
        logging="YES",
        compression="DISABLED",
        compress_for="BASIC",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_range_partition_statement_and_name():
    part = Partition("RANGE", make_tab_partition(partition_name="P1"))
    ddl = part.get_partition()
    assert "PARTITION P1 VALUES LESS THAN (TO_DATE('2024-02-01'" in ddl


def test_list_partition_statement():
    part = Partition("LIST", make_tab_partition(high_value="('A','B')"))
    ddl = part.get_partition()
    assert "PARTITION P_202401 VALUES ('A','B')" in ddl


def test_partition_name_skips_sys_p_prefix():
    part = Partition("RANGE", make_tab_partition(partition_name="SYS_P12345"))
    ddl = part.get_partition()
    assert "PARTITION  VALUES LESS THAN" in ddl  # no name injected


def test_logging_yes_and_no():
    part_yes = Partition("RANGE", make_tab_partition(logging="YES"))
    ddl_yes = part_yes.get_partition()
    assert "\n    LOGGING" in ddl_yes

    part_no = Partition("RANGE", make_tab_partition(logging="NO"))
    ddl_no = part_no.get_partition()
    assert "\n    NOLOGGING" in ddl_no


def test_compression_disabled_basic_advanced():
    # disabled -> NOCOMPRESS
    part_nc = Partition("RANGE", make_tab_partition(compression="DISABLED"))
    ddl_nc = part_nc.get_partition()
    assert "\n    NOCOMPRESS" in ddl_nc

    # BASIC -> COMPRESS BASIC
    part_basic = Partition(
        "RANGE", make_tab_partition(compression="ENABLED", compress_for="BASIC")
    )
    ddl_basic = part_basic.get_partition()
    assert "\n    COMPRESS BASIC" in ddl_basic

    # ADVANCED -> COMPRESS FOR OLTP
    part_adv = Partition(
        "RANGE", make_tab_partition(compression="ENABLED", compress_for="ADVANCED")
    )
    ddl_adv = part_adv.get_partition()
    assert "\n    COMPRESS FOR OLTP" in ddl_adv


def test_only_tablespace_branch():
    c.conf["storage"]["storage"] = "only_tablespace"
    part = Partition("RANGE", make_tab_partition(tablespace_name="TS1"))
    ddl = part.get_partition()
    assert "\n    TABLESPACE TS1" in ddl


def test_with_storage_calls_helper(monkeypatch):
    calls = {}

    def fake_get_full_storage(*args, **kwargs):
        calls["called"] = True
        indent = args[0]
        return f"\n{indent}-- PART STORAGE --"

    monkeypatch.setattr(
        "pyddl_oracle.partition.get_full_storage", fake_get_full_storage
    )

    c.conf["storage"]["storage"] = "with_storage"
    part = Partition("RANGE", make_tab_partition())
    ddl = part.get_partition()
    assert calls.get("called") is True
    assert "-- PART STORAGE --" in ddl


