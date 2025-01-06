"""Utils module."""

import re
import os
from collections import namedtuple
from pprint import PrettyPrinter
from config import config as c


def get_dataframe_namedtuple(df, index):
    """Returns the row of a pandas dataframe as a namedtuple."""
    if index >= len(df):
        return None
    row = df.iloc[index]
    row_namedtuple = namedtuple("row", row.index)
    return row_namedtuple(*row.values)


def replace_multiple_newlines(text):
    """Replace multiple newlines with a single newline."""
    return re.sub(r"\n+$", "\n", text)


def pprint(variable):
    """Pretty print a variable."""
    pp = PrettyPrinter(
        indent=1, width=80, depth=None, stream=None, compact=False
    )
    try:
        pp.pprint(variable._asdict())
    except AttributeError:
        pp.pprint(variable)


def get_case_formatted(value, config_name_for_upper):
    """Get case formatted value."""
    if not value:
        return ""
    if value != value.upper():
        return f'"{value}"'
    
    if c.conf["case"][config_name_for_upper] == "uppercase":
        return value.upper()
    else:
        return value.lower()


def add_quotes(value):
    """Add quotes to value."""
    if any(char.islower() for char in value):
        return f'"{value}"'
    else:
        return value


def get_indentation():
    """Get indentation based on config."""
    return "    "


def get_file_path(object_type, object_owner, object_name):
    """Get file path based on config."""
    file_path_template = c.conf["file_path"][object_type]
    pattern = r"\{(.*?)\}"
    matches = re.findall(pattern, file_path_template)
    file_path = file_path_template

    for match in matches:
        case_function = str.lower
        if match == match.upper():
            case_function = str.upper

        if match.lower() == "object_type":
            file_path = file_path.replace(
                case_function("{object_type}"), case_function(object_type)
            )
        elif match.lower() == "object_owner":
            file_path = file_path.replace(
                case_function("{object_owner}"), case_function(object_owner)
            )
        elif match.lower() == "object_name":
            file_path = file_path.replace(
                case_function("{object_name}"), case_function(object_name)
            )

    return file_path


def prepare_directories(file_path):
    """Create directories if they don't exist."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_size_formatted(initial_extent):
    """Get size formatted based on config."""
    if initial_extent >= 1024 * 1024 * 1024:
        return str(int(initial_extent / 1024 / 1024 / 1024)) + "G"
    if initial_extent >= 1024 * 1024:
        return str(int(initial_extent / 1024 / 1024)) + "M"
    if initial_extent >= 1024:
        return str(int(initial_extent / 1024)) + "K"


def get_object_name(object_owner, object_name, config_name_for_upper):
    """Get object name based on config."""
    return (
        get_case_formatted(object_owner, config_name_for_upper)
        + "."
        + get_case_formatted(object_name, config_name_for_upper)
    )


def get_prompt(prompt_text, *values):
    """Get prompt based on config."""
    if c.conf["prompts"] == "yes":
        has_placeholders = re.search(r"<:1>", prompt_text)
        prompt = get_case_formatted("PROMPT", "keyword")
        if has_placeholders:
            prompt += f" {prompt_text}\n"
        else:
            prompt += f" {prompt_text}<:1>\n"
        for i, value in enumerate(values, 1):
            placeholder = "<:" + str(i) + ">"
            prompt = prompt.replace(placeholder, str(value))
        return prompt
    else:
        return ""
