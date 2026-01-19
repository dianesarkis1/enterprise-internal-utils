from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# Standard format hint used in error messages
_FORMAT_HINT = "Expected format: MM/DD/YYYY or DD/MM/YYYY"


@dataclass(frozen=True)
class DateParseError(ValueError):
    """Custom exception for date parsing errors with standardized messages."""
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
        raise DateParseError(f"Empty input provided. {_FORMAT_HINT}")

    # Accept either '/' or '-' separators for basic flexibility.
    sep = "/" if "/" in s else "-" if "-" in s else None
    if sep is None:
        raise DateParseError(
            f"Unsupported date format: '{date_str}'. {_FORMAT_HINT}"
        )

    parts = s.split(sep)
    if len(parts) != 3:
        raise DateParseError(
            f"Unsupported date format: '{date_str}'. {_FORMAT_HINT}"
        )

    try:
        a = int(parts[0])
        b = int(parts[1])
        y = int(parts[2])
    except ValueError as e:
        raise DateParseError(
            f"Non-integer date components in '{date_str}'. "
            "All date parts must be integers."
        ) from e

    if y < 1900 or y > 2100:
        raise DateParseError(
            f"Year {y} out of range. Year must be between 1900 and 2100."
        )

    # BUG: assumes a=month, b=day always.
    month = a
    day = b

    try:
        return date(y, month, day)
    except ValueError as e:
        raise DateParseError(
            f"Invalid date: '{date_str}'. "
            "The date components do not form a valid calendar date."
        ) from e

