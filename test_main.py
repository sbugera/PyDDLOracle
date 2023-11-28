import os
import shutil
import main as m
import pandas as pd
import yaml

conf = yaml.safe_load("""
case:
  keyword: "uppercase"
  identifier: "uppercase"
storage:
  storage: "with_storage"
  partitions: "compact"
  collation: "yes"
  logging: "yes"
  compression: "yes"
  cache: "yes"
  result_cache: "yes"
comments:
  comments: "yes"
  empty_line_after_comment: "no"
  vertical_alignment: "yes"
indexes: "yes"
constraints: "yes"
prompts: "yes"
""")
m.conf = conf


if not os.path.isfile("config_con.yaml"):
    shutil.copyfile("config_con.template.yaml", "config_con.yaml")


def store_metadata_into_xlsx():
    db_metadata = m.get_db_metadata("EXTORA_APP")

    (df_tables,
     df_all_tab_columns,
     df_all_part_tables,
     df_all_part_key_columns,
     df_all_tab_partitions,
     df_all_comments,
     df_all_indexes,
     df_all_index_columns,
     df_all_constraints,
     df_all_constraint_columns) = db_metadata

    df_tables.to_excel("test/dfs/df_tables.xlsx", index=False)
    df_all_tab_columns.to_excel("test/dfs/df_all_tab_columns.xlsx", index=False)
    df_all_part_tables.to_excel("test/dfs/df_all_part_tables.xlsx", index=False)
    df_all_part_key_columns.to_excel("test/dfs/df_all_part_key_columns.xlsx", index=False)
    df_all_tab_partitions.to_excel("test/dfs/df_all_tab_partitions.xlsx", index=False)
    df_all_comments.to_excel("test/dfs/df_all_comments.xlsx", index=False)
    df_all_indexes.to_excel("test/dfs/df_all_indexes.xlsx", index=False)
    df_all_index_columns.to_excel("test/dfs/df_all_index_columns.xlsx", index=False)
    df_all_constraints.to_excel("test/dfs/df_all_constraints.xlsx", index=False)
    df_all_constraint_columns.to_excel("test/dfs/df_all_constraint_columns.xlsx", index=False)


def store_metadata_into_files():
    db_metadata = m.get_db_metadata("EXTORA_APP")

    (df_tables,
     df_all_tab_columns,
     df_all_part_tables,
     df_all_part_key_columns,
     df_all_tab_partitions,
     df_all_comments,
     df_all_indexes,
     df_all_index_columns,
     df_all_constraints,
     df_all_constraint_columns) = db_metadata

    df_tables.to_csv("test/dfs/df_tables.csv", index=False)
    df_all_tab_columns.to_csv("test/dfs/df_all_tab_columns.csv", index=False)
    df_all_part_tables.to_csv("test/dfs/df_all_part_tables.csv", index=False)
    df_all_part_key_columns.to_csv("test/dfs/df_all_part_key_columns.csv", index=False)
    df_all_tab_partitions.to_csv("test/dfs/df_all_tab_partitions.csv", index=False)
    df_all_comments.to_csv("test/dfs/df_all_comments.csv", index=False)
    df_all_indexes.to_csv("test/dfs/df_all_indexes.csv", index=False)
    df_all_index_columns.to_csv("test/dfs/df_all_index_columns.csv", index=False)
    df_all_constraints.to_csv("test/dfs/df_all_constraints.csv", index=False)
    df_all_constraint_columns.to_csv("test/dfs/df_all_constraint_columns.csv", index=False)


def get_metadata_from_xlsx():
    df_tables = pd.read_excel("test/dfs/df_tables.xlsx", na_values=[""])
    df_all_tab_columns = pd.read_excel("test/dfs/df_all_tab_columns.xlsx", na_values=[""])
    df_all_part_tables = pd.read_excel("test/dfs/df_all_part_tables.xlsx", na_values=[""])
    df_all_part_key_columns = pd.read_excel("test/dfs/df_all_part_key_columns.xlsx", na_values=[""])
    df_all_tab_partitions = pd.read_excel("test/dfs/df_all_tab_partitions.xlsx", na_values=[""])
    df_all_comments = pd.read_excel("test/dfs/df_all_comments.xlsx", na_values=[""])
    df_all_indexes = pd.read_excel("test/dfs/df_all_indexes.xlsx", na_values=[""])
    df_all_index_columns = pd.read_excel("test/dfs/df_all_index_columns.xlsx", na_values=[""])
    df_all_constraints = pd.read_excel("test/dfs/df_all_constraints.xlsx", na_values=[""])
    df_all_constraint_columns = pd.read_excel("test/dfs/df_all_constraint_columns.xlsx", na_values=[""])

    return (df_tables,
            df_all_tab_columns,
            df_all_part_tables,
            df_all_part_key_columns,
            df_all_tab_partitions,
            df_all_comments,
            df_all_indexes,
            df_all_index_columns,
            df_all_constraints,
            df_all_constraint_columns)


