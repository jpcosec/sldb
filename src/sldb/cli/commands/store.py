from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.cli.utils import get_store_context, resolve_model_ref
from sldb.core.exceptions import SLDBError, SLDBStoreError
from sldb.store.hashing import hash_documents_index, hash_fields, hash_text
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_semantic_dag,
    load_store_index,
    save_documents_index,
    save_models_index,
    save_semantic_dag,
    save_semantic_index,
    save_store_index,
    store_lock,
)
from sldb.store.layout import store_exists
from sldb.store.models import SemanticDAG, StoreEntry, StoreIndex
from sldb.store.models import SemanticIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.semantic import (
    RebuildReport,
    rebuild_sections_indexes,
    rebuild_semantic_indexes,
)


class StoreCLI:
    """Handles store-level lifecycle and federation."""

    def run(self, args: Any) -> int:
        """Dispatch store subcommands."""
        cmd_map = {
            "init": self.init,
            "add": self.add,
            "check": self.check,
            "update": self.update,
            "semantic-map": self.semantic_map,
        }
        handler = cmd_map.get(args.store_command)
        if not handler:
            raise SLDBError(f"Unknown store command: {args.store_command}")
        return handler(args)

    def init(self, args: Any) -> int:
        root = Path(args.path).resolve()
        sp = root / ".sldb"
        if store_exists(sp) and not args.force:
            raise SLDBStoreError(f"Store exists at {sp}.")
        save_store_index(sp, StoreIndex())
        save_semantic_dag(sp, SemanticDAG(equivalences={}))
        save_semantic_index(sp, SemanticIndex())
        print(f"Initialized store at {sp}")
        return 0

    def add(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        other = Path(args.path).resolve()
        if not store_exists(other):
            raise SLDBStoreError(f"No store at {other}")

        idx = load_store_index(sp)
        name = args.name or other.parent.name
        if any(s.name == name for s in idx.stores):
            raise SLDBStoreError(f"Store '{name}' already linked.")

        rel = str(other.relative_to(root)) if other.is_relative_to(root) else str(other)
        idx.stores.append(StoreEntry(name=name, path=rel))
        save_store_index(sp, idx)
        print(f"Linked '{name}' at {rel}")
        return 0

    def check(self, args: Any) -> int:
        from sldb.store.diagnostics import diagnose_store

        sp, root = get_store_context(args.store)
        res = diagnose_store(sp, root, pythonpath=args.pythonpath)

        if args.format in ("json", "yaml"):
            payload = {
                "valid": res.is_valid,
                "hash_a_ok": res.hash_a_ok,
                "models": [
                    {
                        "name": model.name,
                        "hash_b_ok": model.hash_b_ok,
                        "documents": [
                            {
                                "name": doc.name,
                                "path": doc.path,
                                "hash_c_ok": doc.hash_c_ok,
                                "hash_d_ok": doc.hash_d_ok,
                                "path_exists": doc.path_exists,
                                "note": doc.note.value,
                            }
                            for doc in model.documents
                        ],
                    }
                    for model in res.models
                ],
            }
            if args.format == "json":
                print(json.dumps(payload))
            else:
                import yaml

                print(yaml.dump(payload, allow_unicode=True, sort_keys=False))

            if not res.is_valid:
                raise SystemExit(1)
        else:
            print(f"{'PASS' if res.is_valid else 'FAIL'}: store integrity")

        return 0 if res.is_valid else 1

    def update(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        idx = load_store_index(sp)

        skipped_models = []
        skipped_docs = []
        pending: list[tuple[ModelsIndex, DocumentsIndex]] = []

        for m_entry in idx.models:
            try:
                model_type = resolve_model_ref(m_entry.model_ref, args.pythonpath)
            except Exception:
                skipped_models.append(m_entry.name)
                continue

            m_idx = load_models_index(root / m_entry.models_index)
            d_idx = load_documents_index(root / m_idx.documents_index)

            for doc in d_idx.documents:
                doc_path = root / doc.path
                if not doc_path.exists():
                    skipped_docs.append(doc.name)
                    continue

                text = doc_path.read_text(encoding="utf-8")
                doc.hash_c = hash_text(text)
                try:
                    doc.hash_d = hash_fields(model_type, text)
                except Exception:
                    doc.hash_d = ""

            pending.append((m_entry, m_idx, d_idx))

        verbose = getattr(args, "verbose", False)
        wait = getattr(args, "wait", False)
        with store_lock(sp, wait=wait):
            for m_entry, m_idx, d_idx in pending:
                save_documents_index(root / m_idx.documents_index, d_idx)
                m_idx.hash_b = hash_documents_index(d_idx)
                save_models_index(root / m_entry.models_index, m_idx)

            sem_report = rebuild_semantic_indexes(
                sp, root, resolve_model_ref, args.pythonpath
            )
            sec_report = rebuild_sections_indexes(
                sp, root, resolve_model_ref, args.pythonpath
            )
            cascade_hash_a(sp, root, idx)

        print(f"Updated store at {sp}")
        if skipped_models:
            print(f"Skipped broken models: {', '.join(skipped_models)}")
        if skipped_docs:
            print(f"Skipped missing documents: {', '.join(skipped_docs)}")

        print(
            f"Semantic index: {sem_report.docs_processed} processed, "
            f"{sem_report.docs_skipped_missing} missing"
        )
        print(
            f"Sections index: {sec_report.docs_processed} processed, "
            f"{sec_report.docs_skipped_missing} missing, "
            f"{sec_report.docs_empty_sections} empty, "
            f"{sec_report.headings_no_map} unparseable headings"
        )
        if verbose:
            for line in sem_report.verbose + sec_report.verbose:
                print(f"  {line}")

        return 0 if not (skipped_models or skipped_docs) else 1

    def semantic_map(self, args: Any) -> int:
        sp, _root = get_store_context(args.store)
        dag = load_semantic_dag(sp)

        ca = args.concept_a
        cb = args.concept_b

        if ca not in dag.equivalences:
            dag.equivalences[ca] = []
        if cb not in dag.equivalences[ca]:
            dag.equivalences[ca].append(cb)

        if cb not in dag.equivalences:
            dag.equivalences[cb] = []
        if ca not in dag.equivalences[cb]:
            dag.equivalences[cb].append(ca)

        save_semantic_dag(sp, dag)
        print(f"Mapped {ca} <-> {cb}")
        return 0
