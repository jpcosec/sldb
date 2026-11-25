## REFORMULACION
Tarea de decisión (no agregado/paquete). El ejecutor debe obtener de JP una opción: (a) no hacer las dos features y retirarlas; (b) hacer solo clases anidadas sobre listas y tablas, sin AST intermedio; o (c) hacer ambas. Luego debe escribir en `docs/architecture/model-authoring.md`, sección “AST intermedio y clases anidadas”, la fecha, el motivo, las opciones consideradas y su costo; registrar el recibo owner y el `dispose accepted` de JP; crear la tarea de diseño si no es (a); retirar las features según la opción; y commitear el documento. Límites: no implementar ni prototipar; no hacer push salvo el integrador; no cerrar sin recibo aceptado. Repo: `sldb`.

## AMBIGUEDADES
1. “presentar a JP las opciones con costo” y “la lista de las opciones consideradas con su costo”: no se define qué es costo ni cómo medirlo; obligaría a inventar estimaciones o criterios.
2. “por el canal de coordinación (herdr o el supervisor)”: ofrece dos canales sin indicar preferencia ni equivalencia; obligaría a inventar cuál usar.
3. “si elige (b) o (c), las features se retiran cuando exista la tarea de diseño creada (que las cita en references)”: en (b) solo se diseña la feature 2, pero se habla de “las features”; obligaría a inventar si la feature de AST también se retira y si la tarea debe citarla.
4. “en el mismo cierre”: no precisa el orden entre retiro, recibo aceptado y commit; obligaría a inventar la secuencia.
5. “(b) se hace solo (2), clases anidadas sobre listas y tablas”: la feature habla de “una lista o sección” y de tablas que hoy dan dicts; obligaría a inventar el alcance exacto de tablas.

## DRY-RUN
Lecturas: las dos features del drawer, `docs/architecture/model-authoring.md` y referencias kimun citadas. Cambios previstos: sección de decisión en el documento; recibo owner; posible tarea de diseño con contrato completo; posible `deskops drawer remove`. Dependencias: respuesta de JP y su `dispose accepted`; comandos `deskops`; commit con `deskops closeout commit`. Validaciones futuras: `grep -n 'AST intermedio y clases anidadas' docs/architecture/model-authoring.md`, recibo aceptado, tarea creada si no es (a), features retiradas según corresponda. Sin ejecutar nada.

## FUTURO
JP decide y acepta el recibo; el coordinador registra y commitea; el integrador hace push si corresponde. Si la opción no es (a), otro nodo ejecutará el diseño.
