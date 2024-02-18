import pandas as pd
import argparse

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
    df_tables, *db_metadata = get_db_metadata(db_schema_name)

    for db_table_row in df_tables.itertuples():
        print(db_table_row.table_name)
        tabel_dfs = get_table_dfs(db_table_row, db_metadata)
        table = Table(*tabel_dfs)
        table.generate_ddl()
        table.store_ddl_into_file()
