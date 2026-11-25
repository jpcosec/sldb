## REFORMULACION

Propósito: obtener de JP la decisión entre (a) arreglar en sldb la resolución de rutas relativas a través de un store enlazado o (b) cerrarlo como wontfix. Resultado: recibo owner aceptado más la consecuencia —tarea de código con test en `tests/api/test_unresolved_references.py`, o sección "Rutas a través de un store enlazado" en `docs/architecture/references.md`. Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb). Límites: no implementar el arreglo; no hacer push (solo el integrador); nada se ejecuta ni cierra sin recibo aceptado por JP. El nodo no es ejecutable: es `task.decision`; sus hijos son JP (decide y dispone accepted, transfiere opción/fecha/motivo), el coordinador (registra recibo con `deskops review record`, crea la tarea o escribe la sección, transfiere artefacto) y closeout (commitea). Validación conjunta: recibo aceptado + artefacto localizable (grep/ls) + `closeout verify`.

## AMBIGUEDADES

1. "con las opciones, costos y recomendación de este contrato copiados tal cual": el contrato no enumera costos → obligaría a inventar el costo de cada opción.
2. "por el canal de coordinación (herdr o el supervisor)": no se elige canal → obligaría a inventar cuál usar.
3. "deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when)": solo se precisan test y archivo → obligaría a inventar title, why y demás campos.
4. Validación `ls desk/tasks | grep -i enlazado`: depende de que el nombre de la tarea creada contenga "enlazado", no fijado → obligaría a inventar el slug; además no verifica el contrato completo.
5. "basta que exista la tarea" frente a Done When "…o la sección del doc (b) commiteada": no queda claro si el commit es requisito → obligaría a decidir si el commit valida.
6. `status: draft` junto a `current_node: ritual-execution`: no se dice si draft impide ejecutar → obligaría a inventar la precondición.

## DRY-RUN

Hipotético, sin ejecutar: lecturas del TaskDoc, rituales, nota del drawer, `docs/architecture/references.md`, `declared_resolution.py:57-58`, `composition_targets.py:37-49` y Board. Cambios previstos: pregunta a JP; `deskops review record … --kind owner`; dispose accepted de JP; luego `deskops add task` (a) o edición de la sección (b); `deskops closeout commit`. Dependencias: respuesta de JP, CLI deskops, canal. Validaciones futuras: `grep -n 'Rutas a través de un store enlazado'` o `ls desk/tasks | grep -i enlazado`; `closeout verify`.

## FUTURO

JP elige opción, fecha y motivo y dispone accepted; el coordinador redacta el contrato de la tarea hija si (a); el integrador hace push; un nodo posterior implementa el arreglo con el test de dos stores enlazados.
