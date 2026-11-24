# Decisiones: motor Datalog y daemon

| Id | Decision | Actor | Fuente | Fecha |
|---|---|---|---|---|
| D5-rev | D5 de `grafo-operable` queda **revertida**: el grafo pasa a un motor Datalog estable duenio del almacenamiento y la consulta de aristas; networkx deja de ser el destino. Motivo: componer el indice, federar stores y live stale van a mano sobre YAML (28 s la primera carga del indice federado, `specir catalog build` no termina en 280 s). | JP | Nota 20261123-142527 del inbox de sldb | 2026-11-23 |
| D-daemon | JP pide ver ahora el daemon de sldb (diferido desde 2026-11-15). | JP | Nota 20261123-142553 del inbox de sldb | 2026-11-23 |

## Pendientes de JP (una task.decision cada una, con opciones y recomendacion)

| Id | Pregunta | Recomendacion |
|---|---|---|
| P1 | Que motor Datalog | Cozo con almacenamiento sqlite |
| P2 | Hasta donde llega la propiedad del motor (cache de aristas o tambien `eval` y `analyze`) | Duenio de las aristas y de `eval`; `analyze` migra despues, nodo a nodo |
| P3 | Forma del daemon y que pasa sin el | Un daemon por proyecto sobre socket Unix, opcional; sin daemon, base persistida en proceso |
| P4 | Como se invalida el indice | Dirty set de escritura mas HEAD de git y stat de rastreados |

Las cuatro estan registradas como tareas `task.decision` en el Board de sldb, con opciones y recomendacion:

- P1: `task-decision-para-jp-p1-que-motor-datalog-embebido-usa-sldb-cozo-datalevin-u-otro`
- P2: `task-decision-para-jp-p2-hasta-donde-llega-la-propiedad-del-motor-sobre-el-grafo`
- P3: `task-decision-para-jp-p3-forma-del-daemon-de-sldb-y-que-pasa-sin-el`
- P4: `task-decision-para-jp-p4-como-se-invalida-el-indice-del-daemon-con-git-y-con-las-escrituras`

Ninguna se toma por omision: sin respuesta de JP, el DAG no pasa a ejecucion.
