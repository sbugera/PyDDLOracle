"""Test main script."""

import os
import shutil

import pandas as pd
import main as m
import utils as ut
from config import config as c
from table import get_table_dfs
from db_metadata import get_db_metadata

if not os.path.isfile("config_con.yaml"):
    shutil.copyfile("config_con.template.yaml", "config_con.yaml")

c.conf = c.load_config("config.yaml")


def store_metadata_into_xlsx():
    """Store metadata into xlsx files."""
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

    df_tables.to_excel("tests/unit/dfs/df_tables.xlsx", index=False)
    df_all_tab_columns.to_excel(
        "tests/unit/dfs/df_all_tab_columns.xlsx", index=False
    )
    df_all_part_tables.to_excel(
        "tests/unit/dfs/df_all_part_tables.xlsx", index=False
    )
    df_all_part_key_columns.to_excel(
        "tests/unit/dfs/df_all_part_key_columns.xlsx", index=False
    )
    df_all_tab_partitions.to_excel(
        "tests/unit/dfs/df_all_tab_partitions.xlsx", index=False
    )
    df_all_comments.to_excel(
        "tests/unit/dfs/df_all_comments.xlsx", index=False
    )
    df_all_indexes.to_excel("tests/unit/dfs/df_all_indexes.xlsx", index=False)
    df_all_index_columns.to_excel(
        "tests/unit/dfs/df_all_index_columns.xlsx", index=False
    )
    df_all_constraints.to_excel(
        "tests/unit/dfs/df_all_constraints.xlsx", index=False
    )
    df_all_constraint_columns.to_excel(
        "tests/unit/dfs/df_all_constraint_columns.xlsx", index=False
    )
    df_all_grants.to_excel("tests/unit/dfs/df_all_grants.xlsx", index=False)


def store_metadata_into_files():
    """Store metadata into csv files."""
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

    df_tables.to_csv("tests/unit/dfs/df_tables.csv", index=False)
    df_all_tab_columns.to_csv(
        "tests/unit/dfs/df_all_tab_columns.csv", index=False
    )
    df_all_part_tables.to_csv(
        "tests/unit/dfs/df_all_part_tables.csv", index=False
    )
    df_all_part_key_columns.to_csv(
        "tests/unit/dfs/df_all_part_key_columns.csv", index=False
    )
    df_all_tab_partitions.to_csv(
        "tests/unit/dfs/df_all_tab_partitions.csv", index=False
    )
    df_all_comments.to_csv("tests/unit/dfs/df_all_comments.csv", index=False)
    df_all_indexes.to_csv("tests/unit/dfs/df_all_indexes.csv", index=False)
    df_all_index_columns.to_csv(
        "tests/unit/dfs/df_all_index_columns.csv", index=False
    )
    df_all_constraints.to_csv(
        "tests/unit/dfs/df_all_constraints.csv", index=False
    )
    df_all_constraint_columns.to_csv(
        "tests/unit/dfs/df_all_constraint_columns.csv", index=False
    )
    df_all_grants.to_csv("tests/unit/dfs/df_all_grants.csv", index=False)


def get_metadata_from_xlsx():
    """Get metadata from xlsx files."""
    df_tables = pd.read_excel("tests/unit/dfs/df_tables.xlsx", na_values=[""])
    df_all_tab_columns = pd.read_excel(
        "tests/unit/dfs/df_all_tab_columns.xlsx", na_values=[""]
    )
    df_all_part_tables = pd.read_excel(
        "tests/unit/dfs/df_all_part_tables.xlsx", na_values=[""]
    )
    df_all_part_key_columns = pd.read_excel(
        "tests/unit/dfs/df_all_part_key_columns.xlsx", na_values=[""]
    )
    df_all_tab_partitions = pd.read_excel(
        "tests/unit/dfs/df_all_tab_partitions.xlsx", na_values=[""]
    )
    df_all_comments = pd.read_excel(
        "tests/unit/dfs/df_all_comments.xlsx", na_values=[""]
    )
    df_all_indexes = pd.read_excel(
        "tests/unit/dfs/df_all_indexes.xlsx", na_values=[""]
    )
    df_all_index_columns = pd.read_excel(
        "tests/unit/dfs/df_all_index_columns.xlsx", na_values=[""]
    )
    df_all_constraints = pd.read_excel(
        "tests/unit/dfs/df_all_constraints.xlsx", na_values=[""]
    )
    df_all_constraint_columns = pd.read_excel(
        "tests/unit/dfs/df_all_constraint_columns.xlsx", na_values=[""]
    )
    df_all_grants = pd.read_excel(
        "tests/unit/dfs/df_all_grants.xlsx", na_values=[""]
    )

    metadata = {
        "tables": df_tables,
        "tab_columns": df_all_tab_columns,
        "part_tables": df_all_part_tables,
        "part_key_columns": df_all_part_key_columns,
        "tab_partitions": df_all_tab_partitions,
        "comments": df_all_comments,
        "indexes": df_all_indexes,
        "index_columns": df_all_index_columns,
        "constraints": df_all_constraints,
        "constraint_columns": df_all_constraint_columns,
        "grants": df_all_grants,
    }
    return metadata


