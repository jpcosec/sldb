"""`class_package`."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from sldb.models.notation.diagram_specs.base.doc_ref import DocRef
from sldb.models.notation.diagram_specs.class_diagram.aliases import Identifier
from sldb.models.notation.diagram_specs.class_diagram.aliases import Label


class ClassPackage(BaseModel):
    """A UML package: groups classes and other packages (nesting at any depth)."""

    model_config = ConfigDict(extra="forbid")
    label: Label | None = None
    kind: str = Field(
        default="package",
        description="Semantic kind of the package (a domain, a layer...); `style.kinds` styles it by this kind, with the same precedence as any element.",
    )
    contains: list[Identifier] = Field(
        default_factory=list,
        description="Class and package identifiers inside this package. Each class and each package has at most one parent package, without cycles.",
    )
    description: str | None = None
    atoms: list[str] = Field(default_factory=list, description="Optional atom ids that explain this package.")
    refs: list[DocRef] = Field(default_factory=list, description="Optional sldb document refs this package points at.")
