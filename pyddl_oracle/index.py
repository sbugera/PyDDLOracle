"""Handles Oracle database index definitions and DDL generation."""

from pyddl_oracle.config import config as c
from pyddl_oracle.storage import get_full_storage
from pyddl_oracle.utils import get_case_formatted, get_object_name, get_prompt


class Index:
    """Oracle database index with DDL generation."""
    def __init__(self, index_row, index_columns):
        self.row = index_row
        self.index_columns = index_columns

    def get_index_type(self):
        """Get index type."""
        index_type = ""
        if self.row.index_type == "BITMAP":
            index_type += get_case_formatted(" BITMAP", "keyword")
        if self.row.uniqueness == "UNIQUE":
            index_type += get_case_formatted(" UNIQUE", "keyword")
        return index_type

    def get_index_columns(self):
        """Get index columns."""
        index_columns = ""
        for i, index_column in enumerate(self.index_columns.itertuples()):
            index_columns += get_case_formatted(
                index_column.column_name, "identifier"
            )
            if i != len(self.index_columns) - 1:
                index_columns += ", "
        return index_columns

    def get_index_logging(self):
        """Get index logging."""
        logging = ""
        if c.conf["storage"]["logging"] == "yes":
            if self.row.logging == "YES":
                logging = get_case_formatted("\nLOGGING", "keyword")
            elif self.row.logging == "NO":
                logging = get_case_formatted("\nNOLOGGING", "keyword")
        return logging

    def get_index_storage(self):
        """Get index storage."""
        storage = ""
        if c.conf["storage"]["storage"] == "with_storage":
            storage += get_full_storage(
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
        elif (c.conf["storage"]["storage"] == "only_tablespace"
              and self.row.partitioned != "YES"):
            storage += (
                f"\n{get_case_formatted('TABLESPACE', 'keyword')} "
                f"{get_case_formatted(self.row.tablespace_name, 'identifier')}"
            )
        return storage

    def get_index_compression(self):
        """Get index compression."""
        compression = ""
        if c.conf["storage"]["compression"] == "yes":
            if self.row.compression == "ENABLED":
                compression += get_case_formatted(
                    f"\nCOMPRESS {int(self.row.prefix_length)}", "keyword"
                )
            elif self.row.compression != "DISABLED":
                compression += get_case_formatted(
                    f"\nCOMPRESS {self.row.compression}", "keyword"
                )
        return compression

    def get_index_local(self):
        """Get index local."""
        local = ""
        if self.row.partitioned == "YES":
            local = get_case_formatted("\nLOCAL", "keyword")
        return local

    def get_index_visibility(self):
        """Get index visibility."""
        visibility = ""
        if self.row.visibility == "INVISIBLE":
            visibility = get_case_formatted("\nINVISIBLE", "keyword")
        return visibility

    def get_index_degree(self):
        """Get index degree."""
        degree = ""
        if int(self.row.degree) > 1:
            degree = get_case_formatted(
                f"\nPARALLEL ( DEGREE {int(self.row.degree)}"
                f" INSTANCES {self.row.instances} )",
                "keyword",
            )
        return degree

    def get_index_reverse(self):
        """Get index reverse."""
        reverse = ""
        if self.row.index_type == "NORMAL/REV":
            reverse = get_case_formatted("\nREVERSE", "keyword")
        return reverse

    def get_index_monitoring(self, index_name):
        """Get index monitoring."""
        monitoring = ""
        if self.row.monitoring == "YES":
            monitoring = get_case_formatted(
                "ALTER INDEX <:1>\n  MONITORING USAGE;\n\n", "keyword"
            )
            monitoring = monitoring.replace("<:1>", index_name)
        return monitoring

    def get_index(self):
        """Generate complete index DDL fragment."""
        statement = get_case_formatted(
            "CREATE<:1> INDEX <:2> ON <:3>\n(<:4>)", "keyword"
        )

        index_name = get_object_name(
            self.row.owner, self.row.index_name, "identifier"
        )
        table_name = get_object_name(
            self.row.table_owner, self.row.table_name, "identifier"
        )

        index = statement.replace("<:1>", self.get_index_type())
        index = index.replace("<:2>", index_name)
        index = index.replace("<:3>", table_name)
        index = index.replace("<:4>", self.get_index_columns())
        index += self.get_index_logging()
        index += self.get_index_storage()
        index += self.get_index_compression()
        index += self.get_index_local()
        index += self.get_index_visibility()
        index += self.get_index_degree()
        index += self.get_index_reverse()
        index += ";\n\n"
        index += self.get_index_monitoring(index_name)

        return get_prompt("Index ", index_name) + index
