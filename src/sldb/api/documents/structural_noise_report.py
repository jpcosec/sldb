"""The verdict of a structural-noise scan, and the refusal message it renders."""

from __future__ import annotations

from pydantic import BaseModel, Field


class StructuralNoiseReport(BaseModel):
    """Headings a document carries that its model's template never declares.

    Attributes:
        document: The document name, used in the message.
        model: The model the document is (or would be) tracked as.
        undeclared: The offending heading lines, in document order.
    """

    document: str = Field(default="", description="Document name shown in the message.")
    model: str = Field(default="", description="Model whose template was compared against.")
    undeclared: list[str] = Field(default_factory=list, description="Undeclared heading lines, in document order.")
    narrative: bool = Field(default=False, description="The model's template declares no literal heading: a body of free prose, where headings are the author's (policy: allowed).")

    @property
    def clean(self) -> bool:
        """Whether every heading in the document is declared by the model."""
        return not self.undeclared

    def message(self) -> str:
        """The refusal: what was found, then the model change that admits it."""
        head = f"ruido estructural en '{self.document}': el documento trae {len(self.undeclared)} headings que {self.model} no declara:"
        listing = "\n".join(f"  {line}" for line in self.undeclared)
        return f"{head}\n\n{listing}\n\n{self._remedy()}"

    def _remedy(self) -> str:
        """Where the missing declarations belong: a child model, fields as optrev."""
        return ("Un heading dentro de un field es un campo que falta en el modelo. "
                f"Creá un modelo que herede de {self.model} y declare esas secciones como campos optrev.")

    def details(self) -> dict:
        """The report as the `details` payload of an `SLDBValidationError`."""
        return {"document": self.document, "model": self.model, "undeclared": list(self.undeclared)}
