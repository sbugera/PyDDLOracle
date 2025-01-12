from .base_table_test import BaseTableTest

class TestCase1(BaseTableTest):
    """All parameters enabled with uppercase letters."""

    testcase_number = "1"
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
    table: "<:PATH>/ddls/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql"
"""
