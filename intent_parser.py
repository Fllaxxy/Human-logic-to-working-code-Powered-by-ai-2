"""Intent parsing module.

This module normalizes natural language descriptions into a simple internal
representation that downstream components can use for deterministic code
generation. It is intentionally lightweight and rule-based for predictability.
"""
from __future__ import annotations

from typing import Dict


def parse_intent(description: str) -> Dict[str, object]:
    """Normalize a natural language description.

    The parser performs simple rule-based classification. If the description is
    too vague to classify, an ``error`` flag is set in the returned payload.

    Args:
        description: Free-form natural language text.

    Returns:
        Structured intent dictionary with keys:
        - description: original string
        - inputs: list of expected inputs
        - expected_behavior: short behavior label
        - constraints: list of textual constraints
        - error: optional boolean indicating ambiguity
    """

    normalized = {
        "description": description.strip(),
        "inputs": [],
        "expected_behavior": "",
        "constraints": [],
    }

    text = description.lower()

    if not text or len(text.split()) < 4:
        normalized["error"] = True
        normalized["error_message"] = "Description too ambiguous; need more detail."
        return normalized

    if "even" in text and "list" in text and ("int" in text or "integer" in text):
        normalized["inputs"] = ["list_of_integers"]
        normalized["expected_behavior"] = "filter_even"
        normalized["constraints"] = ["Preserve ordering", "Ignore non-numeric values"]
        return normalized

    if "vowel" in text and "string" in text:
        normalized["inputs"] = ["text"]
        normalized["expected_behavior"] = "count_vowels"
        normalized["constraints"] = ["Case-insensitive"]
        return normalized

    if "tuple" in text and "age" in text and "sort" in text:
        normalized["inputs"] = ["tuples_of_name_age"]
        normalized["expected_behavior"] = "sort_by_age_desc"
        normalized["constraints"] = ["Age descending", "Stable for equal ages"]
        return normalized

    normalized["error"] = True
    normalized["error_message"] = "Description too ambiguous; need more detail."
    return normalized


__all__ = ["parse_intent"]
