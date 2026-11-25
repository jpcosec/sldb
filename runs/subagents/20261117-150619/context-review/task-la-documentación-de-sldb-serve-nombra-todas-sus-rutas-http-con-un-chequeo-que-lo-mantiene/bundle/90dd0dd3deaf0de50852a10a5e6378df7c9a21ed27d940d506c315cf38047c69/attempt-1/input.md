FILE:desk/tasks/task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene.md
---
sldb:
  by: agent
  at: '2026-11-17T15:01:38Z'
  authority: generated
  via: save_document_payload
id: task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/user-manual.md
depends_on: []
pills: []
files:
- docs/user-manual.md
- tests/test_serve.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La documentación de sldb serve nombra todas sus rutas HTTP, con un chequeo que lo mantiene

## Rationale

_Explain why this task exists or the business driver behind it._

El documento que describe sldb serve nombra 5 de unas 45 rutas que define src/sldb/cli/serve/ (docs_routes, graph_routes, models_routes, etc.). Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Un documento de sldb lista cada ruta de sldb serve (método, path, parámetros y qué devuelve en una línea), y un test falla si una ruta del código no está en el documento o viceversa.

## Scope

_State what is in scope and what is out of scope._

Entra: encontrar el documento actual de serve (docs/user-manual.md u otro de docs/ que lo describa), completarlo con todas las rutas registradas en src/sldb/cli/serve/, y un test en tests/test_serve.py que compare las rutas registradas con las del documento. CHANGELOG. No entra: cambiar rutas.

Precisiones (coordinador, bundle-1): el destino es docs/user-manual.md §10, en una tabla con una fila por ruta y la primera columna `MÉTODO /path`. La lista del código sale de los dicts de rutas de src/sldb/cli/serve/ (routes.py y los *_routes.py) importados en el test, no de regex sobre el código fuente; la del documento sale de la primera columna de esa tabla. La afirmación de §16 sobre "los 6 endpoints HTTP" se corrige para que cite la tabla de §10. Rutas con parámetros se escriben con el path exacto que registra el código.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver cómo se registran las rutas en src/sldb/cli/serve/http_server.py y los *_routes.py. 2) Completar el documento. 3) Test. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; CHANGELOG y commit.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:docs/user-manual.md
# SLDB — Manual de usuario

Todo lo que aparece acá fue ejecutado contra un store real antes de escribirse.
Los errores que se muestran son los errores que salieron de verdad.

---

## 1. Qué es SLDB

**Un motor que mantiene un documento, una base de datos y un grafo como tres
caras de lo mismo, a partir de un solo contrato.**

Vos declarás un modelo: qué campos tiene un tipo de documento y dónde va cada uno
en la página. De ese contrato SLDB deriva:

| Cara | Para qué sirve |
|---|---|
| El documento `.md` | leerlo, editarlo, versionarlo en git |
| El store `.sldb/` | consultarlo por dirección, buscar, indexar |
| El grafo | ver qué se conecta con qué |

**Ninguna es la original.** No hay fuente y salida, no hay original y copia. Hay
un contrato y tres proyecciones equivalentes.

Si dos no calzan, no es que una mienta: es que el motor falló, y hay un
diagnóstico específico que te dice cuál y por qué.

### Qué NO es

- **No es un editor de Markdown.** El Markdown es cómo se guarda.
- **No es una base de datos con export.** No hay dos cosas que sincronizar.
- **No es un generador de documentación.** No hay "fuente" y "salida".

---

## 2. Quickstart

Siete pasos, de cero a un documento consultable.

### 2.1 · Definir el modelo

```python
# models.py
from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc

class NoteDoc(StructuredNLDoc):
    """A short note with a body and optional source."""
    __semantics__ = {"type": ["knowledge", "note"]}
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
tags: ⸢rev,list•tags⸥
source: ⸢optrev•source⸥
---

# ⸢render•title⸥

## Body

⸢rev•body⸥
""".strip()

    id: str = Field(description="Stable note id.")
    title: str = Field(description="Note title.")
    tags: list[str] = Field(default_factory=list, description="Semantic tags.")
    source: str | None = Field(default=None, description="Where this came from.")
    body: str = Field(description="The note content.")
```

