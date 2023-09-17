from sqlalchemy import create_engine
import pandas as pd
import sql_queries as sql
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')

conf_format = configparser.ConfigParser()
conf_format.read('config.formatter.ini')

db_username = conf['database']['username']
db_password = conf['database']['password']
db_host = conf['database']['host']
db_port = conf['database']['port']
db_service_name = conf['database']['service_name']
connection_string = f"oracle+cx_oracle://{db_username}:{db_password}@{db_host}:{db_port}/?service_name={db_service_name}"
engine = create_engine(connection_string, arraysize=1000)

schema_name = 'EXTORA_APP'

df_tables = pd.read_sql_query(sql.sql_tables, engine, params={
                              'schema_name': schema_name})
df_all_tab_columns = pd.read_sql_query(sql.sql_tab_columns, engine, params={
                                       'schema_name': schema_name})


def get_case_formatted(str, config_name_for_upper):
    if str != str.upper():
        return f'"{str}"'
    if conf_format["case"][config_name_for_upper] == "uppercase":
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


def generate_table_ddl(table, columns):
    ddl = f"""{get_case_formatted("CREATE TABLE", "keyword")} {get_case_formatted(table.owner, "identifier")}.{get_case_formatted(table.table_name, "identifier")}\n(\n"""
    max_column_name_length = get_maximim_column_name_length(columns)

    for i, column in enumerate(columns.itertuples()):
        last_char = "\n" if i == len(columns)-1 else ",\n"
        data_type = get_case_formatted(column.data_type, "keyword") if pd.isnull(
            column.data_type_owner) else get_case_formatted(f"{column.data_type_owner}.{column.data_type}", "keyword")
        if data_type.upper() == "NUMBER":
            if not pd.isnull(column.data_precision) and column.data_scale > 0:
                data_type = f"{data_type}({int(column.data_precision)},{int(column.data_scale)})"
            elif not pd.isnull(column.data_precision):
                data_type = f"{data_type}({int(column.data_precision)})"
            elif pd.isnull(column.data_precision) and column.data_scale == 0:
                data_type = get_case_formatted("INTEGER", "keyword")
        elif data_type.upper() in ("CHAR", "VARCHAR", "VARCHAR2", "NVARCHAR"):
            char_used = get_case_formatted(
                "BYTE", "keyword") if column.char_used == "B" else get_case_formatted("CHAR", "keyword")
            data_type = f"{data_type}({int(column.data_length)} {char_used})"
        elif data_type.upper() in ("UROWID", "RAW", "NCHAR", "NVARCHAR2"):
            data_type = f"{data_type}({int(column.data_length)})"
        elif data_type.upper() in ("FLOAT"):
            data_type = f"{data_type}({int(column.data_precision)})"
        padded_column_name = get_case_formatted(
            column.column_name, "identifier").ljust(max_column_name_length)
        ddl += f"""    {padded_column_name}  {data_type}{last_char}"""

    ddl += ");"
    return ddl


for table in df_tables.itertuples():
    print("----------------------------")
    print(table.table_name)
    print("----------------------------")
    df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"]
                                        == table.table_name]
    table_ddl = generate_table_ddl(table, df_tab_columns)
    print(table_ddl)


engine.dispose()
