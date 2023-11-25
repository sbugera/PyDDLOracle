from sqlalchemy import create_engine
import pandas as pd
import argparse
import configparser
import re
import os
from collections import namedtuple
from pprint import PrettyPrinter
import sql_queries as sql

pd.options.mode.chained_assignment = None  # type: ignore # default='warn'
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def get_dataframe_namedtuple(df, index):
    """
    Returns the row of a pandas dataframe as a namedtuple.
    """
    if index >= len(df):
        return None
    row = df.iloc[index]
    row_namedtuple = namedtuple('row', row.index)
    return row_namedtuple(*row.values)


def replace_multiple_newlines(text):
    return re.sub(r'\n+$', '\n', text)


def pprint(variable):
    pp = PrettyPrinter(indent=1, width=80, depth=None, stream=None, compact=False)
    try:
        pp.pprint(variable._asdict())
    except AttributeError:
        pp.pprint(variable)


def get_case_formatted(str, config_name_for_upper):
    if not str:
        return ""
    if str != str.upper():
        return f'"{str}"'
    if conf["case"][config_name_for_upper] == "uppercase":
        return str.upper()
    else:
        return str.lower()


def add_quotes(value):
    if any(char.islower() for char in value):
        return f'"{value}"'
    else:
        return value


def get_indentation():
    return "    "


def get_entity_name(template_name, object_type, object_owner, object_name):
    pattern = r'\{(.*?)\}'
    matches = re.findall(pattern, template_name)
    entity_name = template_name
    for match in matches:
        case_function = str.lower
        if match == match.upper():
            case_function = str.upper

        if match.lower() == 'object_type':
            entity_name = entity_name.replace(case_function('{object_type}'), case_function(object_type))
        elif match.lower() == 'object_owner':
            entity_name = entity_name.replace(case_function('{object_owner}'), case_function(object_owner))
        elif match.lower() == 'object_name':
            entity_name = entity_name.replace(case_function('{object_name}'), case_function(object_name))
    return entity_name


def get_size_formatted(initial_extent):
    if initial_extent >= 1024 * 1024 * 1024:
        return str(int(initial_extent / 1024 / 1024 / 1024)) + "G"
    if initial_extent >= 1024 * 1024:
        return str(int(initial_extent / 1024 / 1024)) + "M"
    if initial_extent >= 1024:
        return str(int(initial_extent / 1024)) + "K"


def get_full_storage(indentation, tablespace_name, pct_free, ini_trans, max_trans, min_extents, max_extents,
                     pct_increase, buffer_pool, flash_cache, cell_flash_cache, initial_extent=None, next_extent=None,
                     local_index=None):
    storage = ""
    if str(tablespace_name) != "nan" and local_index != "YES":
        statement = get_case_formatted(f"\n{indentation}TABLESPACE <:1>", "keyword")
        storage = statement.replace("<:1>", get_case_formatted(tablespace_name, "identifier"))
    if str(pct_free) != "nan":
        statement = get_case_formatted(f"\n{indentation}PCTFREE    <:1>", "keyword")
        storage += statement.replace("<:1>", str(int(pct_free)))
    if str(ini_trans) != "nan":
        statement = get_case_formatted(f"\n{indentation}INITRANS   <:1>", "keyword")
        storage += statement.replace("<:1>", str(int(ini_trans)))
    if str(max_trans) != "nan":
        statement = get_case_formatted(f"\n{indentation}MAXTRANS   <:1>", "keyword")
        storage += statement.replace("<:1>", str(int(max_trans)))
    storage_tmp = get_case_formatted(f"\n{indentation}STORAGE    (", "keyword")
    if initial_extent and str(initial_extent) not in ("nan", "DEFAULT", "-1"):
        statement = get_case_formatted(f"\n{indentation}            INITIAL          <:1>", "keyword")
        storage_tmp += statement.replace("<:1>", get_size_formatted(initial_extent))
    if next_extent and str(next_extent) not in ("nan", "DEFAULT", "-1"):
        statement = get_case_formatted(f"\n{indentation}            NEXT             <:1>", "keyword")
        storage_tmp += statement.replace("<:1>", str(int(next_extent/1024/1024)) + "M")
    if min_extents and str(min_extents) not in ("nan", "DEFAULT", "-1"):
        statement = get_case_formatted(f"\n{indentation}            MINEXTENTS       <:1>", "keyword")
        storage_tmp += statement.replace("<:1>", str(int(min_extents)))
    if max_extents and str(max_extents) not in ("nan", "DEFAULT", "-1"):
        if max_extents == 2147483645:
            storage_tmp += get_case_formatted(f"\n{indentation}            MAXEXTENTS       UNLIMITED", "keyword")
        else:
            storage_tmp += get_case_formatted(f"\n{indentation}            MAXEXTENTS       {int(max_extents)}", "keyword")
    if pct_increase and str(pct_increase) not in ("nan", "DEFAULT", "-1"):
        storage_tmp += get_case_formatted(f"\n{indentation}            PCTINCREASE      {int(pct_increase)}", "keyword")
    if str(pct_increase) in ("nan", "None") and local_index != "YES":
        storage_tmp += get_case_formatted(f"\n{indentation}            PCTINCREASE      0", "keyword")
    if buffer_pool and buffer_pool != "DEFAULT2":
        statement = get_case_formatted(f"\n{indentation}            BUFFER_POOL      <:1>", "keyword")
        storage_tmp += statement.replace("<:1>", get_case_formatted(buffer_pool, "identifier"))
    if flash_cache and flash_cache != "DEFAULT":
        statement = get_case_formatted(f"\n{indentation}            FLASH_CACHE      <:1>", "keyword")
        storage_tmp += statement.replace("<:1>", get_case_formatted(flash_cache, "identifier"))
    if cell_flash_cache and cell_flash_cache != "DEFAULT":
        statement = get_case_formatted(f"\n{indentation}            CELL_FLASH_CACHE <:1>", "keyword")
        storage_tmp += statement.replace("<:1>", get_case_formatted(cell_flash_cache, "identifier"))
    if storage_tmp != get_case_formatted(f"\n{indentation}STORAGE    (", "keyword"):
        storage += f"{storage_tmp}\n{indentation}            )"
    return storage


