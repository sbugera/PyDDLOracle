"""Generates DDL scripts for Oracle database objects."""

import pandas as pd

from constraint import get_foreign_key_dfs, Constraint
from table import Table, get_table_dfs
from db_metadata import get_db_schema_name, get_db_metadata
from utils import args

pd.options.mode.chained_assignment = None  # type: ignore # default='warn'
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


if __name__ == "__main__":
    db_schema_name = get_db_schema_name(args.schema_name)
    db_metadata = get_db_metadata(db_schema_name)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    print("    Tables")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    df_tables = db_metadata["tables"]
    for db_table_row in df_tables.itertuples():
        print(db_table_row.table_name)
        tabel_dfs = get_table_dfs(db_table_row, db_metadata)
        table = Table(*tabel_dfs)
        table.generate_ddl()
        table.store_ddl_into_file()

    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    print("    Foreign Keys")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++".ljust(107, "+"))
    df_foreign_keys = db_metadata["constraints"].loc[
        db_metadata["constraints"]["constraint_type"] == "R"
    ]
    for db_foreign_key_row in df_foreign_keys.itertuples():
        print(db_foreign_key_row.constraint_name)
        foreign_key_dfs = get_foreign_key_dfs(db_foreign_key_row, db_metadata)
        foreign_key = Constraint(*foreign_key_dfs)
        foreign_key.generate_ddl()
        foreign_key.store_ddl_into_file()
