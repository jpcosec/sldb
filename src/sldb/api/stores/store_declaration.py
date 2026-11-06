"""`.sldb/store.yaml`: what a store declares, the part of it that is source and lives in git.

Everything else in `.sldb/core/` (the store index, the model and document indexes) is derived
from this file, the tracked Markdown and the models' Python classes, and `sldb stores build`
regenerates it (docs/architecture/derived-store-boundary.md). `.sldb/` is versioned whole so
that git holds the tree's past; what is only a cache lives in `.sldb_cache/`, ignored.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, SerializerFunctionWrapHandler, model_serializer

from sldb.api.stores.seed import Seed

DECLARATION_FILE = "store.yaml"
SCAFFOLD_KEYS = ("folders", "seeds")


class StoreDeclaration(BaseModel):
    """Models registered, links to other stores, predicates, and which file is tracked how."""

    version: int = Field(default=1, description="Declaration format version.")
    links: list[dict[str, str]] = Field(default_factory=list, description="`{name, path}` of each linked store; paths relative to the project.")
    models: list[dict[str, Any]] = Field(default_factory=list, description="`{name, model_ref}` plus `path` (a local model's source) or `origin` (the link alias it is inherited from), and `canonical` when true.")
    predicates: dict[str, dict[str, str]] = Field(default_factory=dict, description="Predicate name -> `{axis, description}`.")
    generate: list[dict[str, Any]] = Field(default_factory=list, description="Generators run before tracking, e.g. `{command: selfdoc python-sync, args: [...]}`.")
    derived: list[str] = Field(default_factory=list, description="Project paths (directory prefixes) the generators write: derived, so not versioned and left out of a rebuild check's copy. `.sldb/core/` and `.sldb_cache/` always are.")
    include: list[dict[str, Any]] = Field(default_factory=list, description="`{model, glob}` (each match tracked under its file stem) or `{model, paths: [path | {path, name}]}`.")
    graph_backend: str = Field(default="networkx", description="Graph analysis backend; only `networkx` is admitted in this phase (docs/architecture/graph-backend.md).")
    policy: dict[str, dict[str, str]] = Field(default_factory=dict, description="Model name (or `*`) -> finding code -> `ignore | allow | alert | error | reindex | hook: <command>` (docs/architecture/provenance.md §5).")
    folders: list[str] = Field(default_factory=list, description="Directories `stores scaffold` creates, relative to the project root (docs/architecture/store-declaration.md).")
    seeds: list[Seed] = Field(default_factory=list, description="Files `stores scaffold` writes from a declared source: `{path, mode, text | file | document, track}`.")

    @model_serializer(mode="wrap")
    def _without_empty_scaffold_keys(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        """A declaration without folders or seeds dumps as it did before they existed, and a
        seed dumps only the keys it was written with."""
        dumped = handler(self)
        for key in SCAFFOLD_KEYS:
            if not dumped.get(key):
                dumped.pop(key, None)
        if dumped.get("seeds"):
            dumped["seeds"] = [{k: v for k, v in seed.items() if v is not None} for seed in dumped["seeds"]]
        return dumped


def declaration_path(store_path: Path) -> Path:
    """Where a store's declaration lives."""
    return Path(store_path) / DECLARATION_FILE


def load_declaration(store_path: Path) -> StoreDeclaration:
    """The store's declaration; a missing file is an error, not an empty store."""
    path = declaration_path(store_path)
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist: run `sldb stores declare --write` first")
    definition = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    _validate_graph_backend(definition)
    return StoreDeclaration.model_validate(definition)


def _validate_graph_backend(definition: dict[str, Any]) -> None:
    """Reject a backend this phase cannot run, naming the only admitted one."""
    backend = definition.get("graph_backend", "networkx")
    if backend != "networkx":
        raise ValueError(f'graph_backend {backend} no admitido; admitidos: ["networkx"]')


def declared_graph_backend(store_path: str | Path | None = None) -> str:
    """The store's `graph_backend`, or `networkx` when it has no declaration or no key."""
    if store_path is None:
        return "networkx"
    path = Path(store_path)
    if path.name != ".sldb" and (path / ".sldb").is_dir():
        path = path / ".sldb"
    if not declaration_path(path).is_file():
        return "networkx"
    return load_declaration(path).graph_backend


def save_declaration(store_path: Path, declaration: StoreDeclaration) -> Path:
    """Write the declaration in a stable, reviewable order."""
    path = declaration_path(store_path)
    path.write_text(yaml.safe_dump(declaration.model_dump(), sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    return path


def declared_store(store_arg: str | None) -> tuple[Path, Path]:
    """`(store, project root)` of the store a build targets: `--store` (a `.sldb` directory or
    its project) or the nearest ancestor holding `.sldb/store.yaml`. A store that is only
    declared has no index yet, so the usual discovery, which looks for one, cannot find it."""
    if store_arg:
        store = Path(store_arg).resolve()
        store = store if store.name == ".sldb" else store / ".sldb"
        return store, store.parent
    for folder in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if declaration_path(folder / ".sldb").is_file():
            return folder / ".sldb", folder
    raise FileNotFoundError(f"No .sldb/{DECLARATION_FILE} here or above {Path.cwd()}")
