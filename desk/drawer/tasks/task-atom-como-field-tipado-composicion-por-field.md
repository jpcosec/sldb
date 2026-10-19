# Atom como field tipado: composicion por field resuelta desde el store

ID: task-atom-como-field-tipado-composicion-por-field
Status: deferred
Priority: medium

## Goal

Que un atom sea un field tipado: que una composicion pueda declarar
`{"source_field": "atoms", "ref": "field", "template": "{value}"}` y que ese field
se resuelva contra el store en el momento del render.

Es la Parte D del handoff de segments. Se crea como artefacto propio **antes** de
trabajarla, porque en el handoff vivia como prosa dentro de otro alcance y asi se
perdio una vez el paso 2 del trabajo de field-level indexing.

## Por que va aparte

No es una feature mas: es un cambio de capas. Hoy el renderer es puro — recibe
template + payload y devuelve texto, sin saber de ningun store. Darle acceso al
store para resolver una ref lo convierte en otra cosa. La misma necesidad
(`que el modelo conozca su store`, H2 del analisis) conviene resolverla junto, no
en dos direcciones distintas.

## Estado habilitante (ya existe)

- `compose_field(name, ref_root=None)` en `src/sldb/models/structured_doc.py`:
  el modo por documento funciona y las refs se resuelven contra la raiz del
  proyecto (commit 8264b8a), no contra el CWD.
- `__compositions__` declara `source_field`, `model`, `template`, `separator`.
- La procedencia de composicion (Parte C) existe en main: cada pieza sabe de
  que documento salio (`src/sldb/api/segments/composition_piece.py`).
- `CompositionSpec.ref: Literal["document", "field"]` ya esta declarado, con
  `"document"` por default (`src/sldb/api/segments/composition_spec.py`), pero
  nada lo resuelve todavia: no hay resolver ni rama `ref == "field"`.
- La direccion de un field es `docs/<Modelo>/<doc>/<campo>` (`field_id`,
  commit d8bbcfc), la misma que acepta `sldb fields`.

## Trabajo

1. Definir el resolver y su inyeccion explicita: el render recibe un
   `FieldRefResolver` (o equivalente), no lo importa ni lo busca por un global.
   Sin resolver, el field se rinde vacio, igual que hoy con una ruta inexistente.
2. Usar el `ref` ya declarado en `CompositionSpec`; `"document"` es el
   comportamiento actual y debe seguir siendo el default.
3. Resolver `source_field` cuando `ref == "field"`: el valor es un field de otro
   documento, no una ruta de archivo. Requiere contexto de store, que es
   exactamente lo que el resolver aporta.
4. Confirmar que un marcador render no afecta la validacion: el field compuesto
   se rinde, no se extrae.
5. Test con los modelos de `tests/test_composition.py`: (a) con resolver, el
   atom se resuelve y se rinde con su template; (b) sin resolver, se rinde vacio
   y no rompe; (c) la validacion no cambia en ninguno de los dos casos.

## Decision previa

La direccion del field (`docs/<Modelo>/<doc>/<campo>` vs `docs/<doc>/<campo>`)
es la misma que hay que zanjar al integrar segments. Resolverla una vez, antes de
que las dos cosas aterricen, y no dos veces distinto.

## Done When

- Un atom se resuelve como field tipado con un resolver inyectado.
- Sin resolver, el comportamiento es el de hoy (vacio, sin excepcion).
- La validacion no cambia: es un marcador render.
