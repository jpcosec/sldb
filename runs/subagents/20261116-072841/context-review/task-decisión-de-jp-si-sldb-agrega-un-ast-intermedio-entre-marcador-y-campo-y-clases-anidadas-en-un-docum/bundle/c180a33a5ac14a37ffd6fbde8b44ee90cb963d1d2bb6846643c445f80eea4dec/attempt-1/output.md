**REFORMULACION**
Propósito: obtener y registrar la decisión de JP entre (a) retirar ambas features, (b) hacer solo clases anidadas, o (c) hacer ambas. Resultado: sección “AST intermedio y clases anidadas” en `docs/architecture/model-authoring.md`, con opción, fecha ISO y motivo; recibo owner aceptado; si (b)/(c), tarea de diseño creada; si (a), features retiradas. Repo: `sldb`/desk. Límites: no implementar ni prototipar; solo leer, preguntar, escribir el documento, usar `deskops` y commit; sin push. No es agregado ni paquete: es una tarea de decisión/coordinación no ejecutable; `atoms: []` y `depends_on: []`.

**AMBIGUEDADES**
1. “por el canal de coordinación (herdr o el supervisor)”: no define cuál usar ni el destinatario exacto; obligaría a inventar el canal y el interlocutor.
2. “se crea la tarea de diseño correspondiente” y “con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when)”: no da título, alcance ni condiciones de cierre de esa tarea; obligaría a inventar su contrato.
3. “las features se retiran cuando exista la tarea de diseño creada”: no aclara si el retiro ocurre en el mismo cierre o después; obligaría a inventar la secuencia.
4. “toca la misma frontera átomo/field”: no dice si hay que esperar o coordinar con `task-diseño-set-bootstrap...` antes de decidir; obligaría a inventar una dependencia.

**DRY-RUN**
Un ejecutor futuro leería el Board, esta tarea, las dos features, `docs/architecture/model-authoring.md` y la tarea del set bootstrap. Luego preguntaría a JP, registraría el recibo owner con `deskops review record`, esperaría el `dispose accepted` de JP, escribiría la sección, retiraría features si (a) o crearía la tarea de diseño si (b)/(c), y cerraría con `deskops closeout commit`. Dependencias: respuesta de JP, canal de coordinación y `deskops`. Validaciones futuras: el `grep` del encabezado —insuficiente por sí solo—, inspección de opción/fecha/motivo/opciones, recibo aceptado, existencia de la tarea de diseño o retiro de features, y commit limpio. Sin ejecutar nada.

**FUTURO**
JP decide opción y motivo; JP acepta el recibo; el coordinador ejecuta `deskops` y el commit; el integrador hace push. Si se crea, la tarea de diseño decide después el alcance técnico.
