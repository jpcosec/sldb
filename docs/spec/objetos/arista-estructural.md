---
clase: objeto
tipo: arista
nombre: aristas estructurales
estado: borrador
---

# Aristas estructurales: `has_model`, `has_field`, `has_document`, `has_section`

## Qué es

Cuatro aristas que dicen de qué está hecho el store: el store tiene modelos, un modelo tiene
campos y documentos, un documento tiene secciones. Nadie las escribe. El índice las produce
cuando se crea o se borra el nodo del extremo, y se regeneran con `edges rebuild`. Son el
"esqueleto" del grafo: cada documento de un modelo queda a dos saltos de cualquier otro, por
eso los análisis las dejan fuera salvo que se pida (`src/sldb/store/graph/analysis/relations.py:3`).

## Cómo se nombra

Sin dirección propia: la terna de ids de nodo (`src/sldb/store/edge_index/node_ids.py:13-31`):

| Arista | Origen | Destino |
|---|---|---|
| `has_model` | `sldb://store` | `sldb://model/<Modelo>` |
| `has_field` | `sldb://model/<Modelo>` | `sldb://field/<Modelo>.<campo>` |
| `has_document` | `sldb://model/<Modelo>` | `sldb://document/<Modelo>:<doc>` |
| `has_section` | `sldb://document/<Modelo>:<doc>` | `sldb://section/<Modelo>:<doc>#<ruta>` |

Con la gramática propuesta (borrador) serían los hijos en el árbol de contención:
`st/<Modelo>`, `st/<Modelo>/@<campo>`, `st/<Modelo>/<doc>`, `st/<Modelo>/<doc>#<sección>`
(`docs/architecture/one-address-grammar-two-spaces.md`). La arista `has_*` sería entonces la
relación entre una dirección y su prefijo, que ya está implícita en la dirección.

## Dónde se guarda

Es derivada y nadie la escribe; la fuente de cada una es otra cosa:

- `has_model`: la lista `models` de `.sldb/core/store_index.yaml`
  (`src/sldb/store/edge_index/store_contribution.py:24`).
- `has_field`: la clase Python del modelo (`model_type.model_fields`), no un archivo de datos
  (`src/sldb/store/edge_index/model_contribution.py:31`).
- `has_document`: los documentos que el modelo tiene en su índice (`doc_structure.py:15`).
- `has_section`: los encabezados del Markdown del documento, vistos como registros de sección
  (`doc_structure.py:16`, `src/sldb/store/section_rebuild.py:87`).

La caché es `.sldb_cache/edges/`. Una nota: el campo `origin` de la arista no es el mismo en
las cuatro. `has_model`, `has_document` y `has_section` llevan `structural`; `has_field` lleva
`schema` (`model_contribution.py:31`), igual que `extends`, `contains` y `references`.

## Los cuatro verbos

Qué significa un verbo en una arista que no se escribe. Propuesta, **sin confirmar**: crear,
cambiar y borrar actúan sobre el nodo del extremo, y la arista aparece o desaparece como
consecuencia. Leer actúa sobre la arista.

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `has_model`: `models add`, `models create`. `has_field`: `models fields add` escribe un borrador, que pasa al modelo con `models validate --promote`. `has_document`: `docs create`, `docs track`. `has_section`: no existe comando, nace al escribir un encabezado; buscado en `sections` (solo `show`, `find`, `fields`) | `src/sldb/cli/parsers/models1.py:13`; `src/sldb/cli/commands/models_fields.py:21`; `src/sldb/cli/parsers/models2.py:13`; `src/sldb/cli/parsers/docs1.py:13`; `src/sldb/cli/parsers/sections.py:10`, `:17`, `:28` | **Sin confirmar:** crear el nodo del extremo (modelo, campo, documento, encabezado) crea su arista. |
| Leer | `edges show <nodo>`, `edges show --to`, `graph get/list/neighborhood`; `models show`, `docs list`, `sections show` | `src/sldb/cli/commands/edges.py:30`; `src/sldb/cli/parsers/graph.py:30`, `:46` | **Sin confirmar:** dar los hijos de un nodo, o su padre con `--to`. |
| Cambiar | no existe para ninguna: no hay verbo que mueva un campo de un modelo a otro ni un documento a otro modelo | buscado en `src/sldb/cli/parsers/` y `src/sldb/api/edges/` | **Sin confirmar:** cambiar el extremo sería cambiar de nodo, no de arista; queda sin sentido propio. |
| Borrar | `models remove` (quita `has_model` y sus documentos con `--with-documents`); `docs untrack`, `docs delete`; `models fields remove` (borrador); un encabezado no tiene comando | `src/sldb/cli/parsers/models1.py:26`; `src/sldb/cli/parsers/docs1.py:47`; `models2.py:55` | **Sin confirmar:** borrar el nodo borra su arista; no hay "desenlazar" sin borrar. |

## Aristas que le llegan y que salen

- `has_model` sale del nodo del store. Un modelo heredado de un store enlazado lleva
  `origin_store` (`store_contribution.py:33`).
- `has_document` y `has_field` salen del modelo; `has_section` del documento.
- Cada una es un `RelationTypeDoc` incluido por sldb y que `edges init` registra
  (`src/sldb/models/builtin_relation_types.py:16`, `:18`, `:19`, `:23`). Cardinalidad: `has_document`,
  `has_section` y `has_field` son `one_to_many`; `has_model` es `many_to_many`.

## Qué lo mantiene correcto

- `edges check` valida clases de extremo y cardinalidad contra la definición propia de sldb
  (`src/sldb/store/edge_index/validation.py:62`, `:105`).
- `edges rebuild` y el hash del documento (`hash_c`/`source_hash`) deciden qué se regenera
  (`src/sldb/store/edge_sync.py:28`).
- Las secciones se recalculan desde el Markdown. `SectionContextRecord` no tiene campo de hash
  (`src/sldb/store/models/section_context_record.py:4`).

## Abierto

- ¿Estas cuatro son aristas o la jerarquía del árbol de contención escrita dos veces (en la
  dirección y en la arista)? Decide si quedan en el índice.
- `has_field` lleva `origin: schema` y las otras `structural`: ¿se unifican?
- Un nodo sin verbo para su arista (sección, campo): ¿se puede crear una sección que no esté en el
  texto, o la sección siempre es una consecuencia del texto?

## Fuentes

`src/sldb/store/edge_index/` (`store_contribution.py`, `model_contribution.py`, `doc_structure.py`,
`node_ids.py`, `validation.py`), `src/sldb/store/section_rebuild.py`, `edge_sync.py`;
`src/sldb/models/builtin_relation_types.py`; `src/sldb/cli/commands/models_fields.py`;
`src/sldb/cli/parsers/models1.py`, `models2.py`, `docs1.py`, `sections.py`, `graph.py`;
`src/sldb/store/graph/analysis/relations.py`; `docs/architecture/one-address-grammar-two-spaces.md`.
