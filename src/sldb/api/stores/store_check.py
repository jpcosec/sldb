"""Store integrity check: the CLI's `sldb stores check` reached through sldb.api.

The verification itself is ``sldb.store.diagnostics.diagnose_store`` (the exact
function the CLI calls); this module only projects its per-document verdicts into
a compact ``{ok, checked, mismatched}`` summary with the expected/actual hashes
the diagnosis now carries. Nothing here re-checks the store.

``ok`` and ``valid`` are the same verdict, "no error" (anchoring.md §4): what moved is in
``alerts`` and ``mismatched``, what broke in ``errors``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.store_check_summary import _classified, _summarize


def derived_prefixes(store_path: Path) -> list[str]:
    """The declared `derived` path prefixes of the store; none when it has no readable declaration."""
    from sldb.api.stores.store_declaration import load_declaration

    try:
        return list(load_declaration(store_path).derived)
    except (OSError, ValueError):
        return []


def check_store(store_path: Path, project_root: Path, pythonpath: str | None = None) -> dict[str, Any]:
    """Run the CLI's store integrity check and summarize it."""
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.diagnostics import diagnose_store

    from sldb.api.model_registry.model_reference import same_model_class
    from sldb.store.model_origin import shadowed_models

    diagnosis = diagnose_store(store_path, resolve_model_ref, project_root, pythonpath=pythonpath, derived=derived_prefixes(store_path))
    return {**check_report(diagnosis, structural_noise(store_path, project_root, pythonpath), all_findings(diagnosis, store_path, project_root, pythonpath)), "shadowed_models": shadowed_models(store_path, lambda a, b: same_model_class(a, b, pythonpath)), "broken_links": _broken_links(store_path), "gitignore_policy": _gitignore(store_path), "rewrite_loss": _rewrite_loss(store_path, project_root, pythonpath)}


def all_findings(diagnosis: Any, store_path: Path, project_root: Path, pythonpath: str | None) -> list:
    """The diagnosis' findings and its surroundings', each read through the store's policy
    (`judge_findings`), as `stores check` reports them; then, at their own level, the `on_check`
    rules' and the document anchors' (GO08, `on_check_findings`). A document its model rejects
    is named once, as `store/doc-invalid` (`once_per_invalid`)."""
    from sldb.api.rules.rules_on_check import on_check_findings
    from sldb.api.stores.judge_findings import judged
    from sldb.api.stores.store_findings import diagnosis_findings, once_per_invalid
    from sldb.api.stores.store_surroundings import surroundings_findings

    found = judged(diagnosis_findings(diagnosis) + surroundings_findings(store_path, project_root, pythonpath), store_path, pythonpath)
    return once_per_invalid(found + on_check_findings(store_path, pythonpath), diagnosis)


def _broken_links(store_path: Path) -> list[dict[str, str]]:
    """Links whose target is gone or holds no store (an error, in `errors`)."""
    from sldb.api.stores.store_links import store_links

    return [link for link in store_links(store_path) if link["status"] != "ok"]


def _gitignore(store_path: Path) -> dict[str, bool] | None:
    from sldb.api.stores.gitignore_policy import gitignore_policy

    return gitignore_policy(store_path)


def _rewrite_loss(store_path: Path, project_root: Path, pythonpath: str | None) -> list[dict[str, Any]]:
    from sldb.api.stores.scan_rewrite_loss import scan_rewrite_loss

    return scan_rewrite_loss(store_path, project_root, pythonpath)


def check_report(diagnosis: Any, noise: list[dict[str, Any]], findings: list) -> dict[str, Any]:
    """The compact `{ok, valid, errors, alerts, damaged, ..., checked, mismatched, structural_noise}` view of one diagnosis.

    Args:
        diagnosis: The store diagnosis to project.
        noise: The tracked documents with undeclared headings (see ``structural_noise``).
        findings: Every finding (``all_findings``); ``ok`` and ``valid`` are "none is an error".
    """
    from sldb.core.finding import split

    errors, alerts = split(findings)
    listed = {"valid": not errors, "errors": [f.as_dict() for f in errors], "alerts": [f.as_dict() for f in alerts]}
    return {"ok": not errors, **_classified(diagnosis), **listed, **_summarize(diagnosis), "structural_noise": noise}


def structural_noise(store_path: Path, project_root: Path, pythonpath: str | None) -> list[dict[str, Any]]:
    """Tracked documents with undeclared headings: reported here, refused at write time."""
    from sldb.api.stores.scan_structural_noise import scan_structural_noise

    return [report.details() for report in scan_structural_noise(store_path, project_root, pythonpath)]
