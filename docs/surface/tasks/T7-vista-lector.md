# T7 · Vista LECTOR — anclar sobre texto crudo

Estado: **HECHO** (parcial: falta SourcePicker) · Dificultad: alta
Worktree: `/home/jp/proyectos/hum-ecosystem-worktrees/sldb-surface/surface`

## Qué
Superficie para declarar anchors sobre una selección de texto crudo. Ruta `#/lector`.
Escribe `AnchorDoc` real vía `POST /save`.

Propuesta §6.1 y §16.

## Hallazgo: el AnchorDoc que manda no es el de la propuesta §15.2
La propuesta describe un contrato con `kind`/`tags`/`provenance`
(`sldb.models.anchor_doc`). Este store registra otra variante:
`pron.models:AnchorDoc` (`/home/jp/proyectos/pron/src/pron/models/anchor.py`), con
`symbol`/`forms`/`ref`/`steps`/`motive` — sin `kind`, sin `tags`, sin `provenance`.
Por eso la vista lee los campos del schema en runtime y funciona con las dos variantes:
nunca manda un campo que el modelo no declara.

## Estado de las piezas
- Contrato `AnchorDoc`: existe (la variante de `pron`, no la de la propuesta)
- `anchor_targets.py` resuelve `ref` → nodo del grafo: funciona
- Texto → anchors: **esta vista**
- Anchors → regularidad → modelo: no existe en ningún lado (T9)

## DuplicateWarning (cerrado 2026-09-30)
Al seleccionar un tramo se compara contra los CAMPOS del store (`/corpus/rank?fields=1`) y se
avisa "Posible duplicado (NN%)" desde 0.85, o el parecido con su puntaje desde 0.35. Nunca
bloquea guardar. Por campo y no por documento: el ranking por documento compara contra todos
los strings del payload y diluye el parecido (una frase casi idéntica a una cita daba 0.55; por
campo da 0.99). Tres estados distintos: sin parecidos, corpus no indexado ("Indexar ahora") y no disponible.

## NO implementado (declarado en la vista)
- `SourcePicker` y la barra de % anclado: no hay fuentes en el store; el texto lo pega
  el usuario.

`core/ingest/` se retiró en `d0df139` (producto anterior, muerto e inimportable).

## Nota
Esta tarea y T9 son el mismo problema. El tramo que queda —anchors → regularidad →
modelo— sigue sin existir en ningún lado.
