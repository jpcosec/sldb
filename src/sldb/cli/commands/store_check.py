"""`sldb stores check`: the store's errors and alerts (docs/architecture/anchoring.md, §4).

Exit 1 only on an error. Alerts print by every route (`sldb.cli.alert_sink`): a line each in
text, `--quiet` included (after its verdict line, which is unchanged), and `errors`/`alerts` in the JSON, whose other keys are unchanged
(deskops reads them).
"""

from __future__ import annotations
import json
from typing import Any
from sldb.cli import alert_sink
from sldb.cli.store_context import get_store_context
from sldb.cli.commands.store_check_apply import exit_after_apply
from sldb.cli.commands.store_check_report import print_report
from sldb.core.finding import split


def check_store(args: Any) -> int:
    from sldb.api.stores.store_check import all_findings
    from sldb.store.diagnostics import diagnose_store
    from sldb.cli.model_utils import resolve_model_ref
    sp, root = get_store_context(args.store, mode="readonly")
    if _unbuilt(sp, args.format):
        return 1
    res = diagnose_store(sp, resolve_model_ref, root, pythonpath=args.pythonpath)
    findings = all_findings(res, sp, root, args.pythonpath)
    _print(res, findings, args.format, getattr(args, "quiet", False))
    return exit_after_apply(findings, sp, args)


def _unbuilt(sp: Any, fmt: str) -> bool:
    """A declared store with no index cannot be diagnosed: say so, as the error it is."""
    from sldb.api.stores.store_surroundings import unbuilt
    from sldb.store.layout import store_exists

    found = None if store_exists(sp) else unbuilt(sp)
    if found:
        print(json.dumps({"valid": False, "errors": [found.as_dict()], "alerts": [], "models": []}) if fmt in ("json", "yaml") else "FAIL: store integrity — the store is not built")
        alert_sink.report([found], text=fmt not in ("json", "yaml"))
    return found is not None


def _print(res: Any, findings: list, fmt: str, quiet: bool) -> None:
    if fmt in ("json", "yaml"):
        _print_formatted_diag(res, fmt, findings)
        alert_sink.report(findings, text=False)
        return
    ok = not split(findings)[0]
    print(f"{'PASS' if ok else 'FAIL'}: store integrity" if quiet else res.summary(ok, alert_sink.tally(findings)))
    if not quiet:
        print_report(res)
    alert_sink.report(findings)


def _print_formatted_diag(res: Any, fmt: str, findings: list) -> None:
    payload = diag_payload(res, findings)
    if fmt == "json":
        print(json.dumps(payload))
    else:
        import yaml
        print(yaml.dump(payload, allow_unicode=True, sort_keys=False))


def diag_payload(res: Any, findings: list | None = None) -> dict[str, Any]:
    """The payload `sldb stores check --format json` prints, for callers outside the CLI (the server).

    `hash_a_ok`/`hash_*_ok` stay: deskops reads this shape (deskops/workspace.py) and the
    store's own persisted keys are letters. `valid` is "no error"."""
    errors, alerts = split(findings if findings is not None else [])
    ok = not errors if findings is not None else res.is_valid
    verdict = {"valid": ok, "summary": res.summary(ok, alert_sink.tally(errors + alerts)), "hash_a_ok": res.root_ok, "root_ok": res.root_ok}
    listed = {"errors": [f.as_dict() for f in errors], "alerts": [f.as_dict() for f in alerts]}
    return {**verdict, **_build_finding_counts(res), **listed, "models": [_build_model_payload(m) for m in res.models]}


def _build_finding_counts(res: Any) -> dict[str, Any]:
    """The findings behind the verdict, by category."""
    return {
        "damaged": len(res.damaged_documents),
        "reformatted": len(res.reformatted_documents),
        "roster_only": [m.name for m in res.roster_only_models],
        "moved_contracts": [m.name for m in res.moved_contracts],
    }


def _build_model_payload(model: Any) -> dict[str, Any]:
    flags = {"hash_b_ok": model.roster_ok, "roster_ok": model.roster_ok, "contract_ok": model.contract_ok}
    state = {"legacy_contract": model.legacy_contract, "resolved": model.resolved, "roster_only_failure": model.roster_only_failure}
    return {"name": model.name, **flags, **state, "documents": [_build_doc_payload(d) for d in model.documents]}


def _build_doc_payload(doc: Any) -> dict[str, Any]:
    identity = {"name": doc.name, "path": doc.path, "path_exists": doc.path_exists}
    verdict = {"note": doc.note.value, "explain": doc.explain()}
    return {**identity, **_doc_hash_flags(doc), **verdict, **({"history": doc.history} if doc.history else {})}


def _doc_hash_flags(doc: Any) -> dict[str, Any]:
    """Both namings of the same two booleans: letters for existing readers, semantic names for new ones."""
    return {"hash_c_ok": doc.content_ok, "hash_d_ok": doc.fields_ok, "content_ok": doc.content_ok, "fields_ok": doc.fields_ok}
