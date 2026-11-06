"""`ViewDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field, field_validator
from sldb.models.notation.view_doc_template import VIEW_DOC_TEMPLATE
from sldb.models.notation.view_nodes import normalize_view_nodes
from sldb.models.structured_nl_doc import StructuredNLDoc


class ViewDoc(StructuredNLDoc):
    """Una vista de la gramatica de proyeccion: que documentos y relaciones del store entran,
    en que direccion, y con que notacion y layout se dibujan.

    Es portable: solo nombra modelos, tipos de relacion y una notacion, nunca ids de nodo ni
    rutas de store, asi que la misma vista se evalua contra cualquier store que tenga esos
    modelos y relaciones. graph_ui la evalua (sldb.api.graph) y la crea y guarda por sldb.
    """

    __semantics__ = {
        "type": ["view"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["notation"]
    __template__ = VIEW_DOC_TEMPLATE

    id: str = Field(description="Nombre de la vista; nombre del documento (`ViewDoc:<name>`).")
    name: str = Field(description="Nombre de la vista, igual al id.")
    title: str = Field(description="Rotulo legible de la vista.")
    nodes: list[dict] = Field(
        default_factory=list,
        description="Union de entradas `{model, where}`: documentos de ese modelo que cumplen `where` (gramatica de `sldb find --where`; vacio = todos los del modelo). Lista vacia = todos los documentos.",
    )
    relations: list[str] = Field(default_factory=list, description="Nombres de tipos de relacion que se conservan entre esos nodos; vacio = todos.")
    direction: str = Field(default="both", description="`both`, `outgoing` o `incoming`, como `sldb.api.graph.RelationFilter.direction`.")
    notation: str = Field(default="", description="`NotationDoc:<name>` opcional; su `layout` da el estilo de la vista.")
    layout: dict = Field(
        default_factory=dict,
        description="Override del `layout` de la notacion, misma forma (`kind: graph`, `style: layered|rings`, `ring_field` para rings).",
    )
    params: dict = Field(
        default_factory=dict,
        description="Parametros opcionales de vista compuesta (GD25).",
    )
    sections: list = Field(
        default_factory=list,
        description="Secciones opcionales de vista compuesta (GD25).",
    )
    description: str = Field(default="", description="Para que sirve la vista.")

    @field_validator("nodes", mode="before")
    @classmethod
    def _nodes(cls, value):
        return normalize_view_nodes(value)

    @field_validator("direction")
    @classmethod
    def _direction(cls, value: str) -> str:
        if value not in ("both", "outgoing", "incoming"):
            raise ValueError(f"direction {value!r} must be both, outgoing or incoming")
        return value

    @field_validator("layout", mode="before")
    @classmethod
    def _layout(cls, value):
        value = {} if value is None else value
        style = value.get("style") if isinstance(value, dict) else None
        if style not in (None, "", "layered", "rings"):
            raise ValueError(f"layout.style {style!r} must be layered or rings")
        return value

    @field_validator("notation", mode="before")
    @classmethod
    def _absent_notation(cls, value):
        return "" if value is None else value

    @field_validator("params", mode="before")
    @classmethod
    def _absent_params(cls, value):
        return {} if value is None else value

    @field_validator("sections", mode="before")
    @classmethod
    def _absent_sections(cls, value):
        return [] if value is None else value
