"""Parse a value written as text (JSON first, YAML otherwise).

Moved here from `sldb.cli.utils`, which re-exports `parse_data_value`.
"""

from __future__ import annotations

import json
from typing import Any

import yaml


def parse_data_value(raw: str) -> Any:
    """Parse JSON/YAML scalars or objects from a string.

    Args:
        raw: Text such as `5`, `"Pending"`, `[a, b]` or `{k: v}`.

    Returns:
        The parsed value.

    Raises:
        yaml.YAMLError: When the text is neither valid JSON nor valid YAML.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return yaml.safe_load(raw)
