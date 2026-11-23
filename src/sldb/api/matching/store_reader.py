"""`StoreReader`: lectura de los stores de las vistas con caché por store y avisos como findings.

Lo que queda de `spec2viz.deskops.SldbAtomResolver` sin el descubrimiento del store: documentos,
átomos y aristas por store, leídos una vez. Un store ilegible o sin índice de aristas deja un
finding una sola vez y sigue con vacío.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.matching.atom_payload import atoms_from_documents
from sldb.api.matching.matching_findings import finding
from sldb.api.matching.store_documents import resolve_ref, store_documents
from sldb.api.matching.store_edges import edges_of_index, load_index
from sldb.core.finding import Finding


class StoreReader:
    """Documentos, átomos y aristas de los stores de las vistas, con caché y findings."""

    def __init__(self, pythonpath: str | None = None):
        self.pythonpath = pythonpath
        self.findings: list[Finding] = []
        self._docs: dict[str, list[dict]] = {}
        self._edges: dict[tuple[str, str], list[dict]] = {}
        self._no_edges: set[str] = set()
        self._index: dict[str, tuple] = {}

    def documents(self, store_path: Path) -> list[dict]:
        key = str(Path(store_path).resolve())
        if key not in self._docs:
            try:
                self._docs[key] = store_documents(Path(key), self.pythonpath)
            except Exception as exc:
                self._docs[key] = []
                self.findings.append(finding("store-unreadable", key, f"Failed to load documents through SLDB: {exc}", "revisar el store con sldb stores check"))
        return self._docs[key]

    def atoms(self, store_path: Path) -> dict[str, dict]:
        return atoms_from_documents(self.documents(store_path))

    def resolve_ref(self, store_path: Path, ref: str) -> dict | None:
        return resolve_ref(self.documents(store_path), ref)

    def edges_of(self, store_path: Path, ref: str) -> list[dict]:
        key = str(Path(store_path).resolve())
        if (key, ref) not in self._edges:
            self._edges[(key, ref)] = [] if key in self._no_edges else self._read_edges(key, ref)
        return self._edges[(key, ref)]

    def _read_edges(self, key: str, ref: str) -> list[dict]:
        try:
            if key not in self._index:
                self._index[key] = (load_index(Path(key)), {doc["ref"]: doc["title"] for doc in self.documents(Path(key))})
            index, titles = self._index[key]
            return edges_of_index(index, ref, titles)
        except Exception as exc:
            self._no_edges.add(key)
            self.findings.append(finding("edges-unavailable", key, f"Edge index unavailable through SLDB, relations left out: {exc}", "sldb edges rebuild"))
            return []
