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

    The function automatically detects the format based on the values:
      - If the first number > 12, it must be a day (EU format DD/MM/YYYY)
      - If the second number > 12, it must be a day (US format MM/DD/YYYY)
      - If both numbers are <= 12, defaults to US format (MM/DD/YYYY)
    """
    s = (date_str or "").strip()
    if not s:
        raise DateParseError("date_str is empty")

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

    if a > 12:
        day = a
        month = b
    else:
        month = a
        day = b

    try:
        return date(y, month, day)
    except ValueError as e:
        raise DateParseError(f"Invalid date: {date_str!r}") from e

