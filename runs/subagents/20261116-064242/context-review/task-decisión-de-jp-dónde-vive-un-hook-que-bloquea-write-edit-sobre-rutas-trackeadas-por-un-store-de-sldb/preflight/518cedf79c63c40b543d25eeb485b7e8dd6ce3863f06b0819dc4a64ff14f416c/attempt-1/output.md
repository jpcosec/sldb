## REFORMULACION

Encargo de decisión, no de implementación: obtener de JP la elección sobre dónde vive el hook que bloquea Write/Edit en rutas trackeadas por sldb. Opciones: (a) sldb ofrece `sldb guard-path` y un ejemplo de hook documentado, creando tarea de código; (b) el hook vive solo en `~/setup`; (c) no se hace. Resultado: sección “Escritura por agentes” en `docs/user-manual.md` con decisión fechada, recibo owner aceptado por JP y, si (a), tarea nueva con contrato completo. Repo: `/mnt/ssd/proyectos/SLDB_1`, root `sldb`. Límites: no implementar hook ni comando, no push, nada se ejecuta ni cierra sin recibo aceptado; el commit lo hace el coordinador.

## AMBIGUEDADES

1. “con las opciones, costos y recomendación de este contrato copiados tal cual”: el contrato no enumera costos; obligaría a inventar estimaciones de costo para cada opción.
2. “una línea "Decisión (AAAA-MM-DD, JP): <opción>"”: no define si `<opción>` es la letra, el texto completo o ambos; obligaría a inventar el formato exacto.
3. “un encabezado "## <nombre de la sección>"”: el placeholder no fija el encabezado literal; la validación sugiere “Escritura por agentes”, pero obligaría a decidir si el título es exactamente ese.
4. “La sección existe con la opción y la fecha”: no exige explícitamente motivo ni lista de opciones, aunque el protocolo sí; obligaría a interpretar si la validación debe cubrirlos.

## DRY-RUN

No es agregado ni paquete: es un nodo de decisión con gate humano. Lecturas previstas: ítem del drawer, `docs/user-manual.md` y referencias. Cambios previstos: preguntar a JP por herdr o supervisor; registrar recibo owner con `deskops review record`; obtener dispose accepted; escribir la sección; crear tarea con `deskops add task` si (a); commit con `deskops closeout commit`. Dependencias: respuesta de JP, recibos y `deskops`. Validaciones futuras: `grep -n 'Escritura por agentes' docs/user-manual.md`, recibo aceptado, tarea creada si (a), commit presente. Sin ejecutar nada.

## FUTURO

JP elige y acepta el recibo; el coordinador pregunta, registra y redacta; otro nodo ejecutará la tarea de código si (a); el integrador hará push.
