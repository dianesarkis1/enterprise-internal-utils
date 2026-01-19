import pytest

from utils.dates import DateParseError, parse_date


def test_parse_us_date_mmddyyyy():
    d = parse_date("01/31/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_parse_eu_date_ddmmyyyy():
    # This test is expected to FAIL until the bug is fixed.
    d = parse_date("31/01/2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


# --- Tests for standardized error messages ---


def test_error_empty_string():
    """Test that empty string input raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("")
    assert "Empty input provided" in exc_info.value.message
    assert "Expected format: MM/DD/YYYY or DD/MM/YYYY" in exc_info.value.message


def test_error_whitespace_only():
    """Test that whitespace-only input raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("   ")
    assert "Empty input provided" in exc_info.value.message
    assert "Expected format: MM/DD/YYYY or DD/MM/YYYY" in exc_info.value.message


def test_error_none_input():
    """Test that None input raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date(None)
    assert "Empty input provided" in exc_info.value.message
    assert "Expected format: MM/DD/YYYY or DD/MM/YYYY" in exc_info.value.message


def test_error_unsupported_format_no_separator():
    """Test that input without separator raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01312026")
    assert "Unsupported date format" in exc_info.value.message
    assert "01312026" in exc_info.value.message
    assert "Expected format: MM/DD/YYYY or DD/MM/YYYY" in exc_info.value.message


def test_error_unsupported_format_wrong_parts():
    """Test that input with wrong number of parts raises DateParseError."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/31")
    assert "Unsupported date format" in exc_info.value.message
    assert "01/31" in exc_info.value.message
    assert "Expected format: MM/DD/YYYY or DD/MM/YYYY" in exc_info.value.message


def test_error_unsupported_format_too_many_parts():
    """Test that input with too many parts raises DateParseError."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/31/2026/extra")
    assert "Unsupported date format" in exc_info.value.message
    assert "Expected format: MM/DD/YYYY or DD/MM/YYYY" in exc_info.value.message


def test_error_non_integer_month():
    """Test that non-integer month raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("Jan/31/2026")
    assert "Non-integer date components" in exc_info.value.message
    assert "Jan/31/2026" in exc_info.value.message
    assert "All date parts must be integers" in exc_info.value.message


def test_error_non_integer_day():
    """Test that non-integer day raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/thirty-one/2026")
    assert "Non-integer date components" in exc_info.value.message
    assert "01/thirty-one/2026" in exc_info.value.message
    assert "All date parts must be integers" in exc_info.value.message


def test_error_non_integer_year():
    """Test that non-integer year raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/31/YYYY")
    assert "Non-integer date components" in exc_info.value.message
    assert "01/31/YYYY" in exc_info.value.message
    assert "All date parts must be integers" in exc_info.value.message


def test_error_year_out_of_range_too_low():
    """Test that year below 1900 raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/31/1899")
    assert "Year 1899 out of range" in exc_info.value.message
    assert "Year must be between 1900 and 2100" in exc_info.value.message


def test_error_year_out_of_range_too_high():
    """Test that year above 2100 raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/31/2101")
    assert "Year 2101 out of range" in exc_info.value.message
    assert "Year must be between 1900 and 2100" in exc_info.value.message


def test_error_invalid_date_feb_30():
    """Test that invalid date (Feb 30) raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("02/30/2026")
    assert "Invalid date" in exc_info.value.message
    assert "02/30/2026" in exc_info.value.message
    assert "The date components do not form a valid calendar date" in exc_info.value.message


def test_error_invalid_date_month_13():
    """Test that invalid month (13) raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("13/01/2026")
    assert "Invalid date" in exc_info.value.message
    assert "13/01/2026" in exc_info.value.message
    assert "The date components do not form a valid calendar date" in exc_info.value.message


def test_error_invalid_date_day_32():
    """Test that invalid day (32) raises DateParseError with standardized message."""
    with pytest.raises(DateParseError) as exc_info:
        parse_date("01/32/2026")
    assert "Invalid date" in exc_info.value.message
    assert "01/32/2026" in exc_info.value.message
    assert "The date components do not form a valid calendar date" in exc_info.value.message


# --- Tests for valid inputs (backward compatibility) ---


def test_valid_date_with_dash_separator():
    """Test that dash separator works for valid dates."""
    d = parse_date("01-31-2026")
    assert d.year == 2026 and d.month == 1 and d.day == 31


def test_valid_date_boundary_year_1900():
    """Test that year 1900 is accepted."""
    d = parse_date("01/15/1900")
    assert d.year == 1900 and d.month == 1 and d.day == 15


def test_valid_date_boundary_year_2100():
    """Test that year 2100 is accepted."""
    d = parse_date("12/31/2100")
    assert d.year == 2100 and d.month == 12 and d.day == 31

