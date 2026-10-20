"""How a store reads a finding: through the document's authority and its own declared policy
(docs/architecture/provenance.md §5), never through a table fixed in code.

A response is `ignore` (not even listed), `allow` (same), `alert`, `error`, `reindex` or
`hook: <command>` (both reported as alerts naming what `stores check --apply` would run).
Looked up in order: the store's `policy:` for the model, its `"*"`, then sldb's defaults, where
only what is broken is an error and a declared `source_raw` or `generated` document edited
by hand is too. Codes are matched without their `store/` prefix, `-` and `_` alike.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.policy_subject import Subject  # noqa: F401 - re-exported

ERRORS = frozenset({"missing", "model-unresolved", "unbuilt", "link-broken", "check", "unparseable", "invalid", "unavailable"})
LEVELS = {"error": "error", "alert": "alert", "reindex": "alert", "ignore": None, "allow": None}


class Policy:
    def __init__(self, declared: dict[str, dict[str, str]] | None = None) -> None:
        self.declared = {model: {_key(code): r for code, r in rules.items()} for model, rules in (declared or {}).items()}

    @classmethod
    def of_store(cls, store_path: Path) -> Policy:
        """The `policy:` of the store's declaration, or none when it has no declaration."""
        from sldb.api.stores.store_declaration import declaration_path, load_declaration

        return cls(load_declaration(store_path).policy if declaration_path(store_path).is_file() else {})

    def response(self, code: str, model: str | None, subject: Subject | None = None) -> str:
        key = _key(code)
        for scope in (model, "*"):
            if scope in self.declared and key in self.declared[scope]:
                return self.declared[scope][key]
        return default_response(key, subject or Subject())

    def level(self, code: str, model: str | None, subject: Subject | None = None) -> str | None:
        """`error`, `alert`, or None when the finding is not to be listed."""
        response = self.response(code, model, subject)
        return "alert" if response.startswith("hook:") else LEVELS.get(response, "alert")


def default_response(key: str, subject: Subject) -> str:
    """sldb's reading when the store declares nothing for this code."""
    if key in ERRORS:
        return "error"
    if key == "data-mutation":
        return "error" if subject.declared and subject.authority in ("source_raw", "generated") else "alert"
    if key == "structural-noise":
        return "allow" if subject.narrative or (subject.declared and subject.authority == "authored") else "alert"
    return "alert"


def _key(code: Any) -> str:
    return str(code).split("/", 1)[-1].replace("_", "-")
