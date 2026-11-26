---
clase: objeto
tipo: valor
nombre: valor-en-un-documento
estado: borrador
---

# Valor en un documento

## Qué es

Un valor en un documento no es un nodo propio del grafo: es el documento más una ruta en sus
campos (`one-address-grammar-two-spaces.md`, decisión 3). El valor puede ser un campo entero,
una clave de un campo con subcampos, un elemento de una lista o una celda de una tabla. Se
lee y se escribe siempre a través de su documento: sldb cambia el valor en el payload, vuelve
a renderizar el Markdown completo y comprueba que el resultado se extrae igual.

## Cómo se nombra

- En la CLI de `fields`: `docs/<Doc>/<campo>[/<sub>...]` o `docs/<Modelo>/<Doc>/<campo>...`;
  las barras se vuelven la ruta con puntos del payload (`src/sldb/cli/commands/fields_target.py:13,35`).
- En `sldb legacy`: `st.{Modelo}.<doc>.<campo>.<sub>`, con índices numéricos para listas
  (`docs/addressability_model.md`).
- En las composiciones de campo: `Modelo:nombre#campo` y `docs/<Modelo>/<nombre>/<campo>`
  (`docs/architecture/segments-and-transclusion.md`, "Field Transclusion").
- No tiene id de grafo: los ids `sldb://` llegan hasta el documento y la sección
  (`src/sldb/store/edge_index/node_ids.py:18-23`).
- Con la gramática propuesta (borrador): `[store:]st/<Modelo>/<doc>/<campo>/<sub>...`, el
  documento más un fragmento.

La posición de un elemento de lista cambia si se inserta otro antes
(`one-address-grammar-two-spaces.md`, "Not solved by this").

## Dónde se guarda

En el Markdown del documento, en el lugar que la plantilla del modelo asigna al campo. Nada
lo guarda aparte. Lo único derivado es el hash por campo: un hash por campo de primer nivel
(`src/sldb/store/hashing.py:24`), guardado en `field_hashes` del shard del documento
(`src/sldb/store/models/document_entry.py:17`). Un subcampo o un elemento no tiene hash propio.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `fields create <ruta> <valor>`: asigna el valor y crea las claves intermedias. `fields append`: agrega un elemento al final de una lista | `src/sldb/cli/parsers/fields.py:24-34`, `src/sldb/cli/commands/fields_mutate.py:18,21`, `src/sldb/api/documents/payload_path_writing.py:48-67` | **Sin confirmar:** crear es dar valor a algo que no lo tenía; si ya lo tenía debería fallar |
| Leer | `fields show docs/<Doc>/<ruta>`, `fields query <ruta>` (en todos los documentos), `sections fields docs/<Doc>/<sección>` (los valores que posee una sección) | `src/sldb/cli/commands/fields_show.py:45-47,55`, `src/sldb/cli/commands/sections_fields.py:13` | **Sin confirmar:** leer es resolver la dirección y devolver el valor; con posición exacta en el texto cuando se pide |
| Cambiar | `fields update <ruta> <valor>`: la ruta debe existir (salvo un campo de primer nivel del modelo que falte). `fields clean --dedupe --drop-empty`: depura una lista | `src/sldb/cli/commands/fields_mutate.py:19,22,24-26` | **Sin confirmar:** cambiar es reemplazar el valor existente por otro del mismo tipo |
| Borrar | `fields remove <ruta>` | `src/sldb/cli/commands/fields_mutate.py:20`, `src/sldb/api/documents/payload_path_writing.py:80` | **Sin confirmar:** borrar es dejar el valor vacío o ausente, si el modelo lo permite |

Cómo se aplican los cuatro: `mutate_field` carga el payload, aplica el cambio y llama a
`save_document_payload` (`src/sldb/cli/commands/fields_mutate.py:8-12`,
`src/sldb/cli/commands/fields_save.py:12`). Por eso un cambio de valor reescribe el documento
entero y mueve su `source_hash`.

Lo que verifiqué:

