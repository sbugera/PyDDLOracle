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
arg_parser.add_argument('--schema_name', '-s', type=str, help='DB schema name for which DDL scripts need to be generated')
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


def get_maximim_column_name_length(df):
    df["column_name_quoted"] = df["column_name"].apply(add_quotes)
    return df["column_name_quoted"].str.len().max()


def get_col_data_type(col_data_type, col_data_length, col_data_precision, col_data_scale, col_data_type_owner, col_char_used):
    data_type = get_case_formatted(col_data_type, "keyword") if pd.isnull(
        col_data_type_owner) else get_case_formatted(f"{col_data_type_owner}.{col_data_type}", "keyword")
    if data_type.upper() == "NUMBER":
        if not pd.isnull(col_data_precision) and col_data_scale > 0:
            data_type = f"{data_type}({int(col_data_precision)},{int(col_data_scale)})"
        elif not pd.isnull(col_data_precision):
            data_type = f"{data_type}({int(col_data_precision)})"
        elif pd.isnull(col_data_precision) and col_data_scale == 0:
            data_type = get_case_formatted("INTEGER", "keyword")
    elif data_type.upper() in ("CHAR", "VARCHAR", "VARCHAR2", "NVARCHAR"):
        char_used = get_case_formatted(
            "BYTE", "keyword") if col_char_used == "B" else get_case_formatted("CHAR", "keyword")
        data_type = f"{data_type}({int(col_data_length)} {char_used})"
    elif data_type.upper() in ("UROWID", "RAW", "NCHAR", "NVARCHAR2"):
        data_type = f"{data_type}({int(col_data_length)})"
    elif data_type.upper() in ("FLOAT"):
        data_type = f"{data_type}({int(col_data_precision)})"
    return data_type


def get_column_name(col_column_name, max_column_name_length):
    formatted_column_name = get_case_formatted(col_column_name, "identifier")
    padded_column_name = formatted_column_name.ljust(max_column_name_length)
    return padded_column_name


def get_indentation():
    if conf["alignments"]["indentation_mode"] == "tab":
        indentation = "\t"
    else:
        indentation = " "*int(conf["alignments"]["indentation_size"])
    return indentation


def get_col_default(col_data_default, col_virtual_column, col_default_on_null):
    data_default = ""
    if col_data_default and col_virtual_column == "YES":
        data_default = f""" {get_case_formatted("GENERATED ALWAYS AS", "keyword")} ({col_data_default})"""
    elif col_data_default and col_default_on_null == "YES":
        data_default = f""" {get_case_formatted("DEFAULT ON NULL", "keyword")} {col_data_default}"""
    elif col_data_default:
        data_default = f""" {get_case_formatted("DEFAULT", "keyword")} {col_data_default}"""
    return data_default.rstrip()


def get_col_not_null(col_nullable):
    not_null = ""
    if col_nullable == "N":
        not_null = " NOT NULL"
    return get_case_formatted(not_null, "keyword")


def get_col_collation(col_collation):
    collation = ""
    if col_collation and col_collation != "USING_NLS_COMP":
        collation = f" COLLATE {col_collation}"
    return get_case_formatted(collation, "keyword")


def get_col_invisible(col_hidden_column):
    invisible = ""
    if col_hidden_column == "YES":
        invisible = " INVISIBLE"
    return get_case_formatted(invisible, "keyword")


def get_tab_collation(tab_collation):
    collation = ""
    if tab_collation and tab_collation != "USING_NLS_COMP":
        collation = f"\nDEFAULT COLLATION {tab_collation}"
    return get_case_formatted(collation, "keyword")


def get_tablespace(tab_tablespace_name):
    tablespace = f"\nTABLESPACE {tab_tablespace_name}"
    return tablespace


