"""The docstring metadata profile: a strict YAML frontmatter at the start of a docstring.

Spec: docs/architecture/code-docstring-indexing.spec.md section 2. Only an opening line exactly
`---` starts metadata, a closing `---` line is required, and the block must be a YAML mapping
with unique keys among `id` (required), `kind` and `tags` (each a `namespace:value` tag,
deduplicated). Anything else is a diagnostic, never silently dropped: the earlier reader
returned `{}` for malformed metadata and the declaration lost its identity without a word.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml

from .unique_yaml import UniqueKeyLoader

ALLOWED = ("id", "kind", "tags")
_TAG = re.compile(r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$")  # sldb.models.knowledge_tag.KnowledgeTag


@dataclass
class DocstringMetadata:
    """What one docstring declares: its metadata (empty when it declares none) and its body."""

    declared: bool = False
    values: dict = field(default_factory=dict)
    body: str = ""
    errors: list[str] = field(default_factory=list)


def parse_docstring(docstring: str | None) -> DocstringMetadata:
    text = docstring or ""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return DocstringMetadata(body=text.strip())
    closing = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing is None:
        return DocstringMetadata(declared=True, body=text.strip(), errors=["metadata opens with '---' but never closes"])
    values, errors = _mapping("\n".join(lines[1:closing]))
    return DocstringMetadata(declared=True, values=values, body="\n".join(lines[closing + 1:]).strip(), errors=errors)


def _mapping(block: str) -> tuple[dict, list[str]]:
    try:
        loaded = yaml.load(block, Loader=UniqueKeyLoader) if block.strip() else None
    except yaml.YAMLError as exc:
        return {}, [f"metadata is not valid YAML: {str(exc).splitlines()[0]}"]
    if not isinstance(loaded, dict):
        return {}, ["metadata must be a mapping of id, kind and tags"]
    return _validated(loaded)


def _validated(loaded: dict) -> tuple[dict, list[str]]:
    errors = [f"unknown metadata key '{key}' (allowed: {', '.join(ALLOWED)})" for key in loaded if key not in ALLOWED]
    if not isinstance(loaded.get("id"), str) or not loaded["id"].strip():
        errors.append("metadata 'id' is required and must be a nonempty string")
    if "kind" in loaded and (not isinstance(loaded["kind"], str) or not loaded["kind"].strip()):
        errors.append("metadata 'kind' must be a nonempty string")
    tags, tag_errors = _tags(loaded.get("tags", []))
    tag_errors += _one_per_nearest_namespace(tags)
    values = {key: loaded[key] for key in ("id", "kind") if key in loaded} | {"tags": tags}
    return values, errors + tag_errors


def _tags(raw) -> tuple[list[str], list[str]]:
    if not isinstance(raw, list):
        return [], ["metadata 'tags' must be a list"]
    bad = [str(t) for t in raw if not isinstance(t, str) or not _TAG.match(t)]
    return list(dict.fromkeys(t for t in raw if isinstance(t, str) and _TAG.match(t))), [f"tag '{t}' is not namespace:value" for t in bad]


def _one_per_nearest_namespace(tags: list[str]) -> list[str]:
    """`system:*` and `workspace:*` are inherited by nearest declaration: two local values in
    one of them would have no nearest value (spec section 3)."""
    return [f"more than one '{space}:' tag: {', '.join(t for t in tags if t.startswith(space + ':'))}"
            for space in ("system", "workspace") if sum(t.startswith(space + ":") for t in tags) > 1]

