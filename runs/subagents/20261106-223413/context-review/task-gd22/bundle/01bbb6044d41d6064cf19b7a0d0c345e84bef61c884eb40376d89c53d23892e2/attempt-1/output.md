## REFORMULACION

Encargo: implementar en sldb el nodo GD22, executable `task.code`, no agregado. Propósito: exponer referencias entrantes y su reescritura atómica. Resultado: `sldb.api.referrers(store, target)` y `sldb.api.rewrite_references(...)` con `RewriteReport`; CLI `sldb edges referrers|rewrite`; `GET /edges/referrers` y `POST /edges/rewrite`; tests, `docs/architecture/references.md` y `CHANGELOG.md`. Repo: sldb, worktree de robocop2 separado del de grafo-operable. Límites: no editar `payload_save_steps.py`, no borrar prosa, no retirar código de deskops, no inventar API de graph-operable, cambios aditivos y genéricos.

## AMBIGUEDADES

1. `files:` incluye `- src/sldb/api/edges/rewrite_report.py`, `- src/sldb/api/edges/rewrite_values.py`, `- src/sldb/cli/commands/edges_rewrite.py`, `- src/sldb/cli/serve/edges_rewrite_routes.py`, pero `OUTPUT_SCOPE:` enumera solo `src/sldb/api/edges/referrers.py, src/sldb/api/edges/rewrite_references.py, ... src/sldb/cli/commands/edges.py, src/sldb/cli/serve/edges_routes.py`. Obliga a inventar qué archivos están autorizados.
2. `CLI ... con envelope` frente a `el cuerpo de POST /edges/rewrite y GET /edges/referrers es el mismo JSON que la CLI con --format json (igualdad de datos, sin envelope)`. Obliga a inventar la forma de salida CLI y HTTP.
3. `la reescritura ... pasa por transaction.update ... las reglas on_write ... se evalúan` frente a `--dry-run no cambia ningún byte`. Obliga a decidir si dry-run valida modelo/on_write o solo calcula el reporte.
4. `conserva la forma del valor original (p. ej. prefijo tipo:id si el campo lo usa)` no define cómo detectar prefijo ni cómo formatear `replacement`. Obliga a inventar la regla de forma.
5. `reescribe el texto que el MentionPattern capturó, con límite de palabra` no define límite para identificadores con `:` o `-`. Obliga a inventar la semántica de frontera.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, `src/sldb/api/__init__.py`, `cli/parsers/edges.py`, `cli/commands/edges.py`, `cli/serve/edges_routes.py`, `cli/serve/routes.py`; Board, pills y atoms no vienen en el bundle (`pills: []`, `atoms: []`). Cambios previstos: `referrers.py` sobre `edges_to` y `ProjectGraph.edges_to`; `rewrite_references.py` con `transaction` de GD24 y auxiliares de valores/menciones/reporte; exports en `__init__.py`; parser y comando CLI; rutas serve; tests, doc y CHANGELOG. Dependencias: GD21 y GD24 cerrados; GO07 (`__doc_anchors__`) y GO08 (`on_write`). Validaciones futuras: los `pytest` listados, grep de genericidad, CLI contra store temporal, paridad HTTP/CLI, `test_clean_code_rules.py`, rebase y `files:` contra el diff.

## FUTURO

El supervisor decide la revisión en frío; el coordinador poda archivos autorizados no usados; deskops recibe la nota de cierre y retira su código reemplazado; la familia GD27/on_write consume la reescritura. Nada se ejecuta aquí.
