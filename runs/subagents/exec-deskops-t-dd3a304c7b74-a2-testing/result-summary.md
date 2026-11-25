FALLA

# Testing (intento 2) — retiro de `incomplete` del lenguaje de predicados

- Task: `task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato`
- Commits del ejecutor en la rama `deskops/deskops-e-5cfcba8143e9-a2`:
  - `22cfafb2c29e62a391d23be53d690a21955fe0ee` — retiro de `incomplete` (commit original).
  - `50a0cd167f6b135cfda317ac41437005d20eb88c` — intento 2: doc de graph-backend, selfdoc sync y test `on_write` restaurado.
- El `git log --grep` del checkout principal devuelve `22cfafb2`; el último commit con el trailer `Task-Id` es `50a0cd16`, en el worktree del ejecutor. Probé el árbol de `50a0cd16`, que incluye ambos commits.
- Worktree: `/mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-5cfcba8143e9-a2`.

## Veredicto

**FALLA por documentación incompleta.** Las dos correcciones que pidió el intento anterior están
bien: `docs/architecture/graph-backend.md` ya no describe `incomplete` ni `metadata.unavailable`
como vigentes, la referencia de `rules explain` regenerada con selfdoc ya dice `0/1/3`, y
`test_save_document_payload_returns_the_on_write_alerts_without_a_listener` volvió a
`tests/api/test_rules.py` idéntico al original y pasa.

Queda un defecto real de la misma clase en el documento central de la tarea:

- `docs/architecture/rules-language.md:5` sigue afirmando que el contrato fija **«la semántica
  trivaluada»**. El cuerpo del mismo documento (§3, líneas 167-188) dice ahora que el lenguaje
  es **bivaluado** y que `incomplete` se retiró. La cabecera contradice al cuerpo y al Goal
  («incomplete se retira del lenguaje, de la API y de la doc»). Debe pasar a describir la
  semántica bivaluada (y, si se quiere conservar la historia, remitir a la nota de retiro de §3),
  no anunciar una semántica trivaluada como vigente.

No es un fallo de código: el retiro funcional es coherente (`git grep -n incomplete -- src/sldb`
no encuentra usos del valor del lenguaje) y todos los tests pasan.

## Validación ejecutada

No existe `/tmp/ws-venv` en este contenedor; usé el Python del venv del repo
(`/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python`, Python 3.13.18), con `TMPDIR=/tmp` y de a un
archivo. No corrí la suite completa.

| Comando | rc | Resultado |
|---|---:|---|
| `pytest -q tests/api/test_rules.py` | 0 | 13 passed (incluye el test `on_write` restaurado) |
| `pytest -q tests/api/test_rules_evaluation.py` | 0 | 13 passed |
| `pytest -q tests/test_rules_language_spec.py` | 0 | 52 passed |
| `pytest -q tests/test_predicates_cli.py` (Validation) | 0 | 4 passed |
| `pytest -q tests/test_clean_code_rules.py` (Validation) | 0 | 1235 passed |
| `pytest -q tests/store/test_predicate_language.py` | 0 | 16 passed |
| `pytest -q tests/store/test_graph_language.py` | 0 | 3 passed |
| `pytest -q tests/store/test_graph_backend.py` | 0 | 9 passed |
| `pytest -q tests/store/test_where_empty_and_errors.py` | 0 | 25 passed |
| `pytest -q tests/store/test_where_retired.py` | 0 | 4 passed |
| `pytest -q tests/api/test_rules_end_to_end.py` | 0 | 1 passed |
| `pytest -q tests/api/test_rules_linked_reach.py` | 0 | 4 passed |
| `pytest -q tests/api/test_transaction_rules_dirty.py` | 0 | 4 passed |
| `PATH=.venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast` | 1 | FAIL solo `identidad` por `workbench_demo` (excepción autorizada `f055723d`); pasan `núcleo aislado`, `capas`, `ejes` y `superficie` |
| `PATH=.venv/bin:$PATH PYTHONPATH=src python -m sldb selfdoc check` | 0 | `ok: true`, 0 alertas, 0 documentos cambiados |

## Qué falta para poder cerrar

- Corregir `docs/architecture/rules-language.md:5`: «la semántica trivaluada» → semántica
  bivaluada, con la nota de que `incomplete` se retiró (§3), y commitearlo con el trailer
  `Task-Id`.
- (No bloqueante) El `result-summary.md` del intento 2
  (`runs/subagents/exec-deskops-e-5cfcba8143e9-a2/result-summary.md`) es una lista de cambios y
  no repite la evidencia de la decisión; esa evidencia sí está en el resumen del primer intento
  (`runs/subagents/exec-deskops-e-5cfcba8143e9/result-summary.md`). Si el desk solo lee el run
  a2, conviene enlazarla o repetir el grep y el caso real.
- (No bloqueante) `src/sldb/api/where.py:59-60` quedó con un salto de línea y un punto
  descolgados en el docstring (`... `holds` is `true`\n   . Its finding ...`); no afecta tests ni
  comportamiento, pero es formato descuidado.
