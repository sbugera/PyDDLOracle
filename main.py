from sqlalchemy import create_engine
import pandas as pd
import argparse
import configparser
import re
import os
from collections import namedtuple
from pprint import PrettyPrinter
import sql_queries as sql

pd.options.mode.chained_assignment = None  # type: ignore # default='warn'

arg_parser = argparse.ArgumentParser(description='Generate DDL scripts for Oracle database objects')
arg_parser.add_argument('--schema_name', '-s', type=str,
                        help='DB schema name for which DDL scripts need to be generated')
args = arg_parser.parse_args()

conf_con = configparser.ConfigParser()
conf_con.read('config_con.ini')

conf = configparser.ConfigParser()
conf.read('config.ini')

db_username = conf_con['database']['username']
db_password = conf_con['database']['password']
db_host = conf_con['database']['host']
db_port = conf_con['database']['port']
db_service_name = conf_con['database']['service_name']
connection_string = f"oracle+cx_oracle://{db_username}:{db_password}@{db_host}:{db_port}/?service_name={db_service_name}"
engine = create_engine(connection_string, arraysize=1000)

schema_name = db_username.upper()
if args.schema_name:
    schema_name = args.schema_name.upper()


def get_dataframe_namedtuple(df, index):
    """
    Returns the row of a pandas dataframe as a namedtuple.
    """
    if index >= len(df):
        return None
    row = df.iloc[index]
    row_namedtuple = namedtuple('row', row.index)
    return row_namedtuple(*row.values)


def pprint(variable):
    pp = PrettyPrinter(indent=1, width=80, depth=None, stream=None, compact=False)
    try:
        pp.pprint(variable._asdict())
    except AttributeError:
        pp.pprint(variable)


def get_case_formatted(str, config_name_for_upper):
    if str != str.upper():
        return f'"{str}"'
    if conf["case"][config_name_for_upper] == "uppercase":
        return str.upper()
    else:
        return str.lower()


def add_quotes(value):
    if any(char.islower() for char in value):
        return f'"{value}"'
    else:
        return value


def get_indentation():
    if conf["alignments"]["indentation_mode"] == "tab":
        indentation = "\t"
    else:
        indentation = " " * int(conf["alignments"]["indentation_size"])
    return indentation


def get_entity_name(template_name, object_type, object_owner, object_name):
    pattern = r'\{(.*?)\}'
    matches = re.findall(pattern, template_name)
    entity_name = template_name
    for match in matches:
        case_function = str.lower
        if match == match.upper():
            case_function = str.upper

        if match.lower() == 'object_type':
            entity_name = entity_name.replace(case_function('{object_type}'), case_function(object_type))
        elif match.lower() == 'object_owner':
            entity_name = entity_name.replace(case_function('{object_owner}'), case_function(object_owner))
        elif match.lower() == 'object_name':
            entity_name = entity_name.replace(case_function('{object_name}'), case_function(object_name))
    return entity_name


