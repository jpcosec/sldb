"""Constantes de las notaciones: vocabulario cerrado de enumeraciones, formas y relaciones."""

from __future__ import annotations

import re
from pathlib import Path

NOTATIONS_DIR = Path(__file__).parent / "builtin"

# notacion por defecto de cada tipo de diagrama; los tipos ausentes no llevan notacion
DEFAULT_NOTATIONS: dict[str, str] = {
    "class": "uml-class",
    "state": "statechart",
    "component": "component",
    "deployment": "deployment",
    "sequence": "uml-sequence",
    "activity": "activity",
    "component_view_matrix": "component-view-matrix",
    "reflection": "reflection",
}

# el link comodin: dibuja toda relacion que ningun otro link de la notacion nombre
ANY_RELATION = "*"

DRAW_KINDS = ("line", "nest", "lane", "cell", "axis")
LINE_KINDS = ("solid", "dashed", "dotted")
TERMINALS = (
    "none", "open-arrow", "filled-arrow", "hollow-triangle", "filled-triangle",
    "hollow-diamond", "filled-diamond", "filled-circle", "hollow-circle", "bar", "crowfoot",
)
LEVELS = ("types", "instances", "both")

# formas primitivas que una superficie sabe dibujar: las de las notaciones builtin, mas cylinder
# (bases de datos y almacenamiento), queue (cola: cilindro horizontal), cloud (servicio externo),
# package (la carpeta con pestana de UML) y note (nota UML con esquina doblada)
SHAPES = (
    "artifact", "boundary-box", "boundary-lifeline", "box", "bullseye", "class-box", "column-header",
    "diamond", "filled-circle", "lifeline", "node-box", "rounded-box", "rounded-container", "row-header",
    "stick-figure", "cylinder", "queue", "cloud", "package", "note",
)
LAYOUT_KINDS = ("graph", "tree", "lanes", "grid", "axis", "manual")

# relaciones que cada tipo de diagrama emite al sincronizar (`sldb_sync.spec_edges` mas
# `contains`); None = relaciones libres, no se comprueban
KNOWN_RELATIONS: dict[str, frozenset[str] | None] = {
    "class": frozenset({"inheritance", "realization", "composition", "aggregation", "association", "dependency", "contains"}),
    "state": frozenset({"transitions_to", "contains"}),
    "sequence": frozenset({"sends", "sends_async", "returns", "contains"}),
    "activity": frozenset({"next", "branch", "contains"}),
    "component_view_matrix": frozenset({"occupies", "contains"}),
    "component": None,
    "deployment": None,
    "reflection": None,
}

_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_ID = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
