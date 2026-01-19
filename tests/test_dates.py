from utils.dates import parse_date


def test_parse_us_date_mmddyyyy():
    d = parse_date("01/31/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_eu_date_ddmmyyyy():
    # This test is expected to FAIL until the bug is fixed.
    d = parse_date("31/01/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31

