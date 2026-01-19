from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateParseError(ValueError):
    message: str


def parse_date(date_str: str) -> date:
    """
    Parse a date string into a datetime.date.

    Supported formats:
      - MM/DD/YYYY  (common in US)
      - DD/MM/YYYY  (common in EU)

    Format detection:
      - If the first number is > 12, it's treated as DD/MM/YYYY (EU format)
      - If the second number is > 12, it's treated as MM/DD/YYYY (US format)
      - For ambiguous dates (both values <= 12), defaults to MM/DD/YYYY (US format)
        for backward compatibility

    Separators: Both '/' and '-' are accepted.

    Raises:
        DateParseError: If the date string is empty, has an unsupported format,
            contains non-integer components, or represents an invalid date.
    """
    s = (date_str or "").strip()
    if not s:
        raise DateParseError("date_str is empty")

    # Accept either '/' or '-' separators for basic flexibility.
    sep = "/" if "/" in s else "-" if "-" in s else None
    if sep is None:
        raise DateParseError(f"Unsupported date format: {date_str!r}")

    parts = s.split(sep)
    if len(parts) != 3:
        raise DateParseError(f"Unsupported date format: {date_str!r}")

    try:
        a = int(parts[0])
        b = int(parts[1])
        y = int(parts[2])
    except ValueError as e:
        raise DateParseError(f"Non-integer date components: {date_str!r}") from e

    if y < 1900 or y > 2100:
        raise DateParseError(f"Year out of range: {y}")

    # Detect format based on which value can only be a day (> 12)
    if a > 12:
        # First number > 12, so it must be day (DD/MM/YYYY format)
        day = a
        month = b
    elif b > 12:
        # Second number > 12, so it must be day (MM/DD/YYYY format)
        month = a
        day = b
    else:
        # Ambiguous case (both <= 12): default to US format (MM/DD/YYYY)
        # for backward compatibility
        month = a
        day = b

    try:
        return date(y, month, day)
    except ValueError as e:
        raise DateParseError(f"Invalid date: {date_str!r}") from e

