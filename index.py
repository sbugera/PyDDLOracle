from storage import get_full_storage
from utils import conf, get_case_formatted, get_object_name, get_prompt


class Index:
    def __init__(self, index_row, index_columns):
        self.owner = index_row.owner
        self.index_name = index_row.index_name
        self.index_type = index_row.index_type
        self.table_owner = index_row.table_owner
        self.table_name = index_row.table_name
        self.uniqueness = index_row.uniqueness
        self.compression = index_row.compression
        self.prefix_length = index_row.prefix_length
        self.tablespace_name = index_row.tablespace_name
        self.ini_trans = index_row.ini_trans
        self.max_trans = index_row.max_trans
        self.initial_extent = index_row.initial_extent
        self.next_extent = index_row.next_extent
        self.min_extents = index_row.min_extents
        self.max_extents = index_row.max_extents
        self.pct_increase = index_row.pct_increase
        self.pct_threshold = index_row.pct_threshold
        self.include_column = index_row.include_column
        self.freelists = index_row.freelists
        self.freelist_groups = index_row.freelist_groups
        self.pct_free = index_row.pct_free
        self.logging = index_row.logging
        self.instances = index_row.instances
        self.partitioned = index_row.partitioned
        self.buffer_pool = index_row.buffer_pool
        self.flash_cache = index_row.flash_cache
        self.cell_flash_cache = index_row.cell_flash_cache
        self.visibility = index_row.visibility
        self.monitoring = index_row.monitoring
        self.degree = index_row.degree
        self.instances = index_row.instances
        self.index_columns = index_columns

    def get_index(self):
        statement = get_case_formatted("CREATE<:1> INDEX <:2> ON <:3>\n(<:4>)", "keyword")

        index_type = ""
        if self.index_type == "BITMAP":
            index_type += get_case_formatted(" BITMAP", "keyword")
        if self.uniqueness == "UNIQUE":
            index_type += get_case_formatted(" UNIQUE", "keyword")

        index_name = get_object_name(self.owner, self.index_name, "identifier")
        table_name = get_object_name(self.table_owner, self.table_name, "identifier")

        index_columns = ""
        for i, index_column in enumerate(self.index_columns.itertuples()):
            index_columns += get_case_formatted(index_column.column_name, "identifier")
            if i != len(self.index_columns) - 1:
                index_columns += ", "

        index = get_prompt("Index ", index_name)
        index += (statement
                  .replace("<:1>", index_type)
                  .replace("<:2>", index_name)
                  .replace("<:3>", table_name)
                  .replace("<:4>", index_columns))

        logging = ""
        if conf["storage"]["logging"] == "yes":
            if self.logging == "YES":
                logging = get_case_formatted("\nLOGGING", "keyword")
            elif self.logging == "NO":
                logging = get_case_formatted("\nNOLOGGING", "keyword")
        index += logging

        if conf["storage"]["storage"] == "with_storage":
            index += get_full_storage(
                "", self.tablespace_name, self.pct_free, self.ini_trans, self.max_trans, self.min_extents,
                self.max_extents, self.pct_increase, self.buffer_pool, self.flash_cache, self.cell_flash_cache,
                self.initial_extent, self.next_extent, self.partitioned)
        elif conf["storage"]["storage"] == "only_tablespace" and self.partitioned != "YES":
            statement = get_case_formatted("\nTABLESPACE <:1>", "keyword")
            index += statement.replace("<:1>", get_case_formatted(self.tablespace_name, "identifier"))

        if conf["storage"]["compression"] == "yes":
            if self.compression == "ENABLED":
                index += get_case_formatted(f"\nCOMPRESS {int(self.prefix_length)}", "keyword")
            elif self.compression != "DISABLED":
                index += get_case_formatted(f"\nCOMPRESS {self.compression}", "keyword")

        local = ""
        if self.partitioned == "YES":
            local = get_case_formatted("\nLOCAL", "keyword")
        index += local

        if self.visibility == "INVISIBLE":
            index += get_case_formatted("\nINVISIBLE", "keyword")

        if int(self.degree) > 1:
            index += get_case_formatted(
                f"\nPARALLEL ( DEGREE {int(self.degree)} INSTANCES {self.instances} )", "keyword")

        if self.index_type == "NORMAL/REV":
            index += get_case_formatted("\nREVERSE", "keyword")

        index += ";\n\n"

        if self.monitoring == "YES":
            statement = get_case_formatted("ALTER INDEX <:1>\n  MONITORING USAGE;\n\n", "keyword")
            index += statement.replace("<:1>", index_name)

        return index
