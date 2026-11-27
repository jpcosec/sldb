---
clase: objeto
tipo: nodo            # nodo | arista
nombre: nodo-documento
estado: borrador
---

# Documento

## Qué es

Un documento es un archivo Markdown que un modelo describe y que el store rastrea. El store
guarda de él su nombre, su ruta, sus hashes, sus tags y su procedencia, y deriva su nodo en el
grafo, sus secciones y sus aristas. Es el nodo central: las secciones y los valores se
nombran a partir de él, y casi todas las aristas escritas terminan en un documento.

## Cómo se nombra

Hoy hay varias escrituras, ninguna cubre todo:

- Nombre, `Modelo/nombre`, `Modelo:nombre` o ruta rastreada: lo que aceptan `docs show`, `docs
  update`, `docs delete` y `docs exists` (`src/sldb/cli/parsers/docs1.py:53-65`); `alias:ref`
  llega a un store enlazado. Lo resuelve `doc_status` (`src/sldb/api/stores/doc_status.py:18`).
- `docs/<Doc>` y `docs/<Modelo>/<Doc>/...`: las usan `fields` y `sections`
  (`src/sldb/cli/commands/fields_target.py:13`).
- Id de grafo `sldb://document/Modelo:nombre`, y `store:Modelo:nombre` si es de un store
  enlazado (`src/sldb/store/edge_index/node_ids.py:18`).
- `st.{Modelo}.doc` en `sldb legacy` (`docs/addressability_model.md`).

Con la gramática propuesta (borrador) es `[store:]st/<Modelo>/<doc>`, y es también el id del
nodo (`docs/architecture/one-address-grammar-two-spaces.md`, decisión 2 y 3).

## Dónde se guarda

- El contenido: el archivo Markdown, en la ruta del proyecto. Lo escribe el usuario o sldb.
- El registro: un shard por documento en `.sldb/core/documents/<Modelo>/<nombre>.yaml`
  (`src/sldb/store/layout.py:132`) con `source_hash`, `content_hash`, `field_hashes`, tags y
  procedencia (`src/sldb/store/models/document_entry.py:6-21`).
- La lista de archivos del store: `.sldb/store.yaml`, que `track` y `untrack` mantienen
  (`src/sldb/api/stores/declaration_sync.py`).
- Derivado, nadie lo escribe: secciones, índice de aristas y DAG semántico.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `docs create`: escribe un Markdown nuevo desde un payload y lo rastrea; sobrescribe el archivo si existe. `docs track`: rastrea un Markdown que ya existe (`--glob`, `--force`, `--reindex`) y no lo reescribe | `src/sldb/cli/parsers/docs1.py:12-30`, `src/sldb/cli/commands/doc.py:45,50`, `src/sldb/api/documents/create_document.py:26,33`, `src/sldb/api/documents/track_document_file.py:22` | **Sin confirmar:** crear es que un documento entre: marcar lo que se toma de él. No exige modelo ni que sea "válido"; `create` y `track` son dos caminos a ese efecto. (corregido 2026-11-27 con los fundamentos) |
| Leer | `docs show` (AST y payload), `docs list`, `docs exists`, `docs select`, `docs history`, `docs compose` | `src/sldb/cli/commands/docs.py:40,45,50`, `docs_exists.py:14`, `docs_select.py:15`, `docs_history.py:11` | **Sin confirmar:** leer es una dirección, o una consulta, que devuelve el documento |
| Cambiar | `docs update`: reemplaza el payload entero. `docs replace`: cambia exactamente N apariciones de un texto literal (también en archivos no rastreados). `sldb move`: mueve archivo o directorio y reescribe campos y enlaces. `fields *` cambia un valor (ver `valor-en-un-documento`) | `src/sldb/cli/commands/doc.py:63`, `docs_replace.py:17` y `src/sldb/api/documents/replace_text.py:34`, `src/sldb/cli/commands/move.py:13` y `src/sldb/api/documents/move_path.py:14` | **Sin confirmar:** cambiar es dejar el documento con otro contenido o en otra ruta, conservando su nombre |
| Borrar | `docs untrack`: lo saca del store y deja el archivo. `docs delete`: lo saca y borra el archivo; pregunta salvo `--yes` | `src/sldb/cli/commands/doc.py:90,95`, `src/sldb/api/documents/untrack_document.py:29`, `src/sldb/api/documents/delete_document.py:12,35` | **Sin confirmar:** borrar no existe adentro: es declarar que el documento ya no está o ya no se sigue. El nodo y sus relaciones quedan dichos; el archivo es cosa de afuera. (corregido 2026-11-27 con los fundamentos) |

Lo que verifiqué y no coincide con el registro de ejes:

- No existe `docs move`. El parser de `docs` no lo declara (`src/sldb/cli/parsers/docs1.py`,
  `docs2.py`, `docs3.py`). Lo que existe es `sldb move`, de otro nivel (`src/sldb/cli/parsers/project.py:18`).
  `move_document` (cambia la ruta y conserva el nombre) solo está en la API y en las
  transacciones (`src/sldb/api/documents/move_document.py:18`, `transaction_ops.py:47`).
- `docs update` no pasa por `save_document_payload`, que usan `fields`, las transacciones y
  `anchors`. `docs update` valida el round trip y la familia, pero no corre las reglas
  `on_write`, ni la guarda contra pérdida de encabezados, ni fija las anclas a documento
  (`src/sldb/cli/commands/doc.py:63-73` contra `src/sldb/api/documents/payload_save.py:48-56`).
  Dos comandos que cambian un documento dan garantías distintas.
