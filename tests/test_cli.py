from cli import main


def test_cli_parse_date_smoke(capsys):
    rc = main(["parse-date", "01/31/2026"])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out == "2026-01-31"

