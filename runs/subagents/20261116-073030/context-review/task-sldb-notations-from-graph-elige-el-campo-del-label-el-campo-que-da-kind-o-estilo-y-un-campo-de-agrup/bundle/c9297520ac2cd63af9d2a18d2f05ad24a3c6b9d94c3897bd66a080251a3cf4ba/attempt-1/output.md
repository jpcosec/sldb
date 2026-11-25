REFORMULACION
Propósito: que `sldb notations from-graph` deje de derivar siempre label=id y kind=modelo, y permita elegir el campo de label, el de kind/estilo y uno de agrupación. Resultado: flags `--label-field`, `--kind-field <campo|tag:<ns>>` y `--group-field` en el parser (`_add_from_graph`, `_from_graph_filters`) y su aplicación en `notations_from_graph.py` y en la función de API que compila el grafo a spec; nodos agrupados bajo contenedores con aristas `contains`; tests nuevos y línea de CHANGELOG. Repo: sldb (`src/sldb/cli/...`, `tests/notations/...`). Límites: sin estilos/paletas nuevas; sin flags la salida no cambia; `--snapshot` sin payload usa id y modelo (documentado en `--help`); commit y avisos los hace el coordinador; el informe va a `result-summary.md`. Es un nodo ejecutable (`task.code`), no un agregado.

AMBIGUEDADES
1. "un store en tmp_path con dos RepositoryDoc-like (title y tags system:a / system:b)": el edge index que consume `index_graph` (en el test fake solo expone `node_type`) no garantiza `title` ni `tags`; obligaría a inventar dónde vive ese "payload" y cómo lo lee `--store`.
2. "los nodos con el mismo valor de agrupación quedan dentro de un nodo contenedor con aristas contains": no fija id, label ni tipo del contenedor, ni qué ocurre con nodos sin ese campo; obligaría a inventar esa convención (y si el contenedor sobrevive a `--node-type`/`--drop-isolated`).
3. "Sin flags, la salida es idéntica a hoy (golden del test existente)": el archivo de test mostrado no contiene ningún golden; obligaría a inventarlo o a asumir identidad byte a byte.
4. "el --snapshot sin payload solo usa el id y el modelo": un snapshot node-link sí trae `attrs`; no se aclara si "sin payload" es un caso distinto ni cómo se detecta.

DRY-RUN
Lecturas: `notations_from_graph.py`, `parsers/notations.py`, `tests/notations/test_notations_from_graph_cli.py`, la API `component_spec_from_graph` (importada en el comando) y `CHANGELOG.md`. Cambios previstos: flags en `_add_from_graph`/`_from_graph_filters`; pasarlos por `_compile` a la función de API (posible cambio de firma); construir label/kind desde payload y `tags`; envolver grupos en contenedores con aristas `contains`; tests. Dependencias: firma pública de `component_spec_from_graph` y `test_component_spec_graph.py`. Validaciones futuras: los dos `pytest` citados en el TaskDoc.

FUTURO
Coordinador: commit con `deskops closeout commit`. Aviso a `<repo>` con `deskops message send` o, si responde no registrado, línea "Aviso a <repo>: ..." en el informe. Humano/otro nodo: confirmar que existe el encabezado "## 0.1.13 — not released yet" en CHANGELOG y revisar `result-summary.md`.
