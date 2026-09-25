from __future__ import annotations
import json
from typing import Any
from sldb.cli.store_context import get_store_context
from sldb.cli.commands.store_check_report import print_report

def check_store(args: Any) -> int:
    from sldb.store.diagnostics import diagnose_store
    from sldb.cli.model_utils import resolve_model_ref
    sp, root = get_store_context(args.store, mode="readonly")
    res = diagnose_store(sp, resolve_model_ref, root, pythonpath=args.pythonpath)
    return _handle_check_res(res, args.format, getattr(args, "quiet", False))

def _handle_check_res(res: Any, fmt: str, quiet: bool = False) -> int:
    if fmt in ("json", "yaml"):
        _print_formatted_diag(res, fmt)
        if not res.is_valid:
            raise SystemExit(1)
        return 0
    if quiet:
        print(f"{'PASS' if res.is_valid else 'FAIL'}: store integrity")
    else:
        print_report(res)
    return 0 if res.is_valid else 1

def _print_formatted_diag(res: Any, fmt: str) -> None:
    payload = _build_diag_payload(res)
    if fmt == "json":
        print(json.dumps(payload))
    else:
        import yaml
        print(yaml.dump(payload, allow_unicode=True, sort_keys=False))

def _build_diag_payload(res: Any) -> dict[str, Any]:
    # hash_a_ok/hash_b_ok/hash_c_ok/hash_d_ok stay in the payload: deskops reads this
    # shape (deskops/workspace.py) and the store's own persisted keys are letters.
    return {
        "valid": res.is_valid,
        "summary": res.summary(),
        "hash_a_ok": res.root_ok,
        "root_ok": res.root_ok,
        "damaged": len(res.damaged_documents),
        "reformatted": len(res.reformatted_documents),
        "roster_only": [m.name for m in res.roster_only_models],
        "models": [_build_model_payload(m) for m in res.models],
    }

def _build_model_payload(model: Any) -> dict[str, Any]:
    return {
        "name": model.name,
        "hash_b_ok": model.roster_ok,
        "roster_ok": model.roster_ok,
        "roster_only_failure": model.roster_only_failure,
        "documents": [_build_doc_payload(d) for d in model.documents],
    }

def _build_doc_payload(doc: Any) -> dict[str, Any]:
    identity = {"name": doc.name, "path": doc.path, "path_exists": doc.path_exists}
    verdict = {"note": doc.note.value, "explain": doc.explain()}
    return {**identity, **_doc_hash_flags(doc), **verdict}

def _doc_hash_flags(doc: Any) -> dict[str, Any]:
    """Both namings of the same two booleans: letters for existing readers, semantic
    names for new ones."""
    return {
        "hash_c_ok": doc.content_ok,
        "hash_d_ok": doc.fields_ok,
        "content_ok": doc.content_ok,
        "fields_ok": doc.fields_ok,
    }
