from utils import get_case_formatted, get_object_name


class Constraint:
    def __init__(self, constraint_row, constraint_columns):
        self.constraint_name = constraint_row.constraint_name
        self.constraint_type = constraint_row.constraint_type
        self.search_condition = constraint_row.search_condition
        self.status = constraint_row.status
        self.deferrable = constraint_row.deferrable
        self.deferred = constraint_row.deferred
        self.validated = constraint_row.validated
        self.index_owner = constraint_row.index_owner
        self.index_name = constraint_row.index_name
        self.constraint_columns = constraint_columns

    def get_constraint(self):
        constraint = ""
        constraint_name = get_case_formatted(self.constraint_name, "identifier")

        if self.constraint_type == "P":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  PRIMARY KEY (<:2>)", "keyword")
        elif self.constraint_type == "U":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  UNIQUE (<:2>)", "keyword")
        elif self.constraint_type == "C":
            statement = get_case_formatted("  CONSTRAINT <:1>\n  CHECK (<:2>)", "keyword")
        else:
            statement = ""

        if self.constraint_type == "C":
            constraint += statement.replace("<:1>", constraint_name).replace("<:2>", self.search_condition)
        else:
            constraint_columns = ""
            for i, constraint_column in enumerate(self.constraint_columns.itertuples()):
                constraint_columns += get_case_formatted(constraint_column.column_name, "identifier")
                if i != len(self.constraint_columns) - 1:
                    constraint_columns += ", "
            constraint += statement.replace("<:1>", constraint_name).replace("<:2>", constraint_columns)

        if self.deferrable == "DEFERRABLE":
            constraint += get_case_formatted(f"\n  DEFERRABLE INITIALLY {self.deferred}", "keyword")

        if self.index_name and str(self.index_name) not in ("nan", "None"):
            statement = get_case_formatted("\n  USING INDEX <:1>", "keyword")
            index_name = get_object_name(self.index_owner, self.index_name, "identifier")
            constraint += statement.replace("<:1>", index_name)

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
