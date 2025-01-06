"""Test for tables with enabled all parameters and uppercase letters."""

import os
import shutil
import subprocess
import pytest

CONFIG_FILE_PATH = "config_all_uppercase.yaml"


@pytest.fixture
def config_file():
    """Create configuration for testing."""
    config_content = """
case:
  keyword: "uppercase"
  identifier: "uppercase"

storage:
  storage: "with_storage"

  partitions: "all"
  collation: "yes"
  logging: "yes"
  compression: "yes"
  cache: "yes"
  result_cache: "yes"

comments:
  comments: "yes"
  empty_line_after_comment: "yes"
  vertical_alignment: "yes"

indexes: "yes"
constraints: "yes"
prompts: "yes"
grants: "yes"

file_path:
    table: "./ddls/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    foreign_key: "./ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql"
"""

    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(config_content)

    yield

    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)


@pytest.fixture
def cleanup_ddl():
    """Remove generated DDL files after test."""
    yield

    if os.path.exists("./ddls"):
        shutil.rmtree("./ddls")


def test_main_execution(config_file, cleanup_ddl):
    """Test execution of main.py with PYDDL_TEST schema."""
    result = subprocess.run(
        [
            ".venv/bin/python",
            "main.py",
            "-s",
            "PYDDL_TEST",
            "-c",
            CONFIG_FILE_PATH,
        ],
        capture_output=True,
        text=True,
    )

    assert (
        result.returncode == 0
    ), f"Process failed with error: {result.stderr}"

    table_files = os.listdir("./ddls/PYDDL_TEST/tables")

    for script in table_files:
        with open(
            f"./ddls/PYDDL_TEST/tables/{script}", "r", encoding="utf-8"
        ) as f:
            generated_ddl = f.read()

        current_script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(
            f"{current_script_dir}/test_1_expected_scripts/{script}",
            "r",
            encoding="utf-8",
        ) as f:
            expected_ddl = f.read()

        assert (
            generated_ddl == expected_ddl
        ), f"Generated DDL does not match expected DDL for {script}"
