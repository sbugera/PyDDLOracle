import pandas as pd
from utils import get_case_formatted, get_object_name, get_indentation


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
        if self.data_type_owner and str(self.data_type_owner) != "None" and str(self.data_type_owner) != "nan":
            data_type = get_object_name(self.data_type_owner, self.data_type, "keyword")
        else:
            data_type = get_case_formatted(self.data_type, "keyword")

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
        elif data_type.upper() == "FLOAT":
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
