REFORMULACION

Encargo: obtener de JP la decisión, para H1-H8 de CC34, de si cada una se expresa en la ViewDoc de sldb o queda como agregado de deskops; dejar la decisión en `docs/architecture/views.md`, sección “Decisión H1-H8 (CC34)”, crear una tarea de código en sldb por cada H decidida “sldb” y avisar a deskops de las que quedan de su lado. Repo: sldb, workspace desk; documento `docs/architecture/views.md` y tareas vía deskops. Límites: no implementar; H9-H13 fuera; sin recibo owner aceptado por JP no se ejecuta ni cierra; el commit del documento lo hace el coordinador y nadie hace push salvo el integrador. No es agregado ni paquete: es una tarea de decisión con gate humano.

AMBIGUEDADES

1. “con la fecha y una línea por hipótesis” frente a “una línea ‘Decisión (AAAA-MM-DD, JP): <opción>’, una línea ‘Motivo: <motivo>’ y la lista de las opciones consideradas con su costo”. Obliga a inventar si hay una decisión/motivo globales o uno por H, y cómo conviven con las ocho líneas.

2. “con las opciones, costos y recomendación de este contrato copiados tal cual” y “la lista de las opciones consideradas con su costo”. El contrato solo trae la recomendación H1-H3/H4-H8; no da costos. Obliga a inventar cifras o criterios de coste.

3. “contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when)” frente a campos del TaskDoc como “Rationale”. Obliga a inventar el mapeo de `why` y los nombres exactos que acepta `deskops add task`.

DRY-RUN

Lecturas: `views.md`, nota de origen, Board, rituales y átomos. Secuencia futura: 1) leer; 2) preguntar a JP por herdr/supervisor copiando opciones, costos y recomendación; 3) registrar recibo owner; 4) esperar `dispose accepted` de JP; 5) escribir la sección con fecha ISO; 6) crear una tarea por H “sldb”; 7) enviar mensaje “ViewDoc: H1-H8 decididas” a deskops; 8) validar con `grep -n 'Decisión H1-H8 (CC34)' docs/architecture/views.md`; 9) `deskops closeout commit`. Dependencias: respuesta y recibo de JP, CLI deskops, fecha. Sin ejecutar nada.

FUTURO

JP decide H1-H8 y acepta el recibo; el coordinador presenta, escribe y crea tareas; deskops recibe la lista y, en su repo, agrega lo suyo y quita marcas; el integrador hace push; H9-H13 siguen en sus tareas.
