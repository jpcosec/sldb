REFORMULACION
GO03 es un nodo de código, entrega de PK01, repo dueño `sldb`. Propósito: fijar la costura `GraphBackend` (`load`/`eval`/`analyze`) y una implementación networkx que envuelva el análisis actual, enrutando los seis comandos `graph` y `api/graph` por `analyze` sin cambiar salidas. Resultado: protocolo documentado, backend, selección por `graph_backend` en `store.yaml` (solo `networkx`), `eval` del subconjunto de GO02 sin caminos, tests y CHANGELOG; produce `G_SEAM`. Límites: `compose` queda fuera y entrega el índice; la proyección real en GO03 es `None`; `eval` con camino lanza `NotImplementedError`; no se admiten otros backends; no cambia comportamiento observable. Depende de GO02 y requiere `G_BOUNDARY`.

AMBIGUEDADES
1. “eval la lee cuando el sujeto se pasa como export_id … en GO03 la proyección real es siempre None”: no define qué finding o error produce un sujeto `export_id` si la proyección es `None` o no contiene ese id. Obliga a inventar si no hay finding, se lanza error o se evalúa de otro modo.
2. “mensaje "graph_backend <valor> no admitido; admitidos: networkx"” frente a “mensaje que lista ["networkx"]”: el formato exacto del error no coincide. Obliga a inventar si el texto incluye `networkx` o `["networkx"]`.
3. “un test con un backend espía” frente a “admitidos en esta fase solo "networkx"” y “otro valor = error”: no dice cómo se activa un backend espía si `store.yaml` rechaza cualquier valor distinto. Obliga a inventar un punto de inyección o una excepción de test.

DRY-RUN
Un ejecutor futuro leería GO02, `compose.py`, API/CLI `graph`, `store.yaml` y tests/goldens. Crearía protocolo y backend networkx, enrutaría CLI/API, validaría config y documentaría. Dependencias: contrato de GO02, `G_BOUNDARY`, objeto de `compose` y goldens actuales. Validaría con pytest: goldens idénticos, tests `api/graph` existentes, espía por comando/función, carga del índice propio, `eval` de `has(id) and status != "x"`, path → `NotImplementedError`, config ausente/inválida, CHANGELOG. Sin ejecutar.

FUTURO
GO02 entrega firma y forma de findings; GO01/GO03 cierran `G_BOUNDARY`/`G_SEAM`; el humano acepta la revisión de GO03; GO04 produce la proyección real; GO05 habilitará caminos. Nada de eso es ambigüedad de GO03.
