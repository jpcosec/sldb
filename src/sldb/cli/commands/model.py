from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from sldb.api.model_registry.add_model import add_model
from sldb.api.model_registry.model_index_writes import rehash_documents, relative_model_path, write_new_model_indexes
from sldb.cli.store_context import get_store_context
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.hashing import hash_documents_index
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    store_lock,
)
from sldb.store.ops import cascade_hash_a
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store import documents_hash
from sldb.store.layout import store_exists
from sldb.core.exceptions import SLDBModelError, SLDBError


class ModelCLI:
    """Handles model contract registration and indexing."""

    def run(self, args: Any) -> int:
        """Dispatch model subcommands."""
        cmd_map = {
            "add": self.add,
            "update": self.update,
        }
        handler = cmd_map.get(args.model_command)
        if not handler:
            raise SLDBError(f"Unknown model command: {args.model_command}")
        return handler(args)

    def _get_rel_path(self, path: Path, root: Path) -> str:
        return relative_model_path(path, root)

    def _save_new_model(self, sp: Any, root: Path, idx: Any, args: Any, model_type: Any, m_path: str, mi_rel: str, di_rel: str) -> None:
        """hash_b starts as hash_documents_index of the empty index, not "" --
        an unhashed empty string fails `stores check` until `models update` runs."""
        write_new_model_indexes(sp, root, idx, model_type, args.model, m_path, mi_rel, di_rel, args.canonical, args.pythonpath)

    def add(self, args: Any) -> int:
        sp, err = self._store_or_error(args)
        if err:
            return err
        idx = load_store_index(sp)
        model_type = self._resolve_or_report(args.model, args.pythonpath, idx)
        if model_type is None:
            return 1
        return self._register_or_noop(args, sp, idx, model_type)

    @staticmethod
    def _store_or_error(args: Any) -> tuple[Any, int]:
        sp = get_store_context(args.store)[0]
        if store_exists(sp):
            return sp, 0
        print(f"Store not found at {sp}. Run 'sldb stores init --path .' to create one, or pass --store with an existing store path.", file=sys.stderr)
        return sp, 2

    @staticmethod
    def _resolve_or_report(model_ref: str, pythonpath: str | None, idx: Any) -> type | None:
        try:
            return resolve_model_ref(model_ref, pythonpath)
        except SLDBModelError:
            ModelCLI._report_not_found(model_ref, idx)
            return None

    @staticmethod
    def _register_or_noop(args: Any, sp: Any, idx: Any, model_type: type) -> int:
        if any(m.name == model_type.__name__ for m in idx.models):
            print(f"Model '{model_type.__name__}' already registered.")
            return 0
        registration = add_model(sp, args.model, args.pythonpath, getattr(args, "canonical", False))
        print(f"Registered '{registration.name}'")
        return 0

    @staticmethod
    def _report_not_found(model_ref: str, idx: Any) -> None:
        names = sorted(m.name for m in idx.models)
        listed = ", ".join(names) if names else "none"
        print(f"Model '{model_ref.split(':', 1)[-1]}' not found. Available models: {listed}", file=sys.stderr)

    def _update_doc_hashes(self, root: Path, d_idx: Any, model_type: Any) -> None:
        rehash_documents(root, d_idx, model_type)

    def _save_updated_model(self, sp: Any, root: Path, idx: Any, args: Any, m_entry: Any, m_idx: Any, d_idx: Any) -> None:
        with store_lock(sp):
            save_documents_index(root / m_idx.documents_index, d_idx)
            if getattr(args, "bump_version", False):
                m_idx.version += 1; m_entry.version = m_idx.version
            m_idx.hash_b = hash_documents_index(d_idx)
            m_idx.documents_count = len(d_idx.documents)
            save_models_index(root / m_entry.models_index, m_idx)
            documents_hash.invalidate(sp, m_entry.name)  # a full scan just moved hash_c/hash_d
            rebuild_derived_indexes(sp, root, resolve_model_ref, args.pythonpath)
            cascade_hash_a(sp, root, idx)

    def update(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        idx = load_store_index(sp)
        m_entry = next((m for m in idx.models if m.name == args.model), None)
        if not m_entry: raise SLDBModelError(f"Model '{args.model}' not found.")
        m_idx = load_models_index(root / m_entry.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        self._update_doc_hashes(root, d_idx, resolve_model_ref(m_entry.model_ref, args.pythonpath))
        self._save_updated_model(sp, root, idx, args, m_entry, m_idx, d_idx)
        print(f"Updated '{args.model}'")
        return 0
