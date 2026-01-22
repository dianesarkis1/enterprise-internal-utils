from pathlib import Path

from cli import main


def test_cli_parse_date_smoke(capsys):
    rc = main(["parse-date", "01/31/2026"])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out == "2026-01-31"


def test_cli_validate_config_dry_run_valid(capsys, tmp_path: Path):
    cfg_file = tmp_path / "valid.yaml"
    cfg_file.write_text("service_name: my-service\n", encoding="utf-8")
    rc = main(["validate-config", str(cfg_file), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out == "OK"


def test_cli_validate_config_dry_run_missing_file(capsys, tmp_path: Path):
    missing_file = tmp_path / "missing.yaml"
    rc = main(["validate-config", str(missing_file), "--dry-run"])
    assert rc == 1
    out = capsys.readouterr().out.strip()
    assert "Error:" in out
    assert "Config not found" in out


def test_cli_validate_config_dry_run_invalid_yaml(capsys, tmp_path: Path):
    invalid_file = tmp_path / "invalid.yaml"
    invalid_file.write_text(":\n  - invalid: yaml: content\n", encoding="utf-8")
    rc = main(["validate-config", str(invalid_file), "--dry-run"])
    assert rc == 1
    out = capsys.readouterr().out.strip()
    assert "Error:" in out

