REFORMULACION  
GO03 es un nodo `code`/`delivery` de sldb, no un agregado. Propósito: introducir la costura `GraphBackend` con `load(índice compuesto, proyección de payloads opcional)` y `eval(predicado parseado, sujeto opcional) → findings`, implementada sobre networkx. Resultado: seis comandos `graph` y `api/graph` enrutados por el backend sin cambiar salidas; selección `graph_backend` en `store.yaml` admitiendo solo `["networkx"]`; documento `docs/architecture/graph-backend.md`; CHANGELOG; produce `G_SEAM`. Repo dueño: sldb. Límites: `eval` solo predicados de un documento, sin caminos; no cambia comportamiento observable; no otros motores.

AMBIGUEDADES  
1. Cita: “load(índice compuesto, proyección de payloads opcional)”. “Opcional” no fija tipo, forma ni si GO03 debe implementar esa proyección o solo aceptar el argumento; además GO04, posterior, define la facet `payload`. Obliga a inventar la API y el alcance de esa proyección.

DRY-RUN  
Un ejecutor futuro leería `rules-language.md` de GO02 para firma y forma de findings, el código actual de `compose`, análisis de grafo, `api/graph`, parser CLI y carga de `store.yaml`; verificaría `G_BOUNDARY`. Cambios previstos: protocolo, adaptador networkx, enrutado de seis comandos y API, validación de `graph_backend`, doc, CHANGELOG y tests con goldens, espía, índice real y `has(id)`. Dependencias: GO02 y `G_BOUNDARY`; proyección y caminos quedan fuera, en GO04/GO05. Validaciones futuras: pytest, goldens idénticos, tests existentes de API, espía por comando/función, carga del índice del repo, casos de `store.yaml`, documentación.

FUTURO  
GO02 entrega firma y findings; GO04 consume el backend y añade payload proyectado; GO05 añade caminos; GO01 satisface `G_BOUNDARY`; revisión humana acepta GO03 para `G_SEAM`.
