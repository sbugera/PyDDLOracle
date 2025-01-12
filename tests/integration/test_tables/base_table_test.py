"""Base test class and implementations for table DDL generation tests."""

import os
import shutil
import subprocess
import pytest
from abc import ABC, abstractmethod


class BaseTableTest(ABC):
    """Base class for table DDL generation tests."""

    testcase_number = None
    config_content = None

    @property
    def test_results_path(self) -> str:
        """Get the test results path."""
        return f"./tests/integration/test_tables/test_results/{self.testcase_number}"

    @property
    def config_file_path(self) -> str:
        """Get the config file path."""
        return f"{self.test_results_path}/config_test.yaml"

    @classmethod
    def setup_class(cls):
        """Set up required directories before any tests in the class run."""
        test_path = f"./tests/integration/test_tables/test_results/{cls.testcase_number}/ddls/PYDDL_TEST/tables"
        print(f"Setting up test path: {test_path}")
        if not os.path.exists(test_path):
            os.makedirs(test_path)

    @pytest.fixture
    def config_file(self):
        """Create configuration for testing."""
        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

        with open(self.config_file_path, "w", encoding="utf-8") as f:
            f.write(self.config_content.replace("<:PATH>", self.test_results_path))

        yield

    @pytest.fixture
    def cleanup_ddl(self):
        """Remove generated DDL files after test."""
        if os.path.exists(f"{self.test_results_path}/ddls"):
            shutil.rmtree(f"{self.test_results_path}/ddls")

        yield

    def test_baseline_liquibase_update_sql(self):
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
            f"{self.test_results_path}/baseline-update.sql",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result.stdout)
            f.write("\nCOMMIT;")
            f.write("\nEXIT;")

        assert (
            result.returncode == 0
        ), f"Baseline Liquibase update-sql failed with error: {result.stderr}"

    def test_baseline_database_sqlplus_deployment(self):
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
                f"@{self.test_results_path}/baseline-update.sql",
            ],
            capture_output=True,
            text=True,
        )

        with open(
            f"{self.test_results_path}/baseline-deployment.log",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result.stdout)

        assert (
            result.returncode == 0
        ), f"Baseline SQL*Plus deployment failed with error: {result.stderr}"

        assert (
            "ORA-" not in result.stdout and "SP2-" not in result.stdout
        ), "Baseline SQL*Plus deployment failed with ORA or SP2 error"

        assert (
            "Tables dropped" in result.stdout
        ), "Baseline SQL*Plus deployment did not drop tables"

    def test_main_execution(self, config_file, cleanup_ddl):
        """Test execution of main.py with PYDDL_TEST schema."""
        result = subprocess.run(
            [
                ".venv/bin/python",
                "main.py",
                "-s",
                "PYDDL_TEST",
                "-c",
                self.config_file_path,
            ],
            capture_output=True,
            text=True,
        )

        print(result.stdout)

        assert (
            result.returncode == 0
        ), f"Process failed with error: {result.stderr}"

    def get_ddl_files(self):
        """Get list of generated DDL files."""
        return os.listdir(f"{self.test_results_path}/ddls/PYDDL_TEST/tables")

    def test_generated_ddl(self):
        """Test all generated DDL files against expected DDL."""
        for script in self.get_ddl_files():
            """Test generated DDL against expected DDL."""
            with open(
                f"{self.test_results_path}/ddls/PYDDL_TEST/tables/{script}",
                "r",
                encoding="utf-8",
            ) as f:
                generated_ddl = f.read()

            current_script_dir = os.path.dirname(os.path.realpath(__file__))
            with open(
                f"{current_script_dir}/test_{self.testcase_number}_expected_scripts/{script}",
                "r",
                encoding="utf-8",
            ) as f:
                expected_ddl = f.read()

            assert (
                generated_ddl == expected_ddl
            ), f"Generated DDL does not match expected DDL for {script}"

    def test_liquibase_update_sql(self):
        """Test liquibase generation of update SQL."""
        os.environ["LIQUIBASE_HOME"] = "./liquibase"
        result = subprocess.run(
            [
                "java",
                "-jar",
                "./liquibase/internal/lib/liquibase-core.jar",
                "--defaultsFile=./liquibase/liquibase.properties",
                f"--changeLogFile=./tests/integration/test_tables/test_{self.testcase_number}_expected_scripts/changelog.xml",
                "update-sql",
            ],
            capture_output=True,
            text=True,
        )

        with open(
            f"{self.test_results_path}/update.sql",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result.stdout)
            f.write("\nCOMMIT;")
            f.write("\nEXIT;")

        assert (
            result.returncode == 0
        ), f"Liquibase diff failed with error: {result.stderr}"

    def test_database_sqlplus_deployment(self):
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
                f"@{self.test_results_path}/update.sql",
            ],
            capture_output=True,
            text=True,
        )

        with open(
            f"{self.test_results_path}/deployment.log",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result.stdout)

        assert (
            result.returncode == 0
        ), f"SQL*Plus deployment failed with error: {result.stderr}"

        assert (
            "ORA-" not in result.stdout and "SP2-" not in result.stdout
        ), "SQL*Plus deployment failed with ORA or SP2 error"

        assert (
            "Tables dropped" in result.stdout
        ), "SQL*Plus deployment did not drop tables"
