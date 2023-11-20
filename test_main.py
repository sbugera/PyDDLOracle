import pytest
import os
import shutil
import main as m
import pandas as pd
import json
from io import StringIO
import configparser

conf = configparser.ConfigParser()
conf.read_string("""
[case]
keyword = uppercase
identifier = uppercase

[alignments]
indentation_mode = spaces
indentation_size = 4

[storage]
storage = no_storage
partitions = none
collation = yes
logging = yes
compression = yes
cache = yes
result_cache = yes

[comments]
comments = yes
empty_line_after_comment = no
vertical_alignment = yes

[indexes]
indexes = yes
empty_line_after_index = no

[directory]
table = ../extora_generated_ddls/{OBJECT_OWNER}/tables

[filename]
table = {object_owner}.{object_name}.sql
""")
m.conf = conf

# check if config file exists
# if not, copy config file from config_default.ini
if not os.path.isfile("config_con.ini"):
    shutil.copyfile("config_con.ini.template", "config_con.ini")


def store_metadata_into_xlsx():
    db_metadata = m.get_db_metadata("EXTORA_APP")

    (df_tables,
     df_all_tab_columns,
     df_all_part_tables,
     df_all_part_key_columns,
     df_all_tab_partitions,
     df_all_comments,
     df_all_indexes,
     df_all_index_columns) = db_metadata

    df_tables.to_excel("test/dfs/df_tables.xlsx", index=False)
    df_all_tab_columns.to_excel("test/dfs/df_all_tab_columns.xlsx", index=False)
    df_all_part_tables.to_excel("test/dfs/df_all_part_tables.xlsx", index=False)
    df_all_part_key_columns.to_excel("test/dfs/df_all_part_key_columns.xlsx", index=False)
    df_all_tab_partitions.to_excel("test/dfs/df_all_tab_partitions.xlsx", index=False)
    df_all_comments.to_excel("test/dfs/df_all_comments.xlsx", index=False)
    df_all_indexes.to_excel("test/dfs/df_all_indexes.xlsx", index=False)
    df_all_index_columns.to_excel("test/dfs/df_all_index_columns.xlsx", index=False)


def get_metadata_from_xlsx():
    df_tables = pd.read_excel("test/dfs/df_tables.xlsx", na_values=[""])
    df_all_tab_columns = pd.read_excel("test/dfs/df_all_tab_columns.xlsx", na_values=[""])
    df_all_part_tables = pd.read_excel("test/dfs/df_all_part_tables.xlsx", na_values=[""])
    df_all_part_key_columns = pd.read_excel("test/dfs/df_all_part_key_columns.xlsx", na_values=[""])
    df_all_tab_partitions = pd.read_excel("test/dfs/df_all_tab_partitions.xlsx", na_values=[""])
    df_all_comments = pd.read_excel("test/dfs/df_all_comments.xlsx", na_values=[""])
    df_all_indexes = pd.read_excel("test/dfs/df_all_indexes.xlsx", na_values=[""])
    df_all_index_columns = pd.read_excel("test/dfs/df_all_index_columns.xlsx", na_values=[""])

    return (df_tables,
            df_all_tab_columns,
            df_all_part_tables,
            df_all_part_key_columns,
            df_all_tab_partitions,
            df_all_comments,
            df_all_indexes,
            df_all_index_columns)


def get_content_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content


def checking_tables_ddl(case_name):
    schema_name = "EXTORA_APP"
    df_tables, *db_metadata = get_metadata_from_xlsx()
    # df_tables, *db_metadata = m.get_db_metadata(schema_name)
    for db_table_row in df_tables.itertuples():
        tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
        table = m.Table(*tabel_dfs)
        table.generate_ddl()
        ddl = table.ddl
        expected_ddl = get_content_from_file(f"test/tables__{case_name}/{schema_name.lower()}.{table.table_name.lower()}.sql")
        assert ddl == expected_ddl


