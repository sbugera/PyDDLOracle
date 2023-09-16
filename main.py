from sqlalchemy import create_engine
import pandas as pd
import sql_queries as sql


db_user="system"
db_password="oracle"
db_dsn="192.168.0.127:1521/?service_name=orcl"
connection_string = f"oracle+cx_oracle://{db_user}:{db_password}@{db_dsn}"
engine = create_engine(connection_string, arraysize=1000)

schema_name = 'LOG_APP'

df_tables = pd.read_sql_query(sql.sql_tables, engine, params={'schema_name': schema_name})
df_all_tab_columns = pd.read_sql_query(sql.sql_tab_columns, engine, params={'schema_name': schema_name})


def generate_table_ddl(table, columns):
    ddl = f"CREATE TABLE {table.owner}.{table.table_name} (\n"
    for i, column in enumerate(columns.itertuples()):
        last_char = "\n" if i == len(columns)-1 else ",\n"
        data_type = column.data_type
        if data_type == "NUMBER":
            if column.data_precision is not None:
                data_type = f"{data_type}({column.data_length}, {column.data_precision})"
            elif column.data_length < 22:
                data_type = f"{data_type}({column.data_length})"
        elif data_type in ("CHAR", "VARCHAR", "VARCHAR2", "NCHAR", "NVARCHAR", "NVARCHAR2"):
            char_used = "BYTE" if column.char_used == "B" else "CHAR"
            data_type = f"{data_type}({column.data_length} {char_used})"
        ddl += f"    {column.column_name} {data_type}{last_char}"
    ddl += ");"
    return ddl


for table in df_tables.itertuples():
    print("----------------------------")
    print(table.table_name)
    print("----------------------------")
    df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table.table_name]
    table_ddl = generate_table_ddl(table, df_tab_columns)
    print(table_ddl)


engine.dispose()