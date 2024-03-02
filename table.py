from column import Column
from constraint import Constraint
from partitioning import Partitioning
from index import Index
from storage import get_full_storage
from utils import (conf, get_case_formatted, get_object_name, get_prompt, get_file_path, prepare_directories,
                   add_quotes, replace_multiple_newlines, get_dataframe_namedtuple)


def get_table_dfs(table_row, metadata):
    df_all_tab_columns = metadata["tab_columns"]
    df_all_part_tables = metadata["part_tables"]
    df_all_part_key_columns = metadata["part_key_columns"]
    df_all_tab_partitions = metadata["tab_partitions"]
    df_all_comments = metadata["comments"]
    df_all_indexes = metadata["indexes"]
    df_all_index_columns = metadata["index_columns"]
    df_all_constraints = metadata["constraints"]
    df_all_constraint_cols = metadata["constraint_columns"]
    df_all_grants = metadata["grants"]

    df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table_row.table_name]
    df_part_tables = df_all_part_tables[df_all_part_tables["table_name"] == table_row.table_name]
    df_part_key_columns = df_all_part_key_columns[df_all_part_key_columns["name"] == table_row.table_name]
    df_tab_partitions = df_all_tab_partitions[df_all_tab_partitions["table_name"] == table_row.table_name]
    df_tab_comments = df_all_comments[df_all_comments["table_name"] == table_row.table_name]
    df_tab_indexes = df_all_indexes[df_all_indexes["table_name"] == table_row.table_name]
    df_tab_index_columns = df_all_index_columns[df_all_index_columns["table_name"] == table_row.table_name]
    df_tab_constraints = df_all_constraints[(df_all_constraints["table_name"] == table_row.table_name) &
                                            (df_all_constraints["constraint_type"].isin(['P', 'U', 'C']))]
    df_tab_constraint_columns = df_all_constraint_cols[(df_all_constraint_cols["table_name"] == table_row.table_name) &
                                                       (df_all_constraint_cols["owner"] == table_row.owner)]
    df_tab_grants = df_all_grants[df_all_grants["table_name"] == table_row.table_name]
    part_table_row = get_dataframe_namedtuple(df_part_tables, 0)

    return (table_row,
            part_table_row,
            df_tab_columns,
            df_tab_comments,
            df_part_key_columns,
            df_tab_partitions,
            df_tab_indexes,
            df_tab_index_columns,
            df_tab_constraints,
            df_tab_constraint_columns,
            df_tab_grants)


