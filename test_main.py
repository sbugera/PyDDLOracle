import os
import shutil
if not os.path.isfile("config_con.yaml"):
    shutil.copyfile("config_con.template.yaml", "config_con.yaml")

import main as m
import pandas as pd
import utils as ut
from utils import conf
from table import get_table_dfs
from db_metadata import get_db_metadata


def store_metadata_into_xlsx():
    metadata = get_db_metadata("EXTORA_APP")

    df_tables = metadata["tables"]
    df_all_tab_columns = metadata["tab_columns"]
    df_all_part_tables = metadata["part_tables"]
    df_all_part_key_columns = metadata["part_key_columns"]
    df_all_tab_partitions = metadata["tab_partitions"]
    df_all_comments = metadata["comments"]
    df_all_indexes = metadata["indexes"]
    df_all_index_columns = metadata["index_columns"]
    df_all_constraints = metadata["constraints"]
    df_all_constraint_columns = metadata["constraint_columns"]
    df_all_grants = metadata["grants"]

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
    df_all_grants.to_excel("test/dfs/df_all_grants.xlsx", index=False)


def store_metadata_into_files():
    metadata = get_db_metadata("EXTORA_APP")

    df_tables = metadata["tables"]
    df_all_tab_columns = metadata["tab_columns"]
    df_all_part_tables = metadata["part_tables"]
    df_all_part_key_columns = metadata["part_key_columns"]
    df_all_tab_partitions = metadata["tab_partitions"]
    df_all_comments = metadata["comments"]
    df_all_indexes = metadata["indexes"]
    df_all_index_columns = metadata["index_columns"]
    df_all_constraints = metadata["constraints"]
    df_all_constraint_columns = metadata["constraint_columns"]
    df_all_grants = metadata["grants"]

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
    df_all_grants.to_csv("test/dfs/df_all_grants.csv", index=False)


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
    df_all_grants = pd.read_excel("test/dfs/df_all_grants.xlsx", na_values=[""])

    metadata = {"tables": df_tables,
                "tab_columns": df_all_tab_columns,
                "part_tables": df_all_part_tables,
                "part_key_columns": df_all_part_key_columns,
                "tab_partitions": df_all_tab_partitions,
                "comments": df_all_comments,
                "indexes": df_all_indexes,
                "index_columns": df_all_index_columns,
                "constraints": df_all_constraints,
                "constraint_columns": df_all_constraint_columns,
                "grants": df_all_grants}
    return metadata


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
    df_all_grants = pd.read_csv("test/dfs/df_all_grants.csv", na_values=[""])

    metadata = {"tables": df_tables,
                "tab_columns": df_all_tab_columns,
                "part_tables": df_all_part_tables,
                "part_key_columns": df_all_part_key_columns,
                "tab_partitions": df_all_tab_partitions,
                "comments": df_all_comments,
                "indexes": df_all_indexes,
                "index_columns": df_all_index_columns,
                "constraints": df_all_constraints,
                "constraint_columns": df_all_constraint_columns,
                "grants": df_all_grants}
    return metadata


def get_content_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = ""
    return content


def update_expected_ddl_file(file_path, ddl):
    try:
        with open(file_path, 'w') as f:
            f.write(ddl)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w') as f:
            f.write(ddl)


def checking_tables_ddl(case_name):
    schema_name = "EXTORA_APP"
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    for db_table_row in df_tables.itertuples():
        tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
        table = m.Table(*tabel_dfs)
        table.generate_ddl()
        ddl = table.ddl
        file_path = f"test/tables__{case_name}/{schema_name.lower()}.{table.table_name.lower()}.sql"
        if update_expected_ddl_files:
            update_expected_ddl_file(file_path, ddl)
        expected_ddl = get_content_from_file(file_path)
        assert ddl == expected_ddl


