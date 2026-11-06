"""The Python module of a model declared in JSON: a `StructuredNLDoc` written the way the
models of `sldb.models` are — docstring, `__template__`, one `Field` with a description per
field. A derivative of its declaration: the same declaration regenerates the same module.
Without a template given, one section per field.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from sldb.api.model_create.field_decl import FieldDecl
from sldb.api.model_create.model_declaration import check_compositions, check_field_names, declared_fields
from sldb.api.model_create.model_module_lines import HEADER, composition_section, field_section, module_lines

__all__ = ["HEADER", "ModelSource"]


@dataclass(frozen=True)
class ModelSource:
    """A model's name, fields, template and base: the module they make."""

    name: str
    fields: tuple[FieldDecl, ...]
    template: str | None = None
    base: tuple[str, str] = ("sldb", "StructuredNLDoc")
    containment: dict[str, list[str]] | None = None
    references: list[str] | None = None
    compositions: dict[str, dict] | None = None
    semantics: dict[str, list[str]] | None = None
    authority: str | None = None

    @staticmethod
    def of(
        name: str,
        fields: list,
        template: str | None,
        base: tuple[str, str] | None,
        containment: dict[str, list[str]] | None = None,
        references: list[str] | None = None,
        compositions: dict[str, dict] | None = None,
        semantics: dict[str, list[str]] | None = None,
        authority: str | None = None,
        inherited_fields: set[str] | None = None,
    ) -> "ModelSource":
        decls = declared_fields(name, fields)
        known = {d.name for d in decls} | (inherited_fields or set())
        check_field_names("containment", containment, known, name)
        check_field_names("references", references, known, name)
        check_compositions(compositions, known, template)
        base = base or ("sldb", "StructuredNLDoc")
        return ModelSource(name, decls, template, base, containment, references, compositions, semantics, authority)

    @property
    def snake(self) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.name).lower()

    def default_template(self, head: str | None = None) -> str:
        """One section per field under `head` (the model's name, or its base's template)."""
        sections = [head or f"# {self.name}"]
        sections += [field_section(f) for f in self.fields]
        sections += [composition_section(c) for c in self.compositions or {}]
        return "\n\n".join(sections) + "\n"

    def module(self, head: str | None = None) -> str:
        """The whole module, as text; `head` opens the default template."""
        module, cls = self.base
        template = (self.template or self.default_template(head)).strip()
        attrs = {"__authority__": self.authority, "__semantics__": self.semantics, "__containment__": self.containment, "__references__": self.references, "__compositions__": self.compositions}
        return "\n".join(module_lines(self.name, module, cls, template, self.fields, attrs)) + "\n"
