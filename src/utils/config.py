from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    pass


def load_yaml_config(path: Path) -> dict[str, Any]:
    """
    Load a YAML config file.

    Enterprise-ish behavior:
      - requires the file exist
      - requires it parse to a mapping/dict at top level
      - normalizes some expected keys for downstream services
    """
    if not path.exists():
        raise ConfigError(f"Config not found: {path}")

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ConfigError(f"Failed to parse YAML: {path}") from e

    if raw is None:
        return {}

    if not isinstance(raw, dict):
        raise ConfigError("Top-level YAML must be a mapping/object")

    # Normalize: ensure these keys exist (common in internal services)
    raw.setdefault("service_name", "unknown-service")
    raw.setdefault("environment", "dev")
    raw.setdefault("log_level", "INFO")

    return raw

