"""Handles Oracle database storage definitions and DDL generation."""

from pyddl_oracle.utils import get_case_formatted, get_size_formatted


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class Storage:
    """Builder for Oracle STORAGE/TABLESPACE clauses.

    Usage:
        Storage(indentation, tablespace_name, ...).build()
    """

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(
        self,
        indentation,
        tablespace_name,
        pct_free,
        ini_trans,
        max_trans,
        min_extents,
        max_extents,
        pct_increase,
        buffer_pool,
        flash_cache,
        cell_flash_cache,
        initial_extent=None,
        next_extent=None,
        local_index=None,
    ):
        self.indentation = indentation
        self.tablespace_name = tablespace_name
        self.pct_free = pct_free
        self.ini_trans = ini_trans
        self.max_trans = max_trans
        self.min_extents = min_extents
        self.max_extents = max_extents
        self.pct_increase = pct_increase
        self.buffer_pool = buffer_pool
        self.flash_cache = flash_cache
        self.cell_flash_cache = cell_flash_cache
        self.initial_extent = initial_extent
        self.next_extent = next_extent
        self.local_index = local_index

    # pylint: disable=too-many-branches, too-many-statements
    def build(self):
        """Generate storage clause based on config and settings."""
        indentation = self.indentation
        storage = ""
        if str(self.tablespace_name) != "nan" and self.local_index != "YES":
            statement = get_case_formatted(
                f"\n{indentation}TABLESPACE <:1>", "keyword"
            )
            storage = statement.replace(
                "<:1>", get_case_formatted(self.tablespace_name, "identifier")
            )
        if str(self.pct_free) != "nan":
            statement = get_case_formatted(
                f"\n{indentation}PCTFREE    <:1>", "keyword"
            )
            storage += statement.replace("<:1>", str(int(self.pct_free)))
        if str(self.ini_trans) != "nan":
            statement = get_case_formatted(
                f"\n{indentation}INITRANS   <:1>", "keyword"
            )
            storage += statement.replace("<:1>", str(int(self.ini_trans)))
        if str(self.max_trans) != "nan":
            statement = get_case_formatted(
                f"\n{indentation}MAXTRANS   <:1>", "keyword"
            )
            storage += statement.replace("<:1>", str(int(self.max_trans)))
        storage_tmp = get_case_formatted(
            f"\n{indentation}STORAGE    (",
            "keyword",
        )
        if (
            self.initial_extent
            and str(self.initial_extent) not in ("nan", "DEFAULT", "-1")
        ):
            statement = get_case_formatted(
                f"\n{indentation}            INITIAL          <:1>", "keyword"
            )
            storage_tmp += statement.replace(
                "<:1>", get_size_formatted(self.initial_extent)
            )
        if (
            self.next_extent
            and str(self.next_extent) not in ("nan", "DEFAULT", "-1")
        ):
            statement = get_case_formatted(
                f"\n{indentation}            NEXT             <:1>", "keyword"
            )
            storage_tmp += statement.replace(
                "<:1>", str(int(self.next_extent / 1024 / 1024)) + "M"
            )
        if (
            self.min_extents
            and str(self.min_extents) not in ("nan", "DEFAULT", "-1")
        ):
            statement = get_case_formatted(
                f"\n{indentation}            MINEXTENTS       <:1>", "keyword"
            )
            storage_tmp += statement.replace(
                "<:1>", str(int(self.min_extents))
            )
        if (
            self.max_extents
            and str(self.max_extents) not in ("nan", "DEFAULT", "-1")
        ):
            if self.max_extents == 2147483645:
                storage_tmp += get_case_formatted(
                    f"\n{indentation}            MAXEXTENTS       UNLIMITED",
                    "keyword",
                )
            else:
                storage_tmp += get_case_formatted(
                    f"\n{indentation}            "
                    f"MAXEXTENTS       {int(self.max_extents)}",
                    "keyword",
                )
        if (
            self.pct_increase
            and str(self.pct_increase) not in ("nan", "DEFAULT", "-1")
        ):
            storage_tmp += get_case_formatted(
                f"\n{indentation}            PCTINCREASE      "
                f"{int(self.pct_increase)}",
                "keyword",
            )
        if (
            str(self.pct_increase) in ("nan", "None")
            and self.local_index != "YES"
        ):
            storage_tmp += get_case_formatted(
                f"\n{indentation}            PCTINCREASE      0", "keyword"
            )
        if self.buffer_pool and self.buffer_pool != "DEFAULT2":
            statement = get_case_formatted(
                f"\n{indentation}            BUFFER_POOL      <:1>", "keyword"
            )
            storage_tmp += statement.replace(
                "<:1>", get_case_formatted(self.buffer_pool, "identifier")
            )
        if self.flash_cache and self.flash_cache != "DEFAULT":
            statement = get_case_formatted(
                f"\n{indentation}            FLASH_CACHE      <:1>", "keyword"
            )
            storage_tmp += statement.replace(
                "<:1>", get_case_formatted(self.flash_cache, "identifier")
            )
        if self.cell_flash_cache and self.cell_flash_cache != "DEFAULT":
            statement = get_case_formatted(
                f"\n{indentation}            CELL_FLASH_CACHE <:1>", "keyword"
            )
            storage_tmp += statement.replace(
                "<:1>", get_case_formatted(self.cell_flash_cache, "identifier")
            )
        if storage_tmp != get_case_formatted(
            f"\n{indentation}STORAGE    (", "keyword"
        ):
            storage += f"{storage_tmp}\n{indentation}            )"
        return storage