def get_metadata_from_files():
    """Get metadata from csv files."""
    df_tables = pd.read_csv("tests/unit/dfs/df_tables.csv", na_values=[""])
    df_all_tab_columns = pd.read_csv(
        "tests/unit/dfs/df_all_tab_columns.csv", na_values=[""]
    )
    df_all_part_tables = pd.read_csv(
        "tests/unit/dfs/df_all_part_tables.csv", na_values=[""]
    )
    df_all_part_key_columns = pd.read_csv(
        "tests/unit/dfs/df_all_part_key_columns.csv", na_values=[""]
    )
    df_all_tab_partitions = pd.read_csv(
        "tests/unit/dfs/df_all_tab_partitions.csv", na_values=[""]
    )
    df_all_comments = pd.read_csv(
        "tests/unit/dfs/df_all_comments.csv", na_values=[""]
    )
    df_all_indexes = pd.read_csv(
        "tests/unit/dfs/df_all_indexes.csv", na_values=[""]
    )
    df_all_index_columns = pd.read_csv(
        "tests/unit/dfs/df_all_index_columns.csv", na_values=[""]
    )
    df_all_constraints = pd.read_csv(
        "tests/unit/dfs/df_all_constraints.csv", na_values=[""]
    )
    df_all_constraint_columns = pd.read_csv(
        "tests/unit/dfs/df_all_constraint_columns.csv", na_values=[""]
    )
    df_all_grants = pd.read_csv(
        "tests/unit/dfs/df_all_grants.csv", na_values=[""]
    )

    metadata = {
        "tables": df_tables,
        "tab_columns": df_all_tab_columns,
        "part_tables": df_all_part_tables,
        "part_key_columns": df_all_part_key_columns,
        "tab_partitions": df_all_tab_partitions,
        "comments": df_all_comments,
        "indexes": df_all_indexes,
        "index_columns": df_all_index_columns,
        "constraints": df_all_constraints,
        "constraint_columns": df_all_constraint_columns,
        "grants": df_all_grants,
    }
    return metadata


def get_content_from_file(file_path):
    """Get content of file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""
    return content


def update_expected_ddl_file(file_path, ddl):
    """Update expected DDL file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(ddl)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(ddl)


def checking_tables_ddl(case_name):
    """Check DDL of tables."""
    schema_name = "EXTORA_APP"
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    for db_table_row in df_tables.itertuples():
        tabel_dfs = m.get_table_dfs(db_table_row, db_metadata)
        table = m.Table(*tabel_dfs)
        table.generate_ddl()
        ddl = table.ddl
        file_path = (
            f"tests/unit/tables__{case_name}/{schema_name.lower()}"
            f".{table.table_name.lower()}.sql"
        )
        if UPDATE_EXPECTED_DDL_FILES:
            update_expected_ddl_file(file_path, ddl)
        expected_ddl = get_content_from_file(file_path)
        assert ddl == expected_ddl


def checking_fks_ddl(case_name):
    """Check DDL of foreign keys."""
    schema_name = "EXTORA_APP"
    db_metadata = get_metadata_from_files()
    df_foreign_keys = db_metadata["constraints"].loc[
        db_metadata["constraints"]["constraint_type"] == "R"
    ]
    for db_foreign_key_row in df_foreign_keys.itertuples():
        foreign_key_dfs = m.get_foreign_key_dfs(
            db_foreign_key_row, db_metadata
        )
        foreign_key = m.Constraint(*foreign_key_dfs)
        foreign_key.generate_ddl()
        ddl = foreign_key.ddl
        file_path = (
            f"tests/unit/fks__{case_name}/{schema_name.lower()}"
            f".{foreign_key.constraint_name.lower()}.sql"
        )
        if UPDATE_EXPECTED_DDL_FILES:
            update_expected_ddl_file(file_path, ddl)
        expected_ddl = get_content_from_file(file_path)
        assert ddl == expected_ddl


