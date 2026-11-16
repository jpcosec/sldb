# Resultado — executor deskops-e-ca9ebf095f85

Tarea: `task-referrers-y-rewrite-references-aceptan-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-duplican-men`
Base: HEAD `7cd8a5e3`. Sin commit ni push (los hace el coordinador).

## Estado: LISTO con rc 0 (después de la Corrección 1; el envío original era rc 1, ver abajo)

Los cuatro casos nuevos y el resto de `test_referrers.py` pasan (12/12, rc 0). En `test_rewrite_references.py` pasan los casos nuevos (3) y 13 de los existentes; **5 de los existentes fallan, y ya fallaban en HEAD antes de esta tarea**. La causa es el commit `e82d62ba` ("create_document pinnea las anclas…"), no este cambio (ver "Regresión previa"). No los corregí porque esa regresión es de otra tarea y queda fuera del alcance de este contrato.

## Cambios

### `src/sldb/api/edges/referrers.py`
- `referrers(store, target, pythonpath=None, *, graph: ProjectGraph | None = None)`: si se pasa `graph`, se usa en lugar de `optional_graph(...)`. Ese grafo sirve tanto para resolver el target como para `find_hits`.
- `find_hits`: los hits schema van primero, como antes. Las menciones se filtran (H-c): se descarta una mención cuya ruta es la de un documento con hit schema (export id → ruta con `document_paths`) y cuya línea cae dentro del frontmatter de ese documento. El frontmatter se lee solo si hay solapamiento entre ambos.
- Funciones nuevas:
  - `document_paths(store_path)`: devuelve `{Model:name: ruta trackeada}` a partir de `indexed_documents`.
  - `frontmatter_lines(file)`: devuelve `range`, desde la línea 1 `---` hasta el siguiente `---`, ambas incluidas y numerando desde 1.
  - `_in_frontmatter(referrer, frontmatters)`.
- Docstring del módulo actualizado.

### `src/sldb/api/edges/rewrite_references.py`
- `rewrite_references(..., graph: ProjectGraph | None = None, excluded_sources: Iterable[str] = ())`, ambos keyword-only. Si se pasa `graph`, reemplaza a `optional_graph`.
- Función nueva `excluded_paths(location, graph, sources)`: resuelve cada fuente con `resolve_target` y la compara por ruta trackeada. Si una fuente no resuelve, se propaga el `SLDBDocumentTargetError` de `resolve_target` ("Unknown document target: …"). Si resuelve solo a un nodo del grafo sin documento trackeado (`path is None`), lanza `SLDBDocumentTargetError("Excluded source is not a tracked document: …")`.
- Después de `_grouped`, se filtran `fields` (el export id se mapea a ruta con `document_paths`) y `mentions` (por ruta). La planificación (`plans`, `texts`) y `_write` trabajan sobre lo ya filtrado, así que una fuente excluida no se lee para escribir ni aparece en `changed` ni en `skipped`.
- Docstrings actualizados.

### Tests
- `tests/api/test_referrers.py`: nuevo fixture `desk` (clase `Desk`) con el desk mínimo de la nota y del pill:
  - modelos `Atom` y `Task` (`Task.depends_on` es una referencia a `Atom`);
  - un `ProjectGraphConfig` `DESK_CONFIG` con superficies `atom` (`desk/atoms`, identity `document_id`) y `task` (`desk/tasks`);
  - una `LineMentions` sobre `task` con el patrón `(?i)atom:(?P<id>[a-z0-9-]+)` → `atom:{id}`;
  - el archivo sin trackear `desk/tasks/task-ref.md`, cuya línea 3 dice "Depends on atom:atom-a.";
  - sin `project_graph` en `store.yaml`. El grafo se arma con `ProjectGraph(root, DESK_CONFIG)`, como en `test_project_graph.py`.
  - Casos nuevos:
    - `test_a_graph_built_in_process_gives_the_mentions_the_store_does_not_declare` (H-a): sin `graph` devuelve `[]`; con `graph` devuelve la mención `desk/tasks/task-ref.md:3`.
    - `test_a_declared_field_is_one_schema_referrer_not_also_a_frontmatter_mention` (H-c): `task-b` tiene `depends_on: [Atom:atom-a]`. El test comprueba que el grafo sí tiene la arista de mención desde `task-b.md` y que `referrers` devuelve el campo una sola vez, como schema, más la mención de `task-ref.md`.
  - Control negativo, corrido aparte en el scratchpad y no versionado: con `_in_frontmatter` parcheado a `False`, el test H-c falla.
- `tests/api/test_rewrite_references.py`: se importan `Desk` y `desk`.
  - `test_an_excluded_source_is_left_byte_for_byte_and_the_rest_is_rewritten`, parametrizado con `Task:task-b` y `desk/tasks/task-b.md` (H-b, con `graph` en proceso): `task-b.md` queda byte a byte igual, `task-c` pasa a `Atom:atom-b` y la mención de `task-ref.md` también se reescribe. Las líneas de frontmatter de `task-b` y `task-c` no generan una reescritura de mención duplicada (H-c).
  - `test_an_excluded_source_that_names_no_tracked_document_is_refused`.

### `CHANGELOG.md`
- Una línea en español bajo `## 0.1.13 — not released yet`, primera de la lista, con el estilo de las entradas vecinas.

