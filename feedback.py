"""Feedback module for generated code quality."""
from __future__ import annotations

from typing import Dict, List


def generate_feedback(code: str, execution: Dict[str, object]) -> List[str]:
    """Produce concise refactor suggestions for generated code."""
    suggestions: List[str] = []

    if not code:
        return suggestions

    if "run_task" not in code:
        suggestions.append("Ensure a run_task entry point is defined for execution.")

    suggestions.append("Add docstrings to clarify expected input types and outputs.")
    suggestions.append("Include validation for edge cases such as empty or malformed data.")
    suggestions.append("Extract pure logic into helpers to simplify unit testing.")

    if execution.get("status") == "success":
        suggestions.append("Consider adding type hints for intermediate variables for clarity.")
    else:
        suggestions.append("Improve error handling to provide user-friendly feedback.")

    return suggestions


__all__ = ["generate_feedback"]
