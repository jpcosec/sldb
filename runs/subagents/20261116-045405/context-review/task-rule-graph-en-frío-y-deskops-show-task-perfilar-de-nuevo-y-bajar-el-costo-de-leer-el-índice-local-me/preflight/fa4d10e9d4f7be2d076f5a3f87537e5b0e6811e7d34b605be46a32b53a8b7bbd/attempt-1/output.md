## REFORMULACION
Encargo ejecutable (no agregado). **Propósito:** perfilar de nuevo `rule_graph` en frío y `deskops show task`, identificar el costo dominante y reducirlo. **Resultado:** informe con perfil cProfile antes/después —20 funciones más caras—, tiempos medidos, findings de `rules check` iguales antes y después, tests pasando y commit. Metas: `rule_graph` <1 s y `deskops show task` <2 s. **Repo:** `/mnt/ssd/proyectos/SLDB_1`. **Límites:** tocar solo `src/sldb/store/io/shards.py`, `src/sldb/store/io/__init__.py`, `src/sldb/api/rules/rule_graph.py` y `CHANGELOG.md` si aplica; si el costo dominante queda fuera, detenerse con perfil y propuesta. No entra federación, `run_view` ni cambio de formato de shards. Usar el intérprete de la instalación de `sldb`, no el `.venv` sin `yaml`; medir sobre copia en `/dev/shm` del desk de deskops, en frío sin `.sldb_cache` y en caliente.

## AMBIGUEDADES
1. “Con un perfil nuevo (cProfile) guardado en el informe” frente a “medir con sldb bench (verbo de V0, b60f0891) o con python -m cProfile”: obligaría a inventar si la salida de `sldb bench` satisface el requisito de cProfile.
2. “guardado en el informe”: no fija ruta ni nombre; obligaría a inventar el archivo de destino.
3. “deskops show task menos de 2 s”: no indica qué tarea concreta ni muestra; obligaría a inventar el caso de medición.
4. “comparar findings (rules check antes y después, mismo resultado)”: no da comando, formato ni criterio de igualdad; obligaría a inventar la normalización.

## DRY-RUN
Un ejecutor leería el TaskDoc, el informe `runs/subagents/rg-worker-report.md`, los módulos citados, tests y `CHANGELOG.md`; copiaría `deskops/.sldb` y `desk/` a `/dev/shm`; perfilaría antes, parchearía solo si el costo dominante está en la superficie permitida, perfilaría después y compararía findings. Depende de `task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida`. Validaciones futuras: los tres `pytest` indicados y comparación de findings. Nada ejecutado.

## FUTURO
El nodo ejecutor producirá perfil, mediciones, posible parche y commit. Un humano decidirá si el costo está fuera de alcance, si la meta no se alcanza o si se acepta la detención con propuesta.
