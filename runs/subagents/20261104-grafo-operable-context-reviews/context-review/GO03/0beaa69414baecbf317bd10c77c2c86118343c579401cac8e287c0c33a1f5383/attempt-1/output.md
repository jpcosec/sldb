REFORMULACION  
GO03 es un nodo `delivery` del repo `sldb`: definir y documentar el protocolo `GraphBackend` (`load`, `eval`, `analyze`), implementarlo sobre networkx envolviendo el índice compuesto y el análisis actuales, y enrutar por `analyze` los seis comandos `graph` y `api/graph` sin cambiar sus salidas. Debe añadir la clave `graph_backend` en `store.yaml`, admitir solo `networkx` en esta fase, implementar `eval` para el subconjunto de GO02 sin caminos y documentar todo en `docs/architecture/graph-backend.md`, con CHANGELOG y tests. Límites: el backend no expone su grafo interno; la proyección real es `None`; un predicado con camino lanza `NotImplementedError`; no se altera el comportamiento observable existente. Produce `G_SEAM`.

AMBIGUEDADES  
1. “Selección por la clave graph_backend de store.yaml: lista admitida en esta fase = ["networkx"], sin nombres reservados; ausente = networkx; valor fuera de la lista = error al cargar el store con la lista en el mensaje.” No fija si `graph_backend` es un valor escalar validado contra una allowlist o una lista de nombres de backend. Obligaría a inventar el esquema YAML, la forma del valor y el mensaje exacto de error.

DRY-RUN  
Un ejecutor futuro leería GO03, el contrato de GO02, `compose.py`, los comandos `graph`, `api/graph`, el cargador de `store.yaml` y los goldens/tests actuales. Crearía el protocolo y la implementación networkx, adaptaría comandos y API a `analyze`, añadiría la selección y validación de `graph_backend`, y escribiría tests de goldens, backend espía, carga del índice propio, `eval` del subconjunto, camino con `NotImplementedError` y configuración ausente/inválida. Depende de GO02 para gramática, semántica y forma de `findings`, y de `G_BOUNDARY`. Validaría con pytest, comparación de goldens, espía de invocaciones, índice del repo, `eval` de `has(id) and status != "x"`, error de camino y carga de configuración. Sin ejecutar.

FUTURO  
GO02 produce la gramática, semántica y firma de `eval`; `G_BOUNDARY` debe estar satisfecho; la revisión en frío humana acepta GO03 y satisface `G_SEAM`; GO04 producirá la proyección real y consumirá la costura; GO05 habilitará caminos.