`Field(description=...)` es **obligatorio**. Sin descripción el modelo ni se
define: tira `TypeError`. No es estilo, es parte del contrato.

### 2.2 · Crear el store y registrar

```bash
python -m sldb stores init --path .
# Initialized store at /tmp/manual-test/.sldb

python -m sldb models add models:NoteDoc --store .sldb --pythonpath .
# Registered 'NoteDoc'
```

### 2.3 · Crear un documento

```yaml
# payload.yaml
id: nota-uno
title: Primera nota
tags: [demo, manual]
body: |
  Esto es el cuerpo de la nota.
```

```bash
python -m sldb docs create --model NoteDoc -o notas/nota-uno.md payload.yaml \
  --store .sldb --pythonpath .
# Created and tracked 'nota-uno'
```

Resultado en disco:

```markdown
---
id: nota-uno
title: Primera nota
tags:
- demo
- manual
---

# Primera nota

## Body

Esto es el cuerpo de la nota.
```

Dos cosas que pasaron solas:

- `source` era `None` y **su línea entera desapareció**. Eso es `optrev`.
- `title` aparece dos veces en el template (`rev` en frontmatter, `render` en el
  H1) y una sola vez como dato.

### 2.4 · Leer por dirección

```bash
python -m sldb ls st --store .sldb --pythonpath .
# st.{NoteDoc}

python -m sldb get st.{NoteDoc}.nota-uno.title --store .sldb --pythonpath .
# { "result": "Primera nota" }

python -m sldb get st.{NoteDoc}.nota-uno.tags.0 --store .sldb --pythonpath .
# { "result": "demo" }
```

Las listas se direccionan por índice. Los dicts por clave. Tan profundo como
llegue el payload.

### 2.5 · Escribir por dirección

```bash
python -m sldb fields append docs/nota-uno/tags nuevo --store .sldb --pythonpath .
# Updated field payload for 'nota-uno'
```

El `.md` se reescribió solo, y ambos hashes rotaron:

```
source_hash : 5ecfa5b2… → f450d203…
content_hash: ce2d3ad6… → baf72f1d…
```

**Nunca abrís el archivo para leer o cambiar un valor.**

---

## 3. Los marcadores

El template decide qué es cada campo.

| Marcador | Significa |
|---|---|
| `⸢rev•campo⸥` | va y vuelve. Es dato editable. |
| `⸢optrev•campo⸥` | igual, pero un valor `None` **puede borrar la línea entera** |
| `⸢render•campo⸥` | solo de ida. Se ve, no se extrae. |
| `⸢py•expr⸥` | expresión calculada al renderizar |

Traits: `⸢rev,list•tags⸥`, `⸢rev,markdown•description⸥`, `⸢rev,dict•meta⸥`.

### `optrev` con precision

La linea se borra **solo** si se cumplen las dos condiciones:

1. el valor es `None` - no cadena vacia, no `[]`, no `{}`
2. el marcador esta solo en su linea, o en la forma `clave: <optrev:clave>`

En cualquier otro caso el marcador se reemplaza por texto vacio y la linea
sobrevive:

| Valor | Que pasa |
|---|---|
| `None`, marcador solo en su linea | la linea desaparece |
| cadena vacia | renderiza `source: ''` - la linea queda |
| `[]` / `{}` | renderiza vacio - la linea queda |
| cualquiera, marcador compartiendo linea | se reemplaza por vacio, la linea queda |

Lo ultimo aplica a celdas de tabla, bullets y marcadores con texto al lado.

### Error real: un campo que solo es `render`

Primer intento del quickstart, con `title` únicamente en el H1:

```
title
  Field required [type=missing, input_value={'id': 'nota-uno', ...}]
```

El campo existía en el payload, pero `render` **no se extrae de vuelta**. Al
verificar el round-trip, `title` no aparecía. Un campo que es dato necesita una
declaración `rev` en algún lado.

---

## 4. El store

### Anatomía