- `docs delete` pide confirmación y `docs untrack` no, aunque los dos quitan el nodo.

## Aristas que le llegan y que salen

- `has_document`: del modelo al documento. `has_section`: del documento a cada sección.
  `tagged_as`: del documento a sus tags. Son estructurales y salen del índice al reconstruirlo
  (`src/sldb/store/edge_index/doc_structure.py:15-17`).
- `references`, `contains`, `composes`: salen de los atributos del modelo
  (`src/sldb/store/edge_index/declared_references.py:38`).
- `references` desde un campo `__doc_anchors__` (`src/sldb/store/edge_index/doc_anchor_edges.py:17`).
- Las aristas escritas con `RelationDoc` (`implements` y otras) van de un documento a otro:
  `source_id` y `target_id` se vuelven ids de documento
  (`src/sldb/store/edge_index/doc_kinds.py:52-58`).
- Que una arista termine en una sección o en un valor lo fijó el dueño; hoy no existe.

## Qué lo mantiene correcto

- Round trip bajo el modelo al escribir (`src/sldb/api/documents/payload_save_steps.py:58`).
- Ruido estructural: encabezados que el modelo no declara se rechazan al crear o rastrear,
  salvo que la política del store lo permita (`src/sldb/api/documents/refuse_structural_noise.py:17`).
- Guarda contra sobrescritura con pérdida (`src/sldb/api/documents/lossy_overwrite.py:18`).
- Reglas `on_write` (`src/sldb/api/rules/rules_on_write.py:33`).
- Hashes de archivo, de contenido y por campo (`src/sldb/store/hashing.py:10-24`) y
  `stores check`, que los recorre.
- Procedencia: cada escritura firma el bloque `sldb:` (`payload_save_steps.py:83`).
- Guarda de lectura y escritura: no se sigue un symlink ni una ruta fuera de la raíz
  (`src/sldb/store/source_guard.py:66`, `src/sldb/store/source_read.py:64`).

## Abierto

1. ¿Qué identifica a un documento: su nombre o su ruta? Hoy el nombre es el de la ruta si no
   se da otro, y mover conserva el nombre.
2. ¿`create` sobre un archivo que existe es un error o una sobrescritura permitida? Hoy
   sobrescribe.
3. ¿Mover un documento es "cambiar" o una operación aparte con su propio verbo?
4. ¿Borrar un documento incluye su archivo por defecto, o es `untrack` el borrado y el archivo
   se queda?
5. ¿Cambiar un documento es siempre reemplazar el payload entero, o también admite un parche
   por campo a este nivel?

## Desde los fundamentos

- **Qué es.** Un documento marcado por completo: vive adentro como un nodo con los nodos que se
  tomaron de él. Su archivo sigue siendo un archivo común. Proyectar sus nodos por la estructura
  que tenía devuelve el archivo.
- **De qué principio cuelga.** 3 (adentro y afuera; entrar y proyectar) y 5 (el modelo sale de lo
  que varios documentos comparten, no al revés).
- **Qué contradice los niveles 1 y 2.**
  - (h) "Un documento es un archivo Markdown que un modelo describe y que el store rastrea": define
    todo por el archivo y por el modelo. Para el nivel 2 el archivo está afuera y el documento es
    lo que entró.
  - (c) "que un modelo describe": un documento sin modelo no queda fuera, es un árbol de partes.
  - (a) Borrar: "`docs delete`", "`docs untrack`" y "quita el nodo y sus aristas". Adentro no se
    borra; Abierto 4 (si borrar incluye el archivo) mezcla afuera y adentro.
  - (b) Abierto 1 ("¿Qué identifica a un documento: su nombre o su ruta?"): la identidad es del
    nodo; la ruta es dónde estaba. Mover cambia el "dónde", no el nodo.
  - (g) "Dónde se guarda": el contenido en el archivo, los hashes en `.sldb/`. Sobre lo observado
    manda el archivo; lo declarado (tags, procedencia) vive adentro.
  - (d) "El store guarda su nombre, su ruta, sus hashes": falta que el nodo lleva su contenido.
  - Abierto 2 (sobrescribir con `create`): una edición se aplica sobre la versión vista y muestra
    el choque; el nivel 2 ya lo decide.
- **Qué queda igual.** Que es el nodo desde el cual se nombran secciones y valores, la guarda
  contra pérdida, el round trip, la procedencia por escritura y los hashes de contenido.

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Un documento entra siempre como AST, nunca crudo (JP). Es el nodo raíz de ese árbol; lo demás está metido adentro.

## Fuentes

`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`,
`desk/drawer/plans/spec-de-producto-de-sldb/README.md`,
`docs/architecture/one-address-grammar-two-spaces.md`, `docs/addressability_model.md`,
`docs/architecture/selectors.md`, `docs/architecture/anchoring.md`;
`src/sldb/cli/parsers/docs1.py`, `docs2.py`, `docs3.py`, `project.py`;
`src/sldb/cli/commands/doc.py`, `docs.py`, `docs_replace.py`, `move.py`;
`src/sldb/api/documents/` (`create_document.py`, `track_document_file.py`, `untrack_document.py`,
`delete_document.py`, `replace_text.py`, `move_document.py`, `move_path.py`, `payload_save.py`,
`payload_save_steps.py`, `lossy_overwrite.py`, `transaction_ops.py`);
`src/sldb/store/` (`hashing.py`, `layout.py`, `source_guard.py`, `edge_index/`, `models/document_entry.py`).
