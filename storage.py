from utils import get_case_formatted, get_size_formatted


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
            storage_tmp += get_case_formatted(
                f"\n{indentation}            MAXEXTENTS       {int(max_extents)}", "keyword")
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
