"""The `include` rules that reproduce a store's current tracking, exactly.

A directory becomes one glob only when the glob would track exactly what is tracked there,
under one model, each document named after its file, and never the project root itself (a
new README there is not a new document of that model), nor a folder holding a single tracked
file: `desk/tasks/` with only `Board.md` would make every new task a board. Anything else is listed by path, with
the name when it differs from the file stem: document names enter the `sldb://document/...`
ids, so a rule may not rename what it tracks.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from sldb.store.io import load_documents_index, load_models_index, load_store_index


def tracked_rows(store_path: Path, root: Path) -> list[tuple[str, str, str]]:
    """`(model, path, name)` of every tracked document, sorted."""
    rows = []
    for model in load_store_index(store_path).models:
        models_index = load_models_index(root / model.models_index)
        documents = load_documents_index(root / models_index.documents_index).documents
        rows += [(model.name, doc.path, doc.name) for doc in documents]
    return sorted(rows)


def declared_includes(store_path: Path, root: Path) -> list[dict]:
    """One rule per (model, directory): a glob where it is exact, a path list otherwise."""
    groups: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    for model, path, name in tracked_rows(store_path, root):
        groups[(model, str(Path(path).parent))].append((path, name))
    return [_rule(root, model, folder, docs) for (model, folder), docs in sorted(groups.items())]


def _rule(root: Path, model: str, folder: str, docs: list[tuple[str, str]]) -> dict:
    tracked = {path for path, _ in docs}
    on_disk = {p.relative_to(root).as_posix() for p in (root / folder).glob("*.md")}
    if folder != "." and len(docs) > 1 and tracked == on_disk and all(Path(path).stem == name for path, name in docs):
        return {"model": model, "glob": f"{folder}/*.md"}
    return {"model": model, "paths": [path if Path(path).stem == name else {"path": path, "name": name} for path, name in docs]}
