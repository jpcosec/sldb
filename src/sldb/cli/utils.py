from __future__ import annotations
import sys
from pathlib import Path
from sldb.api.documents.data_values import parse_data_value  # noqa: F401 - moved to sldb.api.documents

def read_text(path: str) -> str:
    """Read text from a file or stdin."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")

def write_text(path: str, content: str) -> None:
    """Write text to a file or stdout."""
    if path == "-":
        sys.stdout.write(content)
        return
    Path(path).write_text(content, encoding="utf-8")

