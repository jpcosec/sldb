## REFORMULACION
Propósito: obtener de JP una decisión vinculante sobre si python-sync/stores build deben destrackear PythonSymbolDoc generados cuyo símbolo desapareció. Resultado: opción registrada en `docs/self-documentation.md`, sección “Símbolos que desaparecen”, con fecha y motivo; recibo `owner` aceptado por JP; y, si es (a) o (b), tarea de código para cambiar `report.py` y `test_sync.py`. Repo: `sldb`. Límites: no implementar, no modificar la alerta de `stores check`, no hacer push, no cerrar sin recibo aceptado. Este nodo es `task.decision`: no es ejecutable por un agente ni es un agregado con hijos; su cumplimiento se delega al coordinador y a JP mediante el protocolo descrito.

## AMBIGUEDADES
1. “por el canal de coordinación (herdr o el supervisor)”: no se define cuál usar ni criterio de elección; obliga a inventar el canal.
2. “con las opciones, costos y recomendación de este contrato copiados tal cual”: el contrato no contiene costos; obliga a inventar su formato y valores.
3. “se escribe con deskops add task ... con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when)”: no se dan esos contenidos; obliga a inventarlos.
4. “si es (a) o (b) se crea la tarea de código que cambia report.py y test_sync.py”: (b) abarca también documentos de comandos y superficies, pero solo se nombran esos archivos; obliga a inventar el alcance real de (b).

## DRY-RUN
Lecturas previstas: `src/sldb/selfdoc/report.py`, `src/sldb/cli/commands/selfdoc_python.py`, `tests/selfdoc/test_sync.py`, `docs/self-documentation.md` y la nota de origen. Cambios previstos: pedir decisión a JP; registrar recibo con `deskops review record`; escribir la sección con decisión, motivo y opciones con costo; si procede, crear tarea con `deskops add task`; commit con `deskops closeout commit`. Dependencias: respuesta de JP, recibo aceptado y disponibilidad de `deskops`. Validaciones futuras: `grep` del encabezado, `deskops review status` y existencia de la tarea de código si aplica; luego `TMPDIR=/dev/shm pytest -q tests/selfdoc/test_sync.py`. Sin ejecución.

## FUTURO
JP elige opción, fecha y motivo; JP acepta el recibo; el coordinador redacta, crea la tarea si corresponde y commitea; el integrador hace push. La implementación de código queda en otra tarea.
