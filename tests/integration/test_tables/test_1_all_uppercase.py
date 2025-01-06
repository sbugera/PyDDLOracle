"""Test for tables with enabled all parameters and uppercase letters."""

import os
import shutil
import subprocess
import pytest


@pytest.fixture
def config_file():
    """Create config.yaml for testing."""
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
    table: "../ddls/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    foreign_key: "../ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql"
"""
    
    with open('config2.yaml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    yield
    
    # if os.path.exists('config2.yaml'):
    #     os.remove('config2.yaml')


@pytest.fixture
def cleanup_ddl():
    """Remove generated DDL files after test."""
    yield
    if os.path.exists('./ddls'):
        shutil.rmtree('./ddls')


def test_main_execution(config_file, cleanup_ddl):
    """Test execution of main.py with PYDDL_TEST schema."""
    # Execute main.py as a subprocess
    result = subprocess.run(['python', 'main.py', '-s', 'PYDDL_TEST'], 
                          capture_output=True, 
                          text=True)
    print(result.returncode)
    print(result.stdout)

    
    # Check if process executed successfully
    assert result.returncode == 0, \
        f"Process failed with error: {result.stderr}"
    
    # Verify DDL directory was created
    assert os.path.exists('./ddls/PYDDL_TEST/tables'), \
        "DDL directory structure was not created"
    
    # Check if any DDL files were generated
    table_files = os.listdir('./ddls/PYDDL_TEST/tables')
    assert len(table_files) > 0, "No DDL files were generated"
    
    # Verify content of one of the files
    with open(f'./ddls/PYDDL_TEST/tables/{table_files[0]}', 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'CREATE TABLE' in content, \
            "Generated DDL does not contain CREATE TABLE statement"
