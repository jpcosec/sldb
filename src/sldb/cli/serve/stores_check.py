"""The body of GET /stores/check: the compact report plus the CLI's model-vs-disk verdicts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.store_check import all_findings, check_report, structural_noise
from sldb.cli.commands.store_check import diag_payload
from sldb.store.diagnostics import diagnose_store

_CLI_KEYS = ("root_ok", "hash_a_ok", "summary", "models")


def check_with_models(store_path: Path, root: Path, pythonpath: str | None) -> dict[str, Any]:
    """One diagnosis, two views: the existing keys untouched, and `root_ok`, `hash_a_ok`,
    `summary` and `models[]` exactly as `sldb stores check --format json` prints them.

    Each `models[]` entry has `roster_ok`, `contract_ok` and `documents[]` with `path`,
    `path_exists`, `content_ok`, `fields_ok`, `note` and `explain` for every document,
    not only the damaged ones.
    """
    diagnosis = diagnose_store(store_path, resolve_model_ref, root, pythonpath=pythonpath)
    findings = all_findings(diagnosis, store_path, root, pythonpath)
    cli = diag_payload(diagnosis, findings)
    noise = structural_noise(store_path, root, pythonpath)
    return {**check_report(diagnosis, noise, findings), **{key: cli[key] for key in _CLI_KEYS}}
