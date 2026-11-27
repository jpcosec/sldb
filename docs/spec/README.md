# Spec de producto de sldb

Estado: **borrador**. El spec es una wiki: una página por cosa, escrita primero como texto aquí.
Mapear estas páginas al store es la tarea 0 del spec (JP, 2026-11-26). La portada con lo que el
dueño fijó está en `desk/drawer/plans/spec-de-producto-de-sldb/README.md`.

Clases de página con que se parte: objeto, operación, mecanismo, plugin, decisión y abierto. Por
ahora solo hay páginas de objeto.

## Objetos

Cada página dice qué es, cómo se nombra, dónde se guarda, qué hace hoy cada uno de los cuatro
verbos (con `ruta:línea` del código, leído el 2026-11-26 sobre `adf24cf0b`) y qué significaría.
Lo que significa cada verbo es propuesta **sin confirmar**. Las escribieron subagentes leyendo el
código; no se corrió ningún comando.

| Nodos | Aristas | Otros |
|---|---|---|
| [store](objetos/nodo-store.md) | [autorada](objetos/arista-autorada.md) (incluye transiciones) | [valor en un documento](objetos/valor-en-un-documento.md) (no es nodo) |
| [modelo](objetos/nodo-modelo.md) | [`links_to`](objetos/arista-links-to.md) | [enlace en el texto](objetos/enlace-en-el-texto.md) (no entra al índice de aristas) |
| [campo de modelo](objetos/nodo-campo-de-modelo.md) | [`contains` y `composes`](objetos/arista-contains-y-composes.md) | |
| [tipo de relación](objetos/nodo-tipo-de-relacion.md) | [`tagged_as`](objetos/arista-tagged-as.md) | |
| [documento](objetos/nodo-documento.md) | [`semantic_parent`](objetos/arista-semantic-parent.md) | |
| [sección](objetos/nodo-seccion.md) | [`semantic_equivalent`](objetos/arista-semantic-equivalent.md) | |
| [tag](objetos/nodo-tag.md) | [estructural](objetos/arista-estructural.md) | |
| [ancla](objetos/nodo-ancla.md) | | |

Plantilla: [`objetos/_plantilla.md`](objetos/_plantilla.md).

## Lo que salió al verificar contra el código

Verbos que no existen hoy:

- store: cambiar y borrar (lo único que borra es `stores init --force`).
- campo de modelo: cambiar.
- sección: crear, cambiar y borrar.
- tag: crear, cambiar y borrar.
- `semantic_equivalent`: borrar. `semantic_parent`, `tagged_as` y las estructurales: cambiar.
- arista autorada: no hay `edges create`; se crea escribiendo un `RelationDoc`, un campo de
  referencia o por el MCP.
- transición: nada la aplica. `apply_effects` calcula y no guarda.

El mismo verbo con garantías distintas:

- `docs update` no pasa por `save_document_payload`: no corre las reglas `on_write`, ni la guarda
  contra pérdida de encabezados, ni fija anclas. `fields` y las transacciones sí.
- `fields create` pisa en silencio un valor que ya existe.
- `semantic equivalent add` guarda una dirección; `stores semantic-map` guarda las dos y no
  refresca el índice.

Cosas que se pierden o no llegan al grafo:

- Los padres y equivalencias de tags declarados a mano viven solo en
  `.sldb_cache/semantic_dag.yaml`, que git ignora. Se pierden al borrar la caché o al clonar.
- `[[destino]]` no entra al índice de aristas.
- Una arista autorada no puede terminar en una sección ni en un valor: ese extremo se descarta.

"Ancla" son tres cosas distintas (`AnchorDoc`, `CodeAnchorDoc`, ancla a documento como valor de
campo), y en el store de sldb `AnchorDoc` está registrado desde `pron`, que está archivado.

Correcciones al registro de ejes (`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`):
`docs move` no existe (es `sldb move`); `edges rewrite` no cambia un `RelationDoc`; el `lint` de
la CLI no revisa `[[…]]`; `move` reescribe `[texto](ruta)` y no `[[…]]`; `docs batch` no lee
enlaces.

## Decisiones

- [La lógica del kernel de sldb es la de kimun](decisiones/el-kernel-sigue-la-logica-de-kimun.md):
  fijado por JP el 2026-11-26; lista qué preguntas abiertas de las páginas de objeto contesta.
  Alcance: este spec es el del refactor de sldb; el paso del kernel a kimun no es parte de él.
