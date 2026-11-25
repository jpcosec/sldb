## REFORMULACION

Propósito: que JP decida cómo resolver conflictos de git en los índices derivados de `.sldb` (`store_index.yaml`, `models/*.yaml`) entre tres opciones. Resultado: sección “Conflictos en los índices derivados” en `docs/versionado-y-colaboracion.md`, con opción y fecha; recibo owner aceptado; tarea de código creada con `deskops add task`. Repo: SLDB_1, según la ruta del input. Límites: no implementar; el hueco 2 solo pasa a la tarea de código si JP elige (a) o (b); no resolver el conflicto en esta tarea. Es una tarea `task.decision`, no un agregado con hijos ni un nodo ejecutable autónomamente: su cumplimiento depende de una decisión humana y de pasos documentales.

## AMBIGUEDADES

1. “Pedir la decisión a JP”: no define canal, formato ni quién valida la respuesta; obligaría a inventar el protocolo de consulta.
2. “Registrar el recibo owner (dispose accepted de JP)”: no indica artefacto, ubicación ni campos; obligaría a inventar el registro.
3. “con la fecha”: no aclara si es fecha de decisión, de documento o formato; obligaría a inventar convención.
4. “presentar las tres opciones con su costo” frente a “La sección existe con la opción y la fecha”: no dice si el documento final conserva las tres opciones o solo la elegida; obligaría a inventar el contenido.
5. “se crea con deskops add task”: no da sintaxis ni campos obligatorios; obligaría a inventar el comando.
6. “commit del doc”: no define rama, mensaje ni push; obligaría a inventar el flujo git.
7. “el hueco 2 … entra en la tarea de código si JP elige (a) o (b)”: no indica cómo verificarlo en “Done When”; obligaría a inventar el criterio de aceptación.

## DRY-RUN

Un ejecutor futuro leería la nota de inbox, `docs/versionado-y-colaboracion.md`, el atom citado y este TaskDoc; comprobaría si la sección y la tarea ya existen. Cambios previstos: obtener la decisión de JP, escribir la sección con fecha, registrar el recibo owner, crear la tarea de código y hacer commit del documento. Dependencias: decisión de JP, `deskops`, git y acceso a los archivos citados. Validaciones futuras: `grep -n 'Conflictos en los índices derivados' docs/versionado-y-colaboracion.md`; recibo aceptado; tarea existente en `desk/tasks`; commit presente. Nada se ejecuta aquí.

## FUTURO

JP elige la opción y acepta el recibo; otro nodo o el ejecutor crea la tarea de código; la implementación futura añadirá tests en `tests/store/test_update_fault_tolerance.py` y `tests/store/test_merkle_shards.py`.
