---
sldb:
  by: agent
  at: '2026-11-15T17:43:29Z'
  authority: generated
  via: save_document_payload
id: task-migrar-a-sldb-los-modelos-de-spec-por-tipo-de-diagrama-de-spec2viz-con-carga-y-validación-junto-a-sp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Migrar a sldb los modelos de spec por tipo de diagrama de spec2viz, con carga y validación, junto a SpecDoc (D3)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: los modelos de spec son genéricos. Los compiladores y renderers se quedan en specIR (IR11 e IR12) como capa visual y consumen estos modelos en vez de redefinirlos.

## Goal

_Describe the concrete result this task must produce._

sldb aloja los modelos de spec de los ocho tipos de diagrama con su carga y validación.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Entra: los modelos de spec de los ocho tipos de diagrama (class, sequence, state, component, activity, deployment, matrix, reflection) más la base y el modelo de catálogo, con su cargador y su validador, en un subpaquete junto a SpecDoc; ParseError como excepción nueva de sldb. Se reutiliza lo que sldb ya tiene: DiagramType, la jerarquía de excepciones de notaciones y SpecDoc/SpecNodeDoc (no se duplican ni se modifican). Sale: compiladores, renderers, linters, json_schema, la CLI y cualquier cambio en spec2viz. Genericidad = condición observable: el subpaquete no importa nada de spec2viz ni de renderers y se importa solo con las dependencias que sldb ya declara. spec2viz NO se retira y conserva su código; el gate IR13 es la tarea IR13 del desk de IR, que decide el retiro; aquí solo se nombra. Paridad: los tests de spec2viz de la pieza se portan con el mínimo cambio.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Comparar primero (hecho al preparar la tarea, a repetir y registrar en el cierre): sldb ya tiene DiagramType idéntico al de spec2viz (src/sldb/notations/diagram_type.py, los mismos ocho valores, se reutiliza y no se migra el de models.base), la jerarquía de excepciones de validación (src/sldb/notations/exceptions.py: ValidationError, UnknownReferenceError, EndpointKindError, StructureError, UnknownKindError y las demás, con raíz NotationError) y SpecDoc/SpecNodeDoc (src/sldb/models/notation/spec_doc.py y spec_node_doc.py), que guardan un spec pero no validan su contenido por tipo. Lo que NO tiene sldb y se migra: los modelos pydantic por tipo, el cargador, el validador y ParseError.
2. Origen (repo hermano spec2viz, existen): paquete spec2viz.models (base, sequence, state, component, activity, deployment, matrix, class_diagram, reflection y catalog), spec2viz.loader (69 líneas), spec2viz.validator (236 líneas) y spec2viz.exceptions solo para ParseError. Los "ocho modelos" son los ocho tipos (class, sequence, state, component, activity, deployment, matrix/component_view_matrix, reflection); base es la clase común y no cuenta entre los ocho. El modelo de catálogo entra: solo importa pydantic y typing, no toca renderers (criterio: ningún import de compilers, renderers ni linters; si al leerlo apareciera uno, se deja fuera y se anota).
3. Destino: un paquete nuevo junto a SpecDoc, bajo src/sldb/models/notation/ (subpaquete de modelos de diagrama con un módulo por tipo, base, catalog, loader y validator; cada módulo bajo el límite de líneas del repo). Importa DiagramType de sldb.notations.diagram_type y las excepciones de sldb.notations.exceptions; la ParseError nueva va como un módulo más en sldb/notations/errors, colgando de NotationError, y se exporta desde sldb.notations.exceptions. Spec2VizError, CompileError y RenderError se quedan en spec2viz (capa visual).
4. Relación con SpecDoc: los modelos por tipo validan el contenido (data) de un spec; SpecDoc lo guarda y no se modifica. Exponer en sldb.api.notations una función load_spec(ruta) y validate_spec(modelo) que usan loader y validator; no se toca SpecSync (D1 recibe esa validación por parámetro).
5. Qué se deja fuera: compiladores, renderers, linters, json_schema y la CLI de spec2viz. Pydantic ya es dependencia de sldb: no se declara ninguna dependencia nueva (PyYAML tampoco; verificar en pyproject al terminar).
6. Tests a portar con el mínimo cambio (imports a los de sldb, fixtures de spec2viz copiadas al directorio de fixtures de tests de sldb): test_base_model (3), test_models_activity (3), test_models_component (3), test_models_deployment (4), test_models_matrix (4), test_models_sequence (3), test_models_state (3), test_loader (16), test_validator (19), test_exceptions (2, solo la jerarquía de ParseError y ValidationError bajo NotationError; los asertos sobre Spec2VizError, CompileError y RenderError no se portan). De test_class_diagram solo los de modelo y validación: test_semantic_errors_are_rejected, test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed, test_overloads_with_distinct_parameter_types_are_allowed y test_invalid_schema_fails_at_load. De test_class_packages solo test_typed_validation y test_package_id_cannot_be_a_class_id. Los que invocan compile_ir, render, la CLI, mermaid o sync se quedan en spec2viz.
7. Paridad de errores: "mismo error" = misma clase (por nombre) y el mismo texto de str(error) para la misma entrada, comprobado con los tests portados y con todos los ejemplos y fixtures de spec2viz (test_every_example_and_fixture_has_only_known_keys). La única diferencia admitida y documentada es la clase raíz (NotationError en sldb, Spec2VizError en spec2viz).
8. spec2viz no se toca: conserva sus modelos, loader y validator. El retiro lo decide la tarea IR13 del desk de IR (gate IR13); aquí solo se nombra. IR11 e IR12 consumirán estos modelos después.