class Column:
    def __init__(self, column_row, max_column_name_length):
        self.max_column_name_length = max_column_name_length
        self.column_name = column_row.column_name
        self.data_type = column_row.data_type
        self.data_length = column_row.data_length
        self.data_precision = column_row.data_precision
        self.data_scale = column_row.data_scale
        self.data_type_owner = column_row.data_type_owner
        self.char_used = column_row.char_used
        self.hidden_column = column_row.hidden_column
        self.collation = column_row.collation
        self.data_default = column_row.data_default
        self.virtual_column = column_row.virtual_column
        self.default_on_null = column_row.default_on_null
        self.nullable = column_row.nullable

    def get_name(self):
        formatted_column_name = get_case_formatted(self.column_name, "identifier")
        padded_column_name = formatted_column_name.ljust(self.max_column_name_length)
        return padded_column_name

    def get_data_type(self):
        data_type = get_case_formatted(self.data_type, "keyword") if pd.isnull(
            self.data_type_owner) else get_case_formatted(f"{self.data_type_owner}.{self.data_type}", "keyword")
        if data_type.upper() == "NUMBER":
            if not pd.isnull(self.data_precision) and self.data_scale > 0:
                data_type = f"{data_type}({int(self.data_precision)},{int(self.data_scale)})"
            elif not pd.isnull(self.data_precision):
                data_type = f"{data_type}({int(self.data_precision)})"
            elif pd.isnull(self.data_precision) and self.data_scale == 0:
                data_type = get_case_formatted("INTEGER", "keyword")
        elif data_type.upper() in ("CHAR", "VARCHAR", "VARCHAR2", "NVARCHAR"):
            char_used = get_case_formatted(
                "BYTE", "keyword") if self.char_used == "B" else get_case_formatted("CHAR", "keyword")
            data_type = f"{data_type}({int(self.data_length)} {char_used})"
        elif data_type.upper() in ("UROWID", "RAW", "NCHAR", "NVARCHAR2"):
            data_type = f"{data_type}({int(self.data_length)})"
        elif data_type.upper() in ("FLOAT"):
            data_type = f"{data_type}({int(self.data_precision)})"
        return data_type

    def get_invisible(self):
        invisible = ""
        if self.hidden_column == "YES":
            invisible = " INVISIBLE"
        return get_case_formatted(invisible, "keyword")

    def get_collation(self):
        collation = ""
        if str(self.collation) not in ("nan", "None") and self.collation != "USING_NLS_COMP":
            collation = f" COLLATE {self.collation}"
        return get_case_formatted(collation, "keyword")

    def get_default(self):
        default = ""
        if str(self.data_default) not in ("nan", "None") and self.virtual_column == "YES":
            default = f""" {get_case_formatted("GENERATED ALWAYS AS", "keyword")} ({self.data_default})"""
        elif str(self.data_default) not in ("nan", "None") and self.default_on_null == "YES":
            default = f""" {get_case_formatted("DEFAULT ON NULL", "keyword")} {self.data_default}"""
        elif str(self.data_default) not in ("nan", "None"):
            default = f""" {get_case_formatted("DEFAULT", "keyword")} {self.data_default}"""
        return default.rstrip()

    def get_not_null(self):
        not_null = ""
        if self.nullable == "N":
            not_null = " NOT NULL"
        return get_case_formatted(not_null, "keyword")

    def get_ddl(self):
        indentation = get_indentation()
        name = self.get_name()
        data_type = self.get_data_type()
        invisible = self.get_invisible()
        collation = self.get_collation()
        data_default = self.get_default()
        not_null = self.get_not_null()
        ddl = f"""{indentation}{name}  {data_type}{invisible}{collation}{data_default}{not_null}"""
        return ddl


