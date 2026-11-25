## REFORMULACION

**Propósito:** que JP decida si sldb incorpora un AST intermedio entre marcador y campo y/o clases anidadas por composición, a partir de dos features del drawer. **Resultado:** sección “AST intermedio y clases anidadas” en `docs/architecture/model-authoring.md`, con opción y fecha; recibo owner aceptado por JP; si la opción no es (a), tarea de diseño creada con `deskops add task`; commit del documento. **Repo:** `/mnt/ssd/proyectos/SLDB_1`. **Límites:** no implementar ni prototipar; solo leer las features y el documento, obtener la decisión de JP, escribir la sección y crear la tarea o dejar las features para retiro según la respuesta. No es un agregado ni un paquete: es una `task.decision` con intervención humana.

## AMBIGUEDADES

1. “JP decide una de: (a) no se hacen...; (b)...; (c)...” — el ejecutor no puede inferir la opción; obligaría a inventar la decisión.
2. “Registrar el recibo owner (dispose accepted de JP)” — no se define formato, ubicación ni evidencia; obligaría a inventar el mecanismo de registro.
3. “crear con deskops add task la tarea de diseño si corresponde” — faltan título, alcance, ruta y contenido; obligaría a inventar el payload de la tarea.
4. “dejar las features para retiro (deskops drawer remove) según la respuesta” — no queda claro si el retiro se ejecuta ahora o se difiere, ni con qué rutas/comandos; obligaría a inventar el momento y la operación.
5. “con fecha” — no se especifica formato, zona horaria ni fuente; obligaría a inventar la representación.
6. “commit del doc” — no hay rama, mensaje ni autorización explícita; obligaría a inventar el procedimiento Git.

## DRY-RUN

**Lecturas:** las dos features citadas y `docs/architecture/model-authoring.md`; opcionalmente las referencias de código solo para contexto. **Cambios previstos:** añadir la sección acordada al documento; registrar el recibo owner; crear la tarea de diseño si aplica; preparar el commit. **Dependencias:** decisión y aceptación de JP; disponibilidad de `deskops`; autorización para commit o retiro. **Validaciones futuras:** `grep -n 'AST intermedio y clases anidadas' docs/architecture/model-authoring.md`; confirmar recibo aceptado y, si aplica, existencia de la tarea de diseño. No se ejecuta nada.

## FUTURO

JP produce la decisión (a/b/c) y acepta el recibo owner. `deskops` produce el identificador de la tarea de diseño si corresponde. Un humano autoriza el commit y, en su caso, el retiro de features.
