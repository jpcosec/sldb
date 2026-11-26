# Dirección única: estructural y semántica, bajo el store

Fecha: 2026-11-25. Repo dueño: sldb. Estado: **borrador** (corregido el 2026-11-26). JP aprobó la
idea de dos espacios de direcciones bajo el store; no aprobó este plan ni su ejecución. La
revisión del modelo y de las operaciones sigue abierta y la gramática puede cambiar con ella.
Ninguna tarea creada, `execution_authorized: false`.

La decisión está en `docs/architecture/one-address-grammar-two-spaces.md`. Aquí va el trabajo
que sale de ella. Estados y dependencias en `dag.yaml`.

## De dónde sale

El 2026-11-25 se quiso pasar la CLI y `sldb serve` a fastmcp. Eso topó con que los grupos de
comandos están mal armados, y eso con que no hay una sola forma de nombrar las cosas: la misma
dirección estructural se escribe de cuatro maneras, ninguna cubre todo, y la semántica quedó
dentro de `sldb legacy`. Sin una dirección única no se puede escribir la taxonomía de comandos.

## Lo propuesto (D1 es de JP, 2026-11-25; el resto es propuesta sin cerrar)

| Id | Decisión |
|---|---|
| D1 | Hay dos formas de dirección, estructural y semántica, las dos bajo el namespace que da un store e independientes de dónde vive la cosa en disco. |
| D2 | Una gramática con barras: `[store:]st/<Modelo>/<doc>/<campo>…`, `#<sección>`, `@<campo>` para el campo del modelo, `[store:]se/<tag>`. |
| D3 | La dirección estructural es el id del nodo del grafo; reemplaza a `sldb://`. |
| D4 | Un modelo se califica con el store dueño. |
| D5 | Una arista puede terminar en cualquier dirección estructural, no solo en un documento. |
| D6 | Las otras escrituras pasan a ser alias de entrada y después se retiran. |
| D7 | Lo que haya que migrar se migra; la compatibilidad con los ids actuales no limita el diseño. |

D4 y D5 no están cerradas por JP.

## Lo que no está decidido

- El orden entre AD04 (cambio de ids) y el nodo DL03 del plan `grafo-datalog-daemon` (el motor
  guarda nodos y aristas). Los dos reescriben el almacenamiento del índice.
- Si la taxonomía de comandos del ADR de fastmcp espera a este plan entero o solo a AD01.

## Orden

Los nodos AD02, AD03 y AD04 tocan `src/sldb/store/` y van en serie. AD05 y AD06 tocan
`store/edge_index/` y van en serie, primero AD06. AD08 son cuatro repos distintos y van en
paralelo, cada uno pedido por el inbox de su repo.
