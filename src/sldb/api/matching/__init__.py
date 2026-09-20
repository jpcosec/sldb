"""Approximate matching: the embedder port, the difflib fallback, and the document index."""

from sldb.api.matching.difflib_matcher import DifflibMatcher, normalize
from sldb.api.matching.document_index import DocumentIndex
from sldb.api.matching.embedder_protocol import Embedder
from sldb.api.matching.matcher import Matcher, cosine

__all__ = ["DifflibMatcher", "DocumentIndex", "Embedder", "Matcher", "cosine", "normalize"]
