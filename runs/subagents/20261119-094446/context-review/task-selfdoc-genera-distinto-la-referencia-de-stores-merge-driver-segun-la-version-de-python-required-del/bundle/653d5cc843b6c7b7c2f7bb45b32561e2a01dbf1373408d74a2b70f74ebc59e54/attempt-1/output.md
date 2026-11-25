## REFORMULACION
Propósito: corregir la divergencia de selfdoc al generar `knowledge/commands/cmd-sldb-stores-merge-driver.md`, donde `required` del argumento `files` sale `false` en Python 3.12 de uv y `true` en el host. Resultado: referencia estable e independiente de la versión de Python, con `selfdoc check` en 0 en host y contenedor scion. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). Límites: dentro, localizar la lectura de `required`, comparar ambos intérpretes y normalizar con test; fuera, cambiar el argparse de merge-driver salvo que la normalización lo exija. Es una tarea de depuración ejecutable, no un agregado.

## AMBIGUEDADES
1. “normalizar en el lector de selfdoc” frente a “se normaliza o se deriva del parser de forma estable”: no fija el punto ni el mecanismo; obligaría a inventar dónde y cómo normalizar.
2. “la 3.12 de uv”: no precisa versión ni ruta del intérprete; obligaría a inventar el Python exacto del contenedor.
3. “contenedor scion”: no define imagen ni comando de reproducción; obligaría a inventar cómo ejecutar allí.
4. “cualquier otro campo derivado de argparse que cambie entre versiones”: alcance indefinido; obligaría a inventar qué campos cubrir.
5. “quick_gates antes del commit”: no identifica el comando; obligaría a inventar el gate.

## DRY-RUN
Lecturas: TaskDoc, Board, rituales, pills/átomos ligados, `src/sldb/selfdoc`, parser del comando, documento generado y tests existentes. Cambios previstos: comparar `action.required` bajo host y uv; normalizar en el lector; añadir test de regresión. Dependencias: ambos intérpretes, `PYTHONPATH=src`, scripts de validación. Validaciones futuras: `PYTHONPATH=src sldb selfdoc check` y `bash tools/check.sh --fast`. Sin ejecutar nada.

## FUTURO
Un humano decide la estrategia de normalización y si se autoriza tocar argparse. Otro nodo reproduce en el contenedor y entrega la salida de introspección de ambos Python. Closeout produce el commit atómico y, si aplica, CHANGELOG.
