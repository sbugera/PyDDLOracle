"""This module contains the Config class to handle configuration settings."""

import argparse
import yaml

class Config:
    """Configuration class."""
    def __init__(self):
        self.args = None
        self.conf = None
        self.conf_con = None

    def get_args(self):
        """Returns command line arguments."""
        arg_parser = argparse.ArgumentParser(
            description="Generate DDL scripts for Oracle database objects"
        )
        arg_parser.add_argument(
            "--schema_name",
            "-s",
            type=str,
            help="DB schema name for which DDL scripts need to be generated",
        )
        arg_parser.add_argument(
            "--config_file",
            "-c",
            type=str,
            default="config.yaml",
            help="Path to the configuration file (default: config.yaml)",
        )
        arg_parser.add_argument(
            "--con_config_file",
            "-cc",
            type=str,
            default="config_con.yaml",
            help="Path to the database connection configuration file (default: config_con.yaml)",
        )
        return arg_parser.parse_args()
    
    def load_config(self, file_path):
        """Load config from YAML file."""
        with open(file_path, "r", encoding="utf-8") as stream:
            try:
                config = yaml.safe_load(stream)
                return config
            except yaml.YAMLError as exc:
                print(f"Error loading YAML file: {exc}")
                return None

config = Config()
