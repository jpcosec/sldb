# Integrar document-segments en main (Partes A/B/C)

ID: task-integrar-document-segments-en-main
Status: deferred
Priority: high

## Goal

Llevar el trabajo de segments (Partes A, B y C) desde `feat/document-segments` a
`feat/surface` y de ahi a `main`, para que el sldb instalado sirva
`GET /document/segments` y `POST /extract/segments` y se pueda apagar el servidor
de referencia (`surface/dev/segments_prototype.py` y `dev/reference_server.py`).

## Estado verificado (2026-09-30)

- Worktree: `hum-ecosystem-worktrees/sldb-segments`, rama `feat/document-segments`.
- HEAD `250e228`: "serve: POST /extract/segments real y degradacion por modelo en
  /schema y /graph". Ancestro `74285b5`: "segments: GET /document/segments real,
  por render instrumentado".
- Su suite corre verde: 1124 passed.
- `74285b5` y `250e228` **no** estan en `feat/surface` ni en `main`.
- **Parte C** (procedencia de composicion) existe: `api/segments/composition_piece.py`
  con `source` y `ref_index`. **Sin test propio** que la cubra: la suite verde no
  prueba que la procedencia sea correcta, solo que nada se rompe.
- **Parte D no existe** en ninguna rama: no hay `FieldRefResolver` ni `ref: "field"`
  en ningun lugar. Ver task atomica aparte.
- El working tree de ese worktree esta limpio; no hay trabajo suelto en riesgo.

## Decision pendiente: la direccion del field

`main` tiene `field_id` = `docs/<Modelo>/<doc>/<campo>` (commit d8bbcfc), unificado
con lo que acepta `sldb fields`.

`feat/document-segments` no tiene ese commit: usa `path` en espacio de payload
(`body`, `steps/2/title`) para ubicar un field *dentro* de un documento. No es un
choque — son cosas distintas y se componen (`docs/{model}/{doc}/{path}`) — pero la
direccion de documento que la UI use define si el `Modelo` va en la ruta. Incluirlo
evita colisiones entre modelos con documentos homonimos; es la decision que main ya
tomo y la que conviene conservar al integrar.

## Trabajo

1. Integrar `feat/document-segments` en `feat/surface` (la rama que consume la UI).
2. Integrar `feat/surface` en `main`. No es un merge trivial: `main` avanzo con
   otros trabajos, y el diff `main..feat/document-segments` es de ~537 archivos.
   Revisar antes de mergear que no se revierta lo que main ya tiene.
3. Verificar el invariante al integrar: el texto decodificado debe ser igual a
   `render_model_markdown(...)` en todos los documentos del store del repo.
4. Agregar el test que falta de la Parte C: que cada pieza compuesta declare su
   documento de origen y su indice, y que una pieza no trackeada quede sin `source`
   (y por lo tanto no sea editable).
5. Apagar el servidor de referencia recien cuando A, B y C sirvan desde main.

## Ya resuelto en main (el merge debe traerlo, no revertirlo)

- Hallazgo 1 (`/schema` se caia entera si un modelo no importaba): resuelto en
  main (09e1452) **y** en la rama (250e228, mismo shape `StoreSchema`/`unavailable`),
  asi que el merge converge sin decidir dos veces lo mismo.
- Hallazgo 2 (`/schema` no exponia `description` por field): resuelto solo en main
  (09e1452, en `api/schema/field_descriptor.py`). La rama no lo tiene.
- Hallazgo 3 (refs de composicion resueltas contra el CWD): resuelto solo en main
  (8264b8a, `compose_field(name, ref_root)`). La rama no lo tiene.

## NO-GOAL

- No reintroducir el monkey-patch del prototipo. La inyeccion es explicita:
  `SLDBRenderer(recorder=None)`, `None` por defecto para no cambiar comportamiento.
- No tocar la Parte D en este alcance.

## Done When

- `feat/document-segments` esta en `main` y el invariante de los 1394+ documentos
  se verifica con un test.
- La Parte C tiene test propio.
- El servidor de referencia no hace falta para que la UI funcione.
