"""Inspect existing knowledge registrations without extracting the whole store."""
from __future__ import annotations

from pathlib import Path
from sldb.selfdoc.planned_document import PlannedDocument
from sldb.store.hashing import hash_fields, hash_text
from sldb.store.io import load_store_index, load_models_index, load_documents_index


class DocumentationRegistry:
    """Read only the indexes for models involved in self-documentation."""

    def __init__(self, store: Path, root: Path) -> None:
        self.store, self.root = store, root
        self.models = {entry.name: entry for entry in load_store_index(store).models}
        self._documents: dict[str, tuple[dict, dict]] = {}

    def status(self, plan: PlannedDocument) -> str | None:
        """Report absent tracking or stale hashes, rejecting identity collisions."""
        entry = self.models.get(plan.model_name)
        if entry is None:
            return "untracked"
        self._validate_model(entry, plan.model_name)
        by_name, by_path = self._document_maps(entry, plan.model_name)
        matches = list({id(item): item for item in (by_name.get(plan.payload.id), by_path.get(plan.path)) if item}.values())
        return self._document_status(matches, plan)

    def _document_maps(self, entry, name: str) -> tuple[dict, dict]:
        if name not in self._documents:
            index = load_models_index(self.root / entry.models_index)
            documents = load_documents_index(self.root / index.documents_index).documents
            self._documents[name] = ({doc.name: doc for doc in documents}, {(self.root / doc.path).resolve(): doc for doc in documents})
        return self._documents[name]

    def _validate_model(self, entry, name: str) -> None:
        expected = f"sldb.models.knowledge_surface:{name}"
        if entry.model_ref != expected:
            raise ValueError(f"Model {name} is registered with a different contract: {entry.model_ref}")

    def managed_paths(self, output: Path, system: str, model_names: set[str]) -> list[Path]:
        """Include missing files whose registration still belongs to this inventory."""
        paths = []
        for name, folder, prefix in self._managed_models():
            if name not in model_names:
                continue
            paths.extend(self._model_paths(name, folder, prefix, output, system))
        return paths

    def _model_paths(self, name, folder, prefix, output, system) -> list[Path]:
        entry = self.models.get(name)
        if entry is None:
            return []
        self._validate_model(entry, name)
        index = load_models_index(self.root / entry.models_index)
        return [path for doc in load_documents_index(self.root / index.documents_index).documents
                if (path := (self.root / doc.path).resolve()).parent == output / folder
                and path.name.startswith(f"{prefix}-{system}-")]

    def _managed_models(self):
        return (("CliCommandDoc", "commands", "cmd"), ("SurfaceDoc", "surfaces", "surface"),
                ("PythonSymbolDoc", "symbols", "python"))

    def _document_status(self, matches, plan):
        if not matches:
            return "untracked"
        if len(matches) != 1 or matches[0].name != plan.payload.id or (self.root / matches[0].path).resolve() != plan.path:
            raise ValueError(f"Document identity/path collision: {plan.payload.id}")
        if plan.previous is None:
            return "stale_indexes"
        if matches[0].hash_c != hash_text(plan.previous) or matches[0].hash_d != hash_fields(type(plan.payload), plan.previous):
            return "stale_indexes"
        return None
