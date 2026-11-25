## REFORMULACION

Encargo: preparar y documentar una decisión de JP sobre la colisión entre `docs.models:SpecDoc` y el `SpecDoc` builtin de sldb. Repo: SLDB (`/mnt/ssd/proyectos/SLDB_1`), workspace `desk`. Resultado: una opción elegida y fechada en `docs/architecture/notations-and-views.md`, sección “SpecDoc local frente al builtin”, más una tarea de implementación creada con `deskops add task`. Límites: no implementar la opción elegida; la elección corresponde a JP, no al ejecutor.

## AMBIGUEDADES

1. “presentar las tres opciones de la nota con su costo” — la nota no está incluida en el input; obligaría a inventar su contenido o asumir que basta el resumen del Scope.
2. “Registrar el recibo owner (el dispose accepted es de JP)” — no se indica comando, formato ni ubicación; obligaría a inventar el procedimiento de recibo.
3. “Contar documentos del modelo local con sldb docs list o sldb stores check” — dos comandos alternativos sin criterio; obligaría a elegir uno y definir qué cuenta como documento.
4. “crear la tarea de implementación con archivos y validación” — no se especifican campos, nombre ni validaciones exactas; obligaría a inventar el contenido de la nueva tarea.
5. “commit del doc” — no se indica mensaje ni autor; obligaría a inventar metadatos del commit.

## DRY-RUN

Lecturas: `docs/models.py` (clase `SpecDoc`, línea 237), `src/sldb/models/notation/spec_doc.py`, `.sldb/store.yaml` líneas 10-25, la nota de inbox y `docs/architecture/notations-and-views.md`.

Cambios previstos: añadir la sección con opción y fecha; registrar el recibo owner; crear la tarea de implementación; commitear el documento. Dependencias: decisión de JP, acceso a la nota, disponibilidad de `sldb` y `deskops`. Validaciones futuras: `grep -n 'SpecDoc local frente al builtin' docs/architecture/notations-and-views.md`; existencia de la tarea; recibo aceptado; commit presente. Sin ejecutar nada.

## FUTURO

JP elige la opción y acepta el `dispose`. Otro nodo implementa la opción elegida y ejecuta `sldb stores build --check` y `deskops doctor` sin la alerta.
