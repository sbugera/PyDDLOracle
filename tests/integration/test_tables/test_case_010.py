from .base_table_test import BaseTableTest


class TestCase10(BaseTableTest):
    """No collation, compact partitioning"""

    testcase_number = "10"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

storage:
  storage: "with_storage"

  partitions: "compact"
  collation: "no"
  logging: "yes"
  compression: "yes"
  cache: "yes"
  result_cache: "yes"

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
