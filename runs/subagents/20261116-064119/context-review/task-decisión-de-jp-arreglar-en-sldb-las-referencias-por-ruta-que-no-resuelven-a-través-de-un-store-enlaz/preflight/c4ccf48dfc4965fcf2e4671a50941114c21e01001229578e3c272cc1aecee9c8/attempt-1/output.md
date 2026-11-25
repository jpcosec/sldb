## REFORMULACION
Propósito: que JP decida entre (a) arreglar en sldb la resolución de rutas a través de stores enlazados o (b) cerrarlo como wontfix documentado. Resultado: recibo owner aceptado por JP y consecuencia ejecutada: nueva tarea de código con test en `tests/api/test_unresolved_references.py`, o sección “Rutas a través de un store enlazado” en `docs/architecture/references.md`. Repo: sldb. Límites: no implementar el arreglo, no hacer push; la decisión se pide por el canal de coordinación, se registra con `deskops review record`, JP la acepta con `dispose accepted`, y el coordinador commitea con `deskops closeout commit`. Es una tarea de decisión, no un agregado ni paquete ejecutable.

## AMBIGUEDADES
1. “la tarea creada agrega en tests/api/test_unresolved_references.py un test…” frente a “No entra: implementar el arreglo.” Obliga a inventar si el test debe escribirse ahora o solo quedar especificado como validación de la tarea futura.
2. “existe la tarea de código (a) o la sección del doc (b) commiteada.” Obliga a inventar si la tarea creada en (a) también debe commitearse o basta con que exista.

## DRY-RUN
Un ejecutor futuro leería el ítem del drawer, `declared_resolution.py`, `composition_targets.py` y la sección pertinente de `docs/architecture/references.md`. Después pediría a JP por herdr o supervisor las dos opciones, costos y recomendación (a), copiados del contrato. Registraría el recibo owner con `deskops review record … --kind owner` y esperaría el `dispose accepted` de JP. Con (a), crearía la tarea mediante `deskops add task --root sldb` con contrato completo, referencias y el test especificado; con (b), añadiría encabezado, línea de decisión, motivo y opciones consideradas, y validaría con el grep. Luego el coordinador haría `deskops closeout commit`; nadie haría push salvo el integrador. Dependencias: respuesta de JP, recibo aceptado, deskops y root sldb. Validaciones futuras: recibo aceptado; existencia de la tarea o grep de la sección; commit correspondiente.

## FUTURO
JP elige (a) o (b) y acepta el recibo. El coordinador ejecuta la consecuencia y commitea; el integrador decide el push. Si (a), otro nodo implementará el arreglo y el test.
