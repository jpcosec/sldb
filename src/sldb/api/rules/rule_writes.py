"""What writing a RuleDoc checks against the store: every `model <= X` of its subject names a
model the store registers. The rest of a RuleDoc's shape is its own validators' (`RuleDoc`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.models.rule_doc import RuleDoc
from sldb.store.graph.language.predicate_ast import top_level_models
from sldb.store.graph.language.predicate_parser import parse_predicate


def refuse_unknown_family(store_path: Path, model_type: Any, payload: dict[str, Any], pythonpath: str | None = None) -> None:
    """Refuse a RuleDoc whose subject names an unregistered model, with the store's own
    unknown-model error (`SLDBStoreError: Model 'X' not registered.`); other models pass.

    Call it after the payload rendered (the model validated it), before anything is written."""
    if not (isinstance(model_type, type) and issubclass(model_type, RuleDoc)):
        return
    for name in top_level_models(parse_predicate(payload["subject"]).root):
        load_registered_model(store_path, name, pythonpath)
