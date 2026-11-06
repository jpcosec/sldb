"""Jerarquía de excepciones del subsistema de notaciones y paletas (un módulo por clase en `errors`)."""

from __future__ import annotations

from sldb.notations.errors.notation_error import NotationError
from sldb.notations.errors.validation_error import ValidationError
from sldb.notations.errors.unknown_reference_error import UnknownReferenceError
from sldb.notations.errors.endpoint_kind_error import EndpointKindError
from sldb.notations.errors.structure_error import StructureError
from sldb.notations.errors.unknown_kind_error import UnknownKindError
from sldb.notations.errors.invalid_color_error import InvalidColorError
from sldb.notations.errors.unknown_icon_error import UnknownIconError
from sldb.notations.errors.unknown_shape_error import UnknownShapeError
from sldb.notations.errors.ambiguous_path_error import AmbiguousPathError
from sldb.notations.errors.unknown_notation_error import UnknownNotationError
from sldb.notations.errors.notation_mismatch_error import NotationMismatchError

__all__ = ["NotationError", "ValidationError", "UnknownReferenceError", "EndpointKindError", "StructureError", "UnknownKindError", "InvalidColorError", "UnknownIconError", "UnknownShapeError", "AmbiguousPathError", "UnknownNotationError", "NotationMismatchError"]
