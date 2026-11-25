## REFORMULACION
Encargo: re-perfilar `rule_graph` en frío y `deskops show task` para bajar el costo de leer el índice local. Propósito: confirmar el hotspot real antes de optimizar (la nota previa ya no aplica: CSafeLoader y `_fast_copy`). Resultado: perfil cProfile antes/después con las 20 funciones más caras en `runs/subagents/<run-dir>/result-summary.md`; cambio en `src/sldb/store/io/shards.py`, `src/sldb/store/io/__init__.py` o `src/sldb/api/rules/rule_graph.py`; metas <1 s y <2 s sobre copia en `/dev/shm`; findings de `rules check` iguales; `CHANGELOG.md` bajo “## 0.1.13 — not released yet”. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no federación, no `run_view`, no cambiar formato de shards; si el hotspot cae fuera de esos módulos, detenerse con perfil y propuesta. El commit lo hace el coordinador; el ejecutor no hace push.

## AMBIGUEDADES
1. “en frío (sin `.sldb_cache`) y en caliente”: no define si “frío” exige proceso nuevo, repeticiones, mediana o descartar caché de página; obligaría a inventar el protocolo de medición.
2. “la primera de `deskops list tasks --root <copia>` en orden alfabético”: no dice si ordena por id, título o ruta ni si el listado ya viene ordenado; obligaría a inventar el criterio de selección.
3. “arreglar el costo dominante si está en …” (singular): no cubre dos hotspots comparables ni un hotspot en un helper invocado desde esos módulos; obligaría a inventar el límite de propiedad del cambio.
4. “Un aviso con `deskops message send --to <repo>`”: no identifica el repo destinatario; obligaría a inventar el destinatario.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout enrutados por Board, `shards.py`, `io/__init__.py`, `rule_graph.py`, `load_edge_index`, tests nombrados, `CHANGELOG.md`. Cambios previstos: copiar desk a `/dev/shm`, perfilar con `python -m cProfile -s cumtime` (intérprete de `head -1 $(which sldb)`, no `.venv`), medir con `sldb bench`, localizar hotspot, optimizar copia/lectura, medir de nuevo, comparar findings, actualizar CHANGELOG. Dependencias: `task-v0-benchmark…`, `/dev/shm`, deskops, fixtures del test. Validaciones futuras: los tres `pytest -q` con `TMPDIR=/dev/shm`; `rules check --format json` antes/después como conjuntos `(code, subject, level)`; tiempos bajo metas; commit del coordinador.

## FUTURO
Decide el coordinador: commit y closeout. Decide un humano: detener si el hotspot está fuera de alcance. Produce otro nodo: `sldb bench` y el mensaje al repo; el aviso alternativo va al informe si el repo no está registrado.
