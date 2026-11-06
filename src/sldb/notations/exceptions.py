"""Jerarquía de excepciones del subsistema de notaciones y paletas."""

from __future__ import annotations


class NotationError(Exception):
    """Excepción base de notaciones y paletas."""


class ValidationError(NotationError):
    """Error de validación semántica de una notación o paleta."""


class UnknownReferenceError(ValidationError):
    """Un spec o notación nombra un id que no existe."""


class EndpointKindError(ValidationError):
    """El kind de un extremo no está permitido."""


class StructureError(ValidationError):
    """Estructura inválida."""


class UnknownKindError(ValidationError):
    """Una notación o spec style nombra un kind no declarado por la paleta."""


class InvalidColorError(ValidationError):
    """Un color no es un token de paleta ni un hex `#rrggbb`."""


class UnknownIconError(ValidationError):
    """Un icono no está en el conjunto de iconos declarado."""


class UnknownShapeError(ValidationError):
    """Una forma no es una primitiva reconocida."""


class AmbiguousPathError(ValidationError):
    """Ruta ambigua en la resolución."""


class UnknownNotationError(ValidationError):
    """Una notación no resuelve a un archivo, builtin ni documento del store."""


class NotationMismatchError(ValidationError, ValueError):
    """La notación existe pero dibuja un tipo de diagrama distinto al spec."""


__all__ = [
    "NotationError",
    "ValidationError",
    "UnknownReferenceError",
    "EndpointKindError",
    "StructureError",
    "UnknownKindError",
    "InvalidColorError",
    "UnknownIconError",
    "UnknownShapeError",
    "AmbiguousPathError",
    "UnknownNotationError",
    "NotationMismatchError",
]
