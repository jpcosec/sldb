---
clase: objeto
tipo: nodo
nombre: modelo
estado: borrador
---

# Modelo

## Qué es

Un modelo es una clase Python (subclase de `StructuredNLDoc`) que define la forma de un
documento: sus campos, su plantilla Markdown y metadatos como `__family__`, `__semantics__`,
`__references__`, `__containment__` y `__compositions__`. El store registra el modelo y sigue a
sus documentos. El modelo es la fuente de la validación de cada documento y de los nodos campo.

## Cómo se nombra

Hoy:

- Nodo del grafo: `sldb://model/<Nombre>` (`src/sldb/store/edge_index/node_ids.py:28-30`).
  Es un solo nodo para todos los stores: `qualify_id` no califica modelos
  (`src/sldb/store/edge_index/federation.py:27-30`).
- CLI: el nombre simple (`models show TaskDoc`), la referencia de código `modulo:Clase` en
  `models add` (`src/sldb/cli/parsers/models1.py:12-17`), `alias:Modelo` en `models inherit`
  (`models1.py:32-36`) y el destino `models/<Nombre>` en `fields show`
  (`src/sldb/cli/commands/fields_target.py:37-38`).
- Espacio `st.{Modelo}` (y `{Modelo+}` para la familia) en `docs/addressability_model.md`.

Con la gramática propuesta (borrador): `[store:]st/<Modelo>`, y calificado por el dueño:
`deskops:st/TaskDoc`. Eso revierte el vocabulario único de hoy (`one-address-grammar-two-spaces.md`,
decisión 4, confirmada por el dueño el 2026-11-26).

## Dónde se guarda

- La definición: el código Python de la clase, en el repo que la escribe (una ruta de
  `store.yaml`: `models: [{name, model_ref, path}]`, `src/sldb/api/stores/store_declaration.py:30`).
- El registro: `.sldb/core/store_index.yaml` y `.sldb/core/models/<Modelo>.yaml` con `roster_hash`,
  `contract_hash` y `model_hash` (`src/sldb/store/model_node.py:21-35`). Es derivado.
- Un modelo heredado no lleva `model_ref` ni `path` propios: dice de qué store viene
  (`src/sldb/api/model_registry/inherit_model.py:21-27`).
- Un borrador de cambio vive en un `.py.temp` junto al código
  (`src/sldb/api/model_drafts/model_draft.py:11-15`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | Dos pasos o uno según la puerta. `models create` solo genera el código Python, no registra. `models add` registra una clase que ya existe. `api.create_model` genera y registra; no hay comando de CLI que lo llame (lo usa `serve`) | `src/sldb/cli/commands/models_create.py:12-16,28-31`, `src/sldb/cli/commands/model.py:50-58`, `src/sldb/api/model_registry/add_model.py:18-40`, `src/sldb/api/model_create/create_model.py:21,66-70`, `src/sldb/cli/serve/models_create_routes.py:18` | **Sin confirmar:** escribir la clase y registrarla en un solo acto, calificada con el store dueño. |
| Leer | `models list`, `models show`, `models check` (registrado o ausente); MCP `list_models` y `describe_model` | `src/sldb/cli/commands/models_list.py:11`, `src/sldb/cli/commands/models.py:69-72`, `src/sldb/cli/commands/models_check.py:11-15`, `src/sldb/mcp/read/models.py:19-32` | **Sin confirmar:** devolver el contrato (campos, plantilla, metadatos) y el origen; los documentos son otra lectura. |
| Cambiar | Por borrador: `models fields add/remove`, `models template edit`, `models metadata edit`, y se aplica con `models validate --promote [--backfill]`. A mano: editar la clase y correr `models update` (recalcula hashes) | `src/sldb/cli/parsers/models2.py:13-14,44-60,78-92`, `src/sldb/api/model_drafts/draft_validation.py:34-43`, `src/sldb/cli/commands/model.py:103-112` | **Sin confirmar:** cambiar el contrato con un borrador validado contra los documentos y una promoción que sube la versión. |
| Borrar | `models remove`: quita el registro, los índices y los shards; no toca la clase. Se rechaza si el modelo aún tiene documentos, salvo `--with-documents`, que los deja de seguir (los archivos quedan). No revisa si otro modelo lo extiende | `src/sldb/cli/commands/models.py:52-56`, `src/sldb/api/model_registry/remove_model.py:20-65` | **Sin confirmar:** desregistrar el modelo; qué pasa con sus documentos es la pregunta abierta de abajo. |

El MCP no escribe modelos: el servidor no sirve escribir código de modelo (`src/sldb/mcp/mutability.py:1-8`, nivel 3 "nunca servido").

## Aristas que le llegan y que salen

- `has_model`: store → modelo, creada al registrar (`store_contribution.py:33-37`).
- `has_field`: modelo → campo, una por campo de la clase (`model_contribution.py:31`).
- `extends`: modelo → modelo base, por `base_models` (`model_contribution.py:32`).
- `has_document`: modelo → documento. El tipo está declarado en
  `src/sldb/models/builtin_relation_types.py:18`; quién emite la arista, sin verificar.
- `tagged_as`: modelo → tag, por `__semantics__` (`model_contribution.py:26-27`).
- `applies_to_source`, `applies_to_target`: tipo de relación → modelo
  (`src/sldb/store/edge_index/doc_kinds.py:41`).
- `names`: ancla → modelo (`src/sldb/store/edge_index/anchor_targets.py:31`).
- `references`, `contains`, `composes` los declara el modelo (`__references__`,
  `__containment__`, `__compositions__`) y los emiten sus documentos; el modelo no es extremo.

## Qué lo mantiene correcto

- `contract_hash` (campos, plantilla, familia, semántica, bases, referencias, contención,
  composiciones) y `model_hash = hash(roster_hash, contract_hash)`
  (`src/sldb/store/hashing.py:80-112`). `stores check` informa `store/contract-moved` y
  `store/contract-mutation` (`src/sldb/api/stores/store_findings.py:20,37`).
- `models validate` revisa cada documento contra el borrador antes de promover
  (`src/sldb/api/model_drafts/draft_validation.py:48-54`).
- Un campo agregado por borrador también agrega su sección a la plantilla, para no quedar
  fantasma (`src/sldb/api/model_drafts/field_drafts.py:1-6`).

## Abierto

- Al borrar un modelo con documentos: ¿se borran los documentos y sus archivos, se dejan de
  seguir y los archivos quedan (hoy), o se prohíbe mientras existan? ¿Y si otro modelo lo extiende?
- Un modelo calificado (`deskops:st/TaskDoc`) que un store hereda: ¿borrar el heredado
  desregistra solo en este store, o el dueño puede borrar y dejar huérfanos a los demás?
- Crear un modelo escribe Python: ¿sldb escribe el archivo, o solo registra uno que alguien
  escribió? Hoy el MCP se niega a lo primero.

## Fuentes

- `desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`, `desk/drawer/plans/spec-de-producto-de-sldb/README.md`
- `docs/architecture/one-address-grammar-two-spaces.md`, `docs/architecture/model-federation-on-the-graph.md`, `docs/addressability_model.md`
- `src/sldb/cli/parsers/{models1,models2}.py`, `src/sldb/cli/commands/{models,model,models_list,models_check,models_create}.py`
- `src/sldb/api/model_registry/`, `src/sldb/api/model_create/`, `src/sldb/api/model_drafts/`
- `src/sldb/store/{hashing,model_node}.py`, `src/sldb/store/edge_index/{node_ids,federation,model_contribution,doc_kinds}.py`
- `src/sldb/mcp/{mutability,read/models}.py`
