---
id: task-go09-transiciones-como-datos-de-la-arista
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
files:
- src/sldb/models/relation_doc.py
- src/sldb/store/models/edge_record.py
- src/sldb/api/edges/edges_holding.py
- src/sldb/api/edges/edge_effects.py
- src/sldb/api/edges/apply_effects.py
- src/sldb/api/edges/__init__.py
- src/sldb/api/__init__.py
- docs/architecture/edges.md
- CHANGELOG.md
- tests/api/test_edge_effects.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO09: Transiciones como datos de la arista

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO09 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK04. Hoy deskops guarda el efecto de una transicion (sets_status, terminal) en su propio YAML; sldb solo dice que arista se cumple (edges_holding). GO09 hace que la arista transporte su efecto (RelationDoc.attributes.sets/terminal) y que sldb lo resuelva y aplique sin persistir. GO05 (8be66bde) dejo edges_holding sobre el lenguaje unico.

## Goal

_Describe the concrete result this task must produce._

Convencion RelationDoc.attributes {sets, terminal} validada en el modelo; edges_holding devuelve cada EdgeRecord con effects = {sets resueltos con {campo}, terminal}; apply_effects(subject, effects, model) puro que devuelve el payload nuevo validado contra el modelo; documentacion de la convencion y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/models/relation_doc.py (validacion de la convencion), EdgeRecord (atributo effects), api/edges (edges_holding, resolucion de effects, apply_effects), la doc de edges en docs/architecture, CHANGELOG.md, tests. Fuera: findings por arista y orden pinneado->reglas (GO08), el retiro de sets_status/terminal en deskops (G_CONSUMER, plan de deskops), shims (GO10).

PRINCIPIO DEL DUENO (2026-11-05): invariantes de UN documento = validadores pydantic del modelo; entre documentos = RuleDoc; los tests solo prueban rechazo. Aplicado aqui: (q1) la convencion de attributes (mapa o ausente/null; sets mapa o ausente/null; terminal booleano o ausente/null; valores de sets escalares o listas de escalares) es un validador pydantic de RelationDoc: escribir un RelationDoc que la viola levanta el ValidationError del modelo con el campo y el motivo, por la via de escritura existente. (q2) Los tests de convencion invalida prueban rechazo, uno por regla (attributes no mapa, sets no mapa, terminal no booleano, valor de sets mapa, valor de sets lista anidada); el valor invalido en apply_effects tambien se prueba por rechazo.

HEREDADO: (h1) {campo} usa la sintaxis y la fuente de where_subject (fill_braces) sobre el payload del sujeto; un {campo} ausente, null o no escalar hace que la arista no se cumpla (GO05 H9). (h2) edges_holding evalua las condiciones con el lenguaje de GO05 (payload_holds).

PRECISIONES (preflight de GO09, 2026-11-06):
p1 (files manda): la lista files manda sobre OUTPUT_SCOPE (criterio de GO03 p6 y GO04 p1); src/sldb/store/models/edge_record.py es editable. effects es un campo nuevo de EdgeRecord que solo llena edges_holding; en cualquier otra lectura queda sin valor y la salida (texto, JSON, YAML) de todo comando y funcion existente no cambia: effects no aparece en la serializacion cuando no tiene valor.
p2 (firma de apply_effects): apply_effects(subject: dict, effects: dict, model: type[StructuredNLDoc]) -> dict; model es la clase del modelo. Quien solo tiene el Model:name la obtiene con el resolutor existente de modelos del store (el mismo que usa la escritura de documentos); apply_effects no resuelve nombres.
p3 (null): un {campo} dentro de un valor de sets que resuelve a ausente, null o no escalar en el sujeto hace que la arista no se cumpla (no aparece en edges_holding), igual que en una condicion. sets: {x: null} con null literal (sin llaves) es un valor asignable y escribe null.
p4 (serializacion): {campo} solo se sustituye dentro de valores string de sets y el resultado sigue siendo string: el escalar se inserta como true/false para booleanos, el numero tal cual (str de int o float, sin notacion de Python como True o 1.0e+00 salvo que sea su forma YAML), y un string sin comillas ni escape. Ejemplo: sets {closed: "{done}"} con done=True da closed = "true".
p5 (compatibilidad): los tests existentes de edges_holding, RelationDoc y EdgeRecord pasan sin cambios; si alguno falla es senal de que cambio una salida existente (contra p1) y se corrige el codigo, no el test.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO09 scope): Convención documentada para RelationDoc.attributes de una transición: sets = mapa campo → valor que la transición escribe en el sujeto (p. ej. {status: closed}); terminal = booleano que sldb solo transporta. attributes debe ser un mapa, o estar ausente o null; otro tipo es error de validación al escribir el RelationDoc. Defaults: attributes ausente o null, sets ausente o null, equivalen a sets = {}; sets presente y no mapa es error de validación; terminal ausente o null equivale a false; terminal con un valor no booleano es error de validación al escribir el RelationDoc (la convención se valida en relation_doc.py). Valores de sets admiten {campo} con la misma sintaxis y fuente que where_subject (payload del sujeto); un {campo} ausente, null o no escalar en el sujeto hace que la arista no se cumpla, igual que en una condición; null sí es un valor asignable en sets (sets: {x: null} escribe null). edges_holding sigue devolviendo la lista de aristas que se cumplen; cada EdgeRecord lleva un atributo nuevo effects = {sets resueltos, terminal} (sustitución {campo} aplicada); GO08 agregará el atributo findings a cada EdgeRecord sin tocar effects. Claves de attributes distintas de sets y terminal se conservan en el RelationDoc y no entran a effects. Función pura apply_effects(subject, effects, model) → nuevo payload: copia del sujeto donde cada clave de sets reemplaza entera la clave de primer nivel del mismo nombre, o la agrega si no existe (sin fusión anidada); los valores de sets son escalares o listas de escalares de YAML (un mapa o una lista anidada es error de validación), y {campo} solo se sustituye dentro de strings, por la serialización YAML del escalar (true/false, números y strings tal cual), nunca por el repr de Python; y el payload completo resultante se valida contra model (el llamante lo conoce: edges_holding sabe el Model:name del sujeto); levanta el error de validación si no valida; nunca persiste. ACEPTACION: En un store de prueba con tres estados y tres transiciones, edges_holding devuelve la transición que aplica con effects resueltos (incluida una sustitución {campo} de un booleano, serializado como true); apply_effects produce el payload esperado y rechaza un valor inválido para el modelo; una arista sin attributes devuelve effects = {sets: {}, terminal: false}; una clave extra en attributes no aparece en effects; la doc de edges describe la convención; CHANGELOG. Nota, no criterio: con esto deskops podrá retirar sets_status/terminal de su YAML (lo verifica deskops en G_CONSUMER). OUTPUT_SCOPE: src/sldb/api/edges/, src/sldb/models/relation_doc.py, docs/architecture/, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: spec, CLI con envelope JSON cuando hay comando, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste; regla 6: ante un contrato ausente registrar la hipotesis, no inventar API).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/api/test_edge_effects.py sin fallos ni saltados
- store de prueba con tres estados y tres transiciones: edges_holding devuelve la transicion que aplica con effects resueltos, incluida una sustitucion {campo} de un booleano serializado como true
- apply_effects produce el payload esperado y rechaza un valor invalido para el modelo
- arista sin attributes -> effects = {sets: {}, terminal: false}; clave extra en attributes no aparece en effects
- convencion invalida rechazada al escribir el RelationDoc, un test de rechazo por regla
- tests existentes de edges_holding y de RelationDoc sin cambios
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO09 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.
