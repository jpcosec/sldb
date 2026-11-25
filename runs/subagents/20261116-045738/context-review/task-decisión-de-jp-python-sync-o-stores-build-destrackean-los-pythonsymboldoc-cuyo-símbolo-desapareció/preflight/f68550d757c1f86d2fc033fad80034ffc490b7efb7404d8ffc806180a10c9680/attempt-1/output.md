## REFORMULACION

- **Propósito:** que JP decida si `python-sync` debe destrackear los `PythonSymbolDoc` cuyo símbolo desapareció.
- **Resultado:** decisión registrada en `docs/self-documentation.md`, sección “Símbolos que desaparecen”, con opción y fecha; recibo owner aceptado; si aplica, tarea de código para cambiar `report.py` y `test_sync.py`.
- **Repo:** `/mnt/ssd/proyectos/SLDB_1`.
- **Límites:** presentar opciones (a), (b), (c) y recomendación (a); no implementar; la alerta de `stores check` es otra tarea. Es una tarea de decisión, no un agregado ni paquete ejecutable.

## AMBIGUEDADES

1. “Pedir decisión” / “Registrar el recibo owner (dispose accepted de JP)”: no se define canal, formato ni evidencia del recibo; obliga a inventar cómo se obtiene y acredita la decisión de JP.
2. “conserva los documentos de comandos y superficies escritos por personas”: no hay criterio para distinguir documentos generados de los escritos por personas; obliga a inventar la clasificación.
3. “se crea la tarea de código que cambia report.py y test_sync.py”: faltan título, ubicación, identificador y contenido mínimo; obliga a inventar metadatos de la tarea.
4. “La sección existe con la opción y la fecha”: no se especifica redacción, formato ni ubicación exacta dentro del archivo; obliga a inventar la plantilla.
5. “recibo owner aceptado por JP”: la validación solo comprueba la sección con `grep`; obliga a inventar cómo se verifica el recibo.

## DRY-RUN

Sin ejecutar: un ejecutor futuro leería `src/sldb/selfdoc/report.py`, `src/sldb/cli/commands/selfdoc_python.py`, `tests/selfdoc/test_sync.py` y `docs/self-documentation.md`. Después pediría la decisión a JP y escribiría la sección con opción y fecha. Si la decisión es (a) o (b), crearía una tarea de código para modificar `report.py` y `test_sync.py`. Dependencias: decisión de JP, recibo owner y documento existente. Validaciones futuras: `grep -n 'Símbolos que desaparecen' docs/self-documentation.md`, comprobar recibo y commit; la prueba `TMPDIR=/dev/shm pytest -q tests/selfdoc/test_sync.py` corresponde a la tarea de código, no a esta.

## FUTURO

JP debe elegir (a), (b) o (c) y aceptar el recibo owner. Si elige (a) o (b), otro nodo ejecutará la tarea de código, modificará `report.py` y `test_sync.py`, y correrá `pytest`. El cierre de esta tarea queda sujeto a la decisión humana y al commit del documento.
