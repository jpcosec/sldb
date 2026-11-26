---
clase: objeto
tipo: nodo
nombre: tag
estado: borrador
---

# Tag

## Qué es

Un tag es una etiqueta de significado, como `type.knowledge.spec` o `area:a.b`. Existe en el
store porque un modelo, un documento o una sección lo lleva; nadie lo crea aparte. Sirve para
buscar por significado (`find`, `se.<tag>`, `model_tag(...)` en reglas) y para agrupar: el nombre
con puntos da al tag un padre implícito por prefijo (`type.knowledge` es padre de
`type.knowledge.spec`). Un tag puede además tener un namespace (`area:`), que `store.yaml` declara.

## Cómo se nombra

Hoy:

- Texto del tag: `type.knowledge.spec`, `area:a.b` (`src/sldb/store/semantic_tags.py:38-41`).
- Id de nodo en el índice de aristas: `sldb://semantic_tag/<tag>`
  (`src/sldb/store/edge_index/node_ids.py:38-40`).
- Dirección legacy: `se.<tag>`, y `gse.<tag>` entre stores enlazados
  (`docs/addressability_model.md:35-55`); solo existe bajo `sldb legacy`.
- `find <tag> --in semantic` lo busca como término (`src/sldb/cli/parsers/find.py:6-7`).

Con la gramática propuesta (borrador): `[store:]se/<tag.con.puntos>`
(`docs/architecture/one-address-grammar-two-spaces.md:55`). **Sin confirmar** que el namespace
`area:` y los puntos se escriban igual en esa forma.

## Dónde se guarda

El tag no tiene archivo propio. Se escribe por dos puertas, ambas de otro objeto:

- El código Python del modelo, `__semantics__`, que `flatten_model_semantics` aplana
  (`src/sldb/store/semantic_tags.py:4-19`).
- El Markdown del documento: campos `semantic_tags` y `tags` (`semantic_tags.py:29-35`); en las
  secciones, `semantic_tags` de la sección (`src/sldb/core/ir/section_context_entry.py:10`).

El nodo del tag en el DAG semántico (`nodes` con sus `parents`) vive solo en
`.sldb_cache/semantic_dag.yaml` (`src/sldb/store/layout.py:48-49`), que git ignora
(`.gitignore:21`). Es derivado: `sync_semantic_dag` lo agranda con los tags nuevos y sus prefijos
(`src/sldb/store/semantic_dag_sync.py:12-19`) y nunca quita un nodo. El detalle de los padres
declarados a mano está en `arista-semantic-parent.md`.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | no existe como comando. Un tag aparece al ponerlo en un documento, sección o modelo. Busqué en `src/sldb/cli/parsers/` (`semantic.py`, `tags.py`) y `src/sldb/api/semantic/`: no hay `tag add` ni `create` | `src/sldb/cli/parsers/semantic.py:11-18`, `src/sldb/cli/parsers/tags.py:19-36`, `src/sldb/store/semantic_dag_sync.py:22-45` | **Sin confirmar:** crear un tag es declararlo en el vocabulario sin que nadie lo lleve aún. |
| Leer | `sldb semantic show <tag>` (padres, hijos, ancestros, descendientes, equivalentes; falla si ningún documento o modelo lo lleva). `sldb tags tree <namespace>` solo para tags de un namespace declarado. `find <tag> --in semantic` lista lo que lo lleva | `src/sldb/api/semantic/dag_reads.py:13-30`, `src/sldb/cli/parsers/tags.py:24-28`, `src/sldb/cli/parsers/find.py:6-7` | Una sola lectura de `se/<tag>`: el tag, sus aristas y lo que lo lleva. **Sin confirmar.** |
| Cambiar | no existe. No hay renombrar tag. Busqué en `src/sldb/cli/` y `src/sldb/api/`. Renombrar hoy es editar cada documento y modelo | `src/sldb/cli/parsers/semantic.py:11-18` | **Sin confirmar:** cambiar un tag es renombrarlo en todo lo que lo lleva y en sus aristas. |
| Borrar | no existe. Quitar un tag de un documento es editar el campo `semantic_tags` de ese documento; el nodo queda en el DAG de la caché | `src/sldb/store/semantic_dag_sync.py:12-19` | **Sin confirmar:** borrar un tag lo quita de lo que lo lleva (ver Abierto). |

## Aristas que le llegan y que salen

- `tagged_as`: llega desde modelo, documento y sección. Las crea el índice de aristas al
  reconstruir, desde `__semantics__` y `semantic_tags`
  (`src/sldb/store/edge_index/model_contribution.py:28`, `doc_structure.py:17-19`).
- `semantic_parent`: sale hacia el padre y llega desde los hijos
  (`src/sldb/store/edge_index/store_contribution.py:27`).
- `semantic_equivalent`: sale hacia otro tag; el DAG guarda una dirección
  (`store_contribution.py:28-29`).

## Qué lo mantiene correcto

- `sldb tags check`: reglas `builtin:tag_namespace:*` sobre los documentos locales
  (`src/sldb/cli/parsers/tags.py:31-33`).
- `sldb edges check`: ciclos en `semantic_parent`
  (`src/sldb/store/edge_index/acyclic.py:13`, `src/sldb/api/edges/check_edges.py:33-34`).
- Una regla (`RuleDoc`) que nombra un tag desconocido se rechaza
  (`src/sldb/api/rules/rule_writes.py:28-38`).
- No hay hash ni procedencia del tag: es derivado.

## Decidido

JP, 2026-11-26: en esto se copia el comportamiento de kimun. Leído en `~/proyectos/kimun`
(`370beaff`), `src/kimun/surface/semantic.cljc:2-12` y `src/kimun/cli/commands/semantic.cljc:105`:

- Un tag es un término: existe porque algo lo lleva. No se crea ni se borra aparte. Los verbos
  crear y borrar de este nodo quedan como exención escrita del eje, no como celda vacía.
- Un tag desaparece cuando nada lo lleva. Quitarlo de lo que lo lleva es cambiar cada portador
  (borrar la arista `tagged_as`), no una operación sobre el tag.
- Los padres que salen de los puntos del nombre se derivan y nunca se guardan.
- Los padres y equivalencias declarados a mano son aristas guardadas en el store versionado, no
  en una caché. Eso corrige la pérdida que hoy tiene sldb (ver "Dónde se guarda").
- kimun tampoco tiene quitar una equivalencia (`parent-add`, `parent-remove`, `equivalent-add`):
  esa celda sigue faltando en los dos.

## Abierto

- Si renombrar un tag deja una equivalencia con el nombre viejo.
- Si el namespace (`area:`) es parte del nombre del tag o un atributo aparte.

## Fuentes

`docs/architecture/tags.md`, `docs/addressability_model.md`,
`docs/architecture/one-address-grammar-two-spaces.md`,
`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`,
`src/sldb/store/semantic_tags.py`, `src/sldb/store/semantic_dag_sync.py`,
`src/sldb/store/layout.py`, `src/sldb/store/edge_index/` (`records.py`, `node_ids.py`,
`doc_structure.py`, `model_contribution.py`, `store_contribution.py`, `acyclic.py`),
`src/sldb/api/semantic/`, `src/sldb/api/tags/`, `src/sldb/cli/parsers/semantic.py`,
`src/sldb/cli/parsers/tags.py`, `src/sldb/cli/parsers/find.py`.
