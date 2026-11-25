FILE:desk/tasks/task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo.md
---
sldb:
  by: agent
  at: '2026-11-16T05:31:04Z'
  authority: generated
  via: save_document_payload
id: task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-214942-suggestion-ir13b-label-key-no-separa-y-normkey-del-cat-logo-s-matching-label-key-underscore.md
depends_on: []
pills: []
files:
- src/sldb/api/matching/atom_keys.py
- tests/matching/test_matching_explicit.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# label_key de sldb.api.matching trata el guion bajo como separador, igual que normKey del catálogo

## Rationale

_Explain why this task exists or the business driver behind it._

sldb.api.matching.label_key (src/sldb/api/matching/atom_keys.py) normaliza con re.sub(r"[^\w\s]+", " ", ...); \w incluye "_", así que label_key("post_published") da "post_published". normKey de la plantilla JS del catálogo usa /[^\p{L}\p{N}\s]+/gu y da "post published". Un elemento sin label se dibuja con su id; si el id lleva "_", el mapa de átomos explícitos queda con una clave que el navegador nunca busca y el átomo no se encuentra. Lo reportó IR13b. Origen: desk/inbox/20261115-214942-suggestion-ir13b-label-key-no-separa-y-normkey-del-cat-logo-s-matching-label-key-underscore.md.

## Goal

_Describe the concrete result this task must produce._

label_key("post_published") devuelve "post published" y, en general, label_key produce la misma clave que normKey para letras, dígitos, espacios, guiones bajos y puntuación.

## Scope

_State what is in scope and what is out of scope._

Entra: cambiar la expresión de label_key en src/sldb/api/matching/atom_keys.py para que "_" cuente como separador con exactamente re.sub(r"[\W_]+", " ", texto), conservando el resto del pipeline (minúsculas, espacios colapsados, strip). Tests nuevos en tests/matching/test_matching_explicit.py: uno con "post_published" -> "post published" y test_label_key_matches_normkey parametrizado con estos pares exactos: ("post_published", "post published"), ("Año_2024", "año 2024"), ("a-b_c.d", "a b c d"), ("  x__y  ", "x y"). Entrada en CHANGELOG.md. No entra: cambiar normalize_key ni _title_aliases del mismo archivo, tocar la plantilla JS del catálogo (vive en el repo IR), cambiar el emparejamiento difuso, ni la tarea task-el-emparejamiento-de-átomos-de-sldb-api-matching-pasa-a-su-propio-eje-y-recuperacion-vuelve-a-ser-un.

Precisiones (preflight-1): la equivalencia con normKey se exige solo para los cuatro pares listados y para letras, dígitos, espacios, guion bajo y puntuación ASCII; símbolos y emoji quedan fuera. Si algún golden de tests/matching/ cambia, se compara su diff: si las únicas diferencias son "_" convertido en espacio, se actualiza el golden; si hay cualquier otra diferencia, no se toca y la tarea se detiene con el diff en el informe.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/matching/atom_keys.py (label_key, línea 14-16) y sus usos con grep "label_key" en src/sldb. 2) Cambiar el regex a [\W_]+. 3) Agregar los tests en tests/matching/test_matching_explicit.py. 4) Correr tests/matching/ completo para ver que ningún golden de emparejamiento dependía del guion bajo; si alguno cambia, ajustar el golden solo si el cambio es exactamente la separación de "_".

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/

## Done When

_Name the observable condition that makes the task complete._

TMPDIR=/dev/shm pytest -q tests/matching/ pasa, incluido el test nuevo label_key("post_published") == "post published"; CHANGELOG.md tiene la entrada; commit con esos archivos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