class Partition:
    def __init__(self, partitioning_type, autolist, tab_partition):
        self.partitioning_type = partitioning_type
        self.autolist = autolist
        self.partition_name = tab_partition.partition_name
        self.high_value = tab_partition.high_value
        self.partition_position = tab_partition.partition_position
        self.tablespace_name = tab_partition.tablespace_name
        self.pct_free = tab_partition.pct_free
        self.ini_trans = tab_partition.ini_trans
        self.max_trans = tab_partition.max_trans
        self.min_extent = tab_partition.min_extent
        self.max_extent = tab_partition.max_extent
        self.pct_increase = tab_partition.pct_increase
        self.buffer_pool = tab_partition.buffer_pool
        self.flash_cache = tab_partition.flash_cache
        self.cell_flash_cache = tab_partition.cell_flash_cache
        self.initial_extent = tab_partition.initial_extent
        self.next_extent = tab_partition.next_extent
        self.logging = tab_partition.logging
        self.compression = tab_partition.compression
        self.compress_for = tab_partition.compress_for

    def get_logging(self):
        logging = ""
        if conf["storage"]["logging"] == "yes":
            if self.logging == "YES":
                logging = f"\n{get_indentation()}LOGGING"
            else:
                logging = f"\n{get_indentation()}NOLOGGING"
        return get_case_formatted(logging, "keyword")

    def get_compression(self):
        compression = ""
        if conf["storage"]["compression"] == "yes":
            if self.compression == "DISABLED":
                compression = f"\n{get_indentation()}NOCOMPRESS"
            else:
                if self.compress_for == "BASIC":
                    compression = f"\n{get_indentation()}COMPRESS BASIC"
                elif self.compress_for == "ADVANCED":
                    compression = f"\n{get_indentation()}COMPRESS FOR OLTP"
        return get_case_formatted(compression, "keyword")

    def get_partition(self):
        statement = ""
        if self.partitioning_type == "RANGE":
            statement = get_case_formatted("\n  PARTITION<:1>VALUES LESS THAN (<:2>)", "keyword")
        elif self.partitioning_type == "LIST" and self.autolist == "NO":
            statement = get_case_formatted("\n  PARTITION<:1>VALUES (<:2>)", "keyword")
        elif self.partitioning_type == "LIST" and self.autolist == "YES":
            statement = get_case_formatted("\n  PARTITION<:1>VALUES (<:2>) AUTOMATIC", "keyword")
        partition_name = " "
        if not self.partition_name.startswith("SYS_P"):
            partition_name = get_case_formatted(f" {self.partition_name} ", "identifier")
        partition = statement.replace("<:1>", partition_name).replace("<:2>", self.high_value)
        partition += self.get_logging()
        partition += self.get_compression()
        if conf["storage"]["storage"] == "with_storage":
            partition += get_full_storage(
                get_indentation(), self.tablespace_name, self.pct_free, self.ini_trans, self.max_trans,self.min_extent,
                self.max_extent, self.pct_increase, self.buffer_pool, self.flash_cache, self.cell_flash_cache,
                self.initial_extent, self.next_extent)
        elif conf["storage"]["storage"] == "only_tablespace":
            partition += f"\n{get_indentation()}TABLESPACE {self.tablespace_name}"
        return partition