def test_get_table_dfs():
    df_tables, *db_metadata = get_metadata_from_xlsx()
    db_table_row = df_tables.iloc[0]
    tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
    assert len(tabel_dfs) == 8


def test_table_ddl():
    df_tables, *db_metadata = get_metadata_from_xlsx()
    db_table_row = df_tables.iloc[0]
    tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
    table = m.Table(*tabel_dfs)
    table.generate_ddl()
    assert len(table.ddl) > 0


def test_tables_ddl__1__uppercase__logging():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "uppercase"
    m.conf["storage"]["storage"] = "with_storage"
    m.conf["storage"]["partitions"] = "all"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "no"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"]["indexes"] = "yes"
    m.conf["indexes"]["empty_line_after_index"] = "yes"
    checking_tables_ddl("1__uppercase__logging")


def test_tables_ddl__2__lowercase__compress():
    m.conf["case"]["keyword"] = "lowercase"
    m.conf["case"]["identifier"] = "lowercase"
    m.conf["storage"]["storage"] = "with_storage"
    m.conf["storage"]["partitions"] = "all"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "no"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"]["indexes"] = "yes"
    m.conf["indexes"]["empty_line_after_index"] = "yes"
    checking_tables_ddl("2__lowercase__compress")


def test_tables_ddl__3__no_storage():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "uppercase"
    m.conf["storage"]["storage"] = "no_storage"
    m.conf["storage"]["partitions"] = "all"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "no"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"]["indexes"] = "yes"
    m.conf["indexes"]["empty_line_after_index"] = "yes"
    checking_tables_ddl("3__no_storage")


def test_tables_ddl__4__only_tablespace():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "uppercase"
    m.conf["storage"]["storage"] = "only_tablespace"
    m.conf["storage"]["partitions"] = "all"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "no"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"]["indexes"] = "yes"
    m.conf["indexes"]["empty_line_after_index"] = "yes"
    checking_tables_ddl("4__only_tablespace")


def test_tables_ddl__5__uppercase__lowercase__compact_part():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "lowercase"
    m.conf["storage"]["storage"] = "with_storage"
    m.conf["storage"]["partitions"] = "compact"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "no"
    m.conf["indexes"]["indexes"] = "yes"
    m.conf["indexes"]["empty_line_after_index"] = "yes"
    checking_tables_ddl("5__uppercase__lowercase__compact_part")


def test_tables_ddl__6__lowercase__uppercase__no_empty_line():
    m.conf["case"]["keyword"] = "lowercase"
    m.conf["case"]["identifier"] = "uppercase"
    m.conf["storage"]["storage"] = "with_storage"
    m.conf["storage"]["partitions"] = "all"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "no"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"]["indexes"] = "no"
    m.conf["indexes"]["empty_line_after_index"] = "yes"
    checking_tables_ddl("6__lowercase__uppercase__no_empty_line")


def test_tables_ddl__7__no_storage__no_part__no_comments():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "uppercase"
    m.conf["storage"]["storage"] = "no_storage"
    m.conf["storage"]["partitions"] = "none"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "no"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"]["indexes"] = "yes"
    m.conf["indexes"]["empty_line_after_index"] = "no"
    checking_tables_ddl("7__no_storage__no_part__no_comments")


# db_metadata = m.get_db_metadata("EXTORA_APP")
#
# (df_tables,
#  df_all_tab_columns,
#  df_all_part_tables,
#  df_all_part_key_columns,
#  df_all_tab_partitions,
#  df_all_comments,
#  df_all_indexes,
#  df_all_index_columns) = db_metadata
#
# df_tables.to_excel("test/dfs/df_tables.xlsx", index=False)
# df_tables_deserialized = pd.read_excel("test/dfs/df_tables.xlsx", keep_default_na=True)
# df_tables_deserialized = df_tables_deserialized.fillna('None')
# print(df_tables)
# print(df_tables_deserialized)
store_metadata_into_xlsx()
