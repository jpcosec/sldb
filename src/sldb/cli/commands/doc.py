from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

from sldb.cli.utils import get_store_context, registered_model, resolve_model_ref
from sldb.runtime.validation import (
    render_model_markdown,
    validate_model_input_roundtrip,
)
from sldb.store.ops import track_document
from sldb.core.exceptions import SLDBValidationError, SLDBASTError, SLDBError


class DocCLI:
    """Handles document management: add, track, update."""

    def run(self, args: Any) -> int:
        """Dispatch doc subcommands."""
        cmd_map = {
            "add": self.add,
            "track": self.track,
            "update": self.update,
            "untrack": self.untrack,
        }
        handler = cmd_map.get(args.doc_command)
        if not handler:
            raise SLDBError(f"Unknown doc command: {args.doc_command}")
        return handler(args)

    def _parse_payload(self, payload_arg: str) -> dict[str, Any]:
        p = Path(payload_arg)
        if p.exists():
            return yaml.safe_load(p.read_text(encoding="utf-8"))
        try:
            data = yaml.safe_load(payload_arg)
            if not isinstance(data, dict):
                raise SLDBASTError("Payload must be object.")
            return data
        except yaml.YAMLError as e:
            raise SLDBASTError(f"Parse error: {e}")

    def add(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        model_type, entry, idx = registered_model(sp, args.model, args.pythonpath)
        data = self._parse_payload(args.payload)
        rendered = render_model_markdown(model_type, data)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SLDBValidationError("Idempotency fail", details)

        out = Path(args.output).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
        track_document(
            sp,
            root,
            idx,
            model_type,
            entry,
            out,
            args.name or out.stem,
            resolve_model_ref,
            args.pythonpath,
        )
        print(f"Created and tracked '{args.name or out.stem}'")
        return 0

    def track(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        model_type, entry, idx = registered_model(sp, args.model, args.pythonpath)
        path = Path(args.path).resolve()

        if not args.force:
            valid, details = validate_model_input_roundtrip(
                model_type, path.read_text(encoding="utf-8")
            )
            if not valid:
                raise SLDBValidationError("Idempotency fail", details)

        track_document(
            sp,
            root,
            idx,
            model_type,
            entry,
            path,
            args.name or path.stem,
            resolve_model_ref,
            args.pythonpath,
        )
        print(f"Tracked '{args.name or path.stem}'")
        return 0

    def update(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        from sldb.store.io import (
            load_store_index,
            load_models_index,
            load_documents_index,
            save_documents_index,
            save_models_index,
            store_lock,
        )
        from sldb.store.hashing import hash_text, hash_fields
        from sldb.store.semantic import rebuild_semantic_indexes
        from sldb.store.ops import cascade_hash_a

        idx = load_store_index(sp)
        doc_ref = args.doc
        found = None
        for m_entry in idx.models:
            m_idx = load_models_index(root / m_entry.models_index)
            d_idx = load_documents_index(root / m_idx.documents_index)
            doc = next(
                (d for d in d_idx.documents if d.name == doc_ref or d.path == doc_ref),
                None,
            )
            if doc:
                found = (m_entry, m_idx, d_idx, doc)
                break

        if not found:
            raise SLDBError(f"Doc '{doc_ref}' not found.")
        m_entry, m_idx, d_idx, doc = found
        model_type = resolve_model_ref(m_entry.model_ref, args.pythonpath)

        data = self._parse_payload(args.payload)
        rendered = render_model_markdown(model_type, data)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SLDBValidationError("Update fail", details)

        doc_path = root / doc.path
        doc_path.write_text(rendered + "\n", encoding="utf-8")
        doc.hash_c = hash_text(rendered + "\n")
        doc.hash_d = hash_fields(model_type, rendered + "\n")

        with store_lock(sp):
            save_documents_index(root / m_idx.documents_index, d_idx)
            m_idx.hash_b = ""
            save_models_index(root / m_entry.models_index, m_idx)

            rebuild_semantic_indexes(sp, root, resolve_model_ref, args.pythonpath)
            cascade_hash_a(sp, root, idx)
        print(f"Updated '{doc.name}'")
        return 0

    def untrack(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        from sldb.store.io import (
            load_documents_index,
            load_models_index,
            load_store_index,
            save_documents_index,
            save_models_index,
            store_lock,
        )
        from sldb.store.hashing import hash_documents_index
        from sldb.store.ops import cascade_hash_a
        from sldb.store.semantic import (
            rebuild_sections_indexes,
            rebuild_semantic_indexes,
        )

        idx = load_store_index(sp)
        doc_ref = args.doc
        found = None
        for m_entry in idx.models:
            m_idx = load_models_index(root / m_entry.models_index)
            d_idx = load_documents_index(root / m_idx.documents_index)
            doc = next(
                (d for d in d_idx.documents if d.name == doc_ref or d.path == doc_ref),
                None,
            )
            if doc is not None:
                found = (m_entry, m_idx, d_idx, doc)
                break

        if not found:
            raise SLDBError(f"Doc '{doc_ref}' not found.")

        m_entry, m_idx, d_idx, doc = found
        d_idx.documents = [entry for entry in d_idx.documents if entry.name != doc.name]

        with store_lock(sp):
            save_documents_index(root / m_idx.documents_index, d_idx)
            m_idx.hash_b = hash_documents_index(d_idx)
            save_models_index(root / m_entry.models_index, m_idx)
            rebuild_semantic_indexes(sp, root, resolve_model_ref, args.pythonpath)
            rebuild_sections_indexes(sp, root, resolve_model_ref, args.pythonpath)
            cascade_hash_a(sp, root, idx)
        print(f"Untracked '{doc.name}'")
        return 0
