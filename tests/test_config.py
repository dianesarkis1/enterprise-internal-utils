from pathlib import Path

import pytest

from utils.config import ConfigError, load_yaml_config


def test_load_yaml_config_missing(tmp_path: Path):
    with pytest.raises(ConfigError):
        load_yaml_config(tmp_path / "nope.yaml")


def test_load_yaml_config_normalizes_defaults(tmp_path: Path):
    p = tmp_path / "cfg.yaml"
    p.write_text("service_name: billing-api\n", encoding="utf-8")
    cfg = load_yaml_config(p)
    assert cfg["service_name"] == "billing-api"
    assert cfg["environment"] == "dev"
    assert cfg["log_level"] == "INFO"

