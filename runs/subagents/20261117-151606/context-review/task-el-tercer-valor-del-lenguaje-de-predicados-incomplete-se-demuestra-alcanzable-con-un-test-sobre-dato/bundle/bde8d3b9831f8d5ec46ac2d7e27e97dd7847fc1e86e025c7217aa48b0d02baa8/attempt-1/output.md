## REFORMULACION
Encargo ejecutable (`task.code`, repo `sldb` en `/mnt/ssd/proyectos/SLDB_1`): determinar si el valor `incomplete` del lenguaje de predicados es alcanzable con un store real construido por API pública en `tmp_path`; si lo es, añadir un test que lo demuestre y documente cuándo ocurre en `tests/api/test_rules_evaluation.py`; si no, retirarlo de API, tipos, tests de spec y `docs/architecture/rules-language.md`, actualizando el hash GO02. Límites: no tocar otros cambios del lenguaje; baseline true/false intacta; CHANGELOG y commit al cierre.

## AMBIGUEDADES
1. «solo si en result-summary.md queda la evidencia de que ningún camino público lo produce (grep de cada sitio que emite incomplete y por qué no se alcanza)»: no fija si basta el grep o exige intento fallido reproducible; obligaría a inventar el criterio de evidencia.
2. «vale un store enlazado que después se borra o se renombra para que quede no disponible» frente a H4: «compose_edge_index descarta las aristas hacia nodos que no existen»: el input no muestra que el índice marque `metadata.unavailable`; habría que inventar si ese camino existe hoy.
3. «los tests de especificación que lo nombran»: `files` no incluye `tests/test_rules_language_spec.py`; obligaría a inventar el alcance de edición.
4. «el hash del contrato GO02 de esa doc»: ese hash no aparece en el input; habría que inventar el mecanismo concreto.
5. «decidir con evidencia en result-summary.md»: sin ruta; obligaría a inventar su ubicación.
6. Rationale cita `predicate_explain.py` y `predicate_reach.py`, ausentes de `files`; habría que inventar si se editan o solo se leen.
7. «el tipo de holds»: sin fichero ni símbolo; obligaría a inventar qué se modifica.

## DRY-RUN
Lecturas: `where.py`, `rules-language.md`, `predicate_explain.py`, `predicate_reach.py`, `api/rules/`, ambos tests, `CHANGELOG.md`. Cambios previstos: grep de emisores/consumidores de `incomplete`; intento de store enlazado no disponible; decisión en `result-summary.md`; test nuevo en `tests/api/test_rules_evaluation.py` o retiro propagado; ajuste de doc/hash. Dependencias: composición del índice tras invalidar el store enlazado, `backend_for`/`GraphBackend.eval`. Validaciones futuras: los cuatro comandos de Validation, empezando por los tests pequeños y terminando en `check.sh --fast`.

## FUTURO
La decisión demostrar/retirar y la evidencia de `result-summary.md` las valida el supervisor del desk; el mecanismo del hash GO02 y el commit/closeout corresponden a nodos posteriores, no son ambigüedades de este encargo.