class Column:
    def __init__(self, column_row, max_column_name_length):
        self.max_column_name_length = max_column_name_length
        self.column_name = column_row.column_name
        self.data_type = column_row.data_type
        self.data_length = column_row.data_length
        self.data_precision = column_row.data_precision
        self.data_scale = column_row.data_scale
        self.data_type_owner = column_row.data_type_owner
        self.char_used = column_row.char_used
        self.hidden_column = column_row.hidden_column
        self.collation = column_row.collation
        self.data_default = column_row.data_default
        self.virtual_column = column_row.virtual_column
        self.default_on_null = column_row.default_on_null
        self.nullable = column_row.nullable

    def get_name(self):
        formatted_column_name = get_case_formatted(self.column_name, "identifier")
        padded_column_name = formatted_column_name.ljust(self.max_column_name_length)
        return padded_column_name

    def get_data_type(self):
        data_type = get_case_formatted(self.data_type, "keyword") if pd.isnull(
            self.data_type_owner) else get_case_formatted(f"{self.data_type_owner}.{self.data_type}", "keyword")
        if data_type.upper() == "NUMBER":
            if not pd.isnull(self.data_precision) and self.data_scale > 0:
                data_type = f"{data_type}({int(self.data_precision)},{int(self.data_scale)})"
            elif not pd.isnull(self.data_precision):
                data_type = f"{data_type}({int(self.data_precision)})"
            elif pd.isnull(self.data_precision) and self.data_scale == 0:
                data_type = get_case_formatted("INTEGER", "keyword")
        elif data_type.upper() in ("CHAR", "VARCHAR", "VARCHAR2", "NVARCHAR"):
            char_used = get_case_formatted(
                "BYTE", "keyword") if self.char_used == "B" else get_case_formatted("CHAR", "keyword")
            data_type = f"{data_type}({int(self.data_length)} {char_used})"
        elif data_type.upper() in ("UROWID", "RAW", "NCHAR", "NVARCHAR2"):
            data_type = f"{data_type}({int(self.data_length)})"
        elif data_type.upper() in ("FLOAT"):
            data_type = f"{data_type}({int(self.data_precision)})"
        return data_type

    def get_invisible(self):
        invisible = ""
        if self.hidden_column == "YES":
            invisible = " INVISIBLE"
        return get_case_formatted(invisible, "keyword")

    def get_collation(self):
        collation = ""
        if self.collation and self.collation != "USING_NLS_COMP":
            collation = f" COLLATE {self.collation}"
        return get_case_formatted(collation, "keyword")

    def get_default(self):
        default = ""
        if self.data_default and self.virtual_column == "YES":
            default = f""" {get_case_formatted("GENERATED ALWAYS AS", "keyword")} ({self.data_default})"""
        elif self.data_default and self.default_on_null == "YES":
            default = f""" {get_case_formatted("DEFAULT ON NULL", "keyword")} {self.data_default}"""
        elif self.data_default:
            default = f""" {get_case_formatted("DEFAULT", "keyword")} {self.data_default}"""
        return default.rstrip()

    def get_not_null(self):
        not_null = ""
        if self.nullable == "N":
            not_null = " NOT NULL"
        return get_case_formatted(not_null, "keyword")

    def get_ddl(self):
        indentation = get_indentation()
        name = self.get_name()
        data_type = self.get_data_type()
        invisible = self.get_invisible()
        collation = self.get_collation()
        data_default = self.get_default()
        not_null = self.get_not_null()
        ddl = f"""{indentation}{name}  {data_type}{invisible}{collation}{data_default}{not_null}"""
        return ddl


