## REFORMULACION

GO03 debe fijar en sldb la costura `GraphBackend` sobre networkx: protocolo con `load(índice compuesto, proyección)`, `eval(predicado, sujeto opcional) → findings` y `analyze(op, args) → resultado` para `path`, `cycles`, `order`, `components`, `central` y `similar`. Los seis comandos `graph` y `api/graph` deben enrutarse por `analyze` sin cambiar salidas. El backend se selecciona por `graph_backend` en `store.yaml` (solo `networkx`, ausente = networkx, otro valor = error). Debe documentarse en `docs/architecture/graph-backend.md`, añadir CHANGELOG y producir `G_SEAM`. Repo dueño: sldb. Límites: no cambia el comportamiento observable de comandos existentes; la proyección real es siempre `None` en GO03; `eval` cubre el subconjunto de GO02 sin caminos; no introduce otro motor.

## AMBIGUEDADES

1. «eval en este nodo acepta exactamente el subconjunto de GO02 sin caminos (has, nonempty, in, ~, model <=, comparaciones, and/or/not, paréntesis)». La lista no menciona la sustitución `{campo}` definida en GO02; obligaría a inventar si GO03 debe aceptarla o rechazarla.
2. «el backend lo recibe, no lo compone» frente a «Implementación networkx que envuelve lo que hoy hacen compose y el análisis de grafo». Contradicción sobre si `load` compone o solo consume el índice ya compuesto; obligaría a elegir una lectura.
3. «load(índice compuesto, proyección)» no declara valor de retorno. Aunque se dice «load la guarda», el protocolo no fija si devuelve `None`, el backend o el grafo interno; obligaría a inventar la firma efectiva.
4. «sin nombres reservados» no enumera qué nombres quedan prohibidos ni qué validación adicional exige; obligaría a inventar reglas de selección no descritas.

## DRY-RUN

Lecturas previstas: `rules-language.md` de GO02 (firma de `eval` y forma de findings), `compose.py`, comandos `graph`, `api/graph`, carga de `store.yaml`, tests/goldens existentes y networkx. Cambios previstos: módulo de backend y protocolo; implementación networkx; enrutado de CLI/API por `analyze`; rama de `eval` para el subconjunto sin caminos con `NotImplementedError` ante caminos; validación de `graph_backend`; documentación; CHANGELOG; tests. Dependencias: GO02 y `G_BOUNDARY`; objeto compuesto por `compose`; networkx. Validaciones futuras: goldens idénticos de los seis comandos; tests actuales de `api/graph` intactos; backend espía invocado por cada comando y función; carga del índice del propio repo; `eval` de `has(id) and status != "x"`; `NotImplementedError` con camino; `store.yaml` sin clave y con clave inválida; protocolo documentado; CHANGELOG.

## FUTURO

GO02 entrega la firma y el formato de findings que GO03 consume. GO04 produce la proyección real y consume `G_SEAM`. PK01 cierra cuando GO01, GO02 y GO03 cumplen sus gates. La revisión en frío aceptada la dispone quien opera el desk de sldb en `reviews/rN.md`; `G_SEAM` queda resuelto por esa aceptación. La promoción del nodo corresponde al TaskDoc y a `deskops add task --from-drawer`.
