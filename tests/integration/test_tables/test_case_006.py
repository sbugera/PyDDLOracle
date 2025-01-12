from .base_table_test import BaseTableTest


class TestCase6(BaseTableTest):
    """Srorage - only tablespace, comments - no empty line after comment, no vertical alignment."""

    testcase_number = "6"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

storage:
  storage: "only_tablespace"

  partitions: "all"
  collation: "yes"
  logging: "yes"
  compression: "yes"
  cache: "yes"
  result_cache: "yes"

comments:
  comments: "yes"
  empty_line_after_comment: "no"
  vertical_alignment: "no"

indexes: "yes"
constraints: "yes"
prompts: "no"
grants: "no"

file_path:
    table: "<:PATH>/ddls/{OBJECT_OWNER}/table.{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key.{object_owner}.{object_name}.sql"
"""
