---
clase: objeto
tipo: nodo
nombre: campo de modelo
estado: borrador
---

# Campo de modelo

## Qué es

Un campo de modelo es una declaración dentro de la clase de un modelo: nombre, tipo, descripción
y valor por defecto. Es parte del esquema. **No es el valor** que un documento guarda en ese
campo: ese valor no es un nodo, es el documento más una ruta dentro de él. El campo es lo que
permite validar el valor y lo que genera la sección correspondiente de la plantilla.

## Cómo se nombra

Hoy:

- Nodo del grafo: `sldb://field/<Modelo>.<campo>`
  (`src/sldb/store/edge_index/node_ids.py:33-35`).
- CLI: `models/<Modelo>/<campo>` como destino de `fields show`
  (`src/sldb/cli/commands/fields_target.py:37-39`, `src/sldb/cli/commands/fields_show.py:12`);
  `models fields add|remove <Modelo> <campo>` (`src/sldb/cli/parsers/models2.py:44-59`).
- Un ancla puede apuntar a un campo con `field:<Modelo>.<campo>`
  (`src/sldb/store/edge_index/anchor_targets.py:27-28`).
- Confusión a evitar: `st.{Modelo}.<doc>.<campo>` y `docs/<doc>/<campo>` nombran el **valor**
  en un documento (`docs/addressability_model.md`, `src/sldb/cli/commands/fields_target.py:15-18`).

Con la gramática propuesta (borrador): `[store:]st/<Modelo>/@<campo>` para el campo y
`[store:]st/<Modelo>/<doc>/<campo>` para el valor; la arroba los separa.

## Dónde se guarda

Solo en el código Python del modelo. El nodo es derivado: lo calcula el índice de aristas al
reconstruir, recorriendo `model_fields` de la clase importada
(`src/sldb/store/edge_index/model_contribution.py:29-31,51-55`). Si la clase no se puede
importar (modelo de un store enlazado), el nodo no se emite (`model_contribution.py:12-15,29`).
Un cambio pendiente vive en el borrador `.py.temp` del modelo
(`src/sldb/api/model_drafts/model_draft.py:11-15`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `models fields add <Modelo> <campo> --type --description [--default]`. Escribe el campo y su sección de plantilla en el **borrador**; no toca el modelo activo hasta promover con `models validate --promote` | `src/sldb/cli/commands/models_fields.py:23-26`, `src/sldb/api/model_drafts/field_drafts.py:26-53`, `src/sldb/cli/parsers/models2.py:13` | **Sin confirmar:** agregar el campo al contrato del modelo, con efecto al promover y con los documentos existentes revisados. |
| Leer | `fields show models/<Modelo>` (todos) o `models/<Modelo>/<campo>` (uno): nombre, descripción, anotación. MCP `describe_model` devuelve los campos con sus tipos. No hay comando de CLI que lea el nodo del grafo con todos sus atributos | `src/sldb/cli/commands/fields_show.py:15-43`, `src/sldb/mcp/read/models.py:25-32` (buscado en `src/sldb/cli/parsers/{fields,edges,graph}.py`) | **Sin confirmar:** devolver los atributos del esquema del campo (tipo, descripción, defecto, requerido). |
| Cambiar | No existe. `models fields` solo tiene `add` y `remove`; `models template edit` y `models metadata edit` no cambian el tipo ni la descripción de un campo. Se cambia editando la clase a mano y corriendo `models update` | `src/sldb/cli/parsers/models2.py:39-59,17-37,78-92`, `src/sldb/cli/commands/model.py:103-112` | **Sin confirmar:** cambiar tipo, descripción o defecto de un campo declarado, pasando por el mismo borrador que `add`. |
| Borrar | `models fields remove <Modelo> <campo>`: quita el campo y su sección de plantilla en el borrador (la plantilla heredada no se toca) | `src/sldb/cli/commands/models_fields.py:36-39`, `src/sldb/api/model_drafts/field_drafts.py:56-76,91-97` | **Sin confirmar:** quitar el campo del contrato; qué hacer con el valor que los documentos ya guardan es la pregunta abierta. |

## Aristas que le llegan y que salen

- `has_field`: modelo → campo, una por campo (`model_contribution.py:31`). Es estructural: nace
  y muere con el campo, nadie la escribe.
- `names`: ancla → campo, cuando el ancla es `field:<Modelo>.<campo>`
  (`anchor_targets.py:27-28`; tipo en `src/sldb/models/builtin_relation_types.py:27`).
- Un ancla cuyo `ref` es una forma `(field Modelo campo)` o una escritura
  `(change (it of Modelo) campo ...)` también termina en el campo
  (`src/sldb/store/edge_index/form_targets.py:10,24-25,33-37`), con la misma arista `names`.
- Del campo no sale ninguna arista. Los campos declarados en `__references__` y
  `__containment__` generan `references` y `contains` entre **documentos**, no hacia el campo
  (`builtin_relation_types.py:28-29`).

## Qué lo mantiene correcto

- El campo entra en `contract_hash` (`_field_schema`, tipo y descripción)
  (`src/sldb/store/hashing.py:97-98`); cambiarlo mueve el hash del modelo y `stores check`
  informa `store/contract-moved` (`src/sldb/api/stores/store_findings.py:37`).
- `models validate` revisa cada documento contra el contrato nuevo antes de promover, y
  `--backfill` completa los que les falta un campo con defecto
  (`src/sldb/api/model_drafts/draft_validation.py:34-43`, `backfill.py:39`).
- `field_set_drift`: un documento firmado con otro conjunto de campos se reconoce como
  desfasado (`src/sldb/store/field_set_drift.py:21-38`).
- Un campo sin marcador en la plantilla no se renderiza ni se extrae: por eso `add` también edita
  la plantilla (`field_drafts.py:1-6`).

## Abierto

- Al quitar un campo que los documentos ya llenan: ¿se borra el valor de cada documento, se
  conserva como texto huérfano, o se rechaza la operación mientras haya valores? Hoy el borrador
  se promueve y qué pasa con el valor no está verificado.
- Cambiar el tipo de un campo con valores existentes: ¿migra los valores, los revalida y falla,
  o se trata como quitar y crear?
- ¿Renombrar un campo es un verbo propio (conserva los valores) o es quitar y crear?

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Un campo es un nodo dentro del AST tipado del modelo: algo metido dentro del nodo del modelo, con sus propias relaciones (tipo, a qué modelos apunta).

## Fuentes

- `desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`, `desk/drawer/plans/spec-de-producto-de-sldb/README.md`
- `docs/architecture/one-address-grammar-two-spaces.md`, `docs/addressability_model.md`
- `src/sldb/cli/parsers/models2.py`, `src/sldb/cli/commands/{models_fields,fields_show,fields_target,model}.py`
- `src/sldb/api/model_drafts/{field_drafts,model_draft,draft_validation,backfill}.py`
- `src/sldb/store/edge_index/{node_ids,model_contribution,anchor_targets,form_targets}.py`
- `src/sldb/store/{hashing,field_set_drift}.py`, `src/sldb/models/builtin_relation_types.py`
