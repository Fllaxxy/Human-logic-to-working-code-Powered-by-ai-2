"""Sandbox execution module.

Executes generated code strings in a constrained namespace to limit available
builtins and capture runtime errors for reporting.
"""
from __future__ import annotations

import builtins
import io
import traceback
from contextlib import redirect_stdout
from typing import Any, Dict

_SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in [
        "__import__",
        "abs",
        "all",
        "any",
        "bool",
        "dict",
        "enumerate",
        "float",
        "int",
        "len",
        "list",
        "map",
        "max",
        "min",
        "pow",
        "range",
        "set",
        "sorted",
        "str",
        "sum",
        "tuple",
        "zip",
        "isinstance",
        "Exception",
        "ValueError",
        "TypeError",
        "print",
    ]
}


class SandboxExecutor:
    """Run code strings safely with limited builtins."""

    def __init__(self) -> None:
        self._globals: Dict[str, Any] = {"__builtins__": _SAFE_BUILTINS}

    def run(self, code: str, input_data: Any) -> Dict[str, Any]:
        """Execute code and return structured execution data."""
        stdout_capture = io.StringIO()
        sandbox_globals: Dict[str, Any] = dict(self._globals)

        try:
            exec(code, sandbox_globals, sandbox_globals)
            run_task = sandbox_globals.get("run_task")
            if run_task is None:
                raise RuntimeError("Generated code missing run_task entry point.")

            with redirect_stdout(stdout_capture):
                output = run_task(input_data)

            return {
                "status": "success",
                "output": output,
                "stdout": stdout_capture.getvalue(),
                "error_type": None,
                "error_message": None,
                "traceback": None,
            }
        except Exception as exc:  # noqa: B902 - intentional broad capture for sandboxing
            return {
                "status": "error",
                "output": None,
                "stdout": stdout_capture.getvalue(),
                "error_type": exc.__class__.__name__,
                "error_message": str(exc),
                "traceback": traceback.format_exc(),
            }


__all__ = ["SandboxExecutor"]
