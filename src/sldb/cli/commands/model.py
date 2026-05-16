from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from sldb.cli.utils import get_store_context, resolve_model_ref
from sldb.store.hashing import hash_documents_index, hash_fields, hash_text
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    store_lock,
)
from sldb.store.models import DocumentsIndex, ModelEntry, ModelsIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.semantic import rebuild_semantic_indexes
from sldb.store.semantic_tags import flatten_model_semantics
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
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path.resolve())

    def add(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        model_type = resolve_model_ref(args.model, args.pythonpath)
        idx = load_store_index(sp)

        if any(m.name == model_type.__name__ for m in idx.models):
            raise SLDBModelError(f"Model '{model_type.__name__}' exists.")

        m_path = self._get_rel_path(Path(inspect.getfile(model_type)), root)
        mi_rel = f".sldb/models/{model_type.__name__}.yaml"
        di_rel = f".sldb/documents/{model_type.__name__}.yaml"

        with store_lock(sp):
            save_documents_index(root / di_rel, DocumentsIndex())
            mi = ModelsIndex(
                name=model_type.__name__,
                model_ref=args.model,
                path=m_path,
                documents_index=di_rel,
                hash_b="",
                canonical=args.canonical,
                semantics=flatten_model_semantics(model_type),
            )
            save_models_index(root / mi_rel, mi)
            idx.models.append(
                ModelEntry(
                    name=mi.name, model_ref=args.model, path=m_path, models_index=mi_rel
                )
            )

            rebuild_semantic_indexes(sp, root, resolve_model_ref, args.pythonpath)
            cascade_hash_a(sp, root, idx)
        print(f"Registered '{model_type.__name__}'")
        return 0

    def update(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        idx = load_store_index(sp)

        m_entry = next((m for m in idx.models if m.name == args.model), None)
        if not m_entry:
            raise SLDBModelError(f"Model '{args.model}' not found.")

        m_idx = load_models_index(root / m_entry.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        model_type = resolve_model_ref(m_entry.model_ref, args.pythonpath)

        for doc in d_idx.documents:
            text = (root / doc.path).read_text(encoding="utf-8")
            doc.hash_c = hash_text(text)
            try:
                doc.hash_d = hash_fields(model_type, text)
            except Exception:
                doc.hash_d = ""

        with store_lock(sp):
            save_documents_index(root / m_idx.documents_index, d_idx)
            m_idx.hash_b = hash_documents_index(d_idx)
            save_models_index(root / m_entry.models_index, m_idx)

            rebuild_semantic_indexes(sp, root, resolve_model_ref, args.pythonpath)
            cascade_hash_a(sp, root, idx)
        print(f"Updated '{args.model}'")
        return 0
