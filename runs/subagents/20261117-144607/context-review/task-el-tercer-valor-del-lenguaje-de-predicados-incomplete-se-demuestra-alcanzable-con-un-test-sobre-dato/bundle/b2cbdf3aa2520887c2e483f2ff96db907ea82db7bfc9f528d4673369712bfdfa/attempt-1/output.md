## REFORMULACION

**Propósito:** resolver si el tercer valor `incomplete` del lenguaje de predicados es alcanzable con datos reales; si lo es, demostrarlo con un test sobre un store construido en `tmp_path` y documentar cuándo ocurre; si no, retirarlo.

**Resultado:** una decisión evidenciada en `result-summary.md`, la implementación de la opción elegida (test nuevo o retiro de `incomplete` del lenguaje, API y doc), doc y CHANGELOG actualizados, y los comandos de Validation en verde.

**Repo:** `SLDB_1` (`sldb`), tarea `task.code`, nodo `ritual-execution`. Es ejecutable, no un agregado.

**Límites:** entran `src/sldb/api/where.py`, `src/sldb/store/graph/language/predicate_explain.py`, `predicate_reach.py`, `src/sldb/api/rules/`, `tests/test_predicates_cli.py`, `docs/architecture/rules-language.md` y `CHANGELOG.md`; no entran otros cambios del lenguaje.

## AMBIGUEDADES

1. «o incomplete se retira del lenguaje, de la API y de la doc» — no fija si el retiro incluye tests de especificación, `GraphBackend.eval`, `StructuredQuery` ni el tipo de `holds`; obligaría a inventar la superficie exacta del retiro.
2. «con un store real armado en tmp_path» — «real» no define si vale un store enlazado simulado como no disponible (H4 dice que hoy se descarta); obligaría a inventar qué cuenta como dato real.
3. «decidir con evidencia en result-summary.md» — no fija ruta ni criterio de suficiencia; obligaría a inventar ubicación y umbral de evidencia.
4. «tests/api/test_rules_evaluation.py» — citado en Scope y Validation pero ausente de `files`; obligaría a inventar si existe o debe crearse.
5. «sin cambiar los resultados true/false existentes» — no define la línea base; obligaría a inventar el conjunto de comparación.
6. «actualizar docs/architecture/rules-language.md» — es contrato GO02 con hash; no dice si se permite editar su semántica; obligaría a inventar la gobernanza del cambio.

## DRY-RUN

**Lecturas:** los archivos citados, `predicate_explain.py`, `predicate_reach.py`, `src/sldb/api/rules/`, tests vecinos, Board y pills.
**Cambios previstos:** grep de `incomplete`; intento de caso real; decisión en `result-summary.md`; test o retiro; doc y CHANGELOG.
**Dependencias:** índice compuesto capaz de marcar aristas `unavailable`; fixture de store enlazado.
**Validaciones futuras:** los cuatro comandos del TaskDoc, más los tests de spec que toquen `incomplete`.

## FUTURO

Un humano decide la opción si el caso real no se construye; otro nodo aporta la capacidad de índice para stores no disponibles; `deskops closeout` ejecuta commit y retiro del Board.
