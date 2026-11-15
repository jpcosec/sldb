"""Approximate matching: the embedder port, the difflib fallback, and the document index.

Also the matching of atoms with diagram elements (migrated from `spec2viz.deskops`): explicit
`atoms:`/`refs:` per element, keys and aliases, the tag filter, the coverage per view and the
fuzzy ranking of atoms through `DocumentIndex.rank`.
"""

from sldb.api.matching.difflib_matcher import DifflibMatcher, normalize
from sldb.api.matching.document_index import DocumentIndex
from sldb.api.matching.embedder_protocol import Embedder
from sldb.api.matching.matcher import Matcher, cosine
from sldb.api.matching.atom_keys import alias_candidates, label_key, normalize_key
from sldb.api.matching.atom_payload import atoms_from_documents, merge_atom, parse_atoms
from sldb.api.matching.atom_ranking import atom_index_items, rank_atoms
from sldb.api.matching.atom_tags import filter_atoms_payload, tag_matches
from sldb.api.matching.atoms_by_view import build_atoms_by_view, raw_atoms_by_view
from sldb.api.matching.coverage import build_coverage_by_view, discover_snapshot_path
from sldb.api.matching.explicit_atoms import atom_index, build_explicit_atoms
from sldb.api.matching.explicit_refs import attach_atom_edges, build_explicit_refs
from sldb.api.matching.spec_view import SpecView
from sldb.api.matching.spec_view_elements import collect_explicit_atoms, collect_explicit_refs, spec_view_elements
from sldb.api.matching.store_documents import ref_payload, resolve_ref, store_documents
from sldb.api.matching.store_edges import STRUCTURAL_RELATIONS, edges_of
from sldb.api.matching.store_reader import StoreReader
from sldb.api.matching.unknown_atom_error import UnknownAtomError

__all__ = [
    "DifflibMatcher", "DocumentIndex", "Embedder", "Matcher", "cosine", "normalize",
    "alias_candidates", "label_key", "normalize_key",
    "atoms_from_documents", "merge_atom", "parse_atoms", "atom_index_items", "rank_atoms",
    "filter_atoms_payload", "tag_matches", "build_atoms_by_view", "raw_atoms_by_view",
    "build_coverage_by_view", "discover_snapshot_path", "atom_index", "build_explicit_atoms",
    "attach_atom_edges", "build_explicit_refs", "SpecView",
    "collect_explicit_atoms", "collect_explicit_refs", "spec_view_elements",
    "ref_payload", "resolve_ref", "store_documents", "STRUCTURAL_RELATIONS", "edges_of",
    "StoreReader", "UnknownAtomError",
]
