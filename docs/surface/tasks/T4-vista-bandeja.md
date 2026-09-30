# T4 · Vista BANDEJA

Estado: **HECHO** (parcial, declarado) · Dificultad: media · Depende de: T1
Worktree: `/home/jp/proyectos/hum-ecosystem-worktrees/sldb-surface/surface`

## Qué
Lo anotado sin ubicar: borradores que todavía no son atoms con lugar. Ruta `#/bandeja`.

Propuesta §6.4.

## Criterio implementado
Un documento entra a la bandeja si su modelo declara `provenance` y la tiene vacía
(regla 2 de la propuesta: "todo atom tiene origen; sin provenance no es conocimiento,
es opinión"), o si está tageado como borrador (`status:draft` y equivalentes).
En este store da 21 documentos sin ubicar.

Decisión de diseño: si el modelo NO declara `provenance`, el documento no entra. Sin
esa regla entran los 53 `RelationDoc` y la bandeja es ruido: la procedencia no le
aplica a un tipo de documento que no la declara.

## Brecha abierta
No sugiere destino. Eso necesita ranking por similitud: `Corpus.rank()` no está servido
por HTTP y `/graph/neighborhood` devuelve solo el nodo consultado. La bandeja lista pero
no sugiere, y lo dice en la vista en vez de simularlo con una heurística inventada.
