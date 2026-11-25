## REFORMULACION
Propósito: obtener de JP una decisión sobre dónde vive un hook PreToolUse de Write/Edit que bloquee rutas trackeadas por el store de SLDB: (a) en sldb con `sldb guard-path` y ejemplo documentado, (b) solo en `~/setup`, o (c) no hacerlo. Resultado: sección “Escritura por agentes” en `docs/user-manual.md` con la opción y fecha; recibo owner aceptado; si es (a), crear la tarea de código correspondiente. Repo: SLDB_1. Límites: no implementar el hook ni el comando; solo presentar opciones, documentar la decisión y crear la tarea si aplica.

## AMBIGUEDADES
1. “Registrar el recibo owner (dispose accepted de JP)”: no define mecanismo, formato ni ubicación; obligaría a inventar dónde y cómo se registra.
2. “crear la tarea si es (a)”: no indica nombre, ruta, plantilla ni campos; obligaría a inventar su estructura.
3. “con fecha”: no precisa formato ni zona horaria; obligaría a inventar la representación.
4. “La sección existe con la opción y la fecha”: no fija contenido mínimo ni estructura; obligaría a inventar el nivel de detalle.

## DRY-RUN
Nodo de decisión documental, no agregado ni paquete ejecutable. Un futuro ejecutor leería el ítem del drawer y `docs/user-manual.md`, localizaría o crearía la sección “Escritura por agentes”, presentaría las opciones y la recomendación (a), y esperaría la decisión de JP. Según la opción, redactaría la sección, registraría el recibo y, solo si es (a), crearía la tarea de código. Dependencias: decisión de JP, formato del recibo y convención de creación de tareas. Validaciones futuras: `grep -n 'Escritura por agentes' docs/user-manual.md`; comprobar opción y fecha, recibo aceptado, tarea creada si es (a), y commit del documento.

## FUTURO
JP decide la opción y acepta el recibo owner. Otro nodo o ejecutor redacta la sección, crea la tarea si corresponde y hace el commit; un humano valida el resultado.
