## REFORMULACION
Propósito: obtener de JP la decisión, para cada H1-H8 de CC34, de si la ViewDoc de sldb la expresa o si queda como agregado de deskops. Resultado: sección “Decisión H1-H8 (CC34)” en `docs/architecture/views.md`, con fecha y una línea por hipótesis; una tarea en `desk/tasks` por cada H decidida “sldb”; mensaje a deskops con las decididas “consumidor”; recibo owner aceptado; commit del documento. Repo: sldb para documentación/tareas, con salida hacia deskops. Límites: no implementar; H9-H13 quedan fuera.

## AMBIGUEDADES
1. “JP decide” y “el dispose accepted lo hace JP”: no se define cómo se solicita/registra la decisión. Obligaría a inventar canal, formato y si el ejecutor puede cerrar sin recibo aceptado.
2. “crear con deskops add task una tarea de código en sldb por cada H que quede en ‘sldb’”: falta sintaxis, destino y campos. Obligaría a inventar comando, ruta/repo y contenido de cada tarea.
3. “mandar a deskops con deskops message send --to deskops la lista”: no fija asunto, cuerpo ni formato. Obligaría a inventar el mensaje.
4. “una línea por hipótesis”: no fija plantilla. Obligaría a inventar el formato de cada línea.
5. “con la fecha”: no aclara si es fecha de decisión, de registro o de commit. Obligaría a inventar cuál usar.
6. “H9-H13 (resueltas o en otra tarea)”: sin contexto suficiente. Obligaría a inventar si deben mencionarse o ignorarse.

## DRY-RUN
No es agregado ni paquete no ejecutable: es una tarea de decisión con ejecución documental. Lecturas previstas: este TaskDoc, la nota de inbox referenciada, `docs/architecture/views.md`, estado git y ayuda/CLI de `deskops`/`desk`. Cambios previstos: insertar la sección con ocho líneas; crear las tareas sldb resultantes; enviar el mensaje a deskops; commitear el documento. Dependencias: decisión de JP, recibo owner aceptado, CLI disponible, permisos y destino correctos. Validaciones futuras: `grep -n 'Decisión H1-H8 (CC34)' docs/architecture/views.md`; contar ocho líneas; comprobar tareas creadas; confirmar mensaje; verificar recibo; verificar commit. Sin ejecutar nada.

## FUTURO
JP decide cada H y acepta el recibo owner. deskops recibe la lista, retira las marcas “pendiente de sldb Hn” y ejecuta lo que quede de su lado. Si H1-H3 van a sldb, nodos de código las implementan. H9-H13 siguen en otra tarea.
