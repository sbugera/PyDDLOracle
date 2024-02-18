from storage import get_full_storage
from utils import conf, get_case_formatted, get_indentation


class Partition:
    def __init__(self, partitioning_type, tab_partition):
        self.partitioning_type = partitioning_type
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
        elif self.partitioning_type == "LIST":
            statement = get_case_formatted("\n  PARTITION<:1>VALUES (<:2>)", "keyword")
        partition_name = " "
        if not self.partition_name.startswith("SYS_P"):
            partition_name = get_case_formatted(f" {self.partition_name} ", "identifier")
        partition = statement.replace("<:1>", partition_name).replace("<:2>", self.high_value)
        partition += self.get_logging()
        partition += self.get_compression()
        if conf["storage"]["storage"] == "with_storage":
            partition += get_full_storage(
                get_indentation(), self.tablespace_name, self.pct_free, self.ini_trans, self.max_trans,
                self.min_extent, self.max_extent, self.pct_increase, self.buffer_pool, self.flash_cache,
                self.cell_flash_cache, self.initial_extent, self.next_extent)
        elif conf["storage"]["storage"] == "only_tablespace":
            partition += f"\n{get_indentation()}TABLESPACE {self.tablespace_name}"
        return partition
