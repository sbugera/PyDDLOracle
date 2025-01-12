from .base_table_test import BaseTableTest

class TestCase3(BaseTableTest):
    """All parameters enabled with uppercase kewords and lowercase identifiers."""

    testcase_number = "3"
    config_content = """
case:
  keyword: "uppercase"
  identifier: "lowercase"

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