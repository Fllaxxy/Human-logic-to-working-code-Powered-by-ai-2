"""Code generation module.

Converts normalized intent structures into deterministic Python code strings
that define a ``run_task`` entry point. The generated snippets are deliberately
minimal and free of side effects.
"""
from __future__ import annotations

from typing import Dict


def generate_code(intent: Dict[str, object]) -> Dict[str, object]:
    """Generate Python code for the provided intent.

    Args:
        intent: Normalized intent dictionary.

    Returns:
        A dictionary with either ``code`` containing the Python source or an
        ``error_message`` explaining why code could not be generated.
    """

    if intent.get("error"):
        return {"error_message": intent.get("error_message", "Invalid intent.")}

    behavior = intent.get("expected_behavior")

    if behavior == "filter_even":
        code = _even_filter_code()
    elif behavior == "count_vowels":
        code = _vowel_count_code()
    elif behavior == "sort_by_age_desc":
        code = _sort_age_code()
    else:
        return {"error_message": "Unsupported intent."}

    return {"code": code}


def _even_filter_code() -> str:
    return '''
from typing import Any, Iterable


def run_task(input_data: Any):
    """Return only even numeric values from the provided iterable."""
    numbers = input_data if input_data is not None else []
    if not isinstance(numbers, Iterable):
        raise ValueError("Expected an iterable of numbers.")

    even_numbers = []
    for value in numbers:
        if isinstance(value, (int, float)) and value % 2 == 0:
            even_numbers.append(value)
    return even_numbers
'''


def _vowel_count_code() -> str:
    return '''
from typing import Any

VOWELS = set("aeiouAEIOU")


def run_task(input_data: Any):
    """Count vowels in the provided text."""
    text = "" if input_data is None else str(input_data)
    count = 0
    for char in text:
        if char in VOWELS:
            count += 1
    return count
'''


def _sort_age_code() -> str:
    return '''
from typing import Any, Iterable, Tuple, List


def run_task(input_data: Any):
    """Sort (name, age) tuples by age descending and preserve stability."""
    records: List[Tuple[Any, Any]] = []
    if input_data is None:
        return records

    if not isinstance(input_data, Iterable):
        raise ValueError("Expected an iterable of (name, age) tuples.")

    for item in input_data:
        if not (isinstance(item, (list, tuple)) and len(item) == 2):
            raise ValueError("Each record must be a (name, age) pair.")
        name, age = item
        records.append((name, age))

    return sorted(records, key=lambda pair: pair[1], reverse=True)
'''


__all__ = ["generate_code"]
