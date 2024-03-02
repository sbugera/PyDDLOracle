from utils import get_case_formatted, get_object_name, get_file_path, prepare_directories, get_prompt


def get_foreign_key_dfs(foreign_key_row, metadata):
    df_all_constraint_cols = metadata["constraint_columns"]

    df_foreign_key_columns = df_all_constraint_cols[
        (df_all_constraint_cols["constraint_name"] == foreign_key_row.constraint_name) &
        (df_all_constraint_cols["owner"] == foreign_key_row.owner)]

    df_remote_key_columns = df_all_constraint_cols[
        (df_all_constraint_cols["constraint_name"] == foreign_key_row.r_constraint_name) &
        (df_all_constraint_cols["owner"] == foreign_key_row.r_owner)]

    return foreign_key_row, df_foreign_key_columns, df_remote_key_columns


class Constraint:
    def __init__(self, constraint_row, constraint_columns, constraint_columns_remote=None):
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

    def get_constraint(self, standalone=False):
        table_name = get_object_name(self.owner, self.table_name, "identifier")
        constraint_name = get_case_formatted(self.constraint_name, "identifier")
        if self.r_table_name and str(self.r_table_name) not in ("nan", "None"):
            r_table_name = get_object_name(self.r_owner, self.r_table_name, "identifier")

        constraint_columns = ""
        for i, constraint_column in enumerate(self.constraint_columns.itertuples()):
            constraint_columns += get_case_formatted(constraint_column.column_name, "identifier")
            if i != len(self.constraint_columns) - 1:
                constraint_columns += ", "

        r_constraint_columns = ""
        if self.constraint_columns_remote is not None and not self.constraint_columns_remote.empty:
            for i, r_constraint_column in enumerate(self.constraint_columns_remote.itertuples()):
                r_constraint_columns += get_case_formatted(r_constraint_column.column_name, "identifier")
                if i != len(self.constraint_columns_remote) - 1:
                    r_constraint_columns += ", "

        if standalone:
            constraint = get_case_formatted("ALTER TABLE <:1> ADD (\n", "keyword").replace("<:1>", table_name)
        else:
            constraint = ""

        if self.constraint_type == "P":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  PRIMARY KEY (<:2>)", "keyword")
        elif self.constraint_type == "U":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  UNIQUE (<:2>)", "keyword")
        elif self.constraint_type == "C":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  CHECK (<:2>)", "keyword")
        elif self.constraint_type == "R":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  FOREIGN KEY (<:2>)\n  REFERENCES <:3> (<:4>)",
                                           "keyword")
        else:
            statement = ""

        constraint += statement.replace("<:1>", constraint_name)
        if self.constraint_type == "C":
            constraint = constraint.replace("<:2>", self.search_condition)
        else:
            constraint = constraint.replace("<:2>", constraint_columns)

        if self.constraint_type == "R":
            constraint = constraint.replace("<:3>", r_table_name)
            constraint = constraint.replace("<:4>", r_constraint_columns)

        if self.deferrable == "DEFERRABLE":
            constraint += get_case_formatted(f"\n  DEFERRABLE INITIALLY {self.deferred}", "keyword")

        if self.index_name and str(self.index_name) not in ("nan", "None"):
            statement = get_case_formatted("\n  USING INDEX <:1>", "keyword")
            index_name = get_object_name(self.index_owner, self.index_name, "identifier")
            constraint += statement.replace("<:1>", index_name)

        if self.delete_rule and str(self.delete_rule) not in ("nan", "None", "NO ACTION"):
            statement = get_case_formatted("\n  ON DELETE <:1>", "keyword")
            constraint += statement.replace("<:1>", get_case_formatted(self.delete_rule, "keyword"))

        if self.status == "ENABLED":
            status = get_case_formatted("ENABLE", "keyword")
        else:
            status = get_case_formatted("DISABLE", "keyword")

        if self.validated == "VALIDATED":
            validate = get_case_formatted("VALIDATE", "keyword")
        else:
            validate = get_case_formatted("NOVALIDATE", "keyword")

        constraint += f"\n  {status} {validate}"

        return constraint

    def generate_ddl(self):
        constraint_name = get_object_name(self.owner, self.constraint_name, "identifier")
        ddl = get_prompt("Foreign key ", constraint_name)
        ddl += self.get_constraint(standalone=True)
        ddl += ");\n"
        self.ddl = ddl

    def store_ddl_into_file(self):
        file_path = get_file_path('foreign_key', self.owner, self.constraint_name)
        prepare_directories(file_path)

        with open(file_path, 'w') as file:
            file.write(self.ddl)

        print(f"   Foreign key stored in {file_path}")
