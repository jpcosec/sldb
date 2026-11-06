"""`EndpointKindError`."""

from __future__ import annotations

from sldb.notations.errors.validation_error import ValidationError


class EndpointKindError(ValidationError):
    """El kind de un extremo no está permitido."""
