---
clase: objeto
tipo: nodo            # nodo | arista
nombre: nodo-seccion
estado: borrador
---

# Sección

## Qué es

Una sección es un encabezado Markdown de un documento, con el texto hasta el siguiente
encabezado de su nivel o superior. Es un nodo derivado: sldb la calcula leyendo el archivo
del documento, sea o no que el modelo la declare. Sirve para nombrar y buscar un tramo del
documento (`sections find`, `sections fields`) y para colgarle tags.

## Cómo se nombra

- Camino de slugs desde el encabezado raíz, por ejemplo `contexto/alcance`. Un slug repetido
  entre hermanos lleva `-2`, `-3` (`src/sldb/store/section_paths.py:13-31`; el slug sale de
  `_slugify`, `src/sldb/store/section_rebuild.py:12`).
- Id de grafo `sldb://section/Modelo:nombre#camino` (`src/sldb/store/edge_index/node_ids.py:23`).
- En la CLI, `docs/<Doc>/<camino>` en `sections fields`
  (`src/sldb/cli/commands/sections_fields.py:18`).
- Con la gramática propuesta (borrador): `[store:]st/<Modelo>/<doc>#<seccion>`.

El camino cambia si cambia el texto del encabezado: la dirección de una sección no es estable
(lo reconoce `docs/architecture/one-address-grammar-two-spaces.md`, "Not solved by this").

## Dónde se guarda

No se escribe. Se reconstruye a partir del Markdown, que es lo que sí se escribe. El resultado
queda en shards por documento (`src/sldb/store/layout.py:75,90`) y en el índice de aristas.
La reconstrucción se salta un modelo si su `model_hash` no cambió y solo relee los documentos
sucios (`src/sldb/store/section_sync.py:24-61`). La versión de las reglas de identidad es
`SECTION_INDEX_VERSION` (`src/sldb/store/section_paths.py:4`).

Qué guarda por sección: `path`, `title`, `breadcrumbs`, `about`, `semantic_tags`, `slug`,
`level`, `line_start`, `line_end` (`src/sldb/store/models/section_context_record.py:4-13`). Los
tags de una sección son los de su documento, copiados (`src/sldb/store/section_rebuild.py:87`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | No existe. Busqué en los parsers de `sections` (solo `show`, `find`, `fields`), en `src/sldb/api/` (ninguna función de sección) y en la ruta HTTP `/sections` (solo lectura). Lo único que crea una sección es escribir un encabezado en el Markdown | `src/sldb/cli/parsers/sections.py:4-30`, `src/sldb/cli/serve/routes.py:102` | **Sin confirmar:** crear una sección es agregar un encabezado, y qué cuerpo lleva depende de lo que el modelo declare (ver Abierto) |
| Leer | `sections show <doc>`, `sections find <término>`, `sections fields docs/<Doc>/<camino>` | `src/sldb/cli/commands/sections_show.py:13`, `sections_find.py:9`, `sections_fields.py:13` | **Sin confirmar:** leer es resolver una dirección de sección y devolver título, camino, tramo de líneas y valores que contiene |
| Cambiar | No existe, mismas búsquedas. Cambiar el texto de un encabezado (por ejemplo con `docs replace`) cambia el camino y por tanto la dirección | `src/sldb/cli/commands/docs_replace.py:17`, `src/sldb/store/section_rebuild.py:32-38` | **Sin confirmar:** cambiar es reescribir su título o su cuerpo; cambiar el título equivale a renombrar |
| Borrar | No existe, mismas búsquedas | `src/sldb/cli/parsers/sections.py:4-30` | **Sin confirmar:** borrar es quitar el encabezado y su cuerpo del documento |

Sobre el registro de ejes: la fila de sección ("crear, cambiar y borrar: —", leer con
`sections show`) es correcta. Además `sections find` y `sections fields` también leen.

Qué limita crear hoy. Aunque se pudiera escribir un encabezado, el store rechaza:

- un documento nuevo (`docs create`, `docs track`) con encabezados que el modelo no declara,
  salvo que la política lo permita (`src/sldb/api/documents/refuse_structural_noise.py:17`);
- una escritura de campo que haga perder un encabezado no declarado
  (`src/sldb/api/documents/lossy_overwrite.py:18`).

## Aristas que le llegan y que salen

- Llega `has_section` desde su documento, estructural
  (`src/sldb/store/edge_index/doc_structure.py:16`).
- Sale `tagged_as` hacia los tags heredados del documento (`doc_structure.py:19`).
- Ninguna arista escrita (`RelationDoc`, `references`) llega hoy a una sección: terminan en
  documentos (`src/sldb/store/edge_index/doc_kinds.py:52-58`). Que puedan terminar en una
  sección lo fijó el dueño.

## Qué lo mantiene correcto

- La sección es derivada, así que no hay nada que validar en ella: se reconstruye tras cada
  escritura de documento (`src/sldb/api/documents/payload_save_steps.py:112`) y tras
  `stores update`.
- No hay hash por sección. Los hashes son del documento y por campo (`src/sldb/store/hashing.py:10-24`),
  de modo que una sección no puede ser destino de un ancla con huella (ver `nodo-ancla`).
  Coincide con el registro de ejes.
- El único control sobre qué secciones puede tener un documento es el del ruido estructural,
  citado arriba.

## Abierto

1. ¿Qué es crear una sección en un documento cuyo modelo no la declara? Hay al menos tres
   lecturas: (a) no se puede, porque el ruido estructural lo rechaza; (b) se puede solo en
   modelos narrativos o `authored`, donde la política ya permite ruido; (c) crear una sección
   obliga a declarar antes un campo en el modelo.
2. ¿Cambiar una sección es cambiar su cuerpo, su título (y con él su dirección) o también
   moverla de lugar en el documento?
3. ¿Borrar una sección borra también las secciones hijas, o falla si las tiene?
4. ¿La identidad de una sección es su camino de slugs, aunque se rompa al renombrar, o debe
   tener un id estable aparte?
5. ¿Los tags de una sección son siempre los de su documento, o una sección puede tener los
   suyos?

## Fuentes

`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`,
`desk/drawer/plans/spec-de-producto-de-sldb/README.md`,
`docs/architecture/one-address-grammar-two-spaces.md`, `docs/addressability_model.md`;
`src/sldb/cli/parsers/sections.py`, `src/sldb/cli/commands/sections*.py`,
`src/sldb/cli/serve/routes.py`, `src/sldb/store/section_rebuild.py`,
`src/sldb/store/section_sync.py`, `src/sldb/store/section_paths.py`,
`src/sldb/store/models/section_context_record.py`, `src/sldb/store/edge_index/doc_structure.py`,
`src/sldb/store/edge_index/node_ids.py`, `src/sldb/api/documents/refuse_structural_noise.py`,
`src/sldb/api/documents/lossy_overwrite.py`.
