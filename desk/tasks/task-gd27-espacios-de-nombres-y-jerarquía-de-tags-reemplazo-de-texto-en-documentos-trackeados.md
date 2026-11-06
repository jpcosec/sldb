---
id: task-gd27-espacios-de-nombres-y-jerarquía-de-tags-reemplazo-de-texto-en-documentos-trackeados
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction
pills: []
files:
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/stores/tag_namespace.py
- src/sldb/api/tags/__init__.py
- src/sldb/api/tags/tag_tree.py
- src/sldb/api/tags/tag_folder.py
- src/sldb/api/tags/tag_check.py
- src/sldb/api/semantic/__init__.py
- src/sldb/api/documents/replace_text.py
- src/sldb/api/__init__.py
- src/sldb/store/semantic_tags.py
- src/sldb/cli/parsers/tags.py
- src/sldb/cli/commands/tags.py
- src/sldb/cli/parsers/docs3.py
- src/sldb/cli/commands/docs.py
- src/sldb/cli/commands/docs_replace.py
- tests/api/test_tags.py
- tests/api/test_replace_text.py
- docs/architecture/tags.md
- docs/architecture/transactions.md
- CHANGELOG.md
- src/sldb/api/rules/builtin_tag_rules.py
- src/sldb/api/rules/rules_on_write.py
- src/sldb/api/rules/rules_check.py
- src/sldb/api/rules/rules_on_check.py
- src/sldb/api/rules/rules_explain.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD27: Espacios de nombres y jerarquía de tags; reemplazo de texto en documentos trackeados

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD27 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG2. Depende de: ['GD24']. Gates requeridos: G_WRITE_API: Transacción y referencias entrantes en sldb.api (satisfied).

## Goal

_Describe the concrete result this task must produce._

StoreDeclaration gana tag_namespaces ({name, hierarchical, folder_axis, anchored_by}); un store que los declara rechaza al escribir un tag de namespace no declarado y un tag jerárquico sin ancla para cada prefijo; sldb.api.tag_tree y tag_folder; sldb.api reexporta sldb.api.semantic; CLI sldb tags namespaces|tree|check; sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None) con conteo exacto, re-extracción, validación contra el modelo y re-track dentro de sldb.api.transaction; CLI sldb docs replace con envelope; docs/architecture/tags.md y sección en transactions.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/store_declaration.py, src/sldb/api/semantic/, src/sldb/api/tags/ (nuevo), src/sldb/api/documents/replace_text.py (nuevo), src/sldb/api/__init__.py, src/sldb/store/semantic_tags.py, src/sldb/cli/parsers/tags.py y commands/tags.py (nuevos), src/sldb/cli/parsers/docs*.py y commands/docs*.py, tests, docs/architecture/tags.md, docs/architecture/transactions.md, CHANGELOG.md. Fuera: editar src/sldb/api/documents/payload_save_steps.py; nombres del caso deskops (domain, atom) en src/sldb/; migrar los tags de deskops (lo hace deskops).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD27). SCOPE: (1) Tags: StoreDeclaration gana tag_namespaces: lista de {name, hierarchical: bool, folder_axis: bool, anchored_by: {model, field} opcional}. Validación al escribir un documento (paso de validación existente, sin tocar payload_save_steps.py: se registra como validador del store): un tag namespace:valor cuyo namespace no está declarado es error si el store declara tag_namespaces (sin la clave, nada cambia); con anchored_by, cada prefijo con punto del valor (la jerarquía de store/semantic_tags.py:35 _prefix_edges) debe tener un documento del modelo anchored_by.model cuyo campo anchored_by.field es ese tag; si falta, error que lista los prefijos faltantes (mecánica de deskops domain_tree.py:80 require_domain_parents, sin sus nombres). Función sldb.api.tag_tree(store, namespace) → {roots: árbol anidado {tag, document, children}, orphans: tags usados sin documento ancla, unplaced: documentos ancla sin uso}; folder_axis: sldb.api.tag_folder(tag) → ruta a/b para a.b (mecánica de atom_tags.py:120). sldb.api.semantic (dag_reads, dag_writes) se reexporta en sldb.api. CLI: sldb tags namespaces, sldb tags tree NAMESPACE, sldb tags check. (2) Reemplazo: sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None) sobre un documento trackeado o un archivo no modelado bajo la raíz: exige exactamente count apariciones de old (si no, error con el número visto y nada se escribe); en un documento trackeado reescribe los bytes, re-extrae y valida contra el modelo (si no valida, error y nada se escribe) y re-trackea con el mismo modelo y nombre; todo dentro de sldb.api.transaction. CLI sldb docs replace REF --old --new [--count N] con envelope. Doc docs/architecture/tags.md y sección en docs/architecture/transactions.md.

