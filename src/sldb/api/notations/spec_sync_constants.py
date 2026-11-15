"""Constantes de la sincronizacion de specs: colecciones de elementos y de aristas por tipo de diagrama.

Migradas de `spec2viz.sldb_sync` (y `_ELEMENT_COLLECTIONS` de `spec2viz.deskops`).
"""

from __future__ import annotations

# claves neutrales de `style.kinds` de un spec (las de un renderer, como `plantuml`, quedan para el)
STYLE_KEYS = ("fill", "stroke", "icon")

# coleccion de aristas por tipo de diagrama: (coleccion, campo con la relacion o None,
# relacion por defecto). Con campo None todas las aristas llevan la relacion por defecto.
# activity y component_view_matrix no tienen coleccion de aristas: salen de los elementos.
_EDGE_COLLECTIONS: dict[str, tuple[str, str | None, str]] = {
    "component": ("edges", "relation", "uses"),
    # el protocolo es un atributo y el rotulo de la conexion, no un tipo de relacion: ":5432" y
    # "Postgres :5432" son la misma relacion `connects`
    "deployment": ("connections", None, "connects"),
    "state": ("transitions", None, "transitions_to"),
    "sequence": ("messages", "kind", "sends"),
    "class": ("relations", "relation", "association"),
    "reflection": ("edges", "relation", "relates_to"),
}

# el `kind` de un mensaje de secuencia como relacion (los renderers tratan todo lo que no es
# async/return como sincrono; aqui los sinonimos que aparecen en los specs)
_MESSAGE_RELATIONS = {
    "sync": "sends", "call": "sends", "": "sends",
    "async": "sends_async", "signal": "sends_async",
    "return": "returns", "reply": "returns", "response": "returns",
}

# en deployment, communication (por defecto) es `connects`; «deploy» y «manifest» son su propia relacion
_DEPLOYMENT_RELATIONS = {"deploy": "deploy", "manifest": "manifest"}

# colecciones de elementos por tipo de diagrama (las de spec2viz.deskops)
_ELEMENT_COLLECTIONS = {
    "component": ("nodes",),
    "deployment": ("nodes", "artifacts"),
    "activity": ("steps",),
    "state": ("states",),
    "class": ("classes",),
    "sequence": ("participants",),
}

# las de deskops mas reflection
_ELEMENT_COLLECTIONS_SYNC: dict[str, tuple[str, ...]] = {**_ELEMENT_COLLECTIONS, "reflection": ("nodes",), "class": ("classes", "packages")}

# campo que mejor describe una arista, para las notas del RelationDoc
_EDGE_LABEL_FIELDS = ("label", "on", "message", "protocol")

# campos del elemento que ya tienen sitio propio en SpecNodeDoc; el resto va a `data`
_ELEMENT_OWN_FIELDS = frozenset({"id", "label", "name", "kind", "type", "contains", "atoms", "refs", "description", "docstring"})

# pseudonodos UML de una actividad: el inicial siempre es propio y fluye al paso de `start`, que
# conserva su glifo (accion o decision); el final es el propio `end` cuando no es un paso
# (`end: end`) y, si `end` nombra un paso, un final aparte al que ese paso fluye
ACTIVITY_INITIAL = "__initial"
ACTIVITY_FINAL = "__final"

# campos de una arista que viajan en `RelationDoc.attributes`, por tipo
_EDGE_ATTRIBUTE_FIELDS: dict[str, tuple[str, ...]] = {
    "class": ("from_multiplicity", "to_multiplicity", "label"),
    "state": ("on", "guard", "action"),
    "sequence": ("kind", "group", "message"),
    "deployment": ("protocol", "label", "kind"),
}