def get_tab_storage(table, part_table):
    storage = ""
    if conf["storage"]["table_storage"] == "no_storage":
        storage = ""
    elif conf["storage"]["table_storage"] == "only_tablespace" and table.partitioned == "NO":
        storage = get_tablespace(table.tablespace_name)
    elif conf["storage"]["table_storage"] == "only_tablespace" and table.partitioned == "YES":
        storage = get_tablespace(part_table.def_tablespace_name)
    elif conf["storage"]["table_storage"] == "with_storage" and table.partitioned == "NO":
        storage = get_tablespace(table.tablespace_name)
        if str(table.pct_free) != "nan":
            storage += f"\nPCTFREE    {int(table.pct_free)}"
        if str(table.ini_trans) != "nan":
            storage += f"\nINITRANS   {int(table.ini_trans)}"
        if str(table.max_trans) != "nan":
            storage += f"\nMAXTRANS   {int(table.max_trans)}"
        storage += f"\nSTORAGE    ("
        if str(table.min_extents) not in ("nan", "DEFAULT"):
            storage += f"\n            MINEXTENTS       {int(table.min_extents)}"
        if str(table.max_extents) not in ("nan", "DEFAULT"):
            storage += f"\n            MAXEXTENTS       {int(table.max_extents)}"
        storage += f"\n            PCTINCREASE      {int(table.pct_increase) if table.pct_increase is not None else 0}"
        if table.buffer_pool != "DEFAULT":
            storage += f"\n            BUFFER_POOL      {table.buffer_pool}"
        if table.flash_cache != "DEFAULT":
            storage += f"\n            FLASH_CACHE      {table.flash_cache}"
        if table.cell_flash_cache != "DEFAULT":
            storage += f"\n            CELL_FLASH_CACHE {table.cell_flash_cache}"
        storage += f"\n            )"
    elif conf["storage"]["table_storage"] == "with_storage" and table.partitioned == "YES":
        storage = get_tablespace(part_table.def_tablespace_name)
        if str(part_table.def_pct_free) != "nan":
            storage += f"\nPCTFREE    {int(part_table.def_pct_free)}"
        if str(part_table.def_ini_trans) != "nan":
            storage += f"\nINITRANS   {int(part_table.def_ini_trans)}"
        if str(part_table.def_max_trans) != "nan":
            storage += f"\nMAXTRANS   {int(part_table.def_max_trans)}"
        storage_tmp = f"\nSTORAGE    ("
        if str(part_table.def_min_extents) not in ("nan", "DEFAULT"):
            storage_tmp += f"\n            MINEXTENTS       {int(part_table.def_min_extents)}"
        if str(part_table.def_max_extents) not in ("nan", "DEFAULT"):
            storage_tmp += f"\n            MAXEXTENTS       {int(part_table.def_max_extents)}"
        if part_table.def_pct_increase not in ("nan", "DEFAULT"):
            storage_tmp += f"\n            PCTINCREASE      {int(part_table.def_pct_increase)}"
        if part_table.def_buffer_pool != "DEFAULT":
            storage_tmp += f"\n            BUFFER_POOL      {part_table.def_buffer_pool}"
        if part_table.def_flash_cache != "DEFAULT":
            storage_tmp += f"\n            FLASH_CACHE      {part_table.def_flash_cache}"
        if part_table.def_cell_flash_cache != "DEFAULT":
            storage_tmp += f"\n            CELL_FLASH_CACHE {part_table.def_cell_flash_cache}"
        if storage_tmp != f"\nSTORAGE    (":
            storage += f"{storage_tmp}\n            )"
    return get_case_formatted(storage, "keyword")


def get_tab_logging(table, part_table):
    if table.partitioned == "NO":
        tab_logging = table.logging
    else:
        tab_logging = part_table.def_logging
    logging = ""
    if conf["storage"]["logging"] == "yes":
        if tab_logging == "YES":
            logging = "\nLOGGING"
        else:
            logging = "\nNOLOGGING"
    return get_case_formatted(logging, "keyword")