```
.sldb/                                 ← se versiona entero en git
├── store.yaml                         ← la declaración del store
└── core/
    ├── store_index.yaml               ← modelos registrados
    ├── models/<Modelo>.yaml           ← el nodo del modelo: hashes y conteo
    └── documents/<Modelo>/<doc>.yaml  ← un archivo por documento
.sldb_cache/                           ← hermana de .sldb/, ignorada por git, se puede borrar
├── sections/       ← secciones por documento
├── edges/          ← shards del grafo
├── semantic/       ← indice semantico
├── graphs/         ← grafos generados (selfdoc)
├── locks/          ← exclusion mutua
├── edges.yaml      ← indice raiz de aristas
└── semantic_dag.yaml
```

(Hasta el 2026-11-04 la caché era `.sldb/runtime/`, con un `journal/` que ya no existe:
`sldb stores migrate-layout` la mueve. El pasado del store se consulta con
`sldb docs history <doc>`.)

**`.sldb` es estado, `.sldb_cache` es caché.** Si la caché se corrompe,
`stores build` (o `stores update`) la rehace desde los documentos.

Un archivo por documento ("shard"): dos ramas de git que tocan documentos
distintos no chocan.

### Qué guarda de un documento

```yaml
name: nota-uno
path: notas/nota-uno.md
source_hash: f450d203…
content_hash: baf72f1d…
semantic_tags: [demo, manual, type.knowledge.note, ...]
```

**No guarda el contenido.** Guarda dónde está, cómo verificarlo y cómo
encontrarlo.

### Los cuatro hashes

| Nombre | Alias viejo | Firma | Se mueve cuando |
|---|---|---|---|
| `store_hash` | `hash_a` | el store entero | cualquier write |
| `model_hash` | `hash_b` | un modelo | cualquier write de ese modelo |
| `source_hash` | `hash_c` | el **texto** markdown | cualquier reescritura |
| `content_hash` | `hash_d` | el **payload extraído** | solo si cambian los campos |

`model_hash` no es una hoja: se compone de **dos hijos** que se guardan por
separado en `ModelsIndex` justo para poder atribuirle la culpa a uno:

```
model_hash = hash(contract_hash + roster_hash)
```

| Hijo | Firma | Se mueve cuando |
|---|---|---|
| `contract_hash` | los campos del modelo (nombre, tipo, descripción) **+ el template** | tocás el modelo |
| `roster_hash` | la lista de documentos `(nombre, source_hash, content_hash)` | agregás, sacás o cambiás un documento |

Por eso `stores check` puede decirte "se movió el contrato" en vez de reportar un
mismatch pelado. Y por eso un campo agregado a la clase mueve el nodo del modelo
aunque ningún `.md` se haya tocado: el mismo texto ahora extrae otra cosa.

### Hash por field

Además del `content_hash`, cada documento guarda un hash **por campo**:

```yaml
content_hash: d43b4ed540a6…
field_hashes:
  id:    19eb5a8300ee…
  title: f6a129542311…
  tags:  87cff60a4a98…
  body:  1d10008a5a36…
```

`content_hash` sigue firmando el payload entero — es el token de concurrencia
optimista de `/save`. `field_hashes` va **al lado**, no lo reemplaza ni se deriva
de él. Sirve para saber *cuál* campo se movió:

```
what : fields changed under the model's contract (a real data change) … [fields: title]
```

Un mapa **vacío** significa "no se pudo calcular" (store escrito antes de que esto
existiera, o documento que ya no extrae), **nunca** "ningún campo cambió" — eso ya
lo responde `content_hash`. Ante un mapa vacío el diagnóstico no inventa
atribución y cae al documento completo.

Ojo con los nombres: `source` es el markdown fuente, `content` es el contenido
semántico. Es al revés de lo que suena.

Las claves persistidas en disco siguen siendo `hash_c`/`hash_d`: renombrarlas
invalidaría todos los stores existentes.

`content_hash` es **función pura del payload**. Mismo payload, mismo hash.
Por eso sirve como token de concurrencia optimista.

---

## 5. Diagnóstico

La distinción entre los dos hashes de documento es todo el veredicto.

### Reformateo: texto que se mueve, campos quietos

