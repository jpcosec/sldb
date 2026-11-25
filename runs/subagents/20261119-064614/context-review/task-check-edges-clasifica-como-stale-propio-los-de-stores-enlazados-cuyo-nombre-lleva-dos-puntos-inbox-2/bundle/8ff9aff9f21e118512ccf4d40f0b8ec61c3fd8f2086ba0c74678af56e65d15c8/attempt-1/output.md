## REFORMULACION

Encargo ejecutable (no agregado) sobre el repo sldb: corregir `check_edges` para que un nodo stale de un store enlazado cuyo nombre contiene `:` no se clasifique como `linked_stale` propio. Resultado: test de regresión que falla antes y pasa después, clasificación por store dueño (no por `s.count(':') == 2` de `src/sldb/api/edges/check_edges.py:29`), entrada en CHANGELOG y gates del desk verdes. Límites: no cambiar el formato de ids (`store:Model:nombre`, `federation.py:30-38`); el alcance se ciñe a `src/sldb/api/edges/check_edges.py`, `src/sldb/store/edge_index/federation.py` (si hace falta propagar `from_store`), `tests/test_api_edges.py`, `tests/test_edge_effects.py`, CHANGELOG.

## AMBIGUEDADES

1. "un documento propio y uno enlazado, ambos stale y con un ':' en el nombre" vs. título "nombre lleva dos puntos" y código `count(':') == 2`: obliga a inventar si el fixture debe tener literalmente dos `:` en el nombre o uno más el separador.
2. "agregarlo donde se arma stale, sin cambiar el formato de los ids": no nombra archivo/función; obliga a inventar el punto de propagación de `from_store`.
3. Done When cita "stores build --check" pero la sección de validación solo lista pytest y `tools/check.sh --fast`; obliga a inventar si ese check es obligatorio.
4. "ver runs/subagents/20261119-repro-check-edges/" no coincide con el path del bundle (`.../20261119-064614/context-review/...`); obliga a inventar qué evidencia usar.

## DRY-RUN

Lecturas: `check_edges.py`, `federation.py` (`qualify_id`, `from_store`), `tests/test_api_edges.py`, `tests/test_edge_effects.py`, CHANGELOG, repro citado. Cambios previstos: p1 test rojo con store enlazado + doc propio/enlazado stale con `:`; p2 sustituir conteo por store dueño, añadiendo el dato donde se construye `index.stale`; p3 CHANGELOG; p4 gates. Dependencia crítica: que `index.stale` exponga el store origen (`from_store`). Validaciones futuras: los tres comandos de la sección y, si aplica, `stores build --check`. Sin ejecutar nada.

## FUTURO

Deciden otros nodos/humanos: si existe el repro y qué evidencia vale; si `from_store` debe añadirse al contrato de `stale`; el commit/closeout vía deskops; y si "stores build --check" entra como validación obligatoria.
