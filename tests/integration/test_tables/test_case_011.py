from .base_table_test import BaseTableTest


class TestCase11(BaseTableTest):
    """No storage, no indexes, no partitions"""

    testcase_number = "11"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

storage:
  storage: "no_storage"

  partitions: "none"
  collation: "no"
  logging: "no"
  compression: "no"
  cache: "no"
  result_cache: "no"

comments:
  comments: "no"
  empty_line_after_comment: "no"
  vertical_alignment: "no"

indexes: "no"
constraints: "no"
prompts: "no"
grants: "no"

file_path:
    table: "<:PATH>/ddls/{OBJECT_OWNER}/table.{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key.{object_owner}.{object_name}.sql"
"""
