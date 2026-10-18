"""`--format` defined once, and the payload printed in the format asked.

`models show`, `models template show` and `docs update` had no `--format`, so the flag most
subcommands take was rejected there (issue-sldb-cli-format-json-coverage-gaps): defining it per
subparser is what let the gap appear.
"""

from __future__ import annotations

import json
from typing import Any

import yaml

FORMATS = ("text", "json", "yaml")


def add_format(parser: Any, default: str = "text") -> None:
    parser.add_argument("--format", choices=FORMATS, default=default, help=f"Output format (default {default})")


def emit(payload: Any, fmt: str, text: str) -> None:
    """`payload` as JSON or YAML; `text` (the human form) otherwise."""
    if fmt == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    elif fmt == "yaml":
        print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip())
    else:
        print(text)
