## REFORMULACION

Nodo de decisión (`task.decision`, `current_node: ritual-execution`, no ejecutable: produce una decisión, no código). Propósito: que JP elija dónde vive el hook PreToolUse que bloquea Write/Edit sobre rutas trackeadas por el store — (a) sldb ofrece `sldb guard-path` + ejemplo de settings y se crea tarea de código, (b) vive solo en `~/setup`, (c) no se hace. Resultado: sección "Escritura por agentes" en `docs/user-manual.md` con opción, motivo, fecha ISO y lista de opciones con costo; recibo `owner` aceptado por JP; tarea creada si (a); commit del doc vía `deskops closeout commit`. Repo: SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`). Límites: no implementa hook ni comando; no push (solo integrador); nada se cierra sin recibo accepted.

## AMBIGUEDADES

1. "La decisión queda en docs/user-manual.md, sección 'Escritura por agentes'" — esa sección no existe en el archivo adjunto (llega hasta "## 16"); obliga a inventar dónde insertarla y qué numeración/encabezado lleva, cuando el contrato exige "un encabezado '## <nombre de la sección>'" sin definir el nombre.
2. "o (c) no se hace" frente a Validation: "grep -n 'Escritura por agentes' docs/user-manual.md" — si gana (c) no hay sección que grepear; obliga a inventar si igual se documenta la opción descartada o la validación falla.
3. "por el canal de coordinación (herdr o el supervisor)" — no fija cuál; obliga a inventar el canal.
4. "Registrar el recibo owner (dispose accepted de JP)" — el input no trae el id del recibo ni el texto exacto del `--reason`; inventar el id es imposible, el motivo queda a criterio del ejecutor.

## DRY-RUN

Lecturas: ítem del drawer citado en `references`, `docs/user-manual.md` completo, Board y `deskops review` del recibo. Cambios previstos: edición de una sección en el manual; un `deskops review record --kind owner`; disposición de JP; `deskops add task` solo si (a); un commit acotado. Dependencias: respuesta de JP (bloqueante), `deskops` disponible, canal de coordinación, árbol limpio. Validaciones futuras: el `grep`, `deskops closeout verify`, y revisión humana de que la fecha y el motivo coinciden con la respuesta.

## FUTURO

JP elige la opción y acepta el recibo; el coordinador comunica y escribe; el integrador pushea. La calidad del hook y del comando, si (a), se decide en la tarea hija, no aquí.
