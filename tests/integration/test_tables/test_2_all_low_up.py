"""Test for tables with enabled all parameters and lowercase kewords and uppercase identifiers."""

import os
import shutil
import subprocess
import pytest

TESTCASE_NUMBER = "2"
CONFIG_FILE_PATH = "config_test_all_low_up.yaml"


@pytest.fixture
def config_file():
    """Create configuration for testing."""
    config_content = """
case:
  keyword: "lowercase"
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

    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)

    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(config_content)

    yield


@pytest.fixture
def cleanup_ddl():
    """Remove generated DDL files after test."""
    if os.path.exists("./ddls"):
        shutil.rmtree("./ddls")

    yield


def test_baseline_liquibase_update_sql():
    """Test baseline liquibase generation of update SQL."""
    os.environ["LIQUIBASE_HOME"] = "./liquibase"
    result = subprocess.run(
        [
            "java",
            "-jar",
            "./liquibase/internal/lib/liquibase-core.jar",
            "--defaultsFile=./liquibase/liquibase.properties",
            "--changeLogFile=./liquibase/migrations/master_changelog.xml",
            "update-sql",
        ],
        capture_output=True,
        text=True,
    )

    with open(
        f"./tests/integration/test_tables/test_{TESTCASE_NUMBER}_expected_scripts/baseline-update.sql",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(result.stdout)

    assert (
        result.returncode == 0
    ), f"Baseline Liquibase update-sql failed with error: {result.stderr}"


def test_baseline_database_sqlplus_deployment():
    """Test deployment of generated baseline DDL to Oracle database using SQL*Plus."""
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_service = os.getenv("DB_SERVICE")

    result = subprocess.run(
        [
            "sqlplus",
            "-S",
            f"{db_user}/{db_pass}@{db_host}:{db_port}/{db_service}",
            f"@tests/integration/test_tables/test_{TESTCASE_NUMBER}_expected_scripts/baseline-update.sql",
        ],
        capture_output=True,
        text=True,
    )

    assert (
        result.returncode == 0
    ), f"Baseline SQL*Plus deployment failed with error: {result.stderr}"

    assert (
        "Tables dropped" in result.stdout
    ), "Baseline SQL*Plus deployment did not drop tables"


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


def test_generated_ddl():
    """Test generated DDL against expected DDL."""
    table_files = os.listdir("./ddls/PYDDL_TEST/tables")

    for script in table_files:
        with open(
            f"./ddls/PYDDL_TEST/tables/{script}", "r", encoding="utf-8"
        ) as f:
            generated_ddl = f.read()

        current_script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(
            f"{current_script_dir}/test_{TESTCASE_NUMBER}_expected_scripts/{script}",
            "r",
            encoding="utf-8",
        ) as f:
            expected_ddl = f.read()

        assert (
            generated_ddl == expected_ddl
        ), f"Generated DDL does not match expected DDL for {script}"


def test_liquibase_update_sql():
    """Test liquibase generation of update SQL."""
    os.environ["LIQUIBASE_HOME"] = "./liquibase"
    result = subprocess.run(
        [
            "java",
            "-jar",
            "./liquibase/internal/lib/liquibase-core.jar",
            "--defaultsFile=./liquibase/liquibase.properties",
            f"--changeLogFile=./tests/integration/test_tables/test_{TESTCASE_NUMBER}_expected_scripts/changelog.xml",
            "update-sql",
        ],
        capture_output=True,
        text=True,
    )

    with open(
        f"./tests/integration/test_tables/test_{TESTCASE_NUMBER}_expected_scripts/update.sql",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(result.stdout)

    assert (
        result.returncode == 0
    ), f"Liquibase diff failed with error: {result.stderr}"


def test_database_sqlplus_deployment():
    """Test deployment of generated DDL to Oracle database using SQL*Plus."""
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_service = os.getenv("DB_SERVICE")

    result = subprocess.run(
        [
            "sqlplus",
            "-S",
            f"{db_user}/{db_pass}@{db_host}:{db_port}/{db_service}",
            f"@tests/integration/test_tables/test_{TESTCASE_NUMBER}_expected_scripts/update.sql",
        ],
        capture_output=True,
        text=True,
    )

    assert (
        result.returncode == 0
    ), f"SQL*Plus deployment failed with error: {result.stderr}"

    assert (
        "Tables dropped" in result.stdout
    ), "SQL*Plus deployment did not drop tables"
