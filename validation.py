"""Validation rules for student marks."""

MIN_MARK = 0
MAX_MARK = 100
INVALID_MARK_MESSAGE = "Invalid marks. Enter 0-100."


def validate_mark(mark):
    """Return True if mark is within the allowed range (inclusive)."""
    return MIN_MARK <= mark <= MAX_MARK
