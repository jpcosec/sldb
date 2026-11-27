---
clase: objeto
tipo: arista
nombre: enlace en el texto
estado: borrador
---

# Enlace en el texto

## Qué es

Una referencia escrita dentro del Markdown de un documento, no en un campo. Hay tres formas:
`[[destino]]`, `[predicado:: [[destino]]]` (un enlace con tipo) y `![[doc]]` o `![[doc#Sección]]`
(transclusión: pide copiar el contenido). Se leen del texto, fuera de bloques y líneas de código
(`src/sldb/links/parser.py:7`, `:8`, `scan_text.py:64`). El destino puede ser un documento
rastreado o una ruta, con `#Sección` opcional (`src/sldb/links/resolver.py:58`).

Hallazgo verificado: estos enlaces NO entran al índice de aristas (ver "Qué lo mantiene
correcto"). Son una cosa aparte de las demás aristas. Si el dueño decide que son aristas, esta
página pasa a describir cómo se convierten; hoy no se convierten.

## Cómo se nombra

El destino se escribe como el nombre de un documento rastreado, o como ruta relativa al documento
o al proyecto, más `#Encabezado` para una sección (`resolver.py:59-61`,
`src/sldb/links/sections.py:30`). El resolvedor busca por `name` entre los documentos del store local (`resolver.py:20`) y por ruta
(`resolver.py:60-61`); no hay código que interprete `Model:name` ni `alias:Model:name`. El predicado va antes de
`::` y debe ser `[A-Za-z0-9_-]+` (`parser.py:8`).
Con la gramática propuesta (borrador) el destino sería una dirección `[store:]st/<Modelo>/<doc>[#sección]`;
hoy no hay forma de enlazar a un documento de un store enlazado ni a un valor.

## Dónde se guarda

En el cuerpo Markdown del documento que enlaza. No hay copia en el índice de aristas, ni en
`.sldb_cache/edges/`: se vuelve a leer del archivo cada vez (`src/sldb/links/recovery.py:24`).

Los tres vocabularios del tipo de enlace viven en lugares distintos:

| Vocabulario | Dónde vive | Para qué lo usa el código |
|---|---|---|
| `predicates` | `.sldb/store.yaml` (`predicates:`, línea 136) y su copia derivada `.sldb/core/store_index.yaml` | El único que leen los enlaces del texto: da el eje (`w5h1_type`) del predicado; uno ausente es `CUSTOM` (`src/sldb/links/parser.py:12`, `recovery.py:25`, `src/sldb/store/predicates.py:55`) |
| `RelationTypeDoc` | un documento del store, modelo `RelationTypeDoc` | Tipo de las aristas del índice (autoradas y propias de sldb); su `axis` dice que se registra como predicado (`src/sldb/models/relation_type_doc.py:59`), pero el código solo registra los builtin (`src/sldb/api/edges/builtin_relation_writes.py:73`) |
| Atributos del modelo | `__references__`, `__containment__`, `__compositions__` en el código Python del modelo | Dan el tipo `references`, `contains` o `composes` de un campo (`src/sldb/store/edge_index/declared_references.py:38`) |

Los predicados se alimentan por `predicates add/sync`, por `stores declare/build`
(`src/sldb/api/stores/apply_declaration.py:71`), por los siete por defecto
(`src/sldb/store/predicates.py:12`) y por `edges init` para los tipos builtin.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | Escribir el texto en el documento (`docs update`, `docs replace`, editor). No hay comando que cree un enlace | `src/sldb/cli/parsers/docs1.py:33`; buscado en `src/sldb/cli/parsers/` | **Sin confirmar:** escribir un enlace en el cuerpo, con destino y tipo opcional. |
| Leer | `docs recover` (un documento o `--all`) resuelve y marca cada enlace; `docs compose` expande `![[…]]`; `docs compose --render-links` lo convierte en `[título](ruta)`; en `serve`, `/lint` lista los no resueltos | `src/sldb/cli/commands/links.py:18`, `:53`; `src/sldb/links/render.py`; `src/sldb/cli/serve/lint_routes.py:58` | **Sin confirmar:** listar los enlaces de un documento con su destino resuelto. |
| Cambiar | `move` reescribe solo enlaces `[texto](ruta)` de Markdown al mover un archivo. `edges rewrite` no toca `[[…]]`: reescribe campos y menciones del grafo de proyecto | `src/sldb/api/documents/move_path_links.py:16`; `src/sldb/api/edges/rewrite_values.py:30` | **Sin confirmar:** cambiar el destino o el tipo de un enlace; hoy es editar el texto. |
| Borrar | Borrar el texto. Sin comando | buscado en `src/sldb/cli/parsers/` | **Sin confirmar:** quitar el enlace sin tocar el resto del párrafo. |

## Aristas que le llegan y que salen

Ninguna en el índice. El grafo de proyecto (`graph project`) captura otra cosa: menciones por
expresión regular (`MentionPattern`, `src/sldb/api/edges/project_graph/mention_pattern.py:11`),
configuradas en `store.yaml`, que no son `[[…]]`. `edges referrers` y `edges rewrite` juntan
campos declarados y esas menciones (`src/sldb/api/edges/referrers.py:1`).

Un segundo lector de `[[id]]` existe fuera de `src/sldb/links/`:
`src/sldb/api/matching/explicit_atoms.py:16` busca `[[id]]` en el cuerpo de los átomos para
enlazar átomos de un spec, un nivel. Tampoco produce aristas.

## Qué lo mantiene correcto

Evidencia de que no entran al índice:

- Los módulos del índice (`src/sldb/store/edge_index/`), `edge_sync.py` y `src/sldb/api/edges/` no
  importan `sldb.links` ni `parse_links`: `grep` de `sldb.links|parse_links|LINK_PATTERN` en
  `src/sldb/store`, `src/sldb/api`, `src/sldb/core` y `src/sldb/mcp` no da resultados de esa
  clase (solo `explicit_atoms.py:16`).
- Los únicos importadores de `sldb.links` son `cli/commands/{docs,docs_batch,legacy,links,links_all}.py`
  y `cli/serve/lint_routes.py`. `docs_batch.py:10` solo usa `tracked_documents`, no el parser.
- La contribución de un documento al índice (`doc_contribution.py:19`) arma nodo, secciones,
  etiquetas y referencias declaradas por el modelo (`doc_structure.py`, `declared_references.py`):
  no lee el cuerpo del texto.

Lo que sí revisa: `docs recover --all` y `GET /lint` informan enlaces `unresolved` y predicados
`custom` (`src/sldb/links/audit.py:7-9`). El comando `lint` de la CLI no revisa `[[…]]`: solo
rutas canónicas (`src/sldb/cli/commands/lint.py:1`).

## Decidido

JP, 2026-11-26: un enlace del texto es una relación más. Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`. Queda por escribir cómo entra al índice.

## Abierto

- ¿Un enlace del texto es una arista más (entra al índice, con tipo y extremos) o una cosa
  distinta de la arista (una mención que se resuelve al leer)?
- ¿Cuál de los tres vocabularios de tipo de enlace queda: `predicates` del store, `RelationTypeDoc`
  o los atributos del modelo? Hoy `implements` es un predicado por defecto (`src/sldb/store/predicates.py:14`) y también el
  ejemplo de nombre de `RelationTypeDoc` (`relation_type_doc.py:47`): dos vocabularios para lo mismo.
- Si es arista: ¿el enlace con tipo `[implements:: [[x]]]` es una arista autorada o una
  referencia declarada?

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es una relación más (JP), que sale de un nodo del AST del texto.

## Fuentes

`src/sldb/links/` (`parser.py`, `scan_text.py`, `resolver.py`, `recovery.py`, `audit.py`,
`composer.py`, `render.py`, `sections.py`); `src/sldb/cli/commands/links.py`, `links_all.py`,
`docs_batch.py`, `lint.py`; `src/sldb/cli/serve/lint_routes.py`;
`src/sldb/cli/commands/predicates.py`; `src/sldb/store/predicates.py`;
`src/sldb/api/documents/move_path_links.py`; `src/sldb/api/matching/explicit_atoms.py`;
`src/sldb/store/edge_index/doc_contribution.py`; `docs/architecture/references.md`,
`segments-and-transclusion.md`; `desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`.
