"""`sldb models check <model>...`: each model registered or missing; exit 1 if any is missing."""

from __future__ import annotations

from typing import Any

from sldb.api.model_registry.registration_query import is_model_registered
from sldb.cli.output_format import emit


def check_models(args: Any) -> int:
    found = {model: is_model_registered(args.store, model) for model in args.models}
    lines = "\n".join(f"{'registered' if ok else 'missing'}: {model}" for model, ok in found.items())
    emit({"models": [{"model": m, "registered": ok} for m, ok in found.items()], "ok": all(found.values())}, args.format, lines)
    return 0 if all(found.values()) else 1
