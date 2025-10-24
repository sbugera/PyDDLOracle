from .base_table_test import BaseTableTest


class TestCase8(BaseTableTest):
    """No result cache, no logging"""

    testcase_number = "8"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

storage:
  storage: "with_storage"

  partitions: "all"
  collation: "yes"
  logging: "no"
  compression: "yes"
  cache: "yes"
  result_cache: "no"

comments:
  comments: "no"
  empty_line_after_comment: "no"
  vertical_alignment: "no"

indexes: "yes"
constraints: "no"
prompts: "yes"
grants: "no"

file_path:
    table: "<:PATH>/ddls/{OBJECT_OWNER}/table.{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key.{object_owner}.{object_name}.sql"
"""
