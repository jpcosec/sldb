"""Repo-relative POSIX paths handled as strings, without building path objects."""

from __future__ import annotations


def has_path_prefix(relative_path: str, prefix: str) -> bool:
    """Whether `relative_path` is `prefix` or sits below it."""
    return relative_path == prefix or relative_path.startswith(f"{prefix}/")


def path_suffix(name: str) -> str:
    """`PurePath.suffix` of a file name: the last dotted part, never a leading dot alone."""
    index = name.rfind(".")
    return name[index:] if 0 < index < len(name) - 1 else ""