class Table:
    def __init__(self, table, columns, part_table):
        self.max_column_name_length = None
        self.ddl = None
        self.columns = columns
        self.owner = table.owner
        self.table_name = table.table_name
        self.default_collation = table.default_collation
        self.logging = table.logging
        self.cache = table.cache
        self.result_cache = table.result_cache
        self.row_movement = table.row_movement
        self.compression = table.compression
        self.compress_for = table.compress_for
        self.partitioned = table.partitioned
        self.tablespace_name = table.tablespace_name
        self.pct_free = table.pct_free
        self.ini_trans = table.ini_trans
        self.max_trans = table.max_trans
        self.min_extents = table.min_extents
        self.max_extents = table.max_extents
        self.pct_increase = table.pct_increase
        self.buffer_pool = table.buffer_pool
        self.flash_cache = table.flash_cache
        self.cell_flash_cache = table.cell_flash_cache
        self.def_tablespace_name = part_table.def_tablespace_name if part_table else None
        self.def_logging = part_table.def_logging if part_table else None
        self.def_compression = part_table.def_compression if part_table else None
        self.def_compress_for = part_table.def_compress_for if part_table else None
        self.def_pct_free = part_table.def_pct_free if part_table else None
        self.def_ini_trans = part_table.def_ini_trans if part_table else None
        self.def_max_trans = part_table.def_max_trans if part_table else None
        self.def_min_extents = part_table.def_min_extents if part_table else None
        self.def_max_extents = part_table.def_max_extents if part_table else None
        self.def_pct_increase = part_table.def_pct_increase if part_table else None
        self.def_buffer_pool = part_table.def_buffer_pool if part_table else None
        self.def_flash_cache = part_table.def_flash_cache if part_table else None
        self.def_cell_flash_cache = part_table.def_cell_flash_cache if part_table else None

    def get_maximum_column_name_length(self):
        self.columns["column_name_quoted"] = self.columns["column_name"].apply(add_quotes)
        return self.columns["column_name_quoted"].str.len().max()

    def get_collation(self):
        collation = ""
        if self.default_collation and self.default_collation != "USING_NLS_COMP":
            collation = f"\nDEFAULT COLLATION {self.default_collation}"
        return get_case_formatted(collation, "keyword")

    def get_storage(self):
        storage = ""
        if conf["storage"]["table_storage"] == "no_storage":
            storage = ""
        elif conf["storage"]["table_storage"] == "only_tablespace" and self.partitioned == "NO":
            storage = f"\nTABLESPACE {self.tablespace_name}"
        elif conf["storage"]["table_storage"] == "only_tablespace" and self.partitioned == "YES":
            storage = f"\nTABLESPACE {self.def_tablespace_name}"
        elif conf["storage"]["table_storage"] == "with_storage" and self.partitioned == "NO":
            storage = f"\nTABLESPACE {self.tablespace_name}"
            if str(self.pct_free) != "nan":
                storage += f"\nPCTFREE    {int(self.pct_free)}"
            if str(self.ini_trans) != "nan":
                storage += f"\nINITRANS   {int(self.ini_trans)}"
            if str(self.max_trans) != "nan":
                storage += f"\nMAXTRANS   {int(self.max_trans)}"
            storage += f"\nSTORAGE    ("
            if str(self.min_extents) not in ("nan", "DEFAULT"):
                storage += f"\n            MINEXTENTS       {int(self.min_extents)}"
            if str(self.max_extents) not in ("nan", "DEFAULT"):
                storage += f"\n            MAXEXTENTS       {int(self.max_extents)}"
            storage += f"\n            PCTINCREASE      {int(self.pct_increase) if self.pct_increase is not None else 0}"
            if self.buffer_pool != "DEFAULT":
                storage += f"\n            BUFFER_POOL      {self.buffer_pool}"
            if self.flash_cache != "DEFAULT":
                storage += f"\n            FLASH_CACHE      {self.flash_cache}"
            if self.cell_flash_cache != "DEFAULT":
                storage += f"\n            CELL_FLASH_CACHE {self.cell_flash_cache}"
            storage += f"\n            )"
        elif conf["storage"]["table_storage"] == "with_storage" and self.partitioned == "YES":
            storage = f"\nTABLESPACE {self.def_tablespace_name}"
            if str(self.def_pct_free) != "nan":
                storage += f"\nPCTFREE    {int(self.def_pct_free)}"
            if str(self.def_ini_trans) != "nan":
                storage += f"\nINITRANS   {int(self.def_ini_trans)}"
            if str(self.def_max_trans) != "nan":
                storage += f"\nMAXTRANS   {int(self.def_max_trans)}"
            storage_tmp = f"\nSTORAGE    ("
            if str(self.def_min_extents) not in ("nan", "DEFAULT"):
                storage_tmp += f"\n            MINEXTENTS       {int(self.def_min_extents)}"
            if str(self.def_max_extents) not in ("nan", "DEFAULT"):
                storage_tmp += f"\n            MAXEXTENTS       {int(self.def_max_extents)}"
            if self.def_pct_increase not in ("nan", "DEFAULT"):
                storage_tmp += f"\n            PCTINCREASE      {int(self.def_pct_increase)}"
            if self.def_buffer_pool != "DEFAULT":
                storage_tmp += f"\n            BUFFER_POOL      {self.def_buffer_pool}"
            if self.def_flash_cache != "DEFAULT":
                storage_tmp += f"\n            FLASH_CACHE      {self.def_flash_cache}"
            if self.def_cell_flash_cache != "DEFAULT":
                storage_tmp += f"\n            CELL_FLASH_CACHE {self.def_cell_flash_cache}"
            if storage_tmp != f"\nSTORAGE    (":
                storage += f"{storage_tmp}\n            )"
        return get_case_formatted(storage, "keyword")

    def get_logging(self):
        logging = ""
        if conf["storage"]["logging"] == "yes":
            if self.logging == "YES":
                logging = "\nLOGGING"
            else:
                logging = "\nNOLOGGING"
        return get_case_formatted(logging, "keyword")

    def get_compression(self):
        if self.partitioned == "NO":
            tab_compression, tab_compress_for = self.compression, self.compress_for
        else:
            tab_compression, tab_compress_for = self.def_compression, self.def_compress_for
        compression = ""
        if conf["storage"]["compression"] == "yes":
            if tab_compression == "DISABLED":
                compression = "\nNOCOMPRESS"
            else:
                if tab_compress_for == "BASIC":
                    compression = "\nCOMPRESS BASIC"
                elif tab_compress_for == "ADVANCED":
                    compression = "\nCOMPRESS FOR OLTP"
        return get_case_formatted(compression, "keyword")

    def get_cache(self):
        cache = ""
        if conf["storage"]["cache"] == "yes":
            if self.cache.strip() == "Y":
                cache = "\nCACHE"
            else:
                cache = "\nNOCACHE"
        return get_case_formatted(cache, "keyword")

    def get_result_cache(self):
        result_cache = ""
        if conf["storage"]["result_cache"] == "yes":
            result_cache = f"\nRESULT_CACHE (MODE {self.result_cache})"
        return get_case_formatted(result_cache, "keyword")

    def get_tab_row_movement(self):
        row_movement = ""
        if self.row_movement == "ENABLED":
            row_movement = "\nENABLE ROW MOVEMENT"
        return get_case_formatted(row_movement, "keyword")

    def generate_ddl(self):
        table_name = get_case_formatted(f"{self.owner}.{self.table_name}", "identifier")
        self.max_column_name_length = self.get_maximum_column_name_length()

        ddl = f"""{get_case_formatted("CREATE TABLE", "keyword")} {table_name}\n(\n"""

        for i, column_row in enumerate(self.columns.itertuples()):
            column = Column(column_row, self.max_column_name_length)
            column_ddl = column.get_ddl()
            last_char = "\n" if i == len(self.columns) - 1 else ",\n"
            ddl += f"""{column_ddl}{last_char}"""

        ddl += ")"
        ddl += self.get_collation()
        ddl += self.get_storage()
        ddl += self.get_logging()
        ddl += self.get_compression()
        ddl += self.get_cache()
        ddl += self.get_result_cache()
        ddl += self.get_tab_row_movement()
        ddl += ";"
        self.ddl = ddl

    def get_file_directory(self):
        file_directory_template = conf['directory']['table']
        file_directory = get_entity_name(file_directory_template, 'table', self.owner, self.table_name)
        return file_directory

    def get_file_name(self):
        file_name_template = conf['filename']['table']
        file_name = get_entity_name(file_name_template, 'table', self.owner, self.table_name)
        return file_name

    def store_ddl_into_file(self):
        file_directory = self.get_file_directory()
        file_name = self.get_file_name()
        if not os.path.exists(file_directory):
            os.makedirs(file_directory)
        with open(os.path.join(file_directory, file_name), 'w') as file:
            file.write(self.ddl)
        print(f"   Stored in {file_directory}/{file_name}")


def get_df_tables():
    return pd.read_sql_query(sql.sql_tables, engine, params={'schema_name': schema_name})


def get_df_tab_columns():
    return pd.read_sql_query(sql.sql_tab_columns, engine, params={'schema_name': schema_name})


def get_df_part_tables():
    return pd.read_sql_query(sql.sql_part_tables, engine, params={'schema_name': schema_name})


if __name__ == "__main__":
    df_tables = get_df_tables()
    df_all_tab_columns = get_df_tab_columns()
    df_all_part_tables = get_df_part_tables()

    for table_row in df_tables.itertuples():
        print(table_row.table_name)
        df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table_row.table_name]
        df_part_tables = df_all_part_tables[df_all_part_tables["table_name"] == table_row.table_name]
        part_table_row = get_dataframe_namedtuple(df_part_tables, 0)

        table = Table(table_row, df_tab_columns, part_table_row)
        table.generate_ddl()
        table.store_ddl_into_file()

    engine.dispose()
