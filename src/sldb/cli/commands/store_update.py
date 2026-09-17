"""`sldb stores update`: CLI adapter over `sldb.api.update_store_indexes` that prints the report.

The refresh helpers moved to `sldb.api.stores`; the ones with unchanged signatures are
re-exported here for existing importers.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.api.stores.index_commit import _rebuild_indexes  # noqa: F401
from sldb.api.stores.index_refresh import _field_hash, _process_doc, _process_model, _process_models  # noqa: F401
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.semantic import RebuildReport

def update_store(args: Any) -> int:
    report = update_store_indexes(args.store, args.pythonpath, wait=getattr(args, "wait", False))
    v = getattr(args, "verbose", False)
    _print_update_result(report.store_path, report.skipped_models, report.skipped_documents, report.semantic_index, report.sections_index, v)
    return 0 if report.complete else 1

def _print_update_result(sp: Path, skipped_models: list[str], skipped_docs: list[str], sem_report: RebuildReport, sec_report: RebuildReport, verbose: bool) -> None:
    print(f"Updated store at {sp}")
    if skipped_models:
        print(f"Skipped broken models: {', '.join(skipped_models)}")
    if skipped_docs:
        print(f"Skipped missing documents: {', '.join(skipped_docs)}")
    _print_reports(sem_report, sec_report, verbose)

def _print_reports(sem_report: RebuildReport, sec_report: RebuildReport, verbose: bool) -> None:
    print(f"Semantic index: {sem_report.docs_processed} processed, {sem_report.docs_skipped_missing} missing")
    print(f"Sections index: {sec_report.docs_processed} processed, {sec_report.docs_skipped_missing} missing, {sec_report.docs_empty_sections} empty, {sec_report.headings_no_map} unparseable headings")
    if verbose:
        for line in sem_report.verbose + sec_report.verbose:
            print(f"  {line}")
