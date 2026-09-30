"""Document segments: the render seen as literals plus field spans.

An instrumented render (see :class:`sldb.core.renderer_engine.span_recorder.SpanRecorder`)
emits sentinels around every value a marker wrote. ``sentinel_decoder`` removes them and
returns character offsets; ``segment_tree`` nests those offsets and fills the gaps with
literal segments, so a consumer can walk a document as an editable sequence.
"""

from sldb.core.segments.segment_tree import build_segment_tree
from sldb.core.segments.sentinel_decoder import decode_sentinels, strip_with_offsets

__all__ = ["build_segment_tree", "decode_sentinels", "strip_with_offsets"]