- `fields create` y `fields update` no se distinguen como "crea" y "cambia": `create` usa
  `deep_set(create=True)`, que asigna aunque la clave exista (`fields_mutate.py:18` y
  `payload_path_writing.py:35-41`), así que `create` sobre un valor existente lo pisa en
  silencio. `update` sí falla si la ruta no existe.
- `fields show` sobre `models/<Modelo>[/campo]` lee el esquema del modelo, no un valor
  (`src/sldb/cli/commands/fields_show.py:10-14`); `fields create/update/remove/append`, en
  cambio, solo aceptan `docs/...` (`fields_target.py:13-17`), no `models/...`. El registro de
  ejes pone `fields create` como "crear valor": es correcto, pero la ayuda dice "Field CRUD"
  sin separar los dos mundos.
- Los valores con posición exacta en el texto (segmentos) solo salen por la API
  (`src/sldb/api/segments/build_document_segments.py:16`) y por `sldb serve`
  (`src/sldb/cli/serve/routes.py:122`); no hay comando de CLI.
- Sin verificar: qué pasa al crear con `fields create` una clave que el modelo no declara
  (el render puede descartarla o el round trip puede fallar).

## Aristas que le llegan y que salen

- Un valor no es extremo de ninguna arista hoy. Que una arista pueda terminar en un valor lo
  fijó el dueño; no existe: las aristas escritas van de documento a documento
  (`src/sldb/store/edge_index/doc_kinds.py:52-58`).
- Un campo es el origen de una arista declarada: `references`, `contains` y `composes` salen
  de los campos que el modelo marca (`src/sldb/store/edge_index/declared_references.py:38`),
  y `references` sale de cada campo `__doc_anchors__`
  (`src/sldb/store/edge_index/doc_anchor_edges.py:17`). La arista parte del documento y
  recuerda el nombre del campo; `edges referrers` los lista como "declared fields (scalar or
  list element)" (`src/sldb/cli/parsers/edges.py:26`).

## Qué lo mantiene correcto

- Validación del modelo (pydantic) y round trip al escribir
  (`src/sldb/api/documents/payload_save_steps.py:58`).
- Forma de los valores que son anclas a documento: validadores del modelo base y de la
  procedencia (`src/sldb/models/structured_doc.py:25`, `src/sldb/models/provenance.py:36`).
- Fijado de anclas sin huella al guardar (`src/sldb/api/documents/doc_anchor_pinning.py:19`).
- Reglas `on_write` y guarda contra pérdida de encabezados (`src/sldb/api/rules/rules_on_write.py:33`,
  `src/sldb/api/documents/lossy_overwrite.py:18`).
- Hash por campo, para saber qué campo se movió en `stores check` (`src/sldb/store/hashing.py:24`).

## Abierto

1. ¿Qué es crear un valor en un campo que el modelo no declara: error, o declarar el campo?
   Y si el campo existe pero está vacío, ¿crear y cambiar son lo mismo?
2. ¿Borrar un valor que el modelo exige es un error, restablece el valor por defecto o es
   borrar el documento?
3. ¿Se direcciona un elemento de lista por posición o por una clave estable (por ejemplo un
   campo identificador del elemento)?
4. ¿Cambiar un valor a este nivel debe poder expresarse sin reescribir el documento entero,
   o es siempre una operación del documento?

## Fuentes

`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`,
`desk/drawer/plans/spec-de-producto-de-sldb/README.md`,
`docs/architecture/one-address-grammar-two-spaces.md`, `docs/addressability_model.md`,
`docs/architecture/segments-and-transclusion.md`;
`src/sldb/cli/parsers/fields.py`, `src/sldb/cli/commands/fields*.py`,
`src/sldb/cli/commands/sections_fields.py`, `src/sldb/api/documents/payload_path_writing.py`,
`src/sldb/api/documents/payload_save.py`, `payload_save_steps.py`, `doc_anchor_pinning.py`,
`src/sldb/api/segments/`, `src/sldb/store/hashing.py`, `src/sldb/store/edge_index/`,
`src/sldb/models/structured_doc.py`, `src/sldb/models/provenance.py`.
