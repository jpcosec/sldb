"""Which registered models cannot be loaded, for endpoints that skip their documents.

``sldb.store.query._load_one`` resolves each model and does ``continue`` when it
cannot: one unimportable model silently removes *every document it tracks* from
the result. Changing that function's contract would touch 21 call sites, so the
degradation stays where it is and is instead made visible here — the endpoints
that list documents report the models whose documents are therefore missing.

Note that ``/health`` currently attributes this to the documents themselves
(``data_mutation``, "fields changed"), which names the symptom rather than the
cause; this listing is what tells a consumer the real reason.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.schema.unavailable_model import UnavailableModel
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.io import load_store_index


def unavailable_models(store_path: Path, pythonpath: str) -> list[UnavailableModel]:
    """Every registered model whose class cannot be imported right now.

    Args:
        store_path: Path of the ``.sldb`` store.
        pythonpath: Directory to import the model modules from.

    Returns:
        One entry per unloadable model, each with the reason it failed.
    """
    return [found for entry in load_store_index(store_path).models if (found := _check(entry, pythonpath))]


def _check(entry: object, pythonpath: str) -> UnavailableModel | None:
    """Try to import one registered model.

    Args:
        entry: The store index entry of the model.
        pythonpath: Directory to import the model module from.

    Returns:
        None when the model loads, else the failure with its reason.
    """
    try:
        resolve_model_ref(entry.model_ref, pythonpath)
        return None
    except Exception as exc:  # noqa: BLE001 - reporting the failure is the point
        return UnavailableModel(model=entry.name, model_ref=entry.model_ref, error=str(exc))