## Done When
- **"Los dos archivos pasan con los tres casos nuevos"**: los casos H-a, H-c y H-b (este último ×2 por parametrización, más el caso de fuente inválida) pasan. `test_referrers.py` da rc 0. `test_rewrite_references.py` da rc 1 solo por las 5 fallas previas descritas abajo.
- **"Sin graph ni excluded_sources el comportamiento es el de hoy"**: los 10 tests existentes de `test_referrers.py` siguen verdes, entre ellos `EXPECTED`, el que verifica que no se recorre el proyecto en caliente y el de la CLI. En `test_rewrite_references.py`, los existentes dan el mismo resultado que en HEAD: 13 pasan y 5 fallan, exactamente los mismos 5.
- **"CHANGELOG, commit y aviso a deskops"**: el CHANGELOG está hecho. El commit lo hace el coordinador con `deskops closeout commit`. El aviso a deskops también va en el cierre, porque su cuerpo lleva el commit y yo no tengo hash. Texto propuesto:
  - Título: el de la tarea.
  - Cuerpo: "referrers(store, target, *, graph=g) y rewrite_references(..., graph=g, excluded_sources=[...]) ya existen en sldb; find_hits no devuelve como mención una línea del frontmatter de un documento que ya es hit schema. deskops puede borrar _rewrite_mentions y _in_frontmatter de deskops/services/references.py y llamar a la API pública. Commit: <hash>."

## Comandos corridos (la salida completa está en `validation.log`)
| Comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py` | 0 (12 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py` | 1 (16 passed, 5 failed; ya fallaban antes) |

`uv` funcionó; no hizo falta el fallback de `uvx`.

## Regresión previa (fuera del alcance, la anoto con evidencia)
Estos 5 tests de `tests/api/test_rewrite_references.py` fallan:
- `test_rewriting_to_another_document_moves_every_field_and_mention_keeping_their_forms`
- `test_removing_empties_the_scalar_drops_the_element_and_keeps_the_prose`
- `test_a_dry_run_reports_the_same_changes_writes_no_byte_and_runs_no_on_write_rule`
- `test_with_the_index_and_the_graph_warm_a_dry_run_walks_nothing`
- `test_the_cli_rewrites_removes_and_dry_runs_with_the_envelope`

Las 5 tienen la misma causa: `A2_CHANGES[2]` espera `"before": "doc:Card:card-a"` para `Review:r1.subject`, pero desde `e82d62ba` `create_document` pinnea el ancla al crear y el valor real es `doc:Card:card-a@sha256:57abcf…`.

Evidencia (está al final de `validation.log`):
- Con `git archive` de HEAD `7cd8a5e3`, sin estos cambios ni los ajenos, corrido en el scratchpad: los mismos 5 fallan.
- Con `git archive` de `e82d62ba~1`: 18 passed.

`e82d62ba` no tocó este archivo de tests. Arreglarlo significa ajustar `A2_CHANGES` (y lo que se derive) al valor pinneado, o decidir que el `before` se reporte sin pin. Es una decisión de la tarea de pinneo, así que queda para el coordinador.

## Archivos tocados (exactos)
- `src/sldb/api/edges/referrers.py`
- `src/sldb/api/edges/rewrite_references.py`
- `tests/api/test_referrers.py`
- `tests/api/test_rewrite_references.py`
- `CHANGELOG.md`
- `runs/subagents/20261116-exec-referrers/validation.log` y este `result-summary.md` (entrega)

No toqué `desk/`, `.sldb/`, los cambios ajenos ni `uv.lock`. Nada se stageó.

## Desvíos y dudas
- No hubo choque entre el pill y el contrato. Para el caso H-c usé el mismo desk mínimo del pill con un `Task` trackeado. El patrón usa `(?i)` para que el valor declarado `Atom:atom-a`, que es la forma que resuelve el índice de aristas, también lo capture la mención del frontmatter y así se reproduzca la duplicación.
- Las fuentes excluidas no aparecen en `skipped` del `RewriteReport`. El contrato no lo pide y el formato no cambia.
- Una fuente excluida que resuelve solo a un nodo del grafo (no a un documento trackeado) lanza `SLDBDocumentTargetError`. Es mi lectura de "a un documento trackeado" en las Precisiones.

## Corrección 1 (pedida por el coordinador)

El coordinador confirmó que `e82d62ba` (create_document pinnea anclas) cambia el comportamiento a propósito y ya está cerrado, y pidió arreglar aquí las 5 fallas sin tocar `src/`.

- Cambio en `tests/api/test_rewrite_references.py`:
  - Helper nuevo `a2_changes(world)`: devuelve `A2_CHANGES` con el `before` de `Review:r1.subject` igual al valor pinneado que deja `create_document`. Ese valor se lee del payload de r1 (`world.payload("Review:r1")["subject"]`), no se copia un hash literal. El helper además verifica que el valor tenga la forma `doc:Card:card-a@sha256:<64 hex>`.
  - `A2_CHANGES` queda como plantilla, sin cambios.
  - Los 5 tests calculan `expected = a2_changes(reference_world)` antes de reescribir y lo usan donde antes iba `A2_CHANGES`:
    - `test_rewriting_to_another_document_…`
    - `test_removing_…` (que usa `expected[:3]` con `after: None`)
    - `test_a_dry_run_…`
    - `test_with_the_index_and_the_graph_warm_…`: aquí `expected` se calcula antes de `count_walks`, así que la lectura del payload no cuenta como recorrido.
    - `test_the_cli_rewrites_…`
- `src/` no cambió.
- Validación: la salida completa está en `validation.log`, sección "Corrección 1".

| Comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py` | 0 (12 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py` | 0 (21 passed) |

- Done When: los dos archivos de Validation pasan, con los casos nuevos incluidos, y todos los tests existentes están verdes. El commit y el aviso a deskops siguen pendientes del cierre del coordinador.
- Archivos tocados en esta corrección: `tests/api/test_rewrite_references.py`, más `validation.log` y este informe.
