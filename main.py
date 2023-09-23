from sqlalchemy import create_engine
import pandas as pd
import argparse
import configparser
import re
import os
import sql_queries as sql

pd.options.mode.chained_assignment = None  # type: ignore # default='warn'

arg_parser = argparse.ArgumentParser(description='Generate DDL scripts for Oracle database objects')
arg_parser.add_argument('--schema_name', '-s', type=str, help='DB schema name for which DDL scripts need to be generated')
args = arg_parser.parse_args()

conf_con = configparser.ConfigParser()
conf_con.read('config_con.ini')

conf = configparser.ConfigParser()
conf.read('config.ini')

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


def get_column_data_type(col_data_type, col_data_length, col_data_precision, col_data_scale, col_data_type_owner, col_char_used):
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
    if conf["alignments"]["indentation-mode"] == "tab":
        indentation = "\t"
    else:
        indentation = " "*int(conf["alignments"]["indentation-size"])
    return indentation


def get_default(col_data_default, col_virtual_column, col_default_on_null):
    data_default = ""
    if col_data_default and col_virtual_column == "YES":
        data_default = f""" {get_case_formatted("GENERATED ALWAYS AS", "keyword")} ({col_data_default})"""
    elif col_data_default and col_default_on_null == "YES":
        data_default = f""" {get_case_formatted("DEFAULT ON NULL", "keyword")} {col_data_default}"""
    elif col_data_default:
        data_default = f""" {get_case_formatted("DEFAULT", "keyword")} {col_data_default}"""
    return data_default.rstrip()


def get_not_null(col_nullable):
    not_null = ""
    if col_nullable == "N":
        not_null = " NOT NULL"
    return get_case_formatted(not_null, "keyword")


def get_collation(col_collation):
    collation = ""
    if col_collation and col_collation != "USING_NLS_COMP":
        collation = f" COLLATE {col_collation}"
    return get_case_formatted(collation, "keyword")


def get_invisible(col_hidden_column):
    invisible = ""
    if col_hidden_column == "YES":
        invisible = " INVISIBLE"
    return get_case_formatted(invisible, "keyword")

    
def generate_table_ddl(table, columns):
    table_name = get_case_formatted(f"{table.owner}.{table.table_name}", "identifier")
    ddl = f"""{get_case_formatted("CREATE TABLE", "keyword")} {table_name}\n(\n"""
    max_column_name_length = get_maximim_column_name_length(columns)

    for i, column in enumerate(columns.itertuples()):
        indentation = get_indentation()
        column_name = get_column_name(column.column_name, max_column_name_length)
        data_type = get_column_data_type(column.data_type, column.data_length, column.data_precision, 
                                         column.data_scale, column.data_type_owner, column.char_used)
        invisible = get_invisible(column.hidden_column)
        collation = get_collation(column.collation)
        data_default = get_default(column.data_default, column.virtual_column, column.default_on_null)
        not_null = get_not_null(column.nullable)
        last_char = "\n" if i == len(columns)-1 else ",\n"
        ddl += f"""{indentation}{column_name}  {data_type}{invisible}{collation}{data_default}{not_null}{last_char}"""

    ddl += ");"
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


db_username = conf_con['database']['username']
db_password = conf_con['database']['password']
db_host = conf_con['database']['host']
db_port = conf_con['database']['port']
db_service_name = conf_con['database']['service_name']
connection_string = f"oracle+cx_oracle://{db_username}:{db_password}@{db_host}:{db_port}/?service_name={db_service_name}"
engine = create_engine(connection_string, arraysize=1000)

schema_name = db_username.upper()
if args.schema_name:
    schema_name = args.schema_name

df_tables = pd.read_sql_query(sql.sql_tables, engine, params={
                              'schema_name': schema_name})
df_all_tab_columns = pd.read_sql_query(sql.sql_tab_columns, engine, params={
                                       'schema_name': schema_name})

for table in df_tables.itertuples():
    print("----------------------------")
    print(table.table_name)
    print("----------------------------")
    df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table.table_name]
    table_ddl = generate_table_ddl(table, df_tab_columns)
    # print(table_ddl)
    # table_ddl = "test content"
    file_directory = get_file_directory('table', schema_name, table.table_name)
    file_name = get_file_name('table', schema_name, table.table_name)
    print(f"Stored in {file_directory}/{file_name}")
    store_ddl_into_file(table_ddl, file_directory, file_name)


engine.dispose()
