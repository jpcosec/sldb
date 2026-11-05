# Coordinator status (robocop2) — 2026-11-04

## Nodo GO02 — Semántica, gramática y firma de evaluación del lenguaje de reglas

- Rama: `wt/go02` (desde main `14575b02`). Worktree: `~/proyectos/SLDB_1/sldb-wt-go02`.
- TaskDoc: `desk/tasks/task-go02-semantica-gramatica-y-firma-de-evaluacion-del-lenguaje-de-reglas.md` (preflight intento 2 y cold-bundle intento 1 ya dispuestos en main; sin tercer intento).
- Worker: pi deepseek-flash (herdr), con dos dispatches: el encargo y una ronda de correcciones del coordinador.

### Commits
- `8ffb141f` docs: fijar gramática y semántica del lenguaje de reglas
- `d24a2af7` docs: registrar hipótesis del ejecutor en el TaskDoc de GO02
- `eb665eae` docs: corregir tabla trivaluada y acotar explicación al envelope
- (este commit) coordinator-status.md

Archivos: `docs/architecture/rules-language.md` (nuevo), `tests/test_rules_language_spec.py` (nuevo), TaskDoc (solo se añade `## Hipótesis del ejecutor (2026-11-04)`). No se toca `src/` ni `dag.yaml`.

### Aceptación, línea por línea
| Criterio (dag.yaml rev 9, GO02) | Evidencia |
|---|---|
| El documento existe | `docs/architecture/rules-language.md`, 8 secciones `## ` (gramática, caminos, semántica, explicación, hash de contrato, firma eval, tabla de equivalencia, hipótesis) |
| Cada construcción de (a) y (b) con ejemplo y resultado esperado | §1: tablas para precedencia, paréntesis, = != < <= > >=, in (lista/subcadena/otro tipo/lista literal), ~, regex inválida, model <=, has, nonempty. §2: paso por campo, campo no declarado = vacío, rel:tipo, ^campo, any/all/none, clausura +, clausura con ciclo, count, sustitución {campo} (presente, ausente, no escalar, dentro de literal), doc inexistente omitido, store no disponible = incomplete |
| Incluidos regex inválida y clausura con ciclo | §1 fila `title ~ "("` → WherePredicateError; §2 `count(depends_on+: has(status)) = 2` con A→B→C→A |
| La tabla cubre los 19 operadores | §7: filas 1–19 (has, nonempty, in, ~, model <=, = != < <= > >=, eq, ne, gt, lt, contains, starts_with, is_null, is_not_null); los nombres viejos no se usan como operadores nuevos |
| El ejemplo de regex inválida espera WherePredicateError | `test_invalid_regex_raises_where_predicate_error` (importa `WherePredicateError` de `where_parse`) |
| Tabla trivaluada: and, or, not, any, all, none y comparación con count | §3: tabla and/or (9 filas), not, cuantificadores con columnas excluyentes (verificadas celda a celda por el coordinador; la primera versión tenía columnas ambiguas y se corrigió en `eb665eae`) y tabla de `count(c: p) cmp n` |
| Sintaxis de caminos (campo, rel:tipo, ^) con un ejemplo cada una | §2 filas "paso por campo", "rel:<tipo>", "^campo" |
| __contract__, orden canónico y firma de eval definidos | §5 (ausente = todos, [] = error al cargar, campo ausente `<campo>=`, orden por bytes UTF-8, sha256, `\n` sin salto final); §6 (eval, dominio, model <= anidado, intersección p5) |
| Ejemplos como tests xfail (no skipped) hasta GO05 | `pytest tests/test_rules_language_spec.py -q -rxs` → `52 xfailed, 1 warning` (0 skipped, 0 failed, 0 xpassed); `xfail(strict=True)`; `EXPECTED_XFAIL = 52` (p9: ≥ 25) |
| Revisión en frío aceptada | Preflight y cold-bundle del TaskDoc dispuestos (accepted_with_corrections). La revisión en frío del documento producido y su disposición en `reviews/` quedan para el supervisor (ver abajo) |

### Suite completa (worktree, 2026-11-04)
`python -m pytest -q tests` → `3 failed, 1588 passed, 27 skipped, 52 xfailed, 2 warnings in 3502.41s (0:58:22)`.
Los 3 fallos **ya están en main `14575b02`** (los reproduje en el clon principal) y son de entorno, no de GO02:
- `tests/store/test_graph_analysis.py::test_centrality_ranks_what_the_rest_leans_on` y `::test_the_analyses_run_over_a_real_semantic_export`: `ModuleNotFoundError: numpy` → SLDBError "PageRank is networkx-on-scipy ... install structuredLanguageDB[graph]".
- `tests/test_serve.py::test_graph_endpoints_use_real_api`: HTTP 500 en el endpoint de centralidad, misma causa.
Los 27 skipped son preexistentes en la suite (ninguno de GO02).

### Hipótesis del worker (en el doc §8 y en el TaskDoc)
H1 API provisional `sldb.store.query_engine.rules` (`parse_predicate`, `eval_predicate(ast, grafo, sujeto=None)`, `contract_hash`); H2 grafo de test como dict nodes/edges; H3 sujeto `Model:name`; H4 `"unavailable": True` para store no disponible; H5 separador `.` entre pasos; H6 `^` invierte también `rel:`; H7 literales sin true/false/null ni listas anidadas; H8 palabras clave en minúsculas; H9 campos con punto como `where_lookup`; H10 clave del envelope → GO06; H11 `__contract__ = []` como `ValueError` en los tests.

### Para el supervisor
1. **Entorno**: el venv no tiene el extra `[graph]` (numpy/scipy); por eso hay 3 rojos preexistentes en main. Propuesta: `pip install 'structuredLanguageDB[graph]'` en `~/proyectos/SLDB_1/.venv` (no lo instalé sin tu visto bueno). Con alcance.md regla 2, ningún nodo cierra en verde hasta resolverlo.
2. Revisión en frío del documento producido y disposición en `desk/drawer/plans/grafo-operable/reviews/`, si la quieres antes del closeout.
3. Inconsistencia del TaskDoc: "Done When" dice "18 operadores"; la aceptación y p8 dicen 19 (la tabla tiene 19).
4. Squash-merge de `wt/go02`, closeout de la tarea, G_SEMANTICS → satisfied en dag.yaml citando el commit.
5. Siguiente: GO03 (depende de GO02). Lo promuevo y reviso en frío cuando GO02 esté en main.