def test_get_table_dfs():
    """Test get_table_dfs function."""
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    db_table_row = df_tables.iloc[0]
    tabel_dfs = get_table_dfs(db_table_row, db_metadata)
    assert len(tabel_dfs) == 11


def test_table_ddl():
    """Test table DDL generation."""
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    db_table_row = df_tables.iloc[0]
    tabel_dfs = get_table_dfs(db_table_row, db_metadata)
    table = m.Table(*tabel_dfs)
    table.generate_ddl()
    assert len(table.ddl) > 0


def test_store_ddl_into_file():
    """Test store DDL into file."""
    db_metadata = get_metadata_from_files()
    df_tables = db_metadata["tables"]
    df_table = df_tables.iloc[0]
    tabel_dfs = m.get_table_dfs(df_table, db_metadata)
    table = m.Table(*tabel_dfs)
    table.generate_ddl()
    c.conf["file_path"][
        "table"
    ] = "./test_results/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    table.store_ddl_into_file()
    file_path = c.conf["file_path"]["table"].format(
        OBJECT_OWNER=df_table.owner.upper(),
        object_owner=df_table.owner.lower(),
        object_name=df_table.table_name.lower(),
    )
    assert os.path.isfile(file_path)
    shutil.rmtree("./test_results")


def test_get_file_path_1():
    """Test get_file_path function."""
    c.conf["file_path"][
        "table"
    ] = "./{OBJECT_OWNER}/{object_type}/{OBJECT_OWNER}.{object_name}.sql"
    file_path = ut.get_file_path("table", "SCHEMA_NAME", "TABLE_NAME")
    assert file_path == "./SCHEMA_NAME/table/SCHEMA_NAME.table_name.sql"


def test_get_file_path_2():
    """Test get_file_path function."""
    c.conf["file_path"][
        "trigger"
    ] = "./{object_owner}/{OBJECT_TYPE}S/{object_owner}.{OBJECT_NAME}.trg"
    file_path = ut.get_file_path("trigger", "schema_name", "trigger_name")
    assert file_path == "./schema_name/TRIGGERS/schema_name.TRIGGER_NAME.trg"


def test_tables_ddl__1__uppercase__logging():
    """Test tables DDL generation."""
    c.conf["case"]["keyword"] = "uppercase"
    c.conf["case"]["identifier"] = "uppercase"
    c.conf["storage"]["storage"] = "with_storage"
    c.conf["storage"]["partitions"] = "all"
    c.conf["storage"]["collation"] = "yes"
    c.conf["storage"]["logging"] = "no"
    c.conf["storage"]["compression"] = "yes"
    c.conf["storage"]["cache"] = "yes"
    c.conf["storage"]["result_cache"] = "yes"
    c.conf["comments"]["comments"] = "yes"
    c.conf["comments"]["empty_line_after_comment"] = "yes"
    c.conf["comments"]["vertical_alignment"] = "yes"
    c.conf["indexes"] = "yes"
    c.conf["constraints"] = "yes"
    c.conf["prompts"] = "yes"
    c.conf["grants"] = "yes"
    checking_tables_ddl("1__uppercase__logging")


def test_tables_ddl__2__lowercase__compress():
    """Test tables DDL generation."""
    c.conf["case"]["keyword"] = "lowercase"
    c.conf["case"]["identifier"] = "lowercase"
    c.conf["storage"]["storage"] = "with_storage"
    c.conf["storage"]["partitions"] = "all"
    c.conf["storage"]["collation"] = "yes"
    c.conf["storage"]["logging"] = "yes"
    c.conf["storage"]["compression"] = "no"
    c.conf["storage"]["cache"] = "yes"
    c.conf["storage"]["result_cache"] = "yes"
    c.conf["comments"]["comments"] = "yes"
    c.conf["comments"]["empty_line_after_comment"] = "yes"
    c.conf["comments"]["vertical_alignment"] = "yes"
    c.conf["indexes"] = "yes"
    c.conf["constraints"] = "yes"
    c.conf["prompts"] = "yes"
    c.conf["grants"] = "yes"
    checking_tables_ddl("2__lowercase__compress")


