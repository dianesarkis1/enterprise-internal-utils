from utils.dates import parse_date


def test_parse_us_date_mmddyyyy():
    d = parse_date("01/31/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_eu_date_ddmmyyyy():
    d = parse_date("31/01/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_date_with_dash_separator():
    d = parse_date("31-01-2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_ambiguous_date_defaults_to_us_format():
    d = parse_date("01/02/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 2

