# T4 · Vista BANDEJA

Estado: **HECHO** · Dificultad: media · Depende de: T1
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

## Sugerencia de destino (cerrada 2026-09-30)
Para cada documento sin ubicar, hasta 3 documentos ya ubicados parecidos, con su puntaje,
vía `GET /corpus/rank` (`among` = los ubicados, en formato `Model:name`: con el nombre pelado
el servidor devuelve `[]` sin avisar). Tres estados distintos, nunca mezclados: sin parecidos,
corpus no indexado (botón "Indexar ahora") y no disponible. No mueve nada solo.
Límite: el puntaje es parecido de TEXTO (difflib), no de significado; no hay embedder por defecto.