def get_tab_comression(table, part_table):
    if table.partitioned == "NO":
        tab_comression, tab_compress_for = table.compression, table.compress_for
    else:
        tab_comression, tab_compress_for = part_table.def_compression, part_table.def_compress_for
    comression = ""
    if conf["storage"]["comression"] == "yes":
        if tab_comression == "DISABLED":
            comression = "\nNOCOMPRESS"
        else:
            if tab_compress_for == "BASIC":
                comression = "\nCOMPRESS BASIC"
            elif tab_compress_for == "ADVANCED":
                comression = "\nCOMPRESS FOR OLTP"
    return get_case_formatted(comression, "keyword")


def get_tab_cache(tab_cache):
    cache = ""
    if conf["storage"]["cache"] == "yes":
        if tab_cache.strip() == "Y":
            cache = "\nCACHE"
        else:
            cache = "\nNOCACHE"
    return get_case_formatted(cache, "keyword")


def get_tab_result_cache(tab_result_cache):
    result_cache = ""
    if conf["storage"]["result_cache"] == "yes":
        result_cache = f"\nRESULT_CACHE (MODE {tab_result_cache})"
    return get_case_formatted(result_cache, "keyword")


def get_tab_row_movement(tab_row_movement):
    row_movement = ""
    if tab_row_movement == "ENABLED":
        row_movement = "\nENABLE ROW MOVEMENT"
    return get_case_formatted(row_movement, "keyword")
    
    
def generate_table_ddl(table, columns, part_table):
    table_name = get_case_formatted(f"{table.owner}.{table.table_name}", "identifier")
    max_column_name_length = get_maximim_column_name_length(columns)

    ddl = f"""{get_case_formatted("CREATE TABLE", "keyword")} {table_name}\n(\n"""
    
    for i, column in enumerate(columns.itertuples()):
        indentation = get_indentation()
        col_name = get_column_name(column.column_name, max_column_name_length)
        col_data_type = get_col_data_type(column.data_type, column.data_length, column.data_precision, 
                                          column.data_scale, column.data_type_owner, column.char_used)
        col_invisible = get_col_invisible(column.hidden_column)
        col_collation = get_col_collation(column.collation)
        col_data_default = get_col_default(column.data_default, column.virtual_column, column.default_on_null)
        col_not_null = get_col_not_null(column.nullable)
        last_char = "\n" if i == len(columns)-1 else ",\n"
        ddl += f"""{indentation}{col_name}  {col_data_type}{col_invisible}{col_collation}{col_data_default}{col_not_null}{last_char}"""

    ddl += ")"
    ddl += get_tab_collation(table.default_collation)
    ddl += get_tab_storage(table, part_table)
    ddl += get_tab_logging(table, part_table)
    ddl += get_tab_comression(table, part_table)
    ddl += get_tab_cache(table.cache)
    ddl += get_tab_result_cache(table.result_cache)
    ddl += get_tab_row_movement(table.row_movement)
    ddl += ";"
    return ddl


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


def get_file_name(object_type, object_owner, object_name):
    file_name_template = conf['filename'][object_type]
    file_name = get_entity_name(file_name_template, object_type, object_owner, object_name)
    return file_name


def get_file_directory(object_type, object_owner, object_name):
    file_directory_template = conf['directory'][object_type]
    file_directory = get_entity_name(file_directory_template, object_type, object_owner, object_name)
    return file_directory
    
    
def store_ddl_into_file(file_content, file_directory, file_name):
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
    with open(os.path.join(file_directory, file_name), 'w') as file:
        file.write(file_content)


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
    
    for table in df_tables.itertuples():
        print(table.table_name)
        df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table.table_name]
        df_part_tables = df_all_part_tables[df_all_part_tables["table_name"] == table.table_name]
        part_table = get_dataframe_namedtuple(df_part_tables, 0)
        
        table_ddl = generate_table_ddl(table, df_tab_columns, part_table)
        file_directory = get_file_directory('table', schema_name, table.table_name)
        file_name = get_file_name('table', schema_name, table.table_name)
        print(f"   Stored in {file_directory}/{file_name}")
        store_ddl_into_file(table_ddl, file_directory, file_name)
        
    engine.dispose()
