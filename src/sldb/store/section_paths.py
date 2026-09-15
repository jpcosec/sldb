"""Deterministic path allocation for persisted Markdown sections."""
from __future__ import annotations

SECTION_INDEX_VERSION = "2"


def section_cache_key(index) -> str:
    """Invalidate persisted headings when section identity rules change."""
    from sldb.store import built_cache
    return f"{built_cache.model_key(index)}|sections:{SECTION_INDEX_VERSION}"


def unique_slug(slug: str, path: str, sections: list[dict]) -> str:
    """Suffix a repeated sibling slug without changing its parent path."""
    existing = {section["path"] for section in sections}
    if path not in existing:
        return slug
    return _next_slug(slug, path, existing)


def _next_slug(slug: str, path: str, existing: set[str]) -> str:
    parent, number = "/".join(path.split("/")[:-1]), 2
    while _path(parent, f"{slug}-{number}") in existing:
        number += 1
    return f"{slug}-{number}"


def section_path(stack: list[dict], slug: str) -> str:
    """Build a hierarchical path from current ancestor slugs."""
    return _path("/".join(item["slug"] for item in stack), slug)


def _path(parent: str, slug: str) -> str:
    return f"{parent}/{slug}" if parent else slug
