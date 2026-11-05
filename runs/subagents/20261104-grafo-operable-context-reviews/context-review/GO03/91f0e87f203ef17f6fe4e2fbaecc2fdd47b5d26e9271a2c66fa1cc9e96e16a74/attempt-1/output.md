REFORMULACION  
Propósito: fijar en sldb la costura `GraphBackend` para que el grafo evalúe predicados sin acoplar reglas al motor. Resultado: protocolo `load`/`eval` con firma y findings de GO02, adaptador networkx, seis comandos `graph` y `api/graph` enrutados sin cambiar salidas, selección `graph_backend` en `store.yaml`, documentación de arquitectura y G_SEAM. Repo: sldb. Límites: no cambia comportamiento observable; `eval` solo soporta predicados de un documento, sin caminos —GO05—; no implementa motores futuros; no toca deskops.

AMBIGUEDADES  
1. “valor fuera de la lista admitida = error al cargar el store con la lista en el mensaje”: no se enuncia la lista admitida. Obliga a inventar si solo admite `networkx` o también nombres futuros —`kuzu`, `neo4j`, `datalevin`— como reservados.  
2. “los seis comandos graph ... y la API api/graph pasan por el backend, sin cambiar ninguna salida”, pero la aceptación solo exige “Goldens de los seis comandos graph idénticos a antes”. Obliga a inventar cómo verificar el enrutado y la salida de `api/graph`.

DRY-RUN  
Lecturas: GO02 `rules-language.md` —firma y findings—, `compose`, comandos `graph`, `api/graph`, carga de `store.yaml` y goldens actuales. Cambios previstos: protocolo y adaptador networkx bajo `src/sldb/store/graph/backend*`; enrutado de CLI/API; validación de `graph_backend`; documento de arquitectura. Dependencias: GO02 y G_BOUNDARY. Validaciones futuras: goldens de los seis comandos, carga del índice propio, `has(id)` con finding de GO02, ausencia y clave inválida de `store.yaml`, protocolo documentado y revisión aceptada. Sin ejecutar.

FUTURO  
GO02 entrega firma y forma de findings; GO04 aportará proyección de payload; GO05, caminos; GO01 satisface G_BOUNDARY; el dueño confirma D5; el revisor acepta G_SEAM.
