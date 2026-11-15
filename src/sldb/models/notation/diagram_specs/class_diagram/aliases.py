"""Alias de tipos de `class_diagram`."""

from __future__ import annotations

from typing import Annotated, Literal
from pydantic import StringConstraints


Identifier = Annotated[str, StringConstraints(pattern=r"^[A-Za-z_][A-Za-z0-9_]*$")]
MemberName = Annotated[str, StringConstraints(pattern=r"^[A-Za-z_][A-Za-z0-9_?!-]*$")]
# Type names are display expressions, not a language-specific type checker.
TypeName = Annotated[str, StringConstraints(pattern=r"^[A-Za-z_][A-Za-z0-9_.\[\], ?|<>-]*$")]
Label = Annotated[str, StringConstraints(min_length=1, pattern=r'^[^\r\n{}\\"]+$')]
Visibility = Literal["public", "private", "protected", "package"]
Multiplicity = Annotated[str, StringConstraints(pattern=r"^(?:\*|[0-9]+(?:\.\.(?:[0-9]+|\*))?)$")]
