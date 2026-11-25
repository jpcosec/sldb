## REFORMULACION
Encargo: obtener de JP una decisión sobre publicar `sldb 0.1.13`. Resultado: recibo owner aceptado; `CHANGELOG.md` refleja la decisión —fecha de release o línea `Release:` con condición—; si aprueba, tag `v0.1.13` en `origin` y aviso a deskops, graph_ui y spec2viz. Repo: `jpcosec/sldb`; archivo: `CHANGELOG.md`. Límites: no subir versión en `pyproject.toml`, no publicar manualmente en PyPI, no decidir por JP, no tag/push sin recibo owner aceptado; solo el integrador hace push. Es una tarea `task.decision`, no un agregado/paquete, y no es ejecutable autónomamente: requiere decisión humana y acciones condicionadas.

## AMBIGUEDADES
1. “suite conjunta esté verde” y “funcionando juntos” frente a “verde para cada repo es el último run de CI de main”: no queda claro si basta con cuatro CI verdes o se exige una suite integrada; obligaría a inventar el criterio.
2. “con las opciones, costos y recomendación de este contrato copiados tal cual”: el contrato no enumera opciones, costos ni recomendación completos; obligaría a inventarlos.
3. “la decisión y su condición quedan escritas” / “Release: pospuesto por JP (AAAA-MM-DD): <condición>”: si JP no da condición, obligaría a inventarla.
4. “git tag ... sobre ese commit” y “El commit del documento lo hace el coordinador con deskops closeout commit”: no se precisa si el tag va sobre el commit de release o el de closeout, ni el orden; obligaría a inventar la secuencia.
5. “si un repo no tiene CI en main, se dice así a JP”: no se define si esa ausencia bloquea la aprobación; obligaría a inventar su efecto.
6. “el enlace de PyPI”: no se da URL exacta ni se aclara si el aviso espera a que PyPI esté visible; obligaría a inventar ambos.

## DRY-RUN
Un ejecutor futuro leería la tarea, `depends_on`, `CHANGELOG.md`, `pyproject.toml`, tags remotos, runs CI de los cuatro repos y el inbox de origen. Verificaría cierre de la tarea de main y CI verde. Preguntaría a JP por el canal de coordinación con opciones, costos y recomendación; registraría `deskops review record`; esperaría `dispose accepted`. Si aprueba: editaría el encabezado a `## 0.1.13 — AAAA-MM-DD`, haría closeout commit, tag anotado y push por el integrador, y enviaría tres avisos. Si rechaza/pospone: añadiría la línea `Release:`. Validaría con `grep`, `gh run list`, `git ls-remote --tags origin v0.1.13` y revisión de inbox. Dependencias: JP, recibo aceptado, CI, integrador y `publish.yml`. Sin ejecutar nada.

## FUTURO
JP elige la opción y acepta el recibo; el integrador empuja el tag; `publish.yml`/PyPI actúan externamente; los consumidores reciben el aviso y el coordinador cierra.
