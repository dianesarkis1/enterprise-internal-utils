from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateParseError(ValueError):
    message: str


def parse_date(date_str: str) -> date:
    """
    Parse a date string into a datetime.date.

    Intended supported formats:
      - MM/DD/YYYY  (common in US)
      - DD/MM/YYYY  (common in EU)

    NOTE: This implementation currently contains an intentional bug:
    it assumes MM/DD/YYYY even when input is DD/MM/YYYY.
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

    # BUG: assumes a=month, b=day always.
    month = a
    day = b

    try:
        return date(y, month, day)
    except ValueError as e:
        raise DateParseError(f"Invalid date: {date_str!r}") from e

