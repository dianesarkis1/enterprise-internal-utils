from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils.config import ConfigError, load_yaml_config
from utils.dates import parse_date


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="enterprise-internal-utils")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_parse = sub.add_parser("parse-date", help="Parse a date string into ISO-8601 (YYYY-MM-DD)")
    p_parse.add_argument("date_str", help='Date string like "01/31/2026" or "31/01/2026"')

    p_cfg = sub.add_parser("validate-config", help="Load a YAML config and print normalized JSON")
    p_cfg.add_argument("path", type=str, help="Path to YAML config file")
    p_cfg.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config without printing full contents; print 'OK' on success or error on failure",
    )

    args = parser.parse_args(argv)

    if args.cmd == "parse-date":
        dt = parse_date(args.date_str)
        print(dt.isoformat())
        return 0

    if args.cmd == "validate-config":
        if args.dry_run:
            try:
                load_yaml_config(Path(args.path))
                print("OK")
                return 0
            except ConfigError as e:
                print(f"Error: {e}")
                return 1
        cfg = load_yaml_config(Path(args.path))
        print(json.dumps(cfg, indent=2, sort_keys=True))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

