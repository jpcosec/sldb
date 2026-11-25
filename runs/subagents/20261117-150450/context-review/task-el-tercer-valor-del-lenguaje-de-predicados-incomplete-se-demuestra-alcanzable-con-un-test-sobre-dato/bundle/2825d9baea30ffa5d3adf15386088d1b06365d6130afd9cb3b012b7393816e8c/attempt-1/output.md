## REFORMULACION
Propósito: resolver si el tercer valor `incomplete` del lenguaje de predicados es alcanzable con datos reales o debe retirarse. Resultado: o un test que, con un store armado por API pública en `tmp_path`, obtiene `incomplete` vía `where` o `rules check` y documenta cuándo; o el retiro de `incomplete` del lenguaje, la API y la doc (`GraphBackend.eval`, `StructuredQuery`, tipo de `holds`, tests de especificación, `docs/architecture/rules-language.md`, hash GO02), sin alterar los resultados `true`/`false`. Repo: SLDB_1. Límites: solo el lenguaje de predicados; nada más. No es agregado: es una tarea ejecutable.

## AMBIGUEDADES
1. «sin cambiar los resultados true/false existentes» frente a «incomplete se retira del lenguaje»: no dice qué devuelve una referencia a store enlazado no disponible tras el retiro (¿`false`, error de evaluación?). Obliga a inventar la semántica sustituta.
2. «decidir con evidencia en result-summary.md»: no fija ruta ni formato del archivo.
3. «se actualiza con el mecanismo que check.sh --fast señala»: no da el hash GO02 vigente ni el comando exacto; obliga a inferirlos.
4. «tests en tests/test_predicates_cli.py o tests/api/test_rules_evaluation.py»: el «o» no asigna qué caso va a qué archivo; además `files` lista `tests/test_predicates_cli.py` y no `test_rules_evaluation.py`.
5. «el tipo de holds»: no nombra símbolo ni módulo; obliga a localizarlo.
6. «un store enlazado que después se borra o se renombra»: no aclara si el índice se construye antes o se reabre tras el borrado, ni si eso sortea H4 («compose_edge_index descarta las aristas hacia nodos que no existen»).

## DRY-RUN
Lecturas: Board, TaskDoc, rituales execution/testing/closeout, `where.py`, `rules-language.md`, `predicate_explain.py`, `predicate_reach.py`, `src/sldb/api/rules/`, ambos tests, CHANGELOG. Cambios previstos: grep de `incomplete` en `src/sldb`; intento de test con store en `tmp_path` (crear, enlazar, borrar/renombrar); decisión con evidencia en `result-summary.md`; si se demuestra, test y doc; si se retira, quitar `incomplete` de `GraphBackend.eval`, `StructuredQuery`, `holds`, tests de spec y doc, y actualizar hash GO02; CHANGELOG. Dependencias: API pública de stores, edge index, fixtures. Validaciones futuras: los cuatro comandos de la sección Validation.

## FUTURO
Un humano u otro nodo aprueba la decisión (demostrar o retirar) leyendo `result-summary.md`; `deskops closeout` y el commit atómico cierran la tarea; el mecanismo de `check.sh --fast` confirma el hash GO02 actualizado.
