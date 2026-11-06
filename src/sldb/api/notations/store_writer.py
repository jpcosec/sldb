"""Common logic for synchronizing notations and palettes to an sldb store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.notation_payloads import relation_type_payload
from sldb.api.notations.sync_constants import _MANAGED_MODELS, MODEL_REFS, RELATION_TYPES_DIR
from sldb.api.notations.sync_report import SyncReport


class StoreWriter:
    """Writes documents of the notation models into a store and reports what changed."""

    def __init__(self, store_path: Path | str, pythonpath: str | None = None, actor: str = "sldb"):
        self.store_path = Path(store_path).resolve()
        self.pythonpath = pythonpath
        self.actor = actor
        self._prepared = False
        self._root: Path | None = None

    def prepare(self) -> None:
        """Register notation models and builtin relations; idempotent."""
        if self._prepared:
            return
        import sldb.api as api
        for name, ref in MODEL_REFS.items():
            try:
                api.load_registered_model(self.store_path, name, self.pythonpath)
            except Exception:
                api.add_model(self.store_path, ref, self.pythonpath, actor=self.actor)
        api.init_relations(self.store_path, self.pythonpath)
        self._prepared = True

    @property
    def root(self) -> Path:
        """The project root of the store."""
        if self._root is None:
            import sldb.api as api

            self._root = Path(api.open_store(self.store_path).project_root).resolve()
        return self._root

    def existing_documents(self) -> dict[tuple[str, str], Any]:
        """The managed documents already in the store, by `(model, name)`."""
        import sldb.api as api

        return {
            (str(doc.model_name), str(doc.name)): doc
            for doc in api.load_runtime_documents(self.store_path, self.pythonpath, include_linked=False)
            if str(doc.model_name) in _MANAGED_MODELS
        }

    def create(self, model: str, name: str, path: Path, payload: dict) -> None:
        """Create a document of `model` at `path`."""
        import sldb.api as api

        api.create_document(self.store_path, model, path, payload, name=name, pythonpath=self.pythonpath, actor=self.actor)

    def upsert(self, existing: dict, report: SyncReport, model: str, name: str, path: Path, payload: dict) -> None:
        """Update the document if it exists, create it otherwise; record it in the report."""
        import sldb.api as api

        if (model, name) in existing:
            api.save_document_payload(self.store_path, model, name, payload, self.pythonpath, actor=self.actor)
            report.updated.append(f"{model}:{name}")
        else:
            self.create(model, name, path, payload)
            report.created.append(f"{model}:{name}")

    def ensure_relation_type(self, existing: dict, report: SyncReport, relation: str, description: str) -> None:
        """Creates `RelationTypeDoc` for `relation` if not present in store."""
        import sldb.api as api

        type_name = f"reltype-{relation}"
        if ("RelationTypeDoc", type_name) in existing or api.doc_exists(self.store_path, f"RelationTypeDoc/{type_name}"):
            return
        path = self.root / RELATION_TYPES_DIR / f"{relation}.md"
        self.create("RelationTypeDoc", type_name, path, relation_type_payload(relation, description))
        report.relation_types_added.append(relation)
        existing[("RelationTypeDoc", type_name)] = None

    def delete(self, existing: dict, report: SyncReport, model: str, name: str) -> None:
        """Delete a document and record it in the report."""
        import sldb.api as api

        api.delete_document(self.store_path, str(existing[(model, name)].path), self.pythonpath, actor=self.actor)
        report.deleted.append(f"{model}:{name}")

    def finish(self, report: SyncReport) -> SyncReport:
        """Rebuild the edge index and record its errors."""
        import sldb.api as api

        api.rebuild_edges(self.store_path, self.pythonpath)
        report.edge_errors = list(api.check_edges(self.store_path).errors)
        return report
