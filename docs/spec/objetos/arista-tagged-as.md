---
clase: objeto
tipo: arista
nombre: tagged_as
estado: borrador
---

# `tagged_as`

## Qué es

Arista de una cosa a un tag: dice que un modelo, un documento o una sección lleva ese tag. Es la
base de buscar por significado y de comparar cosas por lo que comparten
(`sldb graph similar` usa `tagged_as` por defecto). No tiene atributos propios más allá de
`origin: structural`.

## Cómo se nombra

Hoy no tiene dirección propia: se identifica por el par (origen, tag). El origen es el id de un
nodo (`sldb://model/...`, documento o sección) y el destino es `sldb://semantic_tag/<tag>`
(`src/sldb/store/edge_index/records.py:21-23`, `node_ids.py:38-40`). Se ve con
`sldb edges show` y `sldb graph neighborhood`. Declarada en `.sldb/store.yaml:187-189` y como
relación incorporada en `src/sldb/models/builtin_relation_types.py:20`
(muchos a muchos, destino `semantic_tag`).

Con la gramática propuesta (borrador): `st/<cosa>` y `se/<tag>` ya nombran los dos extremos; la
arista sería el par. **Sin confirmar:** si la arista necesita nombre propio.

## Dónde se guarda

No se escribe: es derivada. Nace de dos fuentes que sí se escriben:

- `__semantics__` del modelo en Python (`src/sldb/store/edge_index/model_contribution.py:27-28`).
- Los campos `semantic_tags` y `tags` del documento y `semantic_tags` de cada sección
  (`src/sldb/store/edge_index/doc_structure.py:17-19`).

El índice de aristas está en `.sldb_cache/` (ignorado, regenerable). Ver
`docs/architecture/derived-store-boundary.md`.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | Poner el tag en el campo `semantic_tags` o `tags` del documento (edición del Markdown, p. ej. `docs update`, `fields update`) o en `__semantics__` del modelo. No hay comando que cree solo la arista | `src/sldb/store/semantic_tags.py:29-35`, `src/sldb/store/edge_index/doc_structure.py:17` | Crear la arista es agregar el tag al portador. **Sin confirmar.** |
| Leer | `sldb edges show`, `sldb graph neighborhood`, `sldb graph similar` (relación por defecto `tagged_as`), `sldb find <tag> --in semantic`. Sin verificar: la sintaxis exacta de `edges show` para esta relación | `src/sldb/cli/parsers/graph_analysis.py:62`, `src/sldb/cli/commands/graph_analysis.py:92`, `src/sldb/cli/parsers/find.py:6-7` | Leer en las dos direcciones: qué tags lleva algo, qué lleva un tag. **Sin confirmar.** |
| Cambiar | no existe. Busqué en `src/sldb/cli/` y `src/sldb/api/edges/`: `edges rewrite` es para aristas autoradas, no para esta | `src/sldb/cli/parsers/semantic.py:11-18` | **Sin confirmar:** la arista no tiene atributos; cambiarla sería mover el extremo (otro tag) y es borrar más crear. |
| Borrar | Quitar el tag del campo del documento o de `__semantics__`. No hay comando que borre la arista | `src/sldb/store/edge_index/doc_structure.py:17-19` | Borrar la arista es quitar el tag al portador; el tag no se borra. **Sin confirmar.** |

## Aristas que le llegan y que salen

Es ella misma una arista. Sale de `sldb_model`, `sldb_document` y `sldb_section`; llega a
`semantic_tag`. Las crea el índice de aristas al reconstruir
(`model_contribution.py:28`, `doc_structure.py:17-19`). El grafo de exportación semántica
también la emite (`src/sldb/store/graph/ingest_sldb_nodes.py:29,36,42`).

## Qué lo mantiene correcto

- Cada destino existe como nodo: `tag_nodes` agrega el nodo del tag aunque otro lo aportó
  (`src/sldb/store/edge_index/records.py:15-18`).
- `sldb edges check` revisa el índice completo (`src/sldb/api/edges/check_edges.py:16`).
- `sldb tags check` revisa que los tags con namespace cumplan su regla.

## Abierto

- Si poner un tag a una sección es un verbo propio o es editar el documento (hoy no hay comando
  que lo haga sin editar el Markdown de la sección).
- Qué es "cambiar" una arista sin atributos: nada, o mover el extremo.
- Si la arista de modelo (por `__semantics__`) se puede borrar sin editar código Python.

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es una propiedad semántica de un nodo, y una propiedad es una relación.

## Fuentes

`docs/architecture/tags.md`, `docs/architecture/edges.md`,
`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`,
`src/sldb/store/edge_index/` (`records.py`, `model_contribution.py`, `doc_structure.py`),
`src/sldb/store/graph/ingest_sldb_nodes.py`, `src/sldb/models/builtin_relation_types.py`,
`src/sldb/cli/parsers/graph_analysis.py`, `.sldb/store.yaml`.
