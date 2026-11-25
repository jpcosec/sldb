REFORMULACION

El nodo GD22 es una tarea de código ejecutable en el repo sldb (worktree aparte de grafo-operable): añadir referencias entrantes y su reescritura mediante `referrers(store, target)` y `rewrite_references(...)`, CLI `sldb edges referrers|rewrite` con envelope, `GET /edges/referrers` y `POST /edges/rewrite`, tests, `docs/architecture/references.md` y CHANGELOG. Límites: no editar `payload_save_steps.py`, no borrar prosa, no tocar código de deskops; lo nuevo es aditivo y genérico.

AMBIGUEDADES

1. «una superficie no modelada D (mención en prosa)» y «el texto que el MentionPattern capturó»: no se define el patrón ni su alcance; obligaría a inventar sintaxis y límites de mención.
2. «target acepta export_id, Model:name, ruta trackeada o id de nodo del grafo»: sin prioridad ni resolución de colisiones; obligaría a inventar el orden de resolución.
3. «--remove vacía B»: no aclara si es cadena vacía, `null` o eliminar el campo; obligaría a inventar la semántica.
4. «la operación no recorre el disco con el índice fresco (contado)»: «contado» no indica instrumento ni qué se cuenta; obligaría a inventar la medición.
5. «un fallo inyectado al escribir C»: no especifica el mecanismo de inyección; obligaría a inventar el punto de fallo.
6. «POST /edges/rewrite y la CLI producen el mismo reporte»: no define igualdad entre envelope HTTP y CLI; obligaría a inventar la comparación.
7. «--to NUEVO | --remove»: no dice qué ocurre si faltan ambos o se pasan ambos.

DRY-RUN

Lecturas hipotéticas: contrato del DAG, `project_graph.py:60`, `transaction` de GD24, `edge_reading.py:47`, `declared_references.py:68`, patrón de menciones, tests y docs existentes. Cambios previstos: crear `referrers.py`, `rewrite_references.py` y auxiliares; reexportar en `api/__init__.py`; parser, comandos y rutas CLI/serve; tests; `references.md`; CHANGELOG. Dependencias: GD21 y GD24 cerrados, GO07 cerrado, reglas `on_write` de GO08. Validaciones futuras: los `pytest` listados, grep de genericidad, CLI con `--dry-run`, `test_clean_code_rules.py`, rebase y contraste `files`/diff.

FUTURO

El supervisor decide las revisiones en frío y ejecuta la suite completa sobre el resultado integrado; el coordinador poda archivos autorizados no usados; deskops recibe la nota de cierre y retira su código; la promoción se hace con `deskops add task --from-drawer`.