def test_tables_ddl__3__no_storage():
    """Test tables DDL generation."""
    c.conf["case"]["keyword"] = "uppercase"
    c.conf["case"]["identifier"] = "uppercase"
    c.conf["storage"]["storage"] = "no_storage"
    c.conf["storage"]["partitions"] = "all"
    c.conf["storage"]["collation"] = "yes"
    c.conf["storage"]["logging"] = "yes"
    c.conf["storage"]["compression"] = "yes"
    c.conf["storage"]["cache"] = "no"
    c.conf["storage"]["result_cache"] = "yes"
    c.conf["comments"]["comments"] = "no"
    c.conf["comments"]["empty_line_after_comment"] = "yes"
    c.conf["comments"]["vertical_alignment"] = "yes"
    c.conf["indexes"] = "yes"
    c.conf["constraints"] = "yes"
    c.conf["prompts"] = "no"
    c.conf["grants"] = "yes"
    checking_tables_ddl("3__no_storage")


def test_tables_ddl__4__only_tablespace():
    """Test tables DDL generation."""
    c.conf["case"]["keyword"] = "uppercase"
    c.conf["case"]["identifier"] = "uppercase"
    c.conf["storage"]["storage"] = "only_tablespace"
    c.conf["storage"]["partitions"] = "none"
    c.conf["storage"]["collation"] = "yes"
    c.conf["storage"]["logging"] = "yes"
    c.conf["storage"]["compression"] = "yes"
    c.conf["storage"]["cache"] = "yes"
    c.conf["storage"]["result_cache"] = "no"
    c.conf["comments"]["comments"] = "no"
    c.conf["comments"]["empty_line_after_comment"] = "yes"
    c.conf["comments"]["vertical_alignment"] = "yes"
    c.conf["indexes"] = "yes"
    c.conf["constraints"] = "yes"
    c.conf["prompts"] = "no"
    c.conf["grants"] = "no"
    checking_tables_ddl("4__only_tablespace")


def test_tables_ddl__5__uppercase__lowercase__compact_part():
    """Test tables DDL generation."""
    c.conf["case"]["keyword"] = "uppercase"
    c.conf["case"]["identifier"] = "lowercase"
    c.conf["storage"]["storage"] = "with_storage"
    c.conf["storage"]["partitions"] = "compact"
    c.conf["storage"]["collation"] = "yes"
    c.conf["storage"]["logging"] = "yes"
    c.conf["storage"]["compression"] = "yes"
    c.conf["storage"]["cache"] = "no"
    c.conf["storage"]["result_cache"] = "yes"
    c.conf["comments"]["comments"] = "yes"
    c.conf["comments"]["empty_line_after_comment"] = "yes"
    c.conf["comments"]["vertical_alignment"] = "no"
    c.conf["indexes"] = "yes"
    c.conf["constraints"] = "yes"
    c.conf["prompts"] = "yes"
    c.conf["grants"] = "yes"
    checking_tables_ddl("5__uppercase__lowercase__compact_part")


def test_tables_ddl__6__lowercase__uppercase__no_empty_line():
    """Test tables DDL generation."""
    c.conf["case"]["keyword"] = "lowercase"
    c.conf["case"]["identifier"] = "uppercase"
    c.conf["storage"]["storage"] = "with_storage"
    c.conf["storage"]["partitions"] = "all"
    c.conf["storage"]["collation"] = "yes"
    c.conf["storage"]["logging"] = "yes"
    c.conf["storage"]["compression"] = "yes"
    c.conf["storage"]["cache"] = "yes"
    c.conf["storage"]["result_cache"] = "no"
    c.conf["comments"]["comments"] = "yes"
    c.conf["comments"]["empty_line_after_comment"] = "no"
    c.conf["comments"]["vertical_alignment"] = "yes"
    c.conf["indexes"] = "no"
    c.conf["constraints"] = "no"
    c.conf["prompts"] = "yes"
    c.conf["grants"] = "yes"
    checking_tables_ddl("6__lowercase__uppercase__no_empty_line")


def test_fk_1_lowercase_uppercase_no_prompt():
    """Test foreign keys DDL generation."""
    c.conf["case"]["keyword"] = "lowercase"
    c.conf["case"]["identifier"] = "uppercase"
    c.conf["prompts"] = "no"
    checking_fks_ddl("1_lowercase_uppercase_no_prompt")


def test_fk_2_uppercase_lowercase_no_prompt():
    """Test foreign keys DDL generation."""
    c.conf["case"]["keyword"] = "uppercase"
    c.conf["case"]["identifier"] = "lowercase"
    c.conf["prompts"] = "yes"
    checking_fks_ddl("2_uppercase_lowercase_no_prompt")


UPDATE_EXPECTED_DDL_FILES = False
if os.environ.get("RUN_LOCAL_ONLY", "False") == "True":
    UPDATE_EXPECTED_DDL_FILES = False
    store_metadata_into_xlsx()
    store_metadata_into_files()
