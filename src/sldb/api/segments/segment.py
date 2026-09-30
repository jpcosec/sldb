"""The ``Segment`` union and the forward references that close it.

``FieldSegment`` and ``CompositionPiece`` both hold ``children: list[Segment]``,
so the union cannot live in either file without a cycle. Declaring it here and
rebuilding both models from this module is what makes the recursion resolvable.
"""

from __future__ import annotations

from typing import Annotated, Union

from pydantic import Field

from sldb.api.segments.composition_piece import CompositionPiece
from sldb.api.segments.field_segment import FieldSegment
from sldb.api.segments.literal_segment import LiteralSegment

Segment = Annotated[Union[LiteralSegment, FieldSegment, CompositionPiece], Field(discriminator="type")]

FieldSegment.model_rebuild(_types_namespace={"Segment": Segment})
CompositionPiece.model_rebuild(_types_namespace={"Segment": Segment})
