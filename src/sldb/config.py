import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


PythonExpressionFilter = Callable[[str, Dict[str, Any]], bool]


@dataclass(frozen=True)
class SLDBConfig:
    python_execution_mode: str = "safe"
    python_expression_filter: Optional[PythonExpressionFilter] = None


_VALID_PYTHON_EXECUTION_MODES = {"safe", "unsafe"}
_UNSET = object()


def _normalize_python_execution_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized not in _VALID_PYTHON_EXECUTION_MODES:
        valid_modes = ", ".join(sorted(_VALID_PYTHON_EXECUTION_MODES))
        raise ValueError(
            f"Unsupported python_execution_mode '{mode}'. Expected one of: {valid_modes}."
        )
    return normalized


_active_config = SLDBConfig(
    python_execution_mode=_normalize_python_execution_mode(
        os.getenv("SLDB_PYTHON_EXECUTION_MODE", "safe")
    )
)


def get_config() -> SLDBConfig:
    return _active_config


def configure(
    *,
    python_execution_mode: Optional[str] = None,
    python_expression_filter: Any = _UNSET,
) -> SLDBConfig:
    global _active_config

    mode = _active_config.python_execution_mode
    if python_execution_mode is not None:
        mode = _normalize_python_execution_mode(python_execution_mode)

    expression_filter = _active_config.python_expression_filter
    if python_expression_filter is not _UNSET:
        expression_filter = python_expression_filter

    _active_config = SLDBConfig(
        python_execution_mode=mode,
        python_expression_filter=expression_filter,
    )
    return _active_config


def reset_config() -> SLDBConfig:
    return configure(
        python_execution_mode=_normalize_python_execution_mode(
            os.getenv("SLDB_PYTHON_EXECUTION_MODE", "safe")
        ),
        python_expression_filter=None,
    )


def python_expression_is_allowed(expression: str, data: Dict[str, Any]) -> bool:
    config = get_config()
    if config.python_execution_mode != "unsafe":
        return False

    if config.python_expression_filter is None:
        return True

    return bool(config.python_expression_filter(expression, data))
