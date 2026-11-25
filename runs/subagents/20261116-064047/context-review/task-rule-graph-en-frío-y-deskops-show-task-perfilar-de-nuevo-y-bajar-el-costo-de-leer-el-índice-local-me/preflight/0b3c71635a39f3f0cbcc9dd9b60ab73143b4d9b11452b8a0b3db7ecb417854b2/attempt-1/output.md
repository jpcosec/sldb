REFORMULACION
Propósito: perfilar de nuevo el costo de leer el índice local y reducir el tiempo de `rule_graph` en frío y de `deskops show task`. Resultado: informe con perfil cProfile antes/después (top 20 por `cumtime`), tiempos medidos bajo las metas (`rule_graph` < 1 s; `deskops show task` < 2 s), mismos findings de `rules check`, tests indicados en verde, CHANGELOG si hubo cambio y commit. Repo: `/mnt/ssd/proyectos/SLDB_1`. Superficie prevista: `src/sldb/store/io/shards.py`, `src/sldb/store/io/__init__.py`, `src/sldb/api/rules/rule_graph.py`. Límites: no federación de stores, no `run_view`, no cambiar formato de shards; si el costo dominante queda fuera de esos módulos, detenerse con perfil y propuesta.

AMBIGUEDADES
1. “en frío (sin .sldb_cache)”: no define dónde vive la caché ni cómo garantizar ausencia/limpieza; obliga a inventar el procedimiento de frío.
2. “una copia en /dev/shm del store del desk de deskops”: no fija ruta destino ni si copia `desk/` y `.sldb/` completos; obliga a inventar layout.
3. “arreglar el costo dominante”: no hay umbral de dominancia; obliga a inventar criterio para decidir si se arregla o se detiene.
4. “sldb bench (verbo de V0, b60f0891) o con python -m cProfile”: no concreta invocación exacta de bench; obliga a inferir sintaxis.

DRY-RUN
Lecturas: TaskDoc, informe previo `rg-worker-report.md`, módulos citados, tests de validación, CHANGELOG y fixtures. Copiar el desk a `/dev/shm`; localizar intérprete con `head -1 $(which sldb)`. Ejecutar `python -m cProfile -s cumtime` en frío/caliente y `sldb bench`; guardar top 20. Editar el punto caro dentro de los módulos permitidos. Repetir perfil y bench; comparar `sldb rules check --format json` como conjuntos `(code, subject, level)` con jq/python. Dependencias: intérprete con yaml, espacio en `/dev/shm`, `deskops`, jq/python. Validaciones futuras: los tres `pytest` con `TMPDIR=/dev/shm`.

FUTURO
El coordinador hace `deskops closeout commit` y el aviso al repo; un humano decide si la tarea se detiene por costo fuera de alcance y revisa el informe.
