"""Claves y alias de un átomo: `label_key` (la de `normKey` del template del catálogo),
`normalize_key` y los alias por título y etiquetas.

Migrado de `spec2viz.deskops` (`label_key`, `_normalize_key`, `_alias_candidates`). No se
sustituye por `normalize` de difflib_matcher: ese quita acentos y deja la puntuación, y
`label_key` debe seguir coincidiendo con `normKey`.
"""

from __future__ import annotations

import re


def label_key(value: str) -> str:
    """Misma normalizacion que `normKey` del template (minusculas, sin puntuacion)."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]+", " ", (value or "").strip().lower())).strip()


def normalize_key(value: str) -> str:
    """La clave de un título: minúsculas, puntuación a espacios, espacios colapsados."""
    value = (value or "").strip().lower()
    value = re.sub(r"[^\w\s]+", " ", value)
    return re.sub(r"\s+", " ", value)


def _title_aliases(title: str) -> list[str]:
    """El título normalizado, sus palabras de 3+ letras y cada par de palabras contiguas."""
    normalized_title = normalize_key(title)
    if not normalized_title:
        return []
    words = [word for word in normalized_title.split() if len(word) >= 3]
    return [normalized_title, *words, *[f"{a} {b}" for a, b in zip(words, words[1:])]]


def _tag_aliases(tags: list[str]) -> list[str]:
    """Por cada etiqueta `namespace:valor`, el valor normalizado y sus palabras de 3+ letras."""
    aliases: list[str] = []
    for tag in tags or []:
        if ":" not in tag:
            continue
        _namespace, value = tag.split(":", 1)
        normalized_value = normalize_key(value.replace("-", " ").replace("_", " "))
        if normalized_value:
            aliases.append(normalized_value)
            aliases.extend([word for word in normalized_value.split() if len(word) >= 3])
    return aliases


def alias_candidates(title: str, tags: list[str]) -> list[str]:
    """Los alias de un átomo, sin repetidos y en orden: los del título y luego los de las etiquetas."""
    seen: set[str] = set()
    result: list[str] = []
    for alias in [*_title_aliases(title), *_tag_aliases(tags)]:
        if alias and alias not in seen:
            seen.add(alias)
            result.append(alias)
    return result