class Table:
    def __init__(self,
                 table_attr, part_table, columns, comments, part_key_columns, tab_partitions, indexes, index_columns,
                 tab_constraints, tab_constraint_columns, tab_grants):
        self.max_column_name_length = None
        self.ddl = ""
        self.part_table = part_table
        self.columns = columns
        self.comments = comments
        self.part_key_columns = part_key_columns
        self.tab_partitions = tab_partitions
        self.indexes = indexes
        self.index_columns = index_columns
        self.tab_constraints = tab_constraints
        self.tab_constraint_columns = tab_constraint_columns
        self.tab_grants = tab_grants
        self.owner = table_attr.owner
        self.table_name = table_attr.table_name
        self.table_full_name = None
        self.default_collation = table_attr.default_collation
        self.logging = table_attr.logging
        self.cache = table_attr.cache
        self.result_cache = table_attr.result_cache
        self.row_movement = table_attr.row_movement
        self.compression = table_attr.compression
        self.compress_for = table_attr.compress_for
        self.partitioned = table_attr.partitioned
        self.tablespace_name = table_attr.tablespace_name
        self.pct_free = table_attr.pct_free
        self.ini_trans = table_attr.ini_trans
        self.max_trans = table_attr.max_trans
        self.min_extents = table_attr.min_extents
        self.max_extents = table_attr.max_extents
        self.pct_increase = table_attr.pct_increase
        self.buffer_pool = table_attr.buffer_pool
        self.flash_cache = table_attr.flash_cache
        self.cell_flash_cache = table_attr.cell_flash_cache
        self.def_tablespace_name = part_table.def_tablespace_name if part_table else ""
        self.def_logging = part_table.def_logging if part_table else ""
        self.def_compression = part_table.def_compression if part_table else ""
        self.def_compress_for = part_table.def_compress_for if part_table else ""
        self.def_pct_free = part_table.def_pct_free if part_table else ""
        self.def_ini_trans = part_table.def_ini_trans if part_table else ""
        self.def_max_trans = part_table.def_max_trans if part_table else ""
        self.def_min_extents = part_table.def_min_extents if part_table else ""
        self.def_max_extents = part_table.def_max_extents if part_table else ""
        self.def_pct_increase = part_table.def_pct_increase if part_table else ""
        self.def_buffer_pool = part_table.def_buffer_pool if part_table else ""
        self.def_flash_cache = part_table.def_flash_cache if part_table else ""
        self.def_cell_flash_cache = part_table.def_cell_flash_cache if part_table else ""

    def get_maximum_column_name_length(self):
        self.columns["column_name_quoted"] = self.columns["column_name"].apply(add_quotes)
        return self.columns["column_name_quoted"].str.len().max()

    def get_collation(self):
        collation = ""
        if (self.default_collation and self.default_collation != "USING_NLS_COMP"
                and str(self.default_collation) != "nan"):
            collation = f"\nDEFAULT COLLATION {self.default_collation}"
        return get_case_formatted(collation, "keyword")

    def get_storage(self):
        storage = ""
        if conf["storage"]["storage"] == "no_storage":
            storage = ""
        elif conf["storage"]["storage"] == "only_tablespace" and self.partitioned == "NO":
            storage = f"\nTABLESPACE {self.tablespace_name}"
        elif conf["storage"]["storage"] == "only_tablespace" and self.partitioned == "YES":
            storage = f"\nTABLESPACE {self.def_tablespace_name}"
        elif conf["storage"]["storage"] == "with_storage" and self.partitioned == "NO":
            storage = get_full_storage(
                '', self.tablespace_name, self.pct_free, self.ini_trans, self.max_trans, self.min_extents,
                self.max_extents, self.pct_increase, self.buffer_pool, self.flash_cache, self.cell_flash_cache)
        elif conf["storage"]["storage"] == "with_storage" and self.partitioned == "YES":
            storage = get_full_storage(
                '', self.def_tablespace_name, self.def_pct_free, self.def_ini_trans, self.def_max_trans,
                self.def_min_extents, self.def_max_extents, self.def_pct_increase, self.def_buffer_pool,
                self.def_flash_cache, self.def_cell_flash_cache)
        return storage

    def get_logging(self):
        logging = ""
        if conf["storage"]["logging"] == "yes" and self.partitioned == "NO":
            if self.logging == "YES":
                logging = "\nLOGGING"
            else:
                logging = "\nNOLOGGING"
        return get_case_formatted(logging, "keyword")

    def get_compression(self):
        if self.partitioned == "NO":
            tab_compression, tab_compress_for = self.compression, self.compress_for
        else:
            tab_compression, tab_compress_for = self.def_compression, self.def_compress_for
        compression = ""
        if conf["storage"]["compression"] == "yes":
            if tab_compression in ("DISABLED", "NONE"):
                compression = "\nNOCOMPRESS"
            else:
                if tab_compress_for == "BASIC":
                    compression = "\nCOMPRESS BASIC"
                elif tab_compress_for == "ADVANCED":
                    compression = "\nCOMPRESS FOR OLTP"
        return get_case_formatted(compression, "keyword")

    def get_cache(self):
        cache = ""
        if conf["storage"]["cache"] == "yes":
            if self.cache.strip() == "Y":
                cache = "\nCACHE"
            else:
                cache = "\nNOCACHE"
        return get_case_formatted(cache, "keyword")

    def get_result_cache(self):
        result_cache = ""
        if conf["storage"]["result_cache"] == "yes":
            result_cache = f"\nRESULT_CACHE (MODE {self.result_cache})"
        return get_case_formatted(result_cache, "keyword")

    def get_tab_row_movement(self):
        row_movement = ""
        if self.row_movement == "ENABLED":
            row_movement = "\nENABLE ROW MOVEMENT"
        return get_case_formatted(row_movement, "keyword")

    def get_partitioning(self):
        if self.partitioned == "NO":
            return ""
        partitioning = Partitioning(self.part_table, self.part_key_columns, self.tab_partitions)
        return partitioning.get_partitioning()

    def get_indexes(self):
        indexes = ""
        if conf["indexes"] == "yes":
            for index_row in self.indexes.itertuples():
                index_columns = self.index_columns[self.index_columns["index_name"] == index_row.index_name]
                index = Index(index_row, index_columns)
                indexes += index.get_index()
        if indexes != "":
            indexes = indexes+"\n"
        return indexes

    def get_constraints(self):
        constraints = ""
        if conf["constraints"] == "yes":
            if len(self.tab_constraints) > 0:
                constraints = get_prompt("Constraints for table ", self.table_full_name)
                statement = get_case_formatted("ALTER TABLE <:1> ADD (\n", "keyword")
                constraints += statement.replace("<:1>", self.table_full_name)
            for i, constraint_row in enumerate(self.tab_constraints.itertuples()):
                constraint_columns = self.tab_constraint_columns[
                    self.tab_constraint_columns["constraint_name"] == constraint_row.constraint_name]
                constraint = Constraint(constraint_row, constraint_columns)
                if i > 0:
                    constraints += ",\n"
                constraints += constraint.get_constraint()
        if constraints != "":
            constraints += ");\n\n\n"
        return constraints

    def get_comments(self):
        comments = ""
        end_line_char = ""
        if conf["comments"]["empty_line_after_comment"] == "yes":
            end_line_char = "\n"
        if conf["comments"]["comments"] == "yes":
            for comment_row in self.comments.itertuples():
                if not comment_row.column_name or str(comment_row.column_name) == "nan":
                    statement = get_case_formatted(f"COMMENT ON TABLE <:1> IS '<:2>';\n{end_line_char}", "keyword")
                    comments += statement.replace("<:1>", self.table_full_name).replace("<:2>", comment_row.comments)
                else:
                    statement = get_case_formatted(
                        f"COMMENT ON COLUMN <:1>.<:2> IS '<:3>';\n{end_line_char}", "keyword")
                    column_name = get_case_formatted(comment_row.column_name, "identifier")
                    if conf["comments"]["vertical_alignment"] == "yes":
                        # todo: Vertical alignment consider maximum column name length only for columns with comments
                        column_name = column_name.ljust(self.max_column_name_length)
                    comments += (statement
                                 .replace("<:1>", self.table_full_name)
                                 .replace("<:2>", column_name)
                                 .replace("<:3>", comment_row.comments))
        if comments != "":
            comments = comments+"\n"
            if conf["comments"]["empty_line_after_comment"] == "no":
                comments = comments+"\n"
        return comments

    def get_grants(self):
        grants = ""
        if conf["grants"] == "yes":
            tab_grants_grouped = (self.tab_grants
                                  .groupby(['grantee', 'grantable'])['privilege']
                                  .apply(lambda x: ', '.join(sorted(x)))
                                  .reset_index()
                                  .sort_values(['grantee', 'grantable']))
            previous_grantee = ""
            for tab_grants_group in tab_grants_grouped.itertuples():
                grantee = get_case_formatted(tab_grants_group.grantee, "identifier")
                privileges = get_case_formatted(tab_grants_group.privilege, "keyword")
                grant_option = ""
                if tab_grants_group.grantable == "YES":
                    grant_option = " WITH GRANT OPTION"

                prompt = get_prompt("Grants on table <:1> to <:2>", self.table_full_name, grantee)
                if previous_grantee == grantee:
                    prompt = ""
                    grants = grants[:-1]  # remove last newline
                grant = get_case_formatted(f"GRANT <:1> ON <:2> TO <:3>{grant_option};\n\n", "keyword")
                grants += prompt + (grant
                                    .replace("<:1>", privileges)
                                    .replace("<:2>", self.table_full_name)
                                    .replace("<:3>", grantee))
                previous_grantee = grantee
        if grants != "":
            grants = grants+"\n"
        return grants

    def generate_ddl(self):
        self.table_full_name = get_object_name(self.owner, self.table_name, "identifier")
        self.max_column_name_length = self.get_maximum_column_name_length()
        statement = get_case_formatted(f"CREATE TABLE <:1>\n(\n", "keyword")
        ddl = get_prompt("Table ", self.table_full_name) + statement.replace("<:1>", self.table_full_name)

        for i, column_row in enumerate(self.columns.itertuples()):
            column = Column(column_row, self.max_column_name_length)
            column_ddl = column.get_ddl()
            last_char = "\n" if i == len(self.columns) - 1 else ",\n"
            ddl += f"""{column_ddl}{last_char}"""

        ddl += ")"
        ddl += self.get_collation()
        if self.partitioned == "YES":
            ddl += self.get_compression()
        ddl += self.get_storage()
        ddl += self.get_partitioning()
        ddl += self.get_logging()
        if self.partitioned == "NO":
            ddl += self.get_compression()
        ddl += self.get_cache()
        ddl += self.get_result_cache()
        ddl += self.get_tab_row_movement()
        # todo: Add LOB storage
        ddl += ";\n\n\n"

        ddl += self.get_comments()
        ddl += self.get_indexes()
        ddl += self.get_constraints()
        ddl += self.get_grants()

        self.ddl = replace_multiple_newlines(ddl)

    def store_ddl_into_file(self):
        file_path = get_file_path('table', self.owner, self.table_name)
        prepare_directories(file_path)

        with open(file_path, 'w') as file:
            file.write(self.ddl)

        print(f"   Table stored in {file_path}")