```bash
printf '\n' >> notas/nota-uno.md
python -m sldb stores check --store .sldb
```

```
PASS: store integrity — 1 documents in 1 models — 1 reformatted (ok)
```

Un salto de línea de más cambió `source_hash`, no `content_hash`. No hay
problema.

### Cambio real de datos

```bash
sed -i 's/^title: Primera nota/title: Titulo cambiado a mano/' notas/nota-uno.md
python -m sldb stores check --store .sldb
```

```
FAIL: store integrity — 1 documents in 1 models — 1 damaged

NoteDoc: 1 documents
  data_mutation: nota-uno
    what    : fields changed under the model's contract (a real data change) ... `stores update` accepts it, but confirm the change was intended first
    inspect : notas/nota-uno.md
    fix     : decide first: if the edit was intended, sldb stores update; if not, restore the file (git checkout -- <path>) before updating, because the index holds the previous hash and nothing else holds the previous value
    source_hash (text)  : on disk 9e52d372344f != in index f450d203bd21
    content_hash (fields): on disk a4e646979574 != in index baf72f1d0637

next: 1 finding(s) need a decision before any command is run (see 'fix:' above).
```

(En la salida real cada campo es UNA sola linea; aca van cortados para que entren.)

No dice "corrupto". Dice `data_mutation` y **"decide first"**.

`on_disk` es lo recalculado del archivo ahora. `in_index` es lo que el store
registró al último write. **Ninguno es autoritativo**: cuál está viejo es
justamente lo que estás averiguando.

### Documento que su modelo rechaza

Si una edición a mano deja un documento que su modelo no acepta (un validador
lo rechaza), `stores check` no se corta: lo nombra con el error
`store/doc-invalid` y diagnostica el resto del store.

```
error: [store/doc-invalid] Memo:a: invalid: Memo rejects a.md: 1 validation error(s); first: status: Value error, status bad is not a status
```

El mensaje trae la primera línea de hasta tres errores de pydantic, sin la URL
de errors.pydantic.dev. En el JSON el documento sale con `note: doc_invalid` y
el hallazgo en `errors`; el comando sale con exit 1. Cada documento inválido
aparece **una sola vez**: no pasa por las otras comprobaciones que extraen con
el modelo (campos, ruido estructural, pérdida por reescritura). El arreglo es
editar el archivo hasta que el modelo lo acepte y correr `sldb stores update`,
o `sldb docs untrack <name>` si sobra.

Un documento inválido tampoco frena las escrituras de sus vecinos: un `untrack`
o una escritura de otro documento del mismo modelo, aun con el caché frío de un
clon limpio, lo saltea al reconstruir las aristas (no aporta aristas
declaradas) y le deja los tags que tenía.

---

## 6. El grafo

### Cómo se generan las aristas

Cinco fuentes, y **solo cinco**:

1. **Estructura** — todo documento aporta su nodo, sus secciones y sus tags
2. **Documentos especiales** — `RelationTypeDoc`, `RelationDoc`, y documentos
   con tag de anchor
3. **Modelos** — cada modelo aporta su nodo, un nodo por campo, `has_field`,
   `extends`
4. **Referencias declaradas** — `__references__` aporta `references` y
   `__containment__` aporta aristas contains, una por id, con el nombre del
   campo en la arista
5. **Composiciones** — `__compositions__` aporta `composes`, una arista por ref,
   con el campo compuesto, el campo que guarda los refs y el ref tal como fue
   escrito

Las tres últimas son `origin: "schema"`, igual que `has_field` y `extends`:
apuntar a un documento que no está trackeado se descarta en `resolve_edges` en vez
de reportarse, porque el modelo declaró una forma y no una aserción autoral. Un
documento especial no aporta referencias declaradas: sus campos de id ya son la
arista que ese documento contribuye.

> **Cuidado:** el id declarado se escribe `Modelo:nombre`. Un nombre pelado es
> ambiguo entre modelos y se omite en vez de adivinarlo, así que un campo de
> `__references__` que guarde rutas no produce aristas.
>
> También se exponen por HTTP: `/schema` devuelve los dos; `fields_routes` expone
> únicamente `__references__`, como `is_reference`.

