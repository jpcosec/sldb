"""`DocRef`: id de export de un documento sldb."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

# `Model:name` export id of an sldb document, optionally prefixed by the alias of a
# linked store (`store:Model:name`). The same format sldb resolves in declared
# references; an id without the model part is not a reference.
DOC_REF_PATTERN = r"^(?:[A-Za-z0-9][A-Za-z0-9._-]*:)?[A-Za-z_][A-Za-z0-9_]*:[^\s:]+$"
DocRef = Annotated[str, Field(pattern=DOC_REF_PATTERN)]
