"""Natural language to code service entry point.

Example:
    >>> from main import process_nl_request
    >>> response = process_nl_request({
    ...     "natural_language": "Given a list of integers, return only the even ones.",
    ...     "input_data": [1, 2, 3, 4],
    ... })
    >>> print(response["execution"]["output"])
    [2, 4]

Sample JSON output shape:
    {
        "normalized_intent": {...},
        "generated_code": "...",
        "execution": {
            "status": "success",
            "output": [2, 4],
            "stdout": "",
            "error_type": null,
            "error_message": null,
            "traceback": null
        },
        "refactor_suggestions": ["..."]
    }
"""
from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from code_generator import generate_code
from feedback import generate_feedback
from intent_parser import parse_intent
from sandbox import SandboxExecutor


def process_nl_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Process a natural language request into code and execution results."""
    description = request.get("natural_language", "")
    input_data = request.get("input_data")

    normalized_intent = parse_intent(description)

    code_payload = generate_code(normalized_intent)
    generated_code = code_payload.get("code", "")

    if "error_message" in code_payload:
        execution = {
            "status": "error",
            "output": None,
            "stdout": "",
            "error_type": "IntentError",
            "error_message": code_payload["error_message"],
            "traceback": None,
        }
        refactor_suggestions = []
    else:
        executor = SandboxExecutor()
        execution = executor.run(generated_code, input_data)
        refactor_suggestions = generate_feedback(generated_code, execution)

    return {
        "normalized_intent": normalized_intent,
        "generated_code": generated_code,
        "execution": execution,
        "refactor_suggestions": refactor_suggestions,
    }


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Natural language to code service")
    parser.add_argument("--desc", "--description", dest="description", required=True, help="Task description")
    parser.add_argument("--input", dest="input_data", default=None, help="JSON input data")
    args = parser.parse_args()

    input_value: Any
    if args.input_data is None:
        input_value = None
    else:
        try:
            input_value = json.loads(args.input_data)
        except json.JSONDecodeError:
            input_value = args.input_data

    response = process_nl_request({
        "natural_language": args.description,
        "input_data": input_value,
    })

    print(json.dumps(response, indent=2, default=str))


if __name__ == "__main__":
    _cli()
