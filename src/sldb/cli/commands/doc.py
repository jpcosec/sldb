from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

from sldb.cli.store_context import get_store_context
from sldb.api.documents.create_document import create_document
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents.untrack_document import forget_document, untrack_document
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.commands.doc_lookup import find_doc
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.io import load_store_index, save_models_index, store_lock
from sldb.store.io.shards import save_document_shard
from sldb.store.hashing import hash_text, hash_fields
from sldb.store.layout import documents_shard_path
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store.ops import cascade_hash_a
from sldb.store import documents_hash
from sldb.core.exceptions import SLDBValidationError, SLDBASTError, SLDBError

class DocCLI:

    def run(self, args: Any) -> int:
        cmd_map = {"add": self.add, "track": self.track, "update": self.update, "untrack": self.untrack, "delete": self.delete}
        if args.doc_command not in cmd_map: raise SLDBError(f"Unknown doc command: {args.doc_command}")
        return cmd_map[args.doc_command](args)

    def _parse_payload(self, payload_arg: str) -> dict[str, Any]:
        p = Path(payload_arg)
        try:
            if p.exists(): return yaml.safe_load(p.read_text(encoding="utf-8"))
        except OSError: pass
        try:
            if not isinstance(data := yaml.safe_load(payload_arg), dict): raise SLDBASTError("Payload must be object.")
            return data
        except yaml.YAMLError as e: raise SLDBASTError(f"Parse error: {e}")

    def add(self, args: Any) -> int:
        created = create_document(args.store, args.model, args.output, self._parse_payload(args.payload), args.name, args.pythonpath)
        print(f"Created and tracked '{created.name}'")
        return 0

    def track(self, args: Any) -> int:
        tracked = track_document_file(args.store, args.model, args.path, args.name, args.pythonpath, args.force)
        print(f"Tracked '{tracked.name}'")
        return 0

    def update(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        m_entry, m_idx, doc = find_doc(sp, root, load_store_index(sp), args.doc)
        model_type = resolve_model_ref(m_entry.model_ref, args.pythonpath)
        rendered = render_model_markdown(model_type, self._parse_payload(args.payload))
        if not validate_model_input_roundtrip(model_type, rendered)[0]: raise SLDBValidationError("Update fail", validate_model_input_roundtrip(model_type, rendered)[1])
        (root / doc.path).write_text(rendered + "\n", encoding="utf-8")
        doc.hash_c, doc.hash_d = hash_text(rendered + "\n"), hash_fields(model_type, rendered + "\n")
        self._save_updated(sp, root, load_store_index(sp), m_entry, m_idx, doc, args)
        print(f"Updated '{doc.name}'")
        return 0

    def _save_updated(self, sp: Any, root: Path, idx: Any, m_entry: Any, m_idx: Any, doc: Any, args: Any) -> None:
        with store_lock(sp):
            save_document_shard(documents_shard_path(sp, m_entry.name, doc.name), doc)
            documents_hash.note(sp, m_entry.name, doc)
            # PLAN 15 capa 8: hash_b correct right away, not blanked for a later rebuild to fill in
            m_idx.hash_b = documents_hash.hash_b_of(sp, m_entry.name)
            m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
            save_models_index(root / m_entry.models_index, m_idx)
            rebuild_derived_indexes(sp, root, resolve_model_ref, args.pythonpath)  # semantic, sections, edges
            cascade_hash_a(sp, root, idx)

    def _save_untracked(self, sp: Any, root: Path, idx: Any, args: Any, m_entry: Any, m_idx: Any, doc: Any) -> None:
        forget_document(sp, root, idx, m_entry, m_idx, doc, args.pythonpath)

    def untrack(self, args: Any) -> int:
        untracked = untrack_document(args.store, args.doc, args.pythonpath)
        print(f"Untracked '{untracked.name}'")
        return 0

    def delete(self, args: Any) -> int:
        """Untrack a document and delete its Markdown file, asking first unless --yes."""
        if not getattr(args, "yes", False) and not self._confirm(args.doc):
            print("Aborted.")
            return 1
        deleted = delete_document(args.store, args.doc, args.pythonpath)
        print(f"Deleted '{deleted.name}' ({deleted.model}) and its file {deleted.path}")
        return 0

    def _confirm(self, doc: str) -> bool:
        """Ask before deleting a file; a non-interactive stdin answers no."""
        try:
            return input(f"Delete '{doc}' and its Markdown file? [y/N] ").strip().lower() in {"y", "yes"}
        except EOFError:
            return False
