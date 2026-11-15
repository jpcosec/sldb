"""Alias de tipos de `catalog`."""

from __future__ import annotations


_PATH_RULE = (
    "Relative paths follow one rule for `src`, `mmd`, `specs` and `notation`: first next to the config file "
    "(the folder of the vistas.yml), then from the repo root (nearest ancestor with `.git`, else `.sldb`). "
    "If both exist and are different files the path is ambiguous (AmbiguousPathError); if neither exists the "
    "error lists the paths tried."
)
