"""Generates DDL scripts for Oracle database objects."""

import pandas as pd

from pyddl_oracle.config import config as c
from pyddl_oracle.constraint import Constraint, get_foreign_key_dfs
from pyddl_oracle.db_metadata import DBMetadata
from pyddl_oracle.table import Table, get_table_dfs

pd.options.mode.chained_assignment = None  # type: ignore # default='warn'
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


def run() -> None:
    """Entry point for the CLI generation workflow."""
    c.args = c.get_args()
    c.conf = c.load_config(c.args.config_file)
    c.conf_con = c.load_config(c.args.con_config_file)
    db_metadata = DBMetadata()
    db_metadata.load_db_metadata()

    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    print("    Tables")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    df_tables = db_metadata.tables
    for db_table_row in df_tables.itertuples():
        print(db_table_row.table_name)
        tabel_dfs = get_table_dfs(db_table_row, db_metadata)
        table = Table(*tabel_dfs)
        table.generate_ddl()
        table.store_ddl_into_file()

    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    print("    Foreign Keys")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    df_foreign_keys = db_metadata.constraints.loc[
        db_metadata.constraints["constraint_type"] == "R"
    ]
    for db_foreign_key_row in df_foreign_keys.itertuples():
        print(db_foreign_key_row.constraint_name)
        foreign_key_dfs = get_foreign_key_dfs(db_foreign_key_row, db_metadata)
        foreign_key = Constraint(*foreign_key_dfs)
        foreign_key.generate_ddl()
        foreign_key.store_ddl_into_file()


if __name__ == "__main__":
    run()
