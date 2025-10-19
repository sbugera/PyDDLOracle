"""Unit tests for pyddl_oracle.config.Config."""

import sys

from pyddl_oracle.config import config as c


def test_get_args_defaults(monkeypatch):
    monkeypatch.setenv("PYTHONWARNINGS", "")
    monkeypatch.setattr(sys, "argv", ["prog"])  # no args
    args = c.get_args()
    assert args.schema_name is None
    assert args.config_file == "config.yaml"
    assert args.con_config_file == "config_con.yaml"


def test_get_args_custom_values(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "prog",
            "-s",
            "test_schema",
            "-c",
            "my_config.yaml",
            "-cc",
            "my_con.yaml",
        ],
    )
    args = c.get_args()
    assert args.schema_name == "test_schema"
    assert args.config_file == "my_config.yaml"
    assert args.con_config_file == "my_con.yaml"


def test_load_config_success(tmp_path):
    yaml_path = tmp_path / "cfg.yaml"
    yaml_path.write_text(
        """
case:
  keyword: uppercase
"""
    )
    data = c.load_config(str(yaml_path))
    assert isinstance(data, dict)
    assert data["case"]["keyword"] == "uppercase"


def test_load_config_invalid_yaml(tmp_path, capsys):
    bad_path = tmp_path / "bad.yaml"
    bad_path.write_text("case: [unclosed\n")
    result = c.load_config(str(bad_path))
    captured = capsys.readouterr().out
    assert result is None
    assert "Error loading YAML file:" in captured


