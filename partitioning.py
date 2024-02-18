from partition import Partition
from utils import conf, get_case_formatted, get_indentation


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
        if (self.partitioning_type in ("RANGE", "LIST", "HASH")
                and conf["storage"]["partitions"] in ("all", "compact")):
            statement = get_case_formatted(f"PARTITION BY {self.partitioning_type}", "keyword")
            key_columns = self.get_list_of_key_columns()
            partitioning = f"\n{statement} ({key_columns})"
            if str(self.interval) not in ("nan", "None"):
                statement = get_case_formatted("INTERVAL", "keyword")
                partitioning += f"\n{statement} ({self.interval})"
            if self.partitioning_type == "LIST" and self.autolist == "YES":
                partitioning += get_case_formatted(" AUTOMATIC", "keyword")
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
                    partition = Partition(self.partitioning_type, tab_partition)
                    partitioning += f"{partition.get_partition()},"
                partitioning = partitioning[:-1]
                partitioning += "\n)"
            if self.partitioning_type == "HASH":
                partitioning += get_case_formatted(
                    f"\n{get_indentation()}PARTITIONS {len(self.tab_partitions)}", "keyword")
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