## Validation

_List the checks required before this task can close._

- Tests de origen en spec2viz: test_base_model, test_models_activity, test_models_component, test_models_deployment, test_models_matrix, test_models_sequence, test_models_state, test_loader, test_validator, test_exceptions (jerarquía de errores de validación y ParseError), y de test_class_diagram y test_class_packages solo los de modelo y validación (test_semantic_errors_are_rejected, test_inheritance_cycle_is_rejected_but_dependency_cycles_are_allowed, test_overloads_with_distinct_parameter_types_are_allowed, test_invalid_schema_fails_at_load, test_typed_validation, test_package_id_cannot_be_a_class_id).
- Destino previsto: un archivo de tests por modelo y uno de loader, validator y excepciones, junto a los de los modelos de notación de sldb, con las fixtures de spec2viz copiadas al directorio de fixtures de tests de sldb.
- Comparar errores: mismas clases y mismo texto sobre todos los ejemplos y fixtures de spec2viz, y registrar la comparación con SpecDoc y DiagramType en el cierre.
- TMPDIR=/dev/shm pytest -q de cada archivo tocado, uno a la vez; antes de entregar, todos los tests/*.py de a uno.
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin faltantes nuevos.

## Done When

_Name the observable condition that makes the task complete._

1. Los ocho modelos por tipo, la base, el catálogo, el cargador y el validador están en sldb junto a SpecDoc, y load_spec y validate_spec están exportados desde sldb.api.notations.
2. Reutilizan DiagramType y las excepciones de sldb; solo ParseError es nueva; no hay modelo ni excepción duplicada, y SpecDoc y SpecNodeDoc quedan sin cambios.
3. Los tests portados (lista en Validation) pasan, y sobre los ejemplos y fixtures de spec2viz los errores tienen la misma clase y el mismo texto que en spec2viz.
4. El subpaquete no importa spec2viz ni renderers; pyproject de sldb sin dependencias nuevas (o, si hiciera falta una, declarada con su motivo en el cierre).
5. spec2viz sin cambios (retiro = gate IR13, tarea IR13 del desk de IR).
6. Suite de a un archivo, tools/check.sh y sldb stores build --check en verde; deskops graph missing sin faltantes nuevos.