Un ref de composición sí es una ruta del proyecto, no un id. Qué documento es
dueño de una ruta no lo sabe un shard solo, así que la arista se emite con la ruta
en `metadata["ref_path"]` y el target se resuelve al componer el índice, donde ya
viven las reglas que cruzan documentos. `./sub/a.md` y `sub/a.md` son el mismo
documento; una ruta de la que nadie es dueño no deja arista.

Eso es lo que hace que el radio de impacto recorra la composición: con
`edges to` sobre un hijo salén los padres que lo componen y que quedaron rancios
al cambiarlo.

### Los nodos tienen tipo

```
sldb://document/NoteDoc:nota-uno
sldb://section/NoteDoc:nota-uno#body
sldb://model/NoteDoc
sldb://semantic_tag/type.knowledge.note
sldb://anchor/...
```

**Las secciones son nodos.** Por eso podés citar un fragmento, no solo un
archivo.

### Registrar el vocabulario

```bash
python -m sldb edges init --store .sldb --pythonpath .
# Initialized relations: models added: 2 · builtin relation types written: 11
#                        · predicates added: 11
```

Los 11 builtin: `has_document`, `has_section`, `has_field`, `has_model`,
`extends`, `tagged_as`, `names`, `applies_to_source`, `applies_to_target`,
`semantic_parent`, `semantic_equivalent`.

### Declarar un tipo de relación nuevo

Un tipo de arista **es un documento SLDB**:

```yaml
# rt.yaml
title: Comments On
name: comments_on
direction: directed
cardinality: many_to_one
axis: WHAT
source_types: [LinkedDoc]
target_types: [NoteDoc]
condition: ""
description: One note commenting on another.
```

```bash
python -m sldb docs create --model RelationTypeDoc -o rel/comments-on.md rt.yaml \
  --store .sldb --pythonpath .
# Created and tracked 'comments-on'
```

| Campo | Qué define |
|---|---|
| `name` | el verbo que llevará cada arista |
| `direction` | dirigida, o no dirigida (se materializa en ambos sentidos) |
| `cardinality` | validado al ingerir |
| `source_types` / `target_types` | qué modelos puede conectar |
| `axis` | eje predicativo: WHAT, WHY, HOW, WHERE, WHEN, PROVENANCE |
| `condition` | condición que heredan todas las aristas del tipo |

Las relaciones internas de SLDB también son `RelationTypeDoc`. **El grafo se
describe a sí mismo con el mismo mecanismo que usás vos.**

### Crear una arista

```yaml
# ed.yaml
title: enlace-uno comenta nota-uno
source_id: LinkedDoc:enlace-uno
target_id: NoteDoc:nota-uno
relation_type: comments_on
condition: ""
notes: Creada a mano para el manual.
```

```bash
python -m sldb docs create --model RelationDoc -o rel/edge-uno.md ed.yaml \
  --store .sldb --pythonpath .
python -m sldb edges rebuild --store .sldb --pythonpath .
```

Consultarla — **por node id, no por nombre de documento**:

```bash
python -m sldb edges show "sldb://document/LinkedDoc:enlace-uno" --store .sldb
```

```json
{
  "metadata": {
    "origin": "relation_doc",
    "relation_doc": "edge-uno",
    "condition": "",
    "axis": "WHAT"
  }
}
```

El `axis: WHAT` no estaba en la arista: **se heredó del tipo**.

### Análisis

```bash
python -m sldb graph path "sldb://document/LinkedDoc:enlace-uno" \
                         "sldb://document/NoteDoc:nota-uno" --store .sldb
# ["sldb://document/LinkedDoc:enlace-uno", "sldb://document/NoteDoc:nota-uno"]

python -m sldb edges check --store .sldb
# Edges OK
```

Doce comandos disponibles:

| Comando | Qué responde |
|---|---|
| `neighborhood` | vecinos hasta profundidad N |
| `path` | cómo se conecta A con B |
| `cycles` | ciclos donde debería ser un DAG |
| `order` | orden topológico de dependencias |
| `components` | qué anda junto y qué quedó suelto |
| `central` | de qué nodos depende el resto |
| `similar` | qué se parece a esto, por destinos compartidos |
| `snapshot` | exportar o cargar el grafo portable |
| `get` | un nodo del índice |
| `list` | todos los node ids |
| `query` | consulta estructurada desde un JSON |
| `ingest-sldb` | convertir un export semántico a node-link JSON |

