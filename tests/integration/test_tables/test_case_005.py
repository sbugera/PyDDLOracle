from .base_table_test import BaseTableTest


class TestCase5(BaseTableTest):
    """No storage parameters, no comments, no prompts, no grants."""

    testcase_number = "5"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

storage:
  storage: "no_storage"

  partitions: "all"
  collation: "yes"
  logging: "yes"
  compression: "yes"
  cache: "yes"
  result_cache: "yes"

comments:
  comments: "no"
  empty_line_after_comment: "yes"
  vertical_alignment: "yes"

indexes: "yes"
constraints: "yes"
prompts: "no"
grants: "no"

file_path:
    table: "<:PATH>/ddls/{OBJECT_OWNER}/tables/{object_owner}.{object_name}.sql"
    foreign_key: "<:PATH>/ddls/{OBJECT_OWNER}/foreign_key/{object_owner}.{object_name}.sql"
"""
