REFORMULACION
Propósito: que JP elija entre (a) destrackear solo `PythonSymbolDoc` generados, (b) destrackear también comandos y superficies, o (c) mantener retención y solo reportar. Resultado: sección “Símbolos que desaparecen” en `docs/self-documentation.md`, recibo owner aceptado y, si es (a)/(b), tarea de código para `report.py` y `test_sync.py`. Repo: `sldb`. Límites: no implementar, no tocar la alerta de `stores check`, no hacer push. No es agregado ni paquete: es un nodo de decisión no ejecutable, sin hijos (`atoms: []`, `pills: []`).

AMBIGUEDADES
1. “python-sync o stores build destrackean…” frente a “No entra: implementar; la alerta de stores check sobre documentos derivados ausentes es otra tarea.” Obligaría a inventar si `stores build/check` es una opción decisoria o solo contexto.
2. Validation: “grep -n 'Símbolos que desaparecen' docs/self-documentation.md” frente a Done When: “recibo owner aceptado por JP; tarea de código creada si es (a) o (b)”. Obligaría a inventar cómo validar el recibo y la tarea.
3. `current_node: ritual-execution` frente a “nada se ejecuta ni se cierra sin ese recibo aceptado”. Obligaría a inventar si el nodo ya está en ejecución o bloqueado esperando la decisión.

DRY-RUN
Un ejecutor futuro leería `report.py`, `selfdoc_python.py`, `tests/selfdoc/test_sync.py`, `docs/self-documentation.md`, la nota de origen y el estado del recibo. Previsto: preguntar a JP por el canal indicado; registrar el recibo owner; escribir la sección con decisión, motivo, fecha y opciones con costo; crear la tarea de código si procede; cerrar con `deskops closeout commit`. Dependencias: respuesta de JP, recibo aceptado y acceso a `deskops`; el coordinador registra y JP dispone. Validaciones futuras: `grep` de la sección, `deskops review status`, existencia de la tarea si (a)/(b), commit del documento y, en la tarea de código, `TMPDIR=/dev/shm pytest -q tests/selfdoc/test_sync.py`.

FUTURO
JP decide la opción y acepta el recibo; el coordinador escribe y commitea. Si es (a)/(b), otro nodo implementará el cambio en `report.py` y `test_sync.py`. El integrador hará push. La alerta de `stores check` queda como tarea separada.
