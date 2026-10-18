"""Find the frontmatter keys a document carries that its model never declares.

Symmetric with the heading check: a heading the model never declares is refused
on write, but a frontmatter key it never declares used to be dropped silently —
the document lost the key on the first re-render. That is the same silent loss
this module now refuses.
"""

from __future__ import annotations

import re

import yaml

from sldb.core.ast import AST_Handler
from sldb.core.exceptions import SLDBValidationError

#: A top-level YAML key: no leading whitespace, `name` then optional space and `:`.
_TOP_LEVEL_KEY = re.compile(r"^([A-Za-z0-9_-]+)\s*:")


#: A frontmatter that is one dict placeholder (`⸢rev,dict•frontmatter⸥`): every key rides in it.
_DICT_PLACEHOLDER = re.compile(r"^\s*⸢[^⸥]*\bdict\b[^⸥]*⸥\s*$")


def undeclared_frontmatter_keys(model_type: type, markdown: str) -> list[str]:
    """The document's top-level frontmatter keys the model's template never declares.

    None when the template's frontmatter is a single dict placeholder: that dict carries any
    key through extraction and back on re-render, so nothing is lost (deskops' TaskDoc).
    """
    template = getattr(model_type, "__template__", "") or ""
    if _frontmatter_is_dict(template):
        return []
    return sorted(_frontmatter_keys(markdown, load_yaml=True) - _frontmatter_keys(template, load_yaml=False))


def refuse_undeclared_frontmatter(model_type: type, markdown: str, name: str) -> None:
    """Raise unless every top-level frontmatter key is declared by the model."""
    keys = undeclared_frontmatter_keys(model_type, markdown)
    if not keys:
        return
    raise SLDBValidationError(
        f"frontmatter no declarado en '{name}': {', '.join(keys)} — "
        f"el modelo {getattr(model_type, '__name__', '?')} no declara estas claves, "
        f"así que se pierden al re-renderizar. Declaralas en el template, o el "
        f"documento pertenece a otra versión del modelo.",
        {"document": name, "model": getattr(model_type, "__name__", "?"), "undeclared_keys": keys},
    )


def _frontmatter_keys(markdown: str, load_yaml: bool) -> set[str]:
    """Top-level keys of a Markdown frontmatter block; see `undeclared_frontmatter_keys`."""
    node = _front_matter_node(markdown)
    if node is None:
        return set()
    content = node.content or ""
    return _yaml_keys(content) if load_yaml else _template_keys(content)


def _frontmatter_is_dict(template: str) -> bool:
    node = _front_matter_node(template)
    return node is not None and bool(_DICT_PLACEHOLDER.match((node.content or "").strip()))


def _yaml_keys(content: str) -> set[str]:
    try:
        data = yaml.safe_load(content)
    except Exception:
        return set()
    return set(data) if isinstance(data, dict) else set()


def _template_keys(content: str) -> set[str]:
    keys = set()
    for line in content.splitlines():
        if match := _TOP_LEVEL_KEY.match(line):
            keys.add(match.group(1))
    return keys


def _front_matter_node(markdown: str):
    for node in AST_Handler().split_nodes(markdown):
        if node.type == "front_matter":
            return node
    return None
