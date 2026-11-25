## REFORMULACION
El nodo es una tarea ejecutable (`task.debug`), no un agregado. Propósito: eliminar la dependencia de la versión de Python en la referencia que selfdoc genera para el argumento `files` de `stores merge-driver`. Resultado: `required` y demás campos derivados de argparse estables, con test, y `selfdoc check` en 0 tanto en host como en contenedor scion. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: investigar `src/sldb/selfdoc` o el parser CLI; no cambiar el argparse de merge-driver salvo que la normalización lo exija.

## AMBIGUEDADES
1. “la 3.12 de uv del contenedor”: no precisa intérprete, ruta, entorno uv ni contenedor; obligaría a inventar el comando de reproducción.
2. “normalizarlo con test”: no define la regla de normalización, su ubicación ni el test esperado; obligaría a inventar política y alcance.
3. “salvo que la normalización lo exija”: no fija criterio para decidir cuándo modificar argparse; obligaría a inventar esa frontera.
4. “quick_gates antes del commit”: no identifica comando ni conjunto de gates; obligaría a inventar la validación.
5. “selfdoc sync en el contenedor y en el host”: no indica invocación concreta en el contenedor; obligaría a inventar el procedimiento.
6. “cualquier otro campo derivado de argparse que cambie entre versiones”: no enumera campos ni versiones; obligaría a inventar el alcance.

## DRY-RUN
Lecturas: TaskDoc, `knowledge/commands/cmd-sldb-stores-merge-driver.md`, `src/sldb/selfdoc`, parser/CLI de `stores merge-driver`, tests y `tools/check.sh`. Cambios previstos: reproducir `action.required` con ambos intérpretes, ajustar el lector de selfdoc para derivar o normalizar `required` de forma estable y añadir test de regresión. Dependencias: `/usr/bin/python3.12`, python 3.12 de uv/scion, `PYTHONPATH=src`, selfdoc y check.sh. Validaciones futuras: comparar `action.required`, ejecutar el test, `selfdoc sync` en host/contenedor, `selfdoc check` en 0 y `bash tools/check.sh --fast`.

## FUTURO
Otro ejecutor reproduce y aplica los cambios; un humano confirma el intérprete/contenedor uv y autoriza tocar argparse si la normalización lo exige; el commit y los quick gates quedan para el nodo de cierre.
