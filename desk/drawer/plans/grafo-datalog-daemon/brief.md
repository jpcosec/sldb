# Brief: motor Datalog y daemon de sldb

Fecha: 2026-11-24. Repo duenio: sldb.

## Encargo de JP (2026-11-23)

1. El grafo de sldb pasa a un motor Datalog estable que es duenio del almacenamiento y la consulta de aristas. Esto revierte D5
   de `grafo-operable/decisiones.md` ("networkx tras la costura, en proceso").
2. Ver ahora el daemon de sldb (diferido desde 2026-11-15): un proceso residente con el indice y el store cargados, para que el CLI,
   `sldb serve`, deskops y specir no recompongan el indice en cada invocacion.

## Por que va junto

El motor y el daemon se necesitan: el motor persistido resuelve la carga en frio; el daemon resuelve la recomposicion por invocacion y
el live stale. La prueba de concepto (`poc/informe.md`) separa lo que aporta cada uno:

- Consultar en proceso no mejora con Datalog (microsegundos contra milisegundos).
- Persistir el motor baja la carga en frio de 3 a 40 s a 7 ms de reapertura.
- Un indice residente baja 50 consultas sueltas de 49 s a menos de 20 ms.
- El stale (~1 s) no lo arregla el motor; lo arregla no reescanear (daemon con invalidacion por evento o por git).

## Forma propuesta

- **Motor.** Cozo (`cozo-embedded`, Datalog con recursion y negacion estratificada, almacenamiento sqlite) tras la misma costura
  `GraphBackend`, ampliada: el backend deja de recibir el indice compuesto y pasa a ser duenio del almacenamiento de aristas
  (`load` se vuelve ingestion; `edges_of`, `reach` y `stale` son consultas). Datalevin no tiene cliente Python.
- **Daemon.** Un proceso por proyecto, socket Unix en `.sldb_cache/`, que mantiene el motor abierto y atiende las lecturas del CLI,
  `sldb serve`, deskops y specir. El cliente prueba el socket; si no hay daemon, abre la base persistida en proceso
  (7 ms), y si tampoco existe, compone como hoy.
- **Invalidacion.** Las escrituras de sldb avisan por el camino de escritura (dirty set que ya existe); los cambios externos se detectan
  por git (HEAD y estado del arbol) y por el stat de los archivos rastreados.

## Lo que no se promete

El motor no acelera la consulta en memoria; la ganancia esta en no recomponer. El plan no mide escrituras incrementales, concurrencia
de lectores ni varios proyectos a la vez: esas mediciones son criterios de aceptacion de los nodos, no resultados.

## Decisiones abiertas para JP

Cada una es una `task.decision` en el Board de sldb; ver `decisiones.md`.
