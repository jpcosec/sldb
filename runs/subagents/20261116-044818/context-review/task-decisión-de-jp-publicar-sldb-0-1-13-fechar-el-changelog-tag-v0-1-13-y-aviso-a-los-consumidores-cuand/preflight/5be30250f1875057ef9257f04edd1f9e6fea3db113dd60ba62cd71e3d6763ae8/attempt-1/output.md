## REFORMULACION

Encargo del nodo (TaskDoc `task.decision`, no agregado ni paquete ejecutable): obtener de JP la decisión de publicar sldb 0.1.13 cuando la precondición `task-main-...-en-verde` esté cerrada y la suite conjunta (sldb, deskops, spec2viz, graph_ui) esté verde. Resultado: recibo owner aceptado por JP y, si aprueba, encabezado `## 0.1.13` fechado en CHANGELOG.md, commit, tag `v0.1.13` en origin y avisos a deskops, graph_ui y spec2viz; si rechaza o aplaza, línea `Release: <decisión, fecha>` bajo ese encabezado. Repo: jpcosec/sldb (archivo CHANGELOG.md). Límites: no tocar pyproject.toml, no publicar a mano en PyPI, no decidir por JP, ningún tag/push sin recibo owner aceptado.

## AMBIGUEDADES

1. "cuando la suite conjunta esté verde" — no define verde para deskops, spec2viz ni graph_ui; obligaría a inventar comandos o criterios de aceptación.
2. "el dispose accepted es de JP" / "recibo owner aceptado por JP" — no indica cómo se registra la aceptación (comando, campo o evidencia); obligaría a inventar el mecanismo.
3. "fechar el encabezado en CHANGELOG.md" — no da formato (fecha ISO, texto exacto); obligaría a inventar la plantilla.
4. "Release: <decisión de JP, fecha>" — marcador sin formato ni valores admitidos; obligaría a inventar la sintaxis.
5. "git tag v0.1.13 sobre ese commit" — no especifica etiqueta anotada vs ligera ni mensaje; obligaría a elegir por convención.
6. "los consumidores" frente a "deskops, graph_ui y spec2viz" — no aclara si son el mismo conjunto; obligaría a asumir equivalencia.

## DRY-RUN

Lecturas: estado de `depends_on`; `gh run list --repo jpcosec/sldb --branch main --limit 1`; `grep -n '^## 0.1.13' CHANGELOG.md`; estado de suite en los otros tres repos (método no definido); `git ls-remote --tags origin v0.1.13`. Cambios previstos: editar CHANGELOG.md, commit, crear y pushear tag, `deskops message send` a tres destinos, `deskops review record --kind owner`. Dependencias: cierre de la tarea de main, CI verde, decisión de JP, coordinador integrador para tag/push. Validaciones futuras: grep del encabezado, ls-remote del tag, avisos en inbox. Sin ejecutar nada.

## FUTURO

JP emite la decisión y acepta el recibo owner; el coordinador integrador crea y pushea el tag; `publish.yml` publica en PyPI (irreversible); los tres desks reciben el aviso; si se aplaza, queda registrada la condición.
