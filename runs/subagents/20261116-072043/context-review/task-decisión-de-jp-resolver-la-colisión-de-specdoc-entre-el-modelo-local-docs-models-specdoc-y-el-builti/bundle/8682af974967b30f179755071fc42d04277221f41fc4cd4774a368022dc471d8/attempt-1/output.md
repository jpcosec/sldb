## REFORMULACION

Nodo de decisión/coordinación (no de código): lograr que JP elija cómo resolver la colisión de nombre `SpecDoc` entre el modelo local `docs.models:SpecDoc` y el builtin `sldb.models.notation.spec_doc` aparecido en SV01. Opciones: (a) renombrar el local y migrar documentos, (b) borrar el local y migrar al builtin, (c) regla de precedencia local sobre builtin; recomendación (a). Resultado: sección en `docs/architecture/notations-and-views.md` con decisión fechada, motivo y opciones con costo; recibo owner aceptado por JP; tarea de implementación creada con `deskops add task --root sldb`; commit del documento por el coordinador. Repo: SLDB_1, workspace `sldb`. Límites: no implementa la opción elegida; no hace push (solo el integrador); nada se cierra sin recibo aceptado.

## AMBIGUEDADES

1. Cita: «se usa el índice: el documents_count de .sldb/core/models/SpecDoc.yaml (leerlo con sldb, por ejemplo sldb docs list --model SpecDoc si existe, o contando las entradas de ese modelo en la salida de `sldb docs list`)». Obliga a inventar el comando exacto y cuál fuente prevalece si el índice y el conteo discrepan.
2. Cita: «un encabezado "## <nombre de la sección>"». El documento usa «## 1.» … «## 6.»; obliga a inventar si la sección se numera (¿7?) y en qué posición se inserta.
3. Cita: «una línea "Motivo: <motivo>"». No fija nivel de detalle ni longitud; obliga a inventar el contenido.

## DRY-RUN

Lecturas: `docs/models.py:237`, `src/sldb/models/notation/spec_doc.py`, `.sldb/store.yaml:10-25`, `.sldb/core/models/SpecDoc.yaml`, la nota de inbox y `docs/architecture/notations-and-views.md`. Cambios previstos: contar documentos del modelo local; preguntar a JP por herdr/supervisor con opciones, costos y recomendación; registrar recibo con `deskops review record`; escribir la sección; crear la tarea hija con contrato completo; commit con `deskops closeout commit`. Dependencias: respuesta de JP, CLI `deskops`, canal de coordinación. Validaciones futuras: `grep -n 'SpecDoc local frente al builtin'`, recibo owner accepted, existencia de la tarea hija, `sldb stores build --check --store .sldb` y `deskops doctor --root sldb` sin la alerta (estas dos, para la hija).

## FUTURO

JP elige opción y motivo y ejecuta el `dispose accepted`; el coordinador registra el recibo, escribe y commitea; otro nodo ejecuta la tarea de implementación creada.
