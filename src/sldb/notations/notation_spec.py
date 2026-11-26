"""`NotationSpec`: una notacion completa, tal como esta en su YAML."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from sldb.notations.diagram_type import DiagramType
from sldb.notations.glyph_spec import GlyphSpec
from sldb.notations.link_spec import LinkSpec
from sldb.notations.marker_spec import MarkerSpec
from sldb.notations.notation_constants import _NAME, ANY_RELATION, LAYOUT_KINDS
from sldb.notations.notation_problems import notation_problems


class StandardSpec(BaseModel):
    """El estandar que una notacion implementa: nombre y, si se sabe, version."""

    model_config = ConfigDict(extra="forbid")

    name: str
    version: str | None = None

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("standard.name must be a non-empty name")
        return v.strip()

    @field_validator("version")
    @classmethod
    def _version(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.strip():
            raise ValueError("standard.version must be non-empty when present")
        return v.strip()

    def label(self) -> str:
        """`<name> <version>`, o solo el nombre sin version."""
        return f"{self.name} {self.version}" if self.version else self.name


class NotationSpec(BaseModel):
    """Una notacion completa, tal como esta en su YAML."""

    model_config = ConfigDict(extra="forbid")

    name: str
    title: str = ""
    diagram_type: str
    level: Literal["types", "instances", "both"] = "types"
    projection: str = "all"
    layout: dict[str, Any] = Field(default_factory=lambda: {"kind": "graph"})
    markers: list[MarkerSpec] = Field(default_factory=list)
    glyphs: list[GlyphSpec] = Field(min_length=1)
    links: list[LinkSpec] = Field(default_factory=list)
    description: str = ""
    # paleta de la notacion (nombre builtin o ruta relativa al YAML); vacia = `default` si algun
    # glifo o link usa estilo, ninguna si no
    palette: str = ""
    # estandar que implementa (UML, BPMN...): opcional; nombre obligatorio, version opcional
    standard: StandardSpec | None = None

    @model_validator(mode="before")
    @classmethod
    def _standard_shape(cls, data: Any) -> Any:
        """Un `standard` sin nombre (o sin ser un mapa) se rechaza nombrando la notacion."""
        if not isinstance(data, dict) or "standard" not in data or data["standard"] is None:
            return data
        who = data.get("name", "?")
        std = data["standard"]
        if not isinstance(std, dict):
            raise ValueError(f"notation {who!r}: standard must be a mapping with name and optional version")
        if not isinstance(std.get("name"), str) or not std["name"].strip():
            raise ValueError(f"notation {who!r}: standard.name is required and must be non-empty (version alone is not a standard)")
        if "version" in std and std["version"] is not None and (not isinstance(std["version"], str) or not std["version"].strip()):
            raise ValueError(f"notation {who!r}: standard.version must be a non-empty string when present")
        return data

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        if not _NAME.match(v):
            raise ValueError(f"notation name {v!r} must match {_NAME.pattern}")
        return v

    @field_validator("diagram_type")
    @classmethod
    def _diagram_type(cls, v: str) -> str:
        if v not in {t.value for t in DiagramType}:
            raise ValueError(f"diagram_type {v!r} is not a valid diagram type")
        return v

    @field_validator("layout")
    @classmethod
    def _layout(cls, v: dict) -> dict:
        kind = v.get("kind", "graph")
        if kind not in LAYOUT_KINDS:
            raise ValueError(f"layout.kind {kind!r} is not one of {', '.join(LAYOUT_KINDS)}")
        if "direction" in v and v["direction"] not in ("TB", "LR", "BT", "RL"):
            raise ValueError(f"layout.direction {v['direction']!r} must be TB, LR, BT or RL")
        # parametros reconocidos de kind graph: style layered|rings, ring_field para rings
        if v.get("style") not in (None, "layered", "rings"):
            raise ValueError(f"layout.style {v['style']!r} must be layered or rings")
        rest = {k: val for k, val in v.items() if k != "kind"}
        if "by" in rest:
            if kind != "partition-lanes":
                raise ValueError("layout.by only applies to kind partition-lanes")
            by = rest["by"]
            if not isinstance(by, str) or not by.strip():
                raise ValueError("layout.by must be a non-empty field name")
            rest["by"] = by.strip()
        return {"kind": kind, **rest}

    @model_validator(mode="after")
    def _consistent(self) -> "NotationSpec":
        problems = notation_problems(self)
        if problems:
            raise ValueError("; ".join(problems))
        return self

    @property
    def relations(self) -> list[str]:
        """Relaciones que la notacion nombra, en orden de declaracion y sin repetir."""
        out: list[str] = []
        for link in self.links:
            for rel in [link.relation, *(e.relation for e in link.ends.values() if e.relation)]:
                if rel and rel != ANY_RELATION and rel not in out:
                    out.append(rel)
        return out

    @property
    def styled(self) -> bool:
        """Si la notacion usa estilo (paleta, kind, colores o iconos)."""
        return bool(self.palette or any(g.kind or g.fill or g.stroke or g.icon for g in self.glyphs) or any(l.color for l in self.links))

    @property
    def models(self) -> list[str]:
        """Modelos que la notacion nombra (glifos, marcas y relaciones reificadas)."""
        out: list[str] = []
        for m in [*(g.model for g in self.glyphs), *(m.model for m in self.markers), *(l.model for l in self.links if l.model)]:
            if m not in out:
                out.append(m)
        return out
