from utils.dates import parse_date


def test_parse_us_date_mmddyyyy():
    """Test US date format (MM/DD/YYYY) where day > 12."""
    d = parse_date("01/31/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_eu_date_ddmmyyyy():
    """Test EU date format (DD/MM/YYYY) where day > 12."""
    d = parse_date("31/01/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_ambiguous_date_defaults_to_us():
    """Test ambiguous date (both components <= 12) defaults to US format."""
    # 01/02/2026 is ambiguous: could be Jan 2 (US) or Feb 1 (EU)
    # Should default to US format: January 2, 2026
    d = parse_date("01/02/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 2


def test_parse_date_with_dash_separator():
    """Test date parsing with dash separator."""
    d = parse_date("31-01-2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31

