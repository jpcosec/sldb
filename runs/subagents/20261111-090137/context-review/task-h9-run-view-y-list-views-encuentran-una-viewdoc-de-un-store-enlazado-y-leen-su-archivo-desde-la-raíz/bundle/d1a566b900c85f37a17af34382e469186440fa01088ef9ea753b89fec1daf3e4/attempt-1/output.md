## REFORMULACION
Propósito: que `run_view`, `list_views` y `sldb serve` resuelvan ViewDocs que solo existen en un store enlazado, lean su archivo desde la raíz de ese store y las evalúen sobre el store llamante. Resultado: cambios v1-v5 en `src/sldb/api/views/`, `tests/api/`, `docs/` y `CHANGELOG.md`, con causa raíz escrita y tests verdes. Repo: sldb. Límites: fuera la forma del resultado de `run_view` y los agregados de deskops. Es una tarea ejecutable (`task.debug`), no un agregado.

## AMBIGUEDADES
1. «si ya está en main; si no, deja un TODO con la referencia a esa tarea.» Obliga a decidir el estado real de la guarda, el formato del TODO y qué hacer si está parcialmente disponible.
2. «los 7 pasos del workflow de sldb los corre el coordinador.» Obliga a inventar cuáles son esos 7 pasos y sus comandos; no están en el input.
3. «la evalúan sobre el store que llama» / «evalúa sobre los documentos de A». Obliga a definir si “documentos” es todo el store o solo las entradas relevantes, y con qué API.
4. «run_view, list_views y sldb serve encuentran» frente a un alcance que solo nombra `src/sldb/api/views/`. Obliga a decidir si se toca código de `serve`.
5. «el error las nombra (ambigua)». Obliga a inventar tipo, texto y calificación exactos del error.
6. «CHANGELOG y docs.» Obliga a elegir qué archivo de `docs/` y qué contenido.
7. «un archivo nuevo necesita eje en contracts/layers.toml». Obliga a saber si habrá archivo nuevo y el nombre del eje.

## DRY-RUN
Lecturas: `list_views.py` (`load_view`, `read_view`, `list_views`), resolución de `project_root`/`open_store`, índice compuesto, tests de views, `docs/`, `CHANGELOG.md`, `contracts/layers.toml` y la tarea de seguridad `source_read`. Cambios previstos: v1 resolución local→enlazada con ambigüedad explícita; v2 lectura desde la raíz del store que trackea la ViewDoc, por `source_read` o TODO; v3 listar enlazadas con nombre calificado; v4 evaluar sobre A; v5 tests A→B. Dependencias: guarda de seguridad en main, formato `'<link>:ViewDoc:<name>'` y límites de clean code. Validaciones futuras: `tests/api`, `test_clean_code_rules`, los 7 pasos en clon limpio y actualización de docs/CHANGELOG. Sin ejecutar.

## FUTURO
El coordinador ejecuta los 7 pasos y decide el cierre; la tarea de seguridad entrega `sldb.store.source_read` o confirma su ausencia; deskops/CC34 se desbloquea; un humano decide redacción de docs/CHANGELOG y el commit atómico.
