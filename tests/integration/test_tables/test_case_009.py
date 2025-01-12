from .base_table_test import BaseTableTest


class TestCase9(BaseTableTest):
    """No cache, no compression"""

    testcase_number = "9"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

storage:
  storage: "with_storage"

  partitions: "all"
  collation: "yes"
  logging: "yes"
  compression: "no"
  cache: "no"
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
    table: "<:PATH>/ddls/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql"
"""
