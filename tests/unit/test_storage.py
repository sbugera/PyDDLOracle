"""Unit tests for pyddl_oracle.storage.get_full_storage."""

import math

import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.storage import Storage


@pytest.fixture(autouse=True)
def set_config_defaults():
    c.conf = {"case": {"keyword": "uppercase", "identifier": "uppercase"}}


def test_full_storage_all_options():
    ddl = Storage(
        indentation="  ",
        tablespace_name="TS_DATA",
        pct_free=12,
        ini_trans=3,
        max_trans=255,
        min_extents=2,
        max_extents=2147483645,  # UNLIMITED
        pct_increase=50,
        buffer_pool="KEEP",
        flash_cache="KEEP",
        cell_flash_cache="KEEP",
        initial_extent=10 * 1024 * 1024,  # 10M
        next_extent=5 * 1024 * 1024,  # 5M
        local_index="NO",
    ).build()
    assert "\n  TABLESPACE TS_DATA" in ddl
    assert "\n  PCTFREE    12" in ddl
    assert "\n  INITRANS   3" in ddl
    assert "\n  MAXTRANS   255" in ddl
    assert "\n  STORAGE    (" in ddl
    assert "\n              INITIAL          10M" in ddl
    assert "\n              NEXT             5M" in ddl
    assert "\n              MINEXTENTS       2" in ddl
    assert "\n              MAXEXTENTS       UNLIMITED" in ddl
    assert "\n              PCTINCREASE      50" in ddl
    assert "\n              BUFFER_POOL      KEEP" in ddl
    assert "\n              FLASH_CACHE      KEEP" in ddl
    assert "\n              CELL_FLASH_CACHE KEEP" in ddl


def test_no_storage_output_when_all_empty_or_nan():
    ddl = Storage(
        indentation="",
        tablespace_name=math.nan,
        pct_free=math.nan,
        ini_trans=math.nan,
        max_trans=math.nan,
        min_extents=None,
        max_extents=None,
        pct_increase=None,
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
        initial_extent=None,
        next_extent=None,
        local_index="YES",  # also prevents default PCTINCREASE 0
    ).build()
    assert ddl == ""


def test_pctincrease_default_zero_when_nan_and_not_local():
    ddl = Storage(
        indentation="",
        tablespace_name="TS",
        pct_free=math.nan,
        ini_trans=math.nan,
        max_trans=math.nan,
        min_extents=None,
        max_extents=None,
        pct_increase=math.nan,
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
        initial_extent=None,
        next_extent=None,
        local_index="NO",
    ).build()
    assert "STORAGE    (" in ddl
    assert "PCTINCREASE      0" in ddl


def test_no_tablespace_when_local_index_yes():
    ddl = Storage(
        indentation="",
        tablespace_name="TS",
        pct_free=math.nan,
        ini_trans=math.nan,
        max_trans=math.nan,
        min_extents=None,
        max_extents=None,
        pct_increase=math.nan,
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
        initial_extent=None,
        next_extent=None,
        local_index="YES",
    ).build()
    assert "TABLESPACE" not in ddl
    assert "PCTINCREASE      0" not in ddl  # suppressed for local index


def test_maxextents_numeric_and_next_extent_units():
    ddl = Storage(
        indentation="",
        tablespace_name="TS",
        pct_free=math.nan,
        ini_trans=math.nan,
        max_trans=math.nan,
        min_extents=1,
        max_extents=10,
        pct_increase=None,
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
        initial_extent=None,
        next_extent=7 * 1024 * 1024,
        local_index="NO",
    ).build()
    assert "MAXEXTENTS       10" in ddl
    assert "NEXT             7M" in ddl


def test_default_values_filtered_out():
    ddl = Storage(
        indentation="",
        tablespace_name="TS",
        pct_free=10,
        ini_trans=2,
        max_trans=255,
        min_extents=-1,
        max_extents="DEFAULT",
        pct_increase="DEFAULT",
        buffer_pool="DEFAULT2",
        flash_cache="DEFAULT",
        cell_flash_cache="DEFAULT",
        initial_extent="DEFAULT",
        next_extent=-1,
        local_index="NO",
    ).build()
    assert "TABLESPACE TS" in ddl
    assert "PCTFREE" in ddl and "INITRANS" in ddl and "MAXTRANS" in ddl
    # Storage block should not include filtered defaults apart from possible PCTINCREASE 0
    assert "INITIAL" not in ddl
    assert "NEXT" not in ddl
    assert "MINEXTENTS" not in ddl
    assert "MAXEXTENTS       UNLIMITED" not in ddl
    assert "BUFFER_POOL" not in ddl
    assert "FLASH_CACHE" not in ddl
    assert "CELL_FLASH_CACHE" not in ddl


