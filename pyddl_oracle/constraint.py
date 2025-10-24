"""Handles Oracle database constraint definitions and DDL generation."""

from pyddl_oracle.db_metadata import DBMetadata
from pyddl_oracle.utils import (
    get_case_formatted,
    get_file_path,
    get_object_name,
    get_prompt,
    prepare_directories,
)


def get_foreign_key_dfs(foreign_key_row, metadata: DBMetadata):
    """Get DataFrames with columns involved in foreign key relationship."""
    df_foreign_key_columns = metadata.constraint_columns[
        (
            metadata.constraint_columns["constraint_name"]
            == foreign_key_row.constraint_name
        )
        & (metadata.constraint_columns["owner"] == foreign_key_row.owner)
    ]

    df_remote_key_columns = metadata.constraint_columns[
        (
            metadata.constraint_columns["constraint_name"]
            == foreign_key_row.r_constraint_name
        )
        & (metadata.constraint_columns["owner"] == foreign_key_row.r_owner)
    ]

    return foreign_key_row, df_foreign_key_columns, df_remote_key_columns


class Constraint:  # pylint: disable=too-many-instance-attributes
    """Oracle database constraint with DDL generation."""

    def __init__(
        self,
        constraint_row,
        constraint_columns,
        constraint_columns_remote=None,
    ):
        self.ddl = ""
        self.owner = constraint_row.owner
        self.table_name = constraint_row.table_name
        self.constraint_name = constraint_row.constraint_name
        self.constraint_type = constraint_row.constraint_type
        self.search_condition = constraint_row.search_condition
        self.status = constraint_row.status
        self.deferrable = constraint_row.deferrable
        self.deferred = constraint_row.deferred
        self.validated = constraint_row.validated
        self.index_owner = constraint_row.index_owner
        self.index_name = constraint_row.index_name
        self.r_owner = constraint_row.r_owner
        self.r_table_name = constraint_row.r_table_name
        self.r_constraint_name = constraint_row.r_constraint_name
        self.delete_rule = constraint_row.delete_rule
        self.constraint_columns = constraint_columns
        self.constraint_columns_remote = constraint_columns_remote

    def _get_r_table_name(self):
        if self.r_table_name and str(self.r_table_name) not in ("nan", "None"):
            return get_object_name(
                self.r_owner, self.r_table_name, "identifier"
            )
        return ""

    def _get_constraint_columns(self):
        columns = ""
        for i, constraint_column in enumerate(
            self.constraint_columns.itertuples()
        ):
            columns += get_case_formatted(
                constraint_column.column_name, "identifier"
            )
            if i != len(self.constraint_columns) - 1:
                columns += ", "
        return columns

    def _get_r_constraint_columns(self):
        columns = ""
        if (
            self.constraint_columns_remote is not None
            and not self.constraint_columns_remote.empty
        ):
            for i, r_constraint_column in enumerate(
                self.constraint_columns_remote.itertuples()
            ):
                columns += get_case_formatted(
                    r_constraint_column.column_name, "identifier"
                )
                if i != len(self.constraint_columns_remote) - 1:
                    columns += ", "
        return columns

    def _get_start_of_statement(self, standalone, table_name):
        if standalone:
            return get_case_formatted(
                "ALTER TABLE <:1> ADD (\n", "keyword"
            ).replace("<:1>", table_name)
        return ""

    def _get_statement_template(self):
        statement = ""
        if self.constraint_type == "P":
            statement = get_case_formatted(
                "  CONSTRAINT <:1>\n  PRIMARY KEY (<:2>)", "keyword"
            )
        elif self.constraint_type == "U":
            statement = get_case_formatted(
                "  CONSTRAINT <:1>\n  UNIQUE (<:2>)", "keyword"
            )
        elif self.constraint_type == "C":
            statement = get_case_formatted(
                "  CONSTRAINT <:1>\n  CHECK (<:2>)", "keyword"
            )
        elif self.constraint_type == "R":
            statement = get_case_formatted(
                "  CONSTRAINT <:1>\n  FOREIGN KEY (<:2>)\n"
                "  REFERENCES <:3> (<:4>)",
                "keyword",
            )
        return statement

    def _replace_constraint_name(self, template, constraint_name):
        return template.replace("<:1>", constraint_name)

    def _replace_constraint_columns(self, template, constraint_columns):
        if self.constraint_type == "C":
            return template.replace("<:2>", self.search_condition)
        return template.replace("<:2>", constraint_columns)

    def _replace_fk_columns(self, template, table_name, columns):
        constraint = template
        if self.constraint_type == "R":
            constraint = constraint.replace("<:3>", table_name)
            constraint = constraint.replace("<:4>", columns)
        return constraint

    def _get_deferrable(self):
        if self.deferrable == "DEFERRABLE":
            return get_case_formatted(
                f"\n  DEFERRABLE INITIALLY {self.deferred}", "keyword"
            )
        return ""

    def _get_index_statement(self):
        statement = ""
        if self.index_name and str(self.index_name) not in ("nan", "None"):
            statement = get_case_formatted("\n  USING INDEX <:1>", "keyword")
            index_name = get_object_name(
                self.index_owner, self.index_name, "identifier"
            )
            statement = statement.replace("<:1>", index_name)
        return statement

    def _get_on_delete_statement(self):
        statement = ""
        if self.delete_rule and str(self.delete_rule) not in (
            "nan",
            "None",
            "NO ACTION",
        ):
            statement = get_case_formatted("\n  ON DELETE <:1>", "keyword")
            statement = statement.replace(
                "<:1>",
                get_case_formatted(self.delete_rule, "keyword"))
        return statement

    def _get_status_statement(self):
        if self.status == "ENABLED":
            status = get_case_formatted("ENABLE", "keyword")
        else:
            status = get_case_formatted("DISABLE", "keyword")

        if self.validated == "VALIDATED":
            validate = get_case_formatted("VALIDATE", "keyword")
        else:
            validate = get_case_formatted("NOVALIDATE", "keyword")

        return f"\n  {status} {validate}"

    def get_constraint(self, standalone=False):
        """Generate DDL for constraint definition."""
        table_name = get_object_name(self.owner, self.table_name, "identifier")
        constraint_name = get_case_formatted(
            self.constraint_name, "identifier"
        )
        r_table_name = self._get_r_table_name()
        constraint_columns = self._get_constraint_columns()
        r_constraint_columns = self._get_r_constraint_columns()
        template = self._get_statement_template()
        constraint = self._get_start_of_statement(standalone, table_name)
        constraint += self._replace_constraint_name(template, constraint_name)
        constraint = self._replace_constraint_columns(
            constraint, constraint_columns)
        constraint = self._replace_fk_columns(
            constraint, r_table_name, r_constraint_columns)
        constraint += self._get_deferrable()
        constraint += self._get_index_statement()
        constraint += self._get_on_delete_statement()
        constraint += self._get_status_statement()
        return constraint

    def generate_ddl(self):
        """Generate complete DDL for constraint creation."""
        constraint_name = get_object_name(
            self.owner, self.constraint_name, "identifier"
        )
        ddl = get_prompt("Foreign key ", constraint_name)
        ddl += self.get_constraint(standalone=True)
        ddl += ");\n"
        self.ddl = ddl

    def store_ddl_into_file(self):
        """Write generated DDL to filesystem."""
        file_path = get_file_path(
            "foreign_key", self.owner, self.constraint_name
        )
        prepare_directories(file_path)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.ddl)

        print(f"   Foreign key stored in {file_path}")