Corre sobre networkx. PageRank pide scipy aparte.

---

## 7. Qué se puede representar

`StructuredNLDoc` declara dos ejes:

```python
__semantics__ = {
    "representation": ["markdown"],      # cómo se guarda — siempre markdown
    "source": ["document", "markdown"],  # qué describe — cualquier cosa
}
```

**El Markdown es el formato, no el tema.** Un subclase cambia `source` cuando
describe código, datos u otra fuente.

Modelos que vienen con SLDB:

| Modelo | `source` | Qué representa |
|---|---|---|
| `PythonSymbolDoc` | `code, python` | una función o clase |
| `CliCommandDoc` | — | un comando de CLI |
| `SurfaceDoc` | — | un subsistema completo |
| `RelationTypeDoc` | — | un tipo de arista |
| `RelationDoc` | — | una arista concreta |
| `AnchorDoc` | — | un alias de pron: una palabra y lo que nombra; resuelve pero no verifica (ver [anclaje](architecture/anchoring.md)) |
| `KnowledgeTag` | — | vocabulario |

Por eso SLDB se auto-documenta: hay un adaptador que lee argparse y genera
`CliCommandDoc`.

**El patrón:** cualquier cosa que puedas describir con campos estables se puede
representar.

---

## 8. Herencia

Los modelos heredan como clases pydantic normales. Ejemplo tomado de una KB
real (`knowledge_antonia-cobranza`); los modelos son del consumidor, no de SLDB:

```
DomainAtom → IndexProxies → StructuredNLDoc

DomainAtom   aporta: id, title, five_wh_one_plus, answer, tags, domain_ref, provenance
IndexProxies aporta: summary, summary_en
```

Y la herencia es **consultable**:

```bash
python -m sldb ls "st.{IndexProxies+}" --store .sldb --pythonpath .
```

El `+` significa "este modelo y todos sus descendientes". Recorre el MRO, así que
la clase base **ni necesita estar registrada**.

---

## 9. Proyección y composición

Dos ideas distintas que conviene no mezclar.

### Proyección — lo mismo desde otro ángulo

- **Las tres caras**: documento, store, grafo
- **`render` vs `rev`**: `title` vive en frontmatter y se proyecta al H1
- **`IndexProjection`**: qué documentos admite un consumidor y cómo lee el texto
  representativo de cada uno

`IndexProjection` tiene un detalle importante: `text_id` nombra la forma de leer,
*"so a change of representation invalidates the index the same way a change of
embedder does"*. Si cambiás qué parte del documento considerás "el texto", el
índice queda inválido. Por eso una cita nunca queda huérfana.

- **`FieldProjection`**: lo mismo, un piso más abajo — qué *fields* de cada
documento se indexan (por defecto excluye identidad y bookkeeping: `id`, `name`,
`slug`, `path`, `tags`, hashes) y cómo se lee el texto de uno.

Cada field es una unidad de indexación propia: dirección
`docs/<Modelo>/<doc>/<campo>` — la misma que acepta `sldb fields` — y hash de ese
field (`DocumentEntry.field_hashes`), no el del documento entero. Es el mismo
índice con clave más fina: editar un campo de un documento de cuarenta re-embebe
uno.

### Composición — varios documentos en uno

| Mecanismo | Qué hace | Vuelta atrás |
|---|---|---|
| `__compositions__` | un campo se arma formateando documentos hijos | ❌ |
| `![[transclusión]]` | expande el texto de otro documento | ❌ |
| `[[link]]` | referencia, no expande | — |

**Límites conocidos, documentados en `composition_modes.md`:**

- No hay edit-through: no se puede editar el hijo desde donde está compuesto
- No hay composición por query: `source_field` exige lista explícita de rutas

---

## 10. Las tres APIs

### CLI

`python -m sldb ...` — para humanos y scripts.

