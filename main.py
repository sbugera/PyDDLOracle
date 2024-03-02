import pandas as pd
import argparse

from constraint import get_foreign_key_dfs, Constraint
from table import Table, get_table_dfs
from db_metadata import get_db_schema_name, get_db_metadata


pd.options.mode.chained_assignment = None  # type: ignore # default='warn'
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def get_args():
    arg_parser = argparse.ArgumentParser(description='Generate DDL scripts for Oracle database objects')
    arg_parser.add_argument('--schema_name', '-s', type=str,
                            help='DB schema name for which DDL scripts need to be generated')
    return arg_parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    db_schema_name = get_db_schema_name(args.schema_name)
    db_metadata = get_db_metadata(db_schema_name)

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("    Tables")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    df_tables = db_metadata["tables"]
    for db_table_row in df_tables.itertuples():
        print(db_table_row.table_name)
        tabel_dfs = get_table_dfs(db_table_row, db_metadata)
        table = Table(*tabel_dfs)
        table.generate_ddl()
        table.store_ddl_into_file()

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("    Foreign Keys")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    df_foreign_keys = db_metadata["constraints"].loc[db_metadata["constraints"]["constraint_type"] == "R"]
    for db_foreign_key_row in df_foreign_keys.itertuples():
        print(db_foreign_key_row.constraint_name)
        foreign_key_dfs = get_foreign_key_dfs(db_foreign_key_row, db_metadata)
        foreign_key = Constraint(*foreign_key_dfs)
        foreign_key.generate_ddl()
        foreign_key.store_ddl_into_file()