ACCEPTANCE: En un store temporal con tag_namespaces [{name: area, hierarchical: true, anchored_by: {model: Anchor, field: tag}}]: escribir un documento con area:a.b sin Anchor de area:a falla nombrando area:a; con los dos Anchor pasa; un tag otro:x falla por namespace no declarado; un store sin tag_namespaces acepta lo mismo que antes (tests existentes verdes); tag_tree devuelve raíz a con hijo a.b, un huérfano y un unplaced del fixture; tag_folder("a.b") = "a/b"; replace_text con count 1 y dos apariciones falla sin escribir; con una aparición reescribe, re-trackea y el documento extrae igual salvo el texto; un reemplazo que rompe el modelo falla y deja el archivo igual (hash); CHANGELOG; docs; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/stores/store_declaration.py, src/sldb/api/semantic/, src/sldb/api/tags/, src/sldb/api/documents/replace_text.py, src/sldb/api/__init__.py, src/sldb/store/semantic_tags.py, src/sldb/cli/parsers/tags.py, src/sldb/cli/commands/tags.py, src/sldb/cli/parsers/docs*.py, src/sldb/cli/commands/docs*.py, tests/, docs/architecture/tags.md, docs/architecture/transactions.md, CHANGELOG.md

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Las revisiones en frío las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`; nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de sldb aparte del de grafo-operable (otras áreas: edges, documents, serve, stores). Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor sobre el resultado integrado. Un nodo no cierra con tests rojos ni saltados.
3. Toda capacidad nueva entra con: función pública en `sldb.api` (reexportada en `sldb/api/__init__.py`), comando CLI con envelope JSON, ruta de `sldb serve` cuando el consumidor la necesita, pruebas, entrada en `CHANGELOG.md` y doc en `docs/architecture/`. Nada queda solo en el código.
4. Genericidad: ningún nombre del caso deskops (TaskDoc, Board, ritual, pill, atom, closeout) aparece en `src/sldb/` ni en sus tests, salvo como dato en fixtures. Un grep lo comprueba en la aceptación de cada nodo.
5. Compatibilidad: ninguna salida existente de la CLI ni de `sldb serve` cambia (goldens existentes verdes); lo nuevo es aditivo. Si un nodo necesita cambiar un contrato existente (p. ej. `/save` pasa a ser atómico), lo nombra en su aceptación y en el CHANGELOG.
6. Ante un contrato ausente de un nodo GO no cerrado, el nodo registra la hipótesis en su TaskDoc, implementa la parte que no depende de él y no inventa la API de grafo-operable.
7. Cada nodo, al cerrar, manda nota a deskops (`deskops message send --to deskops --kind suggestion`) con la función, el comando y la ruta nuevos y el código de deskops que quedan sin motivo (tabla de arriba); así se satisface el gate `G_GDxx` del plan de deskops.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06):
q1 (gates): G_WRITE_API está satisfied (fe36893f) y GD24 cerrado (88f19ac8): sldb.api.transaction existe y replace_text la usa.
q2 (base): GO08 está cerrado en main (556408da): existen las reglas on_write (src/sldb/api/rules/rules_on_write.py, RuleDoc con moment on_write) que save_document_payload evalúa antes de escribir.
q3 (mecanismo de validación de tags, DECIDIDO por el coordinador de proyecto 2026-11-06, opción B): tag_namespaces sigue siendo dato de store.yaml (StoreDeclaration); su chequeo es una familia de reglas incorporada, no una RuleDoc de usuario, que corre dentro de la evaluación de reglas de GO08 en los tres momentos: on_write (check_on_write: un error rechaza la escritura con SLDBRuleViolationError y no se escribe nada), on_check (stores check) y sldb rules check. Condiciones: (a) rules check y rules explain muestran sus hallazgos con la misma forma que los de una RuleDoc (Finding con node, clause y seen; la regla se identifica con un id estable, p. ej. builtin:tag_namespace:<name>); (b) no se edita src/sldb/api/documents/payload_save_steps.py; (c) la familia vive en un módulo hermano nuevo, src/sldb/api/rules/builtin_tag_rules.py, y se engancha en rules_on_write.py (incluido el corte temprano de has_rules: un store sin RuleDocs pero con tag_namespaces también se chequea), rules_check.py, rules_on_check.py y rules_explain.py, agregados a files; (d) sin tag_namespaces en store.yaml nada cambia (las salidas existentes de rules check, explain y stores check son iguales). Coordinación: api/rules es área de grafo-operable (GO08 cerrado; GO10 en curso con where_parse/FieldCondition): el coordinador avisa a w1:p4 antes de despachar y el ejecutor rebasea sobre origin/main antes de entregar.
HIPÓTESIS PARA EL DUEÑO (q3): no es RuleDoc de usuario (opción C) porque el lenguaje de reglas de GO05 no tiene un predicado de prefijo ancla (para cada prefijo con punto de un tag, existe un documento de un modelo dado cuyo campo es ese prefijo); agregarlo tocaría GO05. Si el dueño lo quiere como RuleDoc, el camino es ese predicado y la familia incorporada se reemplaza por RuleDocs declaradas.
q4 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_tags.py
- TMPDIR=/dev/shm pytest -q tests/api/test_replace_text.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_semantic.py
- TMPDIR=/dev/shm pytest -q tests/store/test_stores_build.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout|domain_tree (regla 4)
- sldb tags tree NAMESPACE y sldb docs replace --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con tag_namespaces [{name: area, hierarchical: true, anchored_by: {model: Anchor, field: tag}}]: escribir un documento con area:a.b sin Anchor de area:a falla nombrando area:a; con los dos Anchor pasa; un tag otro:x falla por namespace no declarado; un store sin tag_namespaces acepta lo mismo que antes (tests existentes verdes); tag_tree devuelve raíz a con hijo a.b, un huérfano y un unplaced del fixture; tag_folder("a.b") = "a/b"; replace_text con count 1 y dos apariciones falla sin escribir; con una aparición reescribe, re-trackea y el documento extrae igual salvo el texto; un reemplazo que rompe el modelo falla y deja el archivo igual (hash); CHANGELOG; docs; nota de cierre a deskops.