def get_metadata_from_files():
    df_tables = pd.read_csv("test/dfs/df_tables.csv", na_values=[""])
    df_all_tab_columns = pd.read_csv("test/dfs/df_all_tab_columns.csv", na_values=[""])
    df_all_part_tables = pd.read_csv("test/dfs/df_all_part_tables.csv", na_values=[""])
    df_all_part_key_columns = pd.read_csv("test/dfs/df_all_part_key_columns.csv", na_values=[""])
    df_all_tab_partitions = pd.read_csv("test/dfs/df_all_tab_partitions.csv", na_values=[""])
    df_all_comments = pd.read_csv("test/dfs/df_all_comments.csv", na_values=[""])
    df_all_indexes = pd.read_csv("test/dfs/df_all_indexes.csv", na_values=[""])
    df_all_index_columns = pd.read_csv("test/dfs/df_all_index_columns.csv", na_values=[""])
    df_all_constraints = pd.read_csv("test/dfs/df_all_constraints.csv", na_values=[""])
    df_all_constraint_columns = pd.read_csv("test/dfs/df_all_constraint_columns.csv", na_values=[""])

    return (df_tables,
            df_all_tab_columns,
            df_all_part_tables,
            df_all_part_key_columns,
            df_all_tab_partitions,
            df_all_comments,
            df_all_indexes,
            df_all_index_columns,
            df_all_constraints,
            df_all_constraint_columns)


def get_content_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content


def checking_tables_ddl(case_name):
    schema_name = "EXTORA_APP"
    # df_tables, *db_metadata = get_metadata_from_xlsx()
    df_tables, *db_metadata = get_metadata_from_files()
    # df_tables, *db_metadata = m.get_db_metadata(schema_name)
    for db_table_row in df_tables.itertuples():
        tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
        table = m.Table(*tabel_dfs)
        table.generate_ddl()
        ddl = table.ddl
        expected_ddl = get_content_from_file(f"test/tables__{case_name}/{schema_name.lower()}.{table.table_name.lower()}.sql")
        assert ddl == expected_ddl


def test_get_table_dfs():
    # df_tables, *db_metadata = get_metadata_from_xlsx()
    df_tables, *db_metadata = get_metadata_from_files()
    db_table_row = df_tables.iloc[0]
    tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
    assert len(tabel_dfs) == 10


def test_table_ddl():
    # df_tables, *db_metadata = get_metadata_from_xlsx()
    df_tables, *db_metadata = get_metadata_from_files()
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
    m.conf["indexes"] = "yes"
    m.conf["constraints"] = "yes"
    m.conf["prompts"] = "yes"
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
    m.conf["indexes"] = "yes"
    m.conf["constraints"] = "yes"
    m.conf["prompts"] = "yes"
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
    m.conf["indexes"] = "yes"
    m.conf["constraints"] = "yes"
    m.conf["prompts"] = "yes"
    checking_tables_ddl("3__no_storage")


def test_tables_ddl__4__only_tablespace():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "uppercase"
    m.conf["storage"]["storage"] = "only_tablespace"
    m.conf["storage"]["partitions"] = "none"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "yes"
    m.conf["storage"]["result_cache"] = "no"
    m.conf["comments"]["comments"] = "no"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"] = "yes"
    m.conf["constraints"] = "yes"
    m.conf["prompts"] = "no"
    checking_tables_ddl("4__only_tablespace")


def test_tables_ddl__5__uppercase__lowercase__compact_part():
    m.conf["case"]["keyword"] = "uppercase"
    m.conf["case"]["identifier"] = "lowercase"
    m.conf["storage"]["storage"] = "with_storage"
    m.conf["storage"]["partitions"] = "compact"
    m.conf["storage"]["collation"] = "yes"
    m.conf["storage"]["logging"] = "yes"
    m.conf["storage"]["compression"] = "yes"
    m.conf["storage"]["cache"] = "no"
    m.conf["storage"]["result_cache"] = "yes"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "yes"
    m.conf["comments"]["vertical_alignment"] = "no"
    m.conf["indexes"] = "yes"
    m.conf["constraints"] = "yes"
    m.conf["prompts"] = "yes"
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
    m.conf["storage"]["result_cache"] = "no"
    m.conf["comments"]["comments"] = "yes"
    m.conf["comments"]["empty_line_after_comment"] = "no"
    m.conf["comments"]["vertical_alignment"] = "yes"
    m.conf["indexes"] = "no"
    m.conf["constraints"] = "no"
    m.conf["prompts"] = "yes"
    checking_tables_ddl("6__lowercase__uppercase__no_empty_line")


# store_metadata_into_xlsx()
# store_metadata_into_files()
