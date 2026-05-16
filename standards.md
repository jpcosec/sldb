# SLDB Python Coding Standards

This document defines the architectural and stylistic rules for the SLDB project. Compliance with these rules is mandatory for all contributions.

## Layer 0: System Integrity & Visual Health

1.  **Code as Truth:** The code must be self-documenting. Class and method names must be verbose and accurately reflect their purpose.
2.  **Structural Visualizability:** A health check for the codebase is its ability to be parsed into a readable component diagram. If the resulting diagram is a "spaghetti" mess, the code must be refactored.
3.  **Step 0 - Compliance:** Every task must begin with a compliance check against these standards.

## Layer 1: Modularity & Scale

1.  **The 100-Line Rule:** No file should exceed 100 lines of code (excluding docstrings and imports). Files exceeding this limit must be refactored into classes, with methods potentially moved to separate modules.
2.  **The 15-Line Rule:** No function or method should exceed 15 lines of logic. Complex functions must be divided into smaller, discrete steps.
3.  **Single Class Per File:** Each file should contain exactly one class.
4.  **Single Responsibility (SRP):** No class should perform more than one distinct function. If a class accumulates multiple responsibilities, extract a primitive abstract class or delegate to sibling services.
5.  **Utilitary Consolidation:** If two functions perform essentially the same logic, they must be merged into a separate utility service or base class.
6.  **Complex Functions as Classes:** If a function accumulates more than 4 local variables or requires multiple passes over the same data, transform it into a class with a `__call__` method or discrete stage methods (CS-9).

## Layer 2: Data & Type Safety

1.  **Pydantic-First Boundaries:** All inter-module data transfers must use Pydantic `BaseModel` (or `StructuredNLDoc`) subclasses.
2.  **No Type Erosion:** Never use `dict`, `Any`, or plain `str` to carry structured data across module boundaries.
3.  **Semantic Descriptions:** Every Pydantic field must carry a `Field(description="...")`. The description must explain the *intent* of the data, not just repeat the field name.
4.  **Strict Typing:** Use `from __future__ import annotations` in every module. All public symbols must have complete type hints.

## Layer 3: Documentation

1.  **Standardized Docstrings:** Every public class and method must have a Google-style docstring.
    *   One-line summary.
    *   `Args` section.
    *   `Returns` section.
    *   `Raises` section (if applicable).
2.  **Module Docstrings:** Every module must start with a docstring explaining its role in the system.

## Layer 4: Error Management

1.  **Domain Exceptions:** All custom exceptions must be defined in `sldb.core.exceptions` or a local `exceptions.py`.
2.  **Typed Catching:** Catch only specific, typed exceptions. Never use `except Exception:` for flow control.
3.  **No Silent Errors:** Never use `pass` in an `except` block. Log the error or re-raise.
4.  **Preserve Chains:** Always use `raise NewError(...) from e` to preserve the exception trace.

## Toolchain Configuration

The project uses the following tools for enforcement:

*   **ruff:** For linting and formatting (replaces flake8, isort, black).
*   **mypy:** For strict type checking.
*   **docstring-coverage:** To ensure 100% docstring presence.

---

## Compliance Status

| Component | Status | Note |
|---|---|---|
| sldb.core | Partial | Requires docstring audit and line-length check. |
| sldb.store | Partial | Requires docstring audit. |
| sldb.cli | **FAIL** | `main.py` is oversized (~1165 lines) and violates modularity rules. High priority refactor. |
| sldb.models | Pass | |