class Partitioning:
    def __init__(self, part_table, part_key_columns, tab_partitions):
        self.partitioning_type = part_table.partitioning_type
        self.interval = part_table.interval
        self.autolist = part_table.autolist
        self.part_key_columns = part_key_columns
        self.tab_partitions = tab_partitions

    def get_list_of_key_columns(self):
        list_of_key_columns = ""
        for i, part_key_column in enumerate(self.part_key_columns.itertuples()):
            if i == 0:
                list_of_key_columns += f"{part_key_column.column_name}"
            else:
                list_of_key_columns += f", {part_key_column.column_name}"
        return get_case_formatted(list_of_key_columns, "identifier")

    def get_partitioning(self):
        partitioning = ""
        if conf["storage"]["partitions"] == "none":
            return ""
        if self.partitioning_type in ("RANGE", "LIST", "HASH") and conf["storage"]["partitions"] in ("all", "compact"):
            statement = get_case_formatted(f"PARTITION BY {self.partitioning_type}", "keyword")
            key_columns = self.get_list_of_key_columns()
            partitioning = f"\n{statement} ({key_columns})"
            if str(self.interval) not in ("nan", "None"):
                statement = get_case_formatted("INTERVAL", "keyword")
                partitioning += f"\n{statement} ({self.interval})"
            if self.partitioning_type in ("RANGE", "LIST"):
                partitioning += "\n("
                for i, tab_partition in enumerate(self.tab_partitions.itertuples()):
                    if (tab_partition.partition_position > 1
                            and str(self.interval) not in ("nan", "None")
                            and conf["storage"]["partitions"] == "compact"):
                        break
                    if (tab_partition.partition_name.startswith("SYS_P")
                            and conf["storage"]["partitions"] == "compact"):
                        break
                    partition = Partition(self.partitioning_type, self.autolist, tab_partition)
                    partitioning += f"{partition.get_partition()},"
                partitioning = partitioning[:-1]
                partitioning += "\n)"
            if self.partitioning_type == "HASH":
                partitioning += get_case_formatted(f"\n{get_indentation()}PARTITIONS {len(self.tab_partitions)}", "keyword")
                if conf["storage"]["storage"] in ("only_tablespace", "with_storage"):
                    all_tablespaces = ""
                    for partition in self.tab_partitions.itertuples():
                        if all_tablespaces == "":
                            all_tablespaces = get_case_formatted(partition.tablespace_name, "identifier")
                        else:
                            all_tablespaces += ", " + get_case_formatted(partition.tablespace_name, "identifier")
                    statement = get_case_formatted(f"\n{get_indentation()}STORE IN (<:1>)", "keyword")
                    partitioning += statement.replace("<:1>", all_tablespaces)
        # todo: Implement sub-partitioning

        return partitioning


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

        index_name = get_case_formatted(f"{self.owner}.{self.index_name}", "identifier")
        table_name = get_case_formatted(f"{self.table_owner}.{self.table_name}", "identifier")

        index_columns = ""
        for i, index_column in enumerate(self.index_columns.itertuples()):
            index_columns += get_case_formatted(index_column.column_name, "identifier")
            if i != len(self.index_columns) - 1:
                index_columns += ", "

        index = (statement
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
                "", self.tablespace_name, self.pct_free, self.ini_trans, self.max_trans,self.min_extents,
                self.max_extents, self.pct_increase, self.buffer_pool, self.flash_cache, self.cell_flash_cache,
                self.initial_extent, self.next_extent, self.partitioned)
        elif conf["storage"]["storage"] == "only_tablespace" and self.partitioned != "YES":
            statement = get_case_formatted(f"\nTABLESPACE <:1>", "keyword")
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
            index += get_case_formatted(f"\nPARALLEL ( DEGREE {int(self.degree)} INSTANCES {self.instances} )", "keyword")

        if self.index_type == "NORMAL/REV":
            index += get_case_formatted("\nREVERSE", "keyword")

        index += ";"
        if conf["indexes"]["empty_line_after_index"] == "yes":
            index += "\n"

        if self.monitoring == "YES":
            statement = get_case_formatted("\nALTER INDEX <:1>\n  MONITORING USAGE;\n", "keyword")
            index += statement.replace("<:1>", index_name)

        return index


