"""Unit tests for pyddl_oracle.table.Table methods and assembly."""

from types import SimpleNamespace

import pandas as pd
import pytest

from pyddl_oracle.config import config as c
from pyddl_oracle.table import Table


@pytest.fixture(autouse=True)
def set_config_defaults():
    c.conf = {
        "case": {"keyword": "uppercase", "identifier": "uppercase"},
        "storage": {
            "storage": "with_storage",
            "logging": "yes",
            "compression": "yes",
            "cache": "yes",
            "result_cache": "yes",
            "partitions": "all",
        },
        "indexes": "yes",
        "constraints": "yes",
        "comments": {"comments": "yes", "empty_line_after_comment": "no", "vertical_alignment": "no"},
        "prompts": "yes",
        "grants": "yes",
    }


def make_table_attr(**overrides):
    defaults = dict(
        owner="SCHEMA",
        table_name="TBL",
        default_collation=None,
        logging="YES",
        cache="Y",
        result_cache="DEFAULT",
        row_movement="ENABLED",
        compression="ENABLED",
        compress_for="BASIC",
        partitioned="NO",
        tablespace_name="TS",
        pct_free=10,
        ini_trans=2,
        max_trans=255,
        min_extents=1,
        max_extents=2147483645,
        pct_increase=0,
        buffer_pool=None,
        flash_cache=None,
        cell_flash_cache=None,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def make_part_table(**overrides):
    defaults = dict(
        def_tablespace_name="TS_DEF",
        def_logging="YES",
        def_compression="ENABLED",
        def_compress_for="BASIC",
        def_pct_free=10,
        def_ini_trans=2,
        def_max_trans=255,
        def_min_extents=1,
        def_max_extents=2147483645,
        def_pct_increase=0,
        def_buffer_pool=None,
        def_flash_cache=None,
        def_cell_flash_cache=None,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def make_table(
    table_attr=None,
    part_table=None,
    columns=None,
    comments=None,
    part_key_columns=None,
    tab_partitions=None,
    indexes=None,
    index_columns=None,
    tab_constraints=None,
    tab_constraint_columns=None,
    tab_grants=None,
):
    table_attr = make_table_attr() if table_attr is None else table_attr
    # part_table may be None intentionally
    if columns is None:
        columns = pd.DataFrame({"column_name": ["ID", "Amount", "AMOUNTLONG"]})
    if comments is None:
        comments = pd.DataFrame(
            {"table_name": ["TBL", "TBL"], "column_name": [None, "ID"], "comments": ["Table comment", "Id comment"]}
        )
    if part_key_columns is None:
        part_key_columns = pd.DataFrame({"column_name": []})
    if tab_partitions is None:
        tab_partitions = pd.DataFrame([])
    if indexes is None:
        indexes = pd.DataFrame([], columns=["index_name", "table_name"])
    if index_columns is None:
        index_columns = pd.DataFrame([], columns=["index_name", "column_name"])
    if tab_constraints is None:
        tab_constraints = pd.DataFrame([], columns=["constraint_name", "table_name", "constraint_type"])
    if tab_constraint_columns is None:
        tab_constraint_columns = pd.DataFrame([], columns=["constraint_name", "owner", "column_name"])
    if tab_grants is None:
        tab_grants = pd.DataFrame([], columns=["grantee", "grantable", "privilege", "table_name"])
    return Table(
        table_attr,
        part_table,
        columns,
        comments,
        part_key_columns,
        tab_partitions,
        indexes,
        index_columns,
        tab_constraints,
        tab_constraint_columns,
        tab_grants,
    )


def test_get_maximum_column_name_length_considers_quotes():
    t = make_table()
    maxlen = t.get_maximum_column_name_length()
    # "Amount" adds quotes so length 8; AMOUNTLONG is 10
    assert maxlen >= 10


def test_get_collation_included_and_ignored_cases():
    t1 = make_table(table_attr=make_table_attr(default_collation="BINARY_CI"))
    assert "DEFAULT COLLATION BINARY_CI" in t1.get_collation()

    t2 = make_table(table_attr=make_table_attr(default_collation="USING_NLS_COMP"))
    assert t2.get_collation() == ""


def test_get_storage_variants_use_full_storage(monkeypatch):
    calls = {}

    def fake_full_storage(*args, **kwargs):
        calls["called"] = True
        return "\n-- STORAGE --"

    monkeypatch.setattr("pyddl_oracle.table.get_full_storage", fake_full_storage)

    # with_storage, non-partitioned
    t = make_table()
    c.conf["storage"]["storage"] = "with_storage"
    t.partitioned = "NO"
    assert "-- STORAGE --" in t.get_storage()

    # only_tablespace, non-partitioned
    c.conf["storage"]["storage"] = "only_tablespace"
    t.partitioned = "NO"
    out = t.get_storage()
    assert "TABLESPACE TS" in out

    # only_tablespace, partitioned uses def_tablespace_name
    c.conf["storage"]["storage"] = "only_tablespace"
    t = make_table(table_attr=make_table_attr(partitioned="YES"), part_table=make_part_table(def_tablespace_name="TS_DEF"))
    out = t.get_storage()
    assert "TABLESPACE TS_DEF" in out


def test_get_logging_partition_aware():
    t = make_table()
    t.partitioned = "NO"
    t.logging = "YES"
    assert t.get_logging() == "\nLOGGING"
    t.logging = "NO"
    assert t.get_logging() == "\nNOLOGGING"
    t.partitioned = "YES"
    assert t.get_logging() == ""


def test_get_compression_partitioned_and_nonpartitioned():
    # Non-partitioned: uses table_attr.compression/compress_for
    t = make_table()
    t.partitioned = "NO"
    t.compression = "DISABLED"
    assert t.get_compression() == "\nNOCOMPRESS"
    t.compression = "ENABLED"
    t.compress_for = "BASIC"
    assert t.get_compression() == "\nCOMPRESS BASIC"
    t.compress_for = "ADVANCED"
    assert t.get_compression() == "\nCOMPRESS FOR OLTP"

    # Partitioned: uses defaults from part_table
    t = make_table(table_attr=make_table_attr(partitioned="YES"), part_table=make_part_table(def_compression="DISABLED"))
    assert t.get_compression() == "\nNOCOMPRESS"
    t = make_table(
        table_attr=make_table_attr(partitioned="YES"),
        part_table=make_part_table(def_compression="ENABLED", def_compress_for="BASIC"),
    )
    assert t.get_compression() == "\nCOMPRESS BASIC"


def test_get_cache_and_result_cache():
    t = make_table()
    t.cache = " Y "
    assert t.get_cache() == "\nCACHE"
    t.cache = "N"
    assert t.get_cache() == "\nNOCACHE"

    t.result_cache = "MANUAL"
    assert t.get_result_cache() == "\nRESULT_CACHE (MODE MANUAL)"


def test_get_row_movement():
    t = make_table()
    assert t.get_tab_row_movement() == "\nENABLE ROW MOVEMENT"


def test_get_partitioning_uses_helper(monkeypatch):
    class FakePartitioning:
        def __init__(self, *args, **kwargs):
            pass

        def get_partitioning(self):
            return "\n-- PARTITIONING --"

    monkeypatch.setattr("pyddl_oracle.table.Partitioning", FakePartitioning)

    t = make_table(table_attr=make_table_attr(partitioned="YES"))
    assert "-- PARTITIONING --" in t.get_partitioning()
    t.partitioned = "NO"
    assert t.get_partitioning() == ""


def test_get_indexes_collects_all(monkeypatch):
    class FakeIndex:
        def __init__(self, row, cols):
            self.name = row.index_name

        def get_index(self):
            return f"IDX:{self.name}\n"

    monkeypatch.setattr("pyddl_oracle.table.Index", FakeIndex)

    idx_rows = pd.DataFrame(
        {"index_name": ["I1", "I2"], "table_name": ["TBL", "TBL"]}
    )
    idx_cols = pd.DataFrame(
        {"index_name": ["I1", "I2"], "column_name": ["C1", "C2"], "table_name": ["TBL", "TBL"]}
    )
    t = make_table(indexes=idx_rows, index_columns=idx_cols)
    out = t.get_indexes()
    assert "IDX:I1" in out and "IDX:I2" in out
    assert out.endswith("\n")


def test_get_constraints_builds_block(monkeypatch):
    class FakeConstraint:
        def __init__(self, row, cols):
            self.name = row.constraint_name

        def get_constraint(self):
            return f"C:{self.name}"

    monkeypatch.setattr("pyddl_oracle.table.Constraint", FakeConstraint)

    cons_rows = pd.DataFrame(
        {
            "constraint_name": ["C1", "C2"],
            "table_name": ["TBL", "TBL"],
            "constraint_type": ["P", "U"],
        }
    )
    cons_cols = pd.DataFrame(
        {"constraint_name": ["C1", "C2"], "owner": ["SCHEMA", "SCHEMA"], "column_name": ["ID", "ID"]}
    )
    t = make_table(tab_constraints=cons_rows, tab_constraint_columns=cons_cols)
    t.table_full_name = "SCHEMA.TBL"
    out = t.get_constraints()
    assert "ALTER TABLE SCHEMA.TBL ADD (" in out
    assert "C:C1" in out and ",\nC:C2" in out
    assert out.endswith(");\n\n\n")


def test_get_comments_emits_table_and_column_comments():
    comments = pd.DataFrame(
        {"table_name": ["TBL", "TBL"], "column_name": [None, "ID"], "comments": ["Table comment", "Id comment"]}
    )
    t = make_table(comments=comments)
    t.table_full_name = "SCHEMA.TBL"
    t.max_column_name_length = 5
    out = t.get_comments()
    assert "COMMENT ON TABLE SCHEMA.TBL IS 'Table comment';" in out
    assert "COMMENT ON COLUMN SCHEMA.TBL.ID IS 'Id comment';" in out


def test_get_grants_groups_and_prompts():
    grants = pd.DataFrame(
        {
            "grantee": ["U1", "U1", "U2"],
            "grantable": ["NO", "NO", "YES"],
            "privilege": ["SELECT", "UPDATE", "INSERT"],
            "table_name": ["TBL", "TBL", "TBL"],
        }
    )
    t = make_table(tab_grants=grants)
    t.table_full_name = "SCHEMA.TBL"
    out = t.get_grants()
    # U1 gets combined SELECT, UPDATE
    assert "GRANT SELECT, UPDATE ON SCHEMA.TBL TO U1;" in out
    # U2 with grant option
    assert "GRANT INSERT ON SCHEMA.TBL TO U2 WITH GRANT OPTION;" in out


def test_generate_ddl_full_assembly(monkeypatch):
    # stub collaborators to make assembly deterministic
    class FakeColumn:
        def __init__(self, row, width):
            pass

        def get_ddl(self):
            return "    ID  NUMBER(10)\n"

    class FakePartitioning:
        def __init__(self, *args, **kwargs):
            pass

        def get_partitioning(self):
            return "\n-- PARTS --"

    class FakeIndex:
        def __init__(self, row, cols):
            pass

        def get_index(self):
            return "IDX\n"

    class FakeConstraint:
        def __init__(self, row, cols):
            pass

        def get_constraint(self):
            return "CST"

    def fake_full_storage(*args, **kwargs):
        return "\n-- STORAGE --"

    monkeypatch.setattr("pyddl_oracle.table.Column", FakeColumn)
    monkeypatch.setattr("pyddl_oracle.table.Partitioning", FakePartitioning)
    monkeypatch.setattr("pyddl_oracle.table.Index", FakeIndex)
    monkeypatch.setattr("pyddl_oracle.table.Constraint", FakeConstraint)
    monkeypatch.setattr("pyddl_oracle.table.get_full_storage", fake_full_storage)

    columns = pd.DataFrame({"column_name": ["ID"]})
    indexes = pd.DataFrame({"index_name": ["I1"], "table_name": ["TBL"]})
    index_columns = pd.DataFrame({"index_name": ["I1"], "column_name": ["ID"], "table_name": ["TBL"]})
    constraints = pd.DataFrame({"constraint_name": ["C1"], "table_name": ["TBL"], "constraint_type": ["P"]})
    cons_cols = pd.DataFrame({"constraint_name": ["C1"], "owner": ["SCHEMA"], "column_name": ["ID"]})
    comments = pd.DataFrame({"table_name": ["TBL"], "column_name": [None], "comments": ["Table comment"]})
    grants = pd.DataFrame({"grantee": ["U1"], "grantable": ["NO"], "privilege": ["SELECT"], "table_name": ["TBL"]})

    t = make_table(
        columns=columns,
        comments=comments,
        indexes=indexes,
        index_columns=index_columns,
        tab_constraints=constraints,
        tab_constraint_columns=cons_cols,
        tab_grants=grants,
    )
    t.generate_ddl()
    ddl = t.ddl

    assert "CREATE TABLE SCHEMA.TBL" in ddl
    assert "NUMBER(10)" in ddl
    assert "-- STORAGE --" in ddl
    assert "LOGGING" in ddl
    assert "CACHE" in ddl
    assert "RESULT_CACHE" in ddl
    assert "ENABLE ROW MOVEMENT" in ddl
    assert "IDX" in ddl and "CST" in ddl
    assert "COMMENT ON TABLE" in ddl
    assert "GRANT SELECT" in ddl


