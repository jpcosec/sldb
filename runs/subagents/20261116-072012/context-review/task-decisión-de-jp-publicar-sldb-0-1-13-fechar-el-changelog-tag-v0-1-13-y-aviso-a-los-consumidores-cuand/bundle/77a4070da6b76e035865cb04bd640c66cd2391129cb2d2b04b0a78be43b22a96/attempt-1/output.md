## REFORMULACION

Encargo: obtener de JP la decisión de publicar sldb 0.1.13 cuando la suite conjunta (sldb, deskops, spec2viz, graph_ui) esté verde. Resultado: recibo owner aceptado; si aprueba, encabezado de CHANGELOG fechado, tag anotado `v0.1.13` en origin y aviso a los tres consumidores; si no, línea `Release:` con la condición. Repo: `jpcosec/sldb`; desk de trabajo. Límites: no subir versión en `pyproject.toml`, no publicar a mano en PyPI, no decidir por JP, y ningún tag/push sin recibo owner aceptado. Es un nodo de decisión/coordinación ejecutado por el coordinador, no un agregado de paquete.

## AMBIGUEDADES

1. "el dispose accepted es de JP" y "nada se ejecuta ni se cierra sin ese recibo aceptado": no se define qué ocurre si JP decide por el canal pero no ejecuta `deskops review dispose`; obligaría a inventar si el coordinador puede suplirlo.
2. "por el canal de coordinación (herdr o el supervisor)": no hay canal determinista; obligaría a inventar cuál usar.
3. "Esperar a que depends_on esté cerrada": no se especifica cómo verificar el cierre ni qué hacer si la dependencia falla; obligaría a inventar el criterio de espera/abandono.
4. "si un repo no tiene CI en main, se dice así a JP": no se define si eso cuenta como verde o bloquea; obligaría a inventar la regla de decisión.
5. "el commit que fecha el CHANGELOG" frente a "El commit del documento lo hace el coordinador con deskops closeout commit": no se fija el orden entre commit de cierre y tag; obligaría a inventar sobre qué commit va el tag.
6. "con las opciones, costos y recomendación de este contrato copiados tal cual": el contrato no enumera opciones, costos ni recomendación; obligaría a inventarlos.
7. "los tres desks tienen el aviso en su inbox" frente a `deskops message send --to ...`: no se aclara si el destino es desk o inbox; obligaría a inventar la semántica.

## DRY-RUN

Lecturas: Board, TaskDoc, rituales execution/testing/closeout, CHANGELOG.md y estado de CI de los cuatro repos con `gh run list`. Cambios previstos: registrar recibo owner; si aprueba, editar encabezado, commit, `git tag -a v0.1.13`, push del tag y tres mensajes; si no, añadir línea `Release:`. Dependencias: tarea de main en verde, respuesta de JP, coordinador e integrador. Validaciones futuras: `gh run list ... sldb`, `grep -n '^## 0.1.13' CHANGELOG.md`, `git ls-remote --tags origin v0.1.13` y avisos en inbox.

## FUTURO

Deciden/producen otros: JP (opción y recibo accepted), CI de los cuatro repos (verde o ausencia), integrador (push), deskops (registro y mensajes) y closeout (commit final).