class Table:
    def __init__(self,
                 table, part_table, columns, comments, part_key_columns, tab_partitions, indexes, index_columns,
                 tab_constraints, tab_constraint_columns):
        self.max_column_name_length = None
        self.ddl = ""
        self.columns = columns
        self.comments = comments
        self.indexes = indexes
        self.index_columns = index_columns
        self.part_table = part_table
        self.part_key_columns = part_key_columns
        self.tab_partitions = tab_partitions
        self.owner = table.owner
        self.table_name = table.table_name
        self.default_collation = table.default_collation
        self.logging = table.logging
        self.cache = table.cache
        self.result_cache = table.result_cache
        self.row_movement = table.row_movement
        self.compression = table.compression
        self.compress_for = table.compress_for
        self.partitioned = table.partitioned
        self.tablespace_name = table.tablespace_name
        self.pct_free = table.pct_free
        self.ini_trans = table.ini_trans
        self.max_trans = table.max_trans
        self.min_extents = table.min_extents
        self.max_extents = table.max_extents
        self.pct_increase = table.pct_increase
        self.buffer_pool = table.buffer_pool
        self.flash_cache = table.flash_cache
        self.cell_flash_cache = table.cell_flash_cache
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
        if self.default_collation and self.default_collation != "USING_NLS_COMP":
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
        if conf["indexes"]["indexes"] == "yes":
            for index_row in self.indexes.itertuples():
                index_columns = self.index_columns[self.index_columns["index_name"] == index_row.index_name]
                index = Index(index_row, index_columns)
                indexes += index.get_index()
        if indexes != "":
            indexes = "\n"+indexes+"\n"
        return indexes

    def get_comments(self):
        comments = ""
        end_line_char = ""
        if conf["comments"]["empty_line_after_comment"] == "yes":
            end_line_char = "\n"
        max_column_name_length = self.max_column_name_length + len(self.owner) + len(self.table_name) + 2
        if conf["comments"]["comments"] == "yes":
            for comment_row in self.comments.itertuples():
                if not comment_row.column_name or str(comment_row.column_name) == "nan":
                    statement = get_case_formatted(f"\nCOMMENT ON TABLE <:1> IS '<:2>';{end_line_char}", "keyword")
                    table_name = get_case_formatted(f"{self.owner}.{self.table_name}", "identifier")
                    comments += statement.replace("<:1>", table_name).replace("<:2>", comment_row.comments)
                else:
                    statement = get_case_formatted(f"\nCOMMENT ON COLUMN <:1> IS '<:2>';{end_line_char}", "keyword")
                    column_name = get_case_formatted(f"{self.owner}.{self.table_name}.{comment_row.column_name}", "identifier")
                    if conf["comments"]["vertical_alignment"] == "yes":
                        column_name = column_name.ljust(max_column_name_length)
                    comments += statement.replace("<:1>", column_name).replace("<:2>", comment_row.comments)
        return comments

    def generate_ddl(self):
        table_name = get_case_formatted(f"{self.owner}.{self.table_name}", "identifier")
        self.max_column_name_length = self.get_maximum_column_name_length()

        ddl = f"""{get_case_formatted("CREATE TABLE", "keyword")} {table_name}\n(\n"""

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
        ddl += ";\n"

        ddl += self.get_comments()
        if len(self.comments) > 0:
            ddl += "\n"

        ddl += self.get_indexes()

        self.ddl = replace_multiple_newlines(ddl)

    def get_file_directory(self):
        file_directory_template = conf['directory']['table']
        file_directory = get_entity_name(file_directory_template, 'table', self.owner, self.table_name)
        return file_directory

    def get_file_name(self):
        file_name_template = conf['filename']['table']
        file_name = get_entity_name(file_name_template, 'table', self.owner, self.table_name)
        return file_name

    def store_ddl_into_file(self):
        file_directory = self.get_file_directory()
        file_name = self.get_file_name()
        if not os.path.exists(file_directory):
            os.makedirs(file_directory)
        with open(os.path.join(file_directory, file_name), 'w') as file:
            file.write(self.ddl)
        print(f"   Stored in {file_directory}/{file_name}")


def get_df_tables(engine, schema_name):
    return pd.read_sql_query(sql.sql_tables, engine, params={'schema_name': schema_name})


def get_df_tab_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_tab_columns, engine, params={'schema_name': schema_name})


def get_df_part_tables(engine, schema_name):
    return pd.read_sql_query(sql.sql_part_tables, engine, params={'schema_name': schema_name})


