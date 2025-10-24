"""Handles Oracle database partition definitions and DDL generation."""

from pyddl_oracle.config import config as c
from pyddl_oracle.partition import Partition
from pyddl_oracle.utils import get_case_formatted, get_indentation


class Partitioning:
    """Handles Oracle database partition definitions and DDL generation."""

    def __init__(self, part_table, part_key_columns, tab_partitions):
        self.partitioning_type = part_table.partitioning_type
        self.interval = part_table.interval
        self.autolist = part_table.autolist
        self.part_key_columns = part_key_columns
        self.tab_partitions = tab_partitions

    def get_list_of_key_columns(self):
        """Generate list of key columns."""
        list_of_key_columns = ""
        for i, part_key_column in enumerate(
            self.part_key_columns.itertuples()
        ):
            if i == 0:
                list_of_key_columns += f"{part_key_column.column_name}"
            else:
                list_of_key_columns += f", {part_key_column.column_name}"
        return get_case_formatted(list_of_key_columns, "identifier")

    def get_range_list_partitioning(self):
        """Generate range or list partitioning clause."""
        partitioning = ""

        if self.partitioning_type in ("RANGE", "LIST"):
            partitioning = "\n("
            for _, tab_partition in enumerate(
                self.tab_partitions.itertuples()
            ):
                if (
                    tab_partition.partition_position > 1
                    and str(self.interval) not in ("nan", "None")
                    and c.conf["storage"]["partitions"] == "compact"
                ):
                    break
                if (
                    tab_partition.partition_name.startswith("SYS_P")
                    and c.conf["storage"]["partitions"] == "compact"
                ):
                    break
                partition = Partition(
                    self.partitioning_type, tab_partition
                )
                partitioning += f"{partition.get_partition()},"
            partitioning = partitioning[:-1]
            partitioning += "\n)"

        return partitioning

    def get_hash_partitioning(self):
        """Generate hash partitioning clause."""
        partitioning = ""

        if self.partitioning_type == "HASH":
            partitioning = get_case_formatted(
                f"\n{get_indentation()}PARTITIONS"
                f" {len(self.tab_partitions)}",
                "keyword",
            )
            if c.conf["storage"]["storage"] in (
                "only_tablespace",
                "with_storage",
            ):
                all_tablespaces = ""
                for partition in self.tab_partitions.itertuples():
                    if all_tablespaces == "":
                        all_tablespaces = get_case_formatted(
                            partition.tablespace_name, "identifier"
                        )
                    else:
                        all_tablespaces += ", " + get_case_formatted(
                            partition.tablespace_name, "identifier"
                        )
                statement = get_case_formatted(
                    f"\n{get_indentation()}STORE IN (<:1>)", "keyword"
                )
                partitioning += statement.replace("<:1>", all_tablespaces)
        return partitioning

    def get_interval_clause(self):
        """Generate interval partitioning clause."""
        clause = ""
        if str(self.interval) not in ("nan", "None"):
            statement = get_case_formatted("INTERVAL", "keyword")
            clause += f"\n{statement} ({self.interval})"
        return clause

    def get_automatic_clause(self):
        """Generate automatic partitioning clause."""
        clause = ""
        if self.partitioning_type == "LIST" and self.autolist == "YES":
            clause += get_case_formatted(" AUTOMATIC", "keyword")
        return clause

    def get_partitioning(self):
        """Generate partitioning clause if table is partitioned."""
        partitioning = ""
        if c.conf["storage"]["partitions"] == "none":
            return ""

        if self.partitioning_type not in ("RANGE", "LIST", "HASH"):
            return ""

        if c.conf["storage"]["partitions"] not in ("all", "compact"):
            return ""

        statement = get_case_formatted(
            f"PARTITION BY {self.partitioning_type}", "keyword"
        )
        key_columns = self.get_list_of_key_columns()
        partitioning = f"\n{statement} ({key_columns})"
        partitioning += self.get_interval_clause()
        partitioning += self.get_automatic_clause()
        partitioning += self.get_range_list_partitioning()
        partitioning += self.get_hash_partitioning()

        return partitioning