### Python (`sldb.api`) — la preferida para integrar

> *"the store, model and document operations the CLI performs, **as functions**.
> Consumers call these instead of instantiating `sldb.cli` command classes with
> fake argparse namespaces."*

- devuelve **modelos pydantic**, no imprime
- **lanza excepciones**, no hace `exit`
- capas: `cli → api → store/runtime/core`; nada en `api` importa `cli`

### HTTP (`sldb serve`)

`/document/ir`, `/save` (con `expected` → **409** en conflicto), `/edges/node`,
`/graph/*`, `/find`, `/models/detail`.

### Primitivos sueltos

```python
from sldb import AST_Handler, TemplateExtractor, DataExtractor, SLDBRenderer
```

Round-trip puro, sin store. Es lo que usan `render` / `extract` / `validate`.

---

## 11. Los cinco niveles de extender

| Nivel | Qué hacés | Requiere |
|---|---|---|
| 1 | Definir modelos | heredar de `StructuredNLDoc` |
| 2 | Declarar vocabulario: relaciones, predicados, DAG de tags | **escribir documentos** |
| 3 | Declarar consumo: `IndexProjection` | Python simple |
| 4 | Adaptadores de fuente (como `selfdoc`) | Python |
| 5 | Handlers de render (`list`, `table`, `yaml`, `python_expr`) | tocar el motor |

**La regla que se repite en todos: extendés declarando, no escribiendo
procedimientos.**

---

## 12. Ciclo de vida del contrato

Cambiar un modelo no es editar el `.py` y listo:

```
draft → validate → promote → stores update
```

```bash
python -m sldb models template edit <Modelo> --input tpl.md --store .sldb --pythonpath .
python -m sldb models fields add <Modelo> <campo> --type str --description "..." \
  --store .sldb --pythonpath .
python -m sldb models validate <Modelo> --store .sldb --pythonpath .
python -m sldb models validate <Modelo> --promote --store .sldb --pythonpath .
python -m sldb stores update --store .sldb --pythonpath .
```

(Si tenés el binario instalado, `sldb ...` es equivalente a `python -m sldb ...`.)

Porque cambiar el contrato cambia **las tres caras a la vez**, y hay documentos
existentes que tienen que seguir cumpliéndolo.

---

## 13. Fricciones operativas

Cosas que cuestan tiempo la primera vez:

- **`--store` quiere la ruta a `.sldb`**, no el directorio que lo contiene
- **`edges rebuild` dice `0 shard(s) written` cuando ya está todo hecho.** Es
  caché, no falla: revisá `.sldb_cache/edges/`.

---

## 14. Límites conocidos

- **Sin id estable de sección.** Se direccionan por slug jerárquico; headings
  repetidos se desambiguan por orden de aparición. Mover una sección cambia su
  dirección.
- **Composición de una sola vía.** Sin edit-through, sin composición por query.
  Lo que sí hay es la arista: `__compositions__` aporta `composes` (§6), así que el
  radio de impacto sí recorre la recursión, aunque escribir sobre la salida
  compuesta siga sin propagarse al hijo.
- **`Corpus` sí se exporta en `sldb.api`**, con `rank_fields()` para rankear
  campos. Lo que sigue sin cliente de CLI es el ranking: ni `rank()` (documento)
  ni `rank_fields()` (campo) tienen comando. Se integran por Python.
- **El índice de embeddings tiene dos granularidades.** La de documento
  (`Corpus.index`, clave = documento + su `content_hash`) y la de campo
  (`Corpus.field_index`, clave = `docs/<Modelo>/<doc>/<campo>` + el hash de ese
  field). La de campo vive en su propio archivo derivado
  (`fields.<text_id>.<embedder>.json`), nunca comparte con `docs.*`. Un field de
  un documento de cuarenta se re-embebe solo: medido `embedded=1, reused=3`.
  `api/matching/document_index.py` no cambió — ya keyeaba por hash.
- **Las secciones no tienen hash propio.** `DocSections` se estampa con el
  `source_hash` del documento padre: es clave de caché, no un nivel del Merkle.
  Si el documento cambia, todas sus secciones se reprocesan.

