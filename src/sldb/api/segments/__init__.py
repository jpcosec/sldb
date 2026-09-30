"""Document segments: the boundary types for a document seen as editable spans.

``sldb.core.segments`` produces plain dicts out of an instrumented render; this
package is the Pydantic boundary over them, so ``sldb serve`` and library
consumers get a validated, self-describing contract instead of raw mappings.
"""

from sldb.api.segments.build_document_segments import build_document_segments
from sldb.api.segments.composition_piece import CompositionPiece
from sldb.api.segments.composition_spec import CompositionSpec
from sldb.api.segments.document_segments import DocumentSegments
from sldb.api.segments.field_segment import FieldSegment
from sldb.api.segments.literal_segment import LiteralSegment
from sldb.api.segments.segment import Segment
from sldb.api.segments.source_ref import SourceRef

__all__ = [
    "CompositionPiece", "CompositionSpec", "DocumentSegments", "FieldSegment",
    "LiteralSegment", "Segment", "SourceRef", "build_document_segments",
]
