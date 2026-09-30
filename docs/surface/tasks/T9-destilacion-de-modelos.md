# T9 · Destilación: anchors → regularidad → modelo

Estado: **HECHO** (parcial, declarado) · Dificultad: alta · Ruta `#/destilacion`
Worktree: `/home/jp/AntonIA/repos/AgentsKBs_worktrees/knowledge-surface/sldb-surface`
Commit: `2f9ea1a9`

## Qué
Detectar anchors que se repiten, proponerlos como campos y emitir un borrador de
`__template__`. Es SOLO PROPUESTA: la vista no escribe, no genera archivos ni hace
`POST`; el modelo lo escribe una persona.

Propuesta §16.1: el modelo no se escribe, se destila.

## Hallazgo: el `kind` no existe
La ficha original decía agrupar por `kind`. ESE CAMPO NO EXISTE en el `AnchorDoc` de
este store: sus campos reales son `symbol`, `forms`, `ref`, `steps`, `motive`. El tipo
vive DENTRO de `ref`, que es una s-expression tipada cuyo primer átomo ES el tipo:

- `(field M f)` → campo de `M`
- `(relation R)` → candidato a `__references__`
- `(where M "pred")` → predicado, NO campo

También se leen los refs viejos en string (`model:M`, `predicate:M:<pred>`,
`action:change M.f=v`).

## La regla que hace auditable la destilación
Cada campo propuesto arrastra el `motive` del anchor que lo originó. Un campo sin
`motive` no se propone: sin razón escrita, no es auditable.

## Verificación
Con 4 anchors reales contra el store: agrupó `Factura` con 2 campos y `pago_de` como
relación. Los anchors de prueba se borraron; el store volvió a 114 documentos.

## NO implementado (declarado)
- **Escritura de modelos**: no hay endpoint. Es solo propuesta y la vista lo dice.
- **`__containment__`**: las formas de `ref` no lo distinguen de `__references__`.
- **Dedup por similitud**: `Corpus.rank()` no está servido.
- **"Posición estable" real**: un anchor no guarda posición; se usa como proxy que el
  modelo tenga 2+ campos.
