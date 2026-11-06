"""One `ProjectGraph` per store and process, rebuilt only when something it read moved.

The signature of a build is the store's shards signature, the composed index it read (the
object `compose_edge_index` keeps, so the existing cache invalidation also drops the graph),
`(path, mtime_ns, size)` of every file it read or included (surface documents, declaring
documents, the files its rules kept after the exclusions, `store.yaml`) and the mtime of every
directory it walked (a new file in one of them moves it). Checking it stats that list; it
never walks the tree again. Excluded files are not observed.
"""

from __future__ import annotations

import os
from pathlib import Path

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.edges.project_graph.file_exclusions import FileExclusions
from sldb.api.edges.project_graph.project_graph import ProjectGraph
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.store.edge_index.shard_signature import shards_signature

Stat = tuple[str, int, int]
_GRAPHS: dict[str, tuple["ReadSignature", ProjectGraph]] = {}


def memoized_project_graph(store_path: Path, config: ProjectGraphConfig) -> ProjectGraph:
    """The graph of the project at `store_path.parent`, built again only when its signature moved."""
    key = str(store_path.resolve())
    hit = _GRAPHS.get(key)
    if hit is None or not hit[0].is_current():
        graph = ProjectGraph(store_path.parent, config)
        hit = _GRAPHS[key] = (ReadSignature.of(store_path, graph), graph)
    return hit[1]


class ReadSignature:
    """What one build read, as stats, and whether it still reads the same."""

    def __init__(self, store_path: Path, nodes: object, files: list[Stat], directories: list[Stat]) -> None:
        """Keep the shards signature now, the index's nodes object and the stats of files and directories."""
        self.store_path, self.nodes, self.files, self.directories = store_path, nodes, files, directories
        self.shards = shards_signature(store_path)

    @classmethod
    def of(cls, store_path: Path, graph: ProjectGraph) -> ReadSignature:
        """The signature of a just-built graph."""
        root, config = graph.root, graph.config
        included = {node.path for node in (*graph.nodes.documents, *graph.nodes.files)} | _declaring_documents(root, config)
        files = [_stat(root / path) for path in sorted(included)] + [_stat(store_path / "store.yaml")]
        return cls(store_path, _index_nodes(store_path), files, [_stat(path) for path in _directories(root, config)])

    def is_current(self) -> bool:
        """Whether nothing read has moved; stats only, no walk."""
        if shards_signature(self.store_path) != self.shards or _index_nodes(self.store_path) is not self.nodes:
            return False
        return all(_stat(Path(path)) == (path, mtime, size) for path, mtime, size in (*self.files, *self.directories))


def _index_nodes(store_path: Path) -> object:
    """The composed index's nodes (one object while the shards hold), None without an index."""
    if not (store_path / "core" / "store_index.yaml").is_file():
        return None
    return load_edge_index(store_path, include_linked=False).nodes


def _declaring_documents(root: Path, config: ProjectGraphConfig) -> set[str]:
    found: set[str] = set()
    for declaration in config.declared_file_targets:
        directory = root / declaration.directory
        found |= {path.relative_to(root).as_posix() for path in directory.rglob(declaration.pattern) if path.is_file()} if directory.exists() else set()
    return found


def _directories(root: Path, config: ProjectGraphConfig) -> list[Path]:
    """The project tree as the file walk prunes it, every surface (recursively when its glob is) and every declaring tree."""
    found = _walked(root, root, config.exclusions)
    for surface in config.surfaces:
        directory = root / surface.directory if surface.directory else root
        found += _walked(root, directory, None) if "**" in surface.pattern else [directory]
    for declaration in config.declared_file_targets:
        found += _walked(root, root / declaration.directory, None)
    return sorted(set(found))


def _walked(root: Path, top: Path, exclusions: FileExclusions | None) -> list[Path]:
    found: list[Path] = []
    for dirpath, dirnames, _ in os.walk(str(top)):
        relative = os.path.relpath(dirpath, str(root)).replace(os.sep, "/")
        if exclusions is not None:
            dirnames[:] = [name for name in dirnames if not exclusions.prunes("" if relative == "." else relative, name)]
        found.append(Path(dirpath))
    return found


def _stat(path: Path) -> Stat:
    try:
        st = path.stat()
        return (str(path), st.st_mtime_ns, st.st_size)
    except OSError:
        return (str(path), 0, 0)
