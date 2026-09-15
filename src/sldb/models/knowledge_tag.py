"""Namespaced semantic tags shared by knowledge documents."""
from __future__ import annotations

from typing import Annotated
from pydantic import Field

KnowledgeTag = Annotated[
    str,
    Field(
        pattern=r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$",
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]
