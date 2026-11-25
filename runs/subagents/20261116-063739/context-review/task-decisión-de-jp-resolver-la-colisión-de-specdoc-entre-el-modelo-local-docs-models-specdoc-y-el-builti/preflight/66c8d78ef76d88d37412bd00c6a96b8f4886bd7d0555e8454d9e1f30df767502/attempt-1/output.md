## REFORMULACION

Encargo de **decisión/coordinación**, no de código: no es un agregado ejecutable ni tiene hijos; su cumplimiento es un gate humano más escritura documental. **Propósito:** resolver la colisión entre `docs.models:SpecDoc` y el builtin `sldb.models.notation.SpecDoc` haciendo que JP elija entre tres opciones (a: renombrar y migrar; b: borrar y migrar al builtin; c: precedencia local explícita), con recomendación (a). **Resultado:** sección "SpecDoc local frente al builtin" en `docs/architecture/notations-and-views.md` con decisión fechada, motivo y opciones/costos; recibo owner aceptado por JP; tarea de implementación creada en `desk/tasks`; commit del documento. **Repo/root:** SLDB_1, root `sldb`. **Límites:** no implementar la opción elegida, no hacer push, no cerrar sin recibo aceptado; el coordinador pregunta y commitea, el integrador pushea.

## AMBIGUEDADES

1. "2) Contar documentos del modelo local con sldb docs list o sldb stores check." frente a "`sldb stores check --store .sldb` no cuenta por modelo": obliga a inventar qué comando usar y cómo derivar el conteo.
2. "sldb docs list --model SpecDoc si existe": no fija el fallback; obliga a inventar el comando exacto.
3. "con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when)": no da valores; obliga a inventar contenido, archivos y done_when de la tarea de implementación.
4. "por el canal de coordinación (herdr o el supervisor)": no elige canal; obliga a inventar por dónde preguntar a JP.
5. "un encabezado \"## <nombre de la sección>\"": no aclara si el nombre es literal ni la posición en el documento; obliga a inventar.

## DRY-RUN

**Lecturas:** `docs/models.py:237`, `src/sldb/models/notation/spec_doc.py`, `.sldb/store.yaml:10-25`, `.sldb/core/models/SpecDoc.yaml`, nota de `references`, documento destino. **Cambios previstos:** añadir sección fechada; `deskops add task --root sldb`; `deskops review record` y `dispose accepted`; `deskops closeout commit`. **Dependencias:** respuesta de JP, CLIs `deskops`/`sldb`, git. **Validaciones futuras:** `grep -n 'SpecDoc local frente al builtin'`; `TMPDIR=/dev/shm sldb stores build --check --store .sldb`; `TMPDIR=/dev/shm deskops doctor --root sldb` sin alerta; recibo owner aceptado.

## FUTURO

JP elige opción y fecha; JP acepta el recibo; coordinador pregunta y commitea; integrador pushea; otro nodo ejecuta la tarea de implementación creada.