def get_df_part_key_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_part_key_columns, engine, params={'schema_name': schema_name})


def get_df_comments(engine, schema_name):
    return pd.read_sql_query(sql.sql_comments, engine, params={'schema_name': schema_name})


def get_df_tab_partitions(engine, schema_name):
    return pd.read_sql_query(sql.sql_tab_partitions, engine, params={'schema_name': schema_name})


def get_df_indexes(engine, schema_name):
    return pd.read_sql_query(sql.sql_indexes, engine, params={'schema_name': schema_name})


def get_df_index_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_index_columns, engine, params={'schema_name': schema_name})


def get_df_constraints(engine, schema_name):
    return pd.read_sql_query(sql.sql_constraints, engine, params={'schema_name': schema_name})


def get_df_constraint_columns(engine, schema_name):
    return pd.read_sql_query(sql.sql_constraint_columns, engine, params={'schema_name': schema_name})


def get_db_engine():
    conf_con = configparser.ConfigParser()
    conf_con.read('config_con.ini')
    db_username = conf_con['database']['username']
    db_password = conf_con['database']['password']
    db_host = conf_con['database']['host']
    db_port = conf_con['database']['port']
    db_service_name = conf_con['database']['service_name']
    connection_string = f"oracle+cx_oracle://{db_username}:{db_password}@{db_host}:{db_port}/?service_name={db_service_name}"
    return create_engine(connection_string, arraysize=1000)


def get_db_schema_name(arg_schema_name=None):
    if arg_schema_name:
        username = arg_schema_name.upper()
    else:
        conf_con = configparser.ConfigParser()
        conf_con.read('config_con.ini')
        username = conf_con['database']['username'].upper()
    return username


def get_args():
    arg_parser = argparse.ArgumentParser(description='Generate DDL scripts for Oracle database objects')
    arg_parser.add_argument('--schema_name', '-s', type=str,
                            help='DB schema name for which DDL scripts need to be generated')
    return arg_parser.parse_args()


def get_db_metadata(schema_name):
    engine = get_db_engine()
    db_metadata = (get_df_tables(engine, schema_name),
                   get_df_tab_columns(engine, schema_name),
                   get_df_part_tables(engine, schema_name),
                   get_df_part_key_columns(engine, schema_name),
                   get_df_tab_partitions(engine, schema_name),
                   get_df_comments(engine, schema_name),
                   get_df_indexes(engine, schema_name),
                   get_df_index_columns(engine, schema_name),
                   get_df_constraints(engine, schema_name),
                   get_df_constraint_columns(engine, schema_name))
    engine.dispose()
    return db_metadata


def get_table_dfs(table_row, metadata):
    (df_all_tab_columns,
     df_all_part_tables,
     df_all_part_key_columns,
     df_all_tab_partitions,
     df_all_comments,
     df_all_indexes,
     df_all_index_columns,
     df_all_constraints,
     df_all_constraint_columns) = metadata

    df_tab_columns = df_all_tab_columns[df_all_tab_columns["table_name"] == table_row.table_name]
    df_part_tables = df_all_part_tables[df_all_part_tables["table_name"] == table_row.table_name]
    df_part_key_columns = df_all_part_key_columns[df_all_part_key_columns["name"] == table_row.table_name]
    df_tab_partitions = df_all_tab_partitions[df_all_tab_partitions["table_name"] == table_row.table_name]
    df_tab_comments = df_all_comments[df_all_comments["table_name"] == table_row.table_name]
    df_tab_indexes = df_all_indexes[df_all_indexes["table_name"] == table_row.table_name]
    df_tab_index_columns = df_all_index_columns[df_all_index_columns["table_name"] == table_row.table_name]
    df_tab_constraints = df_all_constraints[df_all_constraints["table_name"] == table_row.table_name]
    df_tab_constraint_columns = df_all_constraint_columns[df_all_constraint_columns["table_name"] == table_row.table_name]
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
            df_tab_constraint_columns)


if __name__ == "__main__":
    args = get_args()
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    schema_name = get_db_schema_name(args.schema_name)
    df_tables, *db_metadata = get_db_metadata(schema_name)

    for db_table_row in df_tables.itertuples():
        print(db_table_row.table_name)
        tabel_dfs = get_table_dfs(db_table_row, db_metadata)
        table = Table(*tabel_dfs)
        table.generate_ddl()
        table.store_ddl_into_file()


