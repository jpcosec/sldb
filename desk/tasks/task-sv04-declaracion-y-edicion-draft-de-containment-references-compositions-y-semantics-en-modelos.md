---
id: task-sv04-declaracion-y-edicion-draft-de-containment-references-compositions-y-semantics-en-modelos
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- 6b80df36
- 6ba8bb20
- tests/api/test_model_metadata_drafts.py
- atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill
depends_on: []
pills: []
files:
- src/sldb/api/model_create/create_model.py
- src/sldb/api/model_create/model_source.py
- src/sldb/api/model_create/model_check.py
- src/sldb/api/model_registry/describe_model.py
- src/sldb/api/model_registry/model_description.py
- src/sldb/api/model_drafts/metadata_drafts.py
- src/sldb/api/model_drafts/metadata_literals.py
- src/sldb/api/model_drafts/draft_contract.py
- src/sldb/api/model_drafts/backfill.py
- src/sldb/api/model_drafts/__init__.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/models2.py
- src/sldb/cli/commands/models.py
- src/sldb/cli/commands/models_create.py
- src/sldb/cli/commands/models_metadata.py
- src/sldb/cli/commands/models_validate.py
- src/sldb/cli/serve/models_routes.py
- docs/architecture/model-authoring.md
- CHANGELOG.md
- tests/api/test_model_metadata_drafts.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SV04: Declaracion y edicion draft de containment, references, compositions y semantics en modelos

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo SV04 del plan desk/drawer/plans/absorber-spec2viz-y-modelos-ui (dag.yaml rev 1). Hoy sldb.api.create_model y sldb.api.model_drafts (y sus rutas en sldb serve) solo permiten declarar y editar fields escalares/listas y __template__. Para que la UI unificada pueda declarar y evolucionar modelos completos de conocimiento, necesita crear, inspeccionar, editar en draft, validar y promover con backfill tambien __containment__, __references__, __compositions__, __semantics__ y __authority__.

## Goal

_Describe the concrete result this task must produce._

create_model acepta containment, references, compositions, semantics y authority; describe_model (y GET /models/detail) expone esos metadatos mas template y has_draft; edit_model_metadata en sldb.api.model_drafts edita __containment__, __references__, __compositions__, __semantics__ y __authority__ en el .draft.py con validacion de contrato y soporte de backfill en CLI y POST /models/* de sldb serve.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/model_create/create_model.py, src/sldb/api/model_create/model_source.py, src/sldb/api/model_create/model_check.py, src/sldb/api/model_registry/describe_model.py, src/sldb/api/model_registry/model_description.py, src/sldb/api/model_drafts/metadata_drafts.py, src/sldb/api/model_drafts/metadata_literals.py, src/sldb/api/model_drafts/draft_contract.py, src/sldb/api/model_drafts/backfill.py, src/sldb/api/model_drafts/__init__.py, src/sldb/api/__init__.py, src/sldb/cli/parsers/models2.py, src/sldb/cli/commands/models.py, src/sldb/cli/commands/models_create.py, src/sldb/cli/commands/models_metadata.py, src/sldb/cli/commands/models_validate.py, src/sldb/cli/serve/models_routes.py, docs/architecture/model-authoring.md, CHANGELOG.md, tests/api/test_model_metadata_drafts.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 1, SV04): (1) En sldb.api.model_create (create_model, ModelSource), agregar parametros opcionales containment: dict[str, list[str]] | None = None, references: list[str] | None = None, compositions: dict[str, dict] | None = None, semantics: dict[str, list[str]] | None = None, authority: str | None = None; validar que cada campo nombrado en containment, references y compositions[k].source_field exista entre los fields declarados (o heredados) y que cada composicion tenga su marcador render en __template__ (o agregarle su seccion por defecto en default_template), y emitir las asignaciones __authority__, __semantics__, __containment__, __references__, __compositions__ en el cuerpo de la clase generada. (2) En describe_model y ModelDescription, agregar containment, references, compositions, semantics_map (el dict __semantics__ declarado), authority, template y has_draft (bool, mas draft_path: str | None). (3) En sldb.api.model_drafts, implementar edit_model_metadata(store, model_name, *, containment=None, references=None, compositions=None, semantics=None, authority=None, pythonpath=None) -> ModelDraft usando AST (metadata_literals.py) para insertar o reemplazar las asignaciones de clase en .draft.py y sincronizar secciones ⸢render•<name>⸥ en __template__ cuando se agregan o quitan composiciones. (4) En draft_contract.py (validate_template_contract) y backfill.py (check_and_plan), validar que __references__, __containment__ y __compositions__ solo referencien campos existentes en model_fields y que toda clave de __compositions__ tenga su marcador render en __template__ (levantando SLDBModelEditError si falta); al promover con backfill=True, re-renderizar documentos afectados y reconstruir indices de modelo, semantico y de aristas. (5) Exponer en CLI (sldb models metadata edit, sldb models validate --promote --backfill) y en sldb serve (POST /models/create, POST /models/metadata-edit y parametro backfill en POST /models/promote).

## Validation

_List the checks required before this task can close._

- pytest tests/api/test_model_metadata_drafts.py -q sin fallos ni saltados
- create_model y edit_model_metadata declaran y editan __containment__, __references__, __compositions__ y __semantics__ y GET /models/detail los devuelve
- validate_model_draft rechaza referencias/containment/compositions hacia campos inexistentes con SLDBModelEditError y promote_model_draft(..., backfill=True) actualiza documentos e indices

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de SV04 cumplida, tests en verde, G_SV_MODEL_EDITOR satisfecho en dag.yaml.
