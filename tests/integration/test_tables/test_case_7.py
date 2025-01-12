from .base_table_test import BaseTableTest


class TestCase7(BaseTableTest):
    """Srorage - only tablespace, no comments, no constraints"""

    testcase_number = "7"
    config_content = """
case:
  keyword: "lowercase"
  identifier: "uppercase"

storage:
  storage: "only_tablespace"

  partitions: "all"
  collation: "yes"
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
    table: "<:PATH>/ddls/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql"
"""
