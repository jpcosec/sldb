## REFORMULACION
Encargo: corregir en el repo sldb un bug detectado en el inbox 20261115-015936. `check_edges` separa stale propio de enlazado contando `':' == 2`, por lo que un documento de store enlazado con `':'` en su nombre se clasifica como propio y `--local` discrepa. Resultado exigido: test de regresión que falle antes (store enlazado + documento propio y otro enlazado, ambos stale, ambos con `':'` en el nombre), clasificación por store dueño sin cambiar formato de ids, entrada de CHANGELOG y gates. Límites: solo ese bug; superficies `src/sldb/api/edges/check_edges.py:29`, `src/sldb/store/edge_index/federation.py` (qualify_id) y `tests/test_api_edges.py`.

## AMBIGUEDADES
1. "from_store en las contribuciones de qualify, o los nombres de los stores enlazados del índice": dos alternativas sin criterio; obliga a inventar cuál usar y cómo propagar el dato hasta `index.stale`.
2. "antes con caché frío y caliente": no define cómo forzar/limpiar caché; obliga a inventar el procedimiento de reproducción.
3. "con rutas nombradas y Task-Id": no fija formato ni valor del Task-Id; obliga a inventar ambos.
4. "stores build --check" aparece en Done When pero no en Validation ni en el Path; obliga a inventar si es gate obligatorio y cómo ejecutarlo.
5. "verificado hoy en HEAD": HEAD no queda identificado; obliga a inventar el commit de referencia.

## DRY-RUN
Lecturas: `check_edges.py:29`, `federation.py:30-38`, `tests/test_api_edges.py`, `tests/test_edge_effects.py`, `runs/subagents/20261119-repro-check-edges/`, `tools/check.sh`, CHANGELOG. Cambios previstos: test de regresión primero; clasificación por store dueño (usar `from_store` o nombres de stores enlazados, añadiendo el dato donde se arma `stale` si falta) sin alterar formato de ids; nota en CHANGELOG. Dependencias: índice federado, `qualify_id`, `EdgeCheckReport.ok`. Validaciones futuras: los dos pytest, `bash tools/check.sh --fast`, `stores build --check`. Nada ejecutado.

## FUTURO
Decide un humano/otro nodo: enfoque `from_store` frente a nombres de stores; commit, PR y Task-Id; resolución de HEAD; obligatoriedad de `stores build --check`; veredicto de gates. No es agregado ni paquete: es una tarea ejecutable única.