def checking_fks_ddl(case_name):
    schema_name = "EXTORA_APP"
    db_metadata = get_metadata_from_files()
    df_foreign_keys = db_metadata["constraints"].loc[db_metadata["constraints"]["constraint_type"] == "R"]
    for db_foreign_key_row in df_foreign_keys.itertuples():
        foreign_key_dfs = m.get_foreign_key_dfs(db_foreign_key_row, db_metadata)
        foreign_key = m.Constraint(*foreign_key_dfs)
        foreign_key.generate_ddl()
        ddl = foreign_key.ddl
        file_path = f"test/fks__{case_name}/{schema_name.lower()}.{foreign_key.constraint_name.lower()}.sql"
        if update_expected_ddl_files:
            update_expected_ddl_file(file_path, ddl)
        expected_ddl = get_content_from_file(file_path)
        assert ddl == expected_ddl


def test_get_table_dfs():
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    db_table_row = df_tables.iloc[0]
    tabel_dfs = get_table_dfs(db_table_row, db_metadata)
    assert len(tabel_dfs) == 11


def test_table_ddl():
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    db_table_row = df_tables.iloc[0]
    tabel_dfs = get_table_dfs(db_table_row, db_metadata)
    table = m.Table(*tabel_dfs)
    table.generate_ddl()
    assert len(table.ddl) > 0


def test_store_ddl_into_file():
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    df_table = df_tables.iloc[0]
    tabel_dfs = m.get_table_dfs(df_table, db_metadata)
    table = m.Table(*tabel_dfs)
    table.generate_ddl()
    conf["file_path"]["table"] = "./test_results/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    table.store_ddl_into_file()
    file_path = conf["file_path"]["table"].format(OBJECT_OWNER=df_table.owner.upper(),
                                                  object_owner=df_table.owner.lower(),
                                                  object_name=df_table.table_name.lower())
    assert os.path.isfile(file_path)
    shutil.rmtree("./test_results")


def test_get_file_path_1():
    conf["file_path"]["table"] = "./{OBJECT_OWNER}/{object_type}/{OBJECT_OWNER}.{object_name}.sql"
    file_path = ut.get_file_path("table", "SCHEMA_NAME", "TABLE_NAME")
    assert file_path == "./SCHEMA_NAME/table/SCHEMA_NAME.table_name.sql"


def test_get_file_path_2():
    conf["file_path"]["trigger"] = "./{object_owner}/{OBJECT_TYPE}S/{object_owner}.{OBJECT_NAME}.trg"
    file_path = ut.get_file_path("trigger", "schema_name", "trigger_name")
    assert file_path == "./schema_name/TRIGGERS/schema_name.TRIGGER_NAME.trg"


def test_tables_ddl__1__uppercase__logging():
    conf["case"]["keyword"] = "uppercase"
    conf["case"]["identifier"] = "uppercase"
    conf["storage"]["storage"] = "with_storage"
    conf["storage"]["partitions"] = "all"
    conf["storage"]["collation"] = "yes"
    conf["storage"]["logging"] = "no"
    conf["storage"]["compression"] = "yes"
    conf["storage"]["cache"] = "yes"
    conf["storage"]["result_cache"] = "yes"
    conf["comments"]["comments"] = "yes"
    conf["comments"]["empty_line_after_comment"] = "yes"
    conf["comments"]["vertical_alignment"] = "yes"
    conf["indexes"] = "yes"
    conf["constraints"] = "yes"
    conf["prompts"] = "yes"
    conf["grants"] = "yes"
    checking_tables_ddl("1__uppercase__logging")


def test_tables_ddl__2__lowercase__compress():
    conf["case"]["keyword"] = "lowercase"
    conf["case"]["identifier"] = "lowercase"
    conf["storage"]["storage"] = "with_storage"
    conf["storage"]["partitions"] = "all"
    conf["storage"]["collation"] = "yes"
    conf["storage"]["logging"] = "yes"
    conf["storage"]["compression"] = "no"
    conf["storage"]["cache"] = "yes"
    conf["storage"]["result_cache"] = "yes"
    conf["comments"]["comments"] = "yes"
    conf["comments"]["empty_line_after_comment"] = "yes"
    conf["comments"]["vertical_alignment"] = "yes"
    conf["indexes"] = "yes"
    conf["constraints"] = "yes"
    conf["prompts"] = "yes"
    conf["grants"] = "yes"
    checking_tables_ddl("2__lowercase__compress")


