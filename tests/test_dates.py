from utils.dates import parse_date


def test_parse_us_date_mmddyyyy():
    d = parse_date("01/31/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_eu_date_ddmmyyyy():
    d = parse_date("31/01/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_eu_date_with_day_greater_than_12():
    d = parse_date("25/12/2025")
    assert d.year == 2025 and d.month == 12 and d.day == 25


def test_parse_us_date_with_day_greater_than_12():
    d = parse_date("12/25/2025")
    assert d.year == 2025 and d.month == 12 and d.day == 25


def test_parse_ambiguous_date_defaults_to_us():
    d = parse_date("01/02/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 2

