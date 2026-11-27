from __future__ import annotations

from typing import Any

from sldb.core.renderer_engine.config import python_expression_is_allowed


class PythonExpressionRenderer:
    """
    Handles rendering of ⸢py•expression⸥ markers.
    """

    def render(self, expression: str, data: dict[str, Any], fallback: str) -> str:
        if not python_expression_is_allowed(expression, data):
            return fallback
        safe_builtins = {"str": str, "int": int, "float": float, "len": len, "min": min, "max": max, "sum": sum, "sorted": sorted, "list": list, "dict": dict, "set": set, "tuple": tuple, "enumerate": enumerate}
        try:
            value = eval(expression, {"__builtins__": safe_builtins}, dict(data))
        except Exception:
            return fallback
        return "" if value is None else str(value)
