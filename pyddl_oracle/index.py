"""Handles Oracle database index definitions and DDL generation."""

from pyddl_oracle.config import config as c
from pyddl_oracle.storage import get_full_storage
from pyddl_oracle.utils import get_case_formatted, get_object_name, get_prompt


class Index:
    """Oracle database index with DDL generation."""
    def __init__(self, index_row, index_columns):
        self.row = index_row
        self.index_columns = index_columns

    def get_index(self):
        """Generate complete index DDL fragment."""
        statement = get_case_formatted(
            "CREATE<:1> INDEX <:2> ON <:3>\n(<:4>)", "keyword"
        )

        index_type = ""
        if self.row.index_type == "BITMAP":
            index_type += get_case_formatted(" BITMAP", "keyword")
        if self.row.uniqueness == "UNIQUE":
            index_type += get_case_formatted(" UNIQUE", "keyword")

        index_name = get_object_name(
            self.row.owner, self.row.index_name, "identifier"
        )
        table_name = get_object_name(
            self.row.table_owner, self.row.table_name, "identifier"
        )

        index_columns = ""
        for i, index_column in enumerate(self.index_columns.itertuples()):
            index_columns += get_case_formatted(
                index_column.column_name, "identifier"
            )
            if i != len(self.index_columns) - 1:
                index_columns += ", "

        index = get_prompt("Index ", index_name)
        index += (
            statement.replace("<:1>", index_type)
            .replace("<:2>", index_name)
            .replace("<:3>", table_name)
            .replace("<:4>", index_columns)
        )

        logging = ""
        if c.conf["storage"]["logging"] == "yes":
            if self.row.logging == "YES":
                logging = get_case_formatted("\nLOGGING", "keyword")
            elif self.row.logging == "NO":
                logging = get_case_formatted("\nNOLOGGING", "keyword")
        index += logging

        if c.conf["storage"]["storage"] == "with_storage":
            index += get_full_storage(
                "",
                self.row.tablespace_name,
                self.row.pct_free,
                self.row.ini_trans,
                self.row.max_trans,
                self.row.min_extents,
                self.row.max_extents,
                self.row.pct_increase,
                self.row.buffer_pool,
                self.row.flash_cache,
                self.row.cell_flash_cache,
                self.row.initial_extent,
                self.row.next_extent,
                self.row.partitioned,
            )
        elif (
            c.conf["storage"]["storage"] == "only_tablespace"
            and self.row.partitioned != "YES"
        ):
            statement = get_case_formatted("\nTABLESPACE <:1>", "keyword")
            index += statement.replace(
                "<:1>",
                get_case_formatted(self.row.tablespace_name, "identifier"),
            )

        if c.conf["storage"]["compression"] == "yes":
            if self.row.compression == "ENABLED":
                index += get_case_formatted(
                    f"\nCOMPRESS {int(self.row.prefix_length)}", "keyword"
                )
            elif self.row.compression != "DISABLED":
                index += get_case_formatted(
                    f"\nCOMPRESS {self.row.compression}", "keyword"
                )

        local = ""
        if self.row.partitioned == "YES":
            local = get_case_formatted("\nLOCAL", "keyword")
        index += local

        if self.row.visibility == "INVISIBLE":
            index += get_case_formatted("\nINVISIBLE", "keyword")

        if int(self.row.degree) > 1:
            index += get_case_formatted(
                f"\nPARALLEL ( DEGREE {int(self.row.degree)}"
                f" INSTANCES {self.row.instances} )",
                "keyword",
            )

        if self.row.index_type == "NORMAL/REV":
            index += get_case_formatted("\nREVERSE", "keyword")

        index += ";\n\n"

        if self.row.monitoring == "YES":
            statement = get_case_formatted(
                "ALTER INDEX <:1>\n  MONITORING USAGE;\n\n", "keyword"
            )
            index += statement.replace("<:1>", index_name)

        return index