def test_tables_ddl__3__no_storage():
    conf["case"]["keyword"] = "uppercase"
    conf["case"]["identifier"] = "uppercase"
    conf["storage"]["storage"] = "no_storage"
    conf["storage"]["partitions"] = "all"
    conf["storage"]["collation"] = "yes"
    conf["storage"]["logging"] = "yes"
    conf["storage"]["compression"] = "yes"
    conf["storage"]["cache"] = "no"
    conf["storage"]["result_cache"] = "yes"
    conf["comments"]["comments"] = "no"
    conf["comments"]["empty_line_after_comment"] = "yes"
    conf["comments"]["vertical_alignment"] = "yes"
    conf["indexes"] = "yes"
    conf["constraints"] = "yes"
    conf["prompts"] = "no"
    conf["grants"] = "yes"
    checking_tables_ddl("3__no_storage")


def test_tables_ddl__4__only_tablespace():
    conf["case"]["keyword"] = "uppercase"
    conf["case"]["identifier"] = "uppercase"
    conf["storage"]["storage"] = "only_tablespace"
    conf["storage"]["partitions"] = "none"
    conf["storage"]["collation"] = "yes"
    conf["storage"]["logging"] = "yes"
    conf["storage"]["compression"] = "yes"
    conf["storage"]["cache"] = "yes"
    conf["storage"]["result_cache"] = "no"
    conf["comments"]["comments"] = "no"
    conf["comments"]["empty_line_after_comment"] = "yes"
    conf["comments"]["vertical_alignment"] = "yes"
    conf["indexes"] = "yes"
    conf["constraints"] = "yes"
    conf["prompts"] = "no"
    conf["grants"] = "no"
    checking_tables_ddl("4__only_tablespace")


def test_tables_ddl__5__uppercase__lowercase__compact_part():
    conf["case"]["keyword"] = "uppercase"
    conf["case"]["identifier"] = "lowercase"
    conf["storage"]["storage"] = "with_storage"
    conf["storage"]["partitions"] = "compact"
    conf["storage"]["collation"] = "yes"
    conf["storage"]["logging"] = "yes"
    conf["storage"]["compression"] = "yes"
    conf["storage"]["cache"] = "no"
    conf["storage"]["result_cache"] = "yes"
    conf["comments"]["comments"] = "yes"
    conf["comments"]["empty_line_after_comment"] = "yes"
    conf["comments"]["vertical_alignment"] = "no"
    conf["indexes"] = "yes"
    conf["constraints"] = "yes"
    conf["prompts"] = "yes"
    conf["grants"] = "yes"
    checking_tables_ddl("5__uppercase__lowercase__compact_part")


def test_tables_ddl__6__lowercase__uppercase__no_empty_line():
    conf["case"]["keyword"] = "lowercase"
    conf["case"]["identifier"] = "uppercase"
    conf["storage"]["storage"] = "with_storage"
    conf["storage"]["partitions"] = "all"
    conf["storage"]["collation"] = "yes"
    conf["storage"]["logging"] = "yes"
    conf["storage"]["compression"] = "yes"
    conf["storage"]["cache"] = "yes"
    conf["storage"]["result_cache"] = "no"
    conf["comments"]["comments"] = "yes"
    conf["comments"]["empty_line_after_comment"] = "no"
    conf["comments"]["vertical_alignment"] = "yes"
    conf["indexes"] = "no"
    conf["constraints"] = "no"
    conf["prompts"] = "yes"
    conf["grants"] = "yes"
    checking_tables_ddl("6__lowercase__uppercase__no_empty_line")


def test_fk_1_lowercase_uppercase_no_prompt():
    conf["case"]["keyword"] = "lowercase"
    conf["case"]["identifier"] = "uppercase"
    conf["prompts"] = "no"
    checking_fks_ddl("1_lowercase_uppercase_no_prompt")


def test_fk_2_uppercase_lowercase_no_prompt():
    conf["case"]["keyword"] = "uppercase"
    conf["case"]["identifier"] = "lowercase"
    conf["prompts"] = "yes"
    checking_fks_ddl("2_uppercase_lowercase_no_prompt")


update_expected_ddl_files = False
if os.environ.get('RUN_LOCAL_ONLY', 'False') == 'True':
    update_expected_ddl_files = False
    store_metadata_into_xlsx()
    store_metadata_into_files()