---

## 15. Anti-patterns

- **No edites a mano un documento trackeado.** Usá `fields` o la API.
- **No reimplementes composición, resolución de referencias, round-trip ni
  índice inverso.** SLDB ya los tiene.
- **No compares ids como strings.** Preguntale al grafo.
- **No infieras el contrato leyendo los artefactos de salida.** Leé el modelo.
- **No inventes jerarquía entre las tres caras.** Si divergen, es un bug con
  diagnóstico, no una decisión de diseño.
- **Si falta algo, registrá el gap** en vez de hacer un workaround local.

---

## 16. Verificacion de este manual

Todo el contenido fue ejecutado contra stores reales antes de escribirse, y
despues auditado por tres revisores independientes que re-verificaron cada
afirmacion contra `src/sldb/`.

Correcciones que salieron de esa auditoria:

| Seccion | Estaba mal | Ahora |
|---|---|---|
| 3 | "optrev borra la linea si queda vacio" | solo con `None` y en dos formas concretas |
| 4 | `runtime/cache/` en el arbol | no existe: los caches viven en `$XDG_CACHE_HOME/sldb` |
| 4 | `core/models/` = "documentos del modelo" | es el nodo del modelo: hashes y conteo |
| 5 | salida de `stores check` cortada en varias lineas | una linea por campo, con `(see 'fix:' above)` |
| 6 | tabla de 8 comandos de graph | son 12: faltaban `get`, `list`, `query`, `ingest-sldb` |
| 6 | "`__containment__`/`__references__` se exponen por /schema y fields_routes" | `fields_routes` solo expone `__references__` |
| 6, 14 | "`__containment__`/`__references__` no generan aristas" | sí las generan (references y contains, `origin: "schema"`): cuarta fuente del grafo |
| 6, 14 | "`__compositions__` no llega al grafo" | ya llega: aporta `composes`, con el target resuelto de ruta a documento al componer el índice |
| 13 | "resuelve por el `path` absoluto" | el path suele ser relativo y se re-ancla al project root |
| 14 | "`Corpus.rank()` no esta en el CLI" | y no se exportaba en `sldb.api`. Ya se exporta, con `rank_fields()`; lo que falta es el comando de CLI, no el cliente |
| 14 | "el indice de embeddings es por documento, no por campo" | tiene dos granularidades: `index` (documento) y `field_index` (`docs/<Modelo>/<doc>/<campo>`, con el hash del field) |
| 4 | los 4 hashes como si `model_hash` fuera hoja | `model_hash` se compone de `contract_hash` + `roster_hash`, guardados por separado |
| 4 | nada sobre granularidad por campo | `field_hashes` por documento, y que un mapa vacio es "no se pudo calcular" |
| 13 | ninguna friccion de performance | los dos re-parseos evitables de `validation.py` y `section_rebuild.py` |
| 13 | `models template show` fallaba si el `path` guardado no era un archivo aquí | busca el fuente importando el `model_ref`, y si tampoco importa nombra el modelo y el store |
| 13 | `ast show` con warnings antes del JSON; `--format json` rechazado por `models show`, `models template show` y `docs update`; `edges show` con un nombre de documento devolvía `[]`; los dos re-parseos | resueltos (2026-10-18): stdout limpio, `--format` en los tres (y un flag desconocido muestra el uso del subcomando), `edges show` rechaza lo que no es un nodo y sugiere el export id, template memoizado y un solo `MarkdownIt` |
| 14 | nada sobre los limites de indexacion | el indice de embeddings tiene granularidad de documento y de campo; las secciones no tienen hash propio |

Verificado en vivo y sin cambios: los 4 hashes y sus alias, `Field(description)`
obligatorio, `render` no se extrae, los 11 relation types builtin, los campos de
`RelationTypeDoc`, `{Modelo+}` recorriendo el MRO sin registrar la base, la cita
de `text_id`, los limites de composicion, los 6 endpoints HTTP, `/save`
devolviendo 409 real ante `expected` distinto, y las 5 fricciones de la seccion
13.

FILE:instruccion
Cold-bundle de la tarea task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

