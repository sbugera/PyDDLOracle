"""Unit tests for pyddl_oracle.main.run orchestration."""

from types import SimpleNamespace

import pandas as pd

from pyddl_oracle.config import config as c


def test_run_invokes_table_and_fk_generation(monkeypatch, capsys):
    import pyddl_oracle.main as main

    # stub args and config loading
    c.args = None

    def fake_get_args():
        return SimpleNamespace(config_file="config.yaml", con_config_file="config_con.yaml")

    def fake_load_config(path):
        # return minimal valid shapes for both config and connection config
        if path.endswith("config.yaml"):
            return {"case": {"keyword": "uppercase", "identifier": "uppercase"}}
        return {"database": {}}

    monkeypatch.setattr(main.c, "get_args", fake_get_args)
    monkeypatch.setattr(main.c, "load_config", fake_load_config)

    # fake metadata
    class FakeDBMetadata:
        def __init__(self):
            self.tables = pd.DataFrame({"table_name": ["T1"]})
            self.constraints = pd.DataFrame(
                {"constraint_type": ["R"], "constraint_name": ["FK1"]}
            )

    monkeypatch.setattr(main, "DBMetadata", FakeDBMetadata)

    # fake get_table_dfs returning the 11 expected elements
    def fake_get_table_dfs(row, metadata):
        # Return tuple matching signature expected by Table(*tabel_dfs)
        return (
            SimpleNamespace(owner="SCHEMA", table_name=row.table_name),  # table_row
            None,  # part_table_row
            pd.DataFrame({"column_name": ["C1"]}),  # columns
            pd.DataFrame([]),  # comments
            pd.DataFrame([]),  # part_key_columns
            pd.DataFrame([]),  # tab_partitions
            pd.DataFrame([]),  # indexes
            pd.DataFrame([]),  # index_columns
            pd.DataFrame([]),  # tab_constraints
            pd.DataFrame([]),  # tab_constraint_columns
            pd.DataFrame([]),  # tab_grants
        )

    monkeypatch.setattr(main, "get_table_dfs", fake_get_table_dfs)

    # capture calls to Table and Constraint
    calls = {"tables": [], "fks": []}

    class FakeTable:
        def __init__(self, *args):
            calls["tables"].append(args)

        def generate_ddl(self):
            calls["tables"].append("gen")

        def store_ddl_into_file(self):
            calls["tables"].append("store")

    class FakeConstraint:
        def __init__(self, *args):
            calls["fks"].append(args)

        def generate_ddl(self):
            calls["fks"].append("gen")

        def store_ddl_into_file(self):
            calls["fks"].append("store")

    # fake FK dfs helper to pass through
    def fake_get_foreign_key_dfs(row, metadata):
        # Return (row, df_fk_cols, df_remote_cols)
        return (
            SimpleNamespace(
                owner="SCHEMA",
                table_name="T1",
                constraint_name=row.constraint_name,
                constraint_type=row.constraint_type,
                search_condition=None,
                status="ENABLED",
                deferrable="NOT DEFERRABLE",
                deferred="IMMEDIATE",
                validated="VALIDATED",
                index_owner=None,
                index_name=None,
                r_owner=None,
                r_table_name=None,
                r_constraint_name=None,
                delete_rule=None,
            ),
            pd.DataFrame({"column_name": ["C1"]}),
            pd.DataFrame({"column_name": ["C1"]}),
        )

    monkeypatch.setattr(main, "Table", FakeTable)
    monkeypatch.setattr(main, "Constraint", FakeConstraint)
    monkeypatch.setattr(main, "get_foreign_key_dfs", fake_get_foreign_key_dfs)

    # run
    main.run()

    # assertions: one table processed and one FK processed, with generation+store
    assert calls["tables"].count("gen") == 1
    assert calls["tables"].count("store") == 1
    assert calls["fks"].count("gen") == 1
    assert calls["fks"].count("store") == 1

    out = capsys.readouterr().out
    assert "Tables" in out and "Foreign Keys" in out
    assert "T1" in out and "FK1" in out


