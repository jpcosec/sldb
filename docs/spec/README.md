# Spec de producto de sldb

Estado: **borrador**. El spec es una wiki: una página por cosa, escrita primero como texto aquí.
Mapear estas páginas al store es la tarea 0 del spec (JP, 2026-11-26). La portada con lo que el
dueño fijó está en `desk/drawer/plans/spec-de-producto-de-sldb/README.md`.

El spec tiene tres niveles (JP, 2026-11-27):

1. **Fundamentos**: [`principios/fundamentos.md`](principios/fundamentos.md). De dónde viene la
   idea (Wittgenstein, Zettelkasten, autopoiesis) y los ocho principios. Es lo que, si se quita,
   sldb deja de ser sldb.
2. **sldb como declaración de sistema**: [`principios/README.md`](principios/README.md). Qué es
   el sistema, dicho desde esos principios: adentro, afuera y sensores, entrar y salir,
   familias, qué pasa cuando el afuera se mueve.
3. **Técnicas, capacidades y estructuras de datos**: todo lo demás de esta carpeta. Lo que ya
   está escrito como objetivo: [`estructuras.md`](estructuras.md). Las páginas de objeto
   describen el sldb de hoy y son insumo del documento de diferencias, que va al final.

Para revisar una pieza o una página contra los principios:
[`principios/criterios.md`](principios/criterios.md). Lo conversado que todavía no existe:
[`principios/futuro.md`](principios/futuro.md).

Clases de página del nivel 3: objeto, operación, mecanismo, plugin, decisión y abierto. Hay
páginas de objeto, tres de mecanismo o decisión y una de abierto:

- Mecanismos: [anillos](mecanismos/anillos.md), [cambio y certeza](mecanismos/cambio-y-certeza.md)
  (propuesta de mínimo viable, sin revisar).
- Decisiones: [el kernel sigue la lógica de kimun](decisiones/el-kernel-sigue-la-logica-de-kimun.md).
- Abiertos: [qué es un hook](abiertos/hooks.md).

## Objetos

Las páginas de objeto se escribieron antes de los niveles 1 y 2. Cada una tiene una sección
"Desde los fundamentos" que dice de qué principio cuelga y qué de la página los contradice.

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
- No perder datos (JP, 2026-11-26): nunca se pierden datos salvo pedido explícito, y todo se
  explicita. Borrar algo con dependientes lo borra y deja a los dependientes marcados como sin
  soporte; no hay cascada implícita. Cierra esa pregunta en las páginas de modelo, campo de
  modelo, tipo de relación, sección y store.
- Toda transición pertenece a una máquina de estados; las sueltas se migran (JP, 2026-11-26).
  Vale para todo lo que hoy existe fuera de un mecanismo declarado.

## Hipótesis de JP sobre el problema de fondo (2026-11-26)

JP: es muy posible que el problema de fondo sea que hay implementación que no se usa, y que venga
de que sldb no se diseñó en anillos y no se respetan las fronteras.

Lo que mide `tools/check_axes.py` del propio repo el 2026-11-26 (corrido con `--units` y
`--dag`; no verifiqué sus números por otra vía):

- El contrato `contracts/layers.toml` declara 5 capas y 32 ejes y la puerta pasa con 0
  violaciones. Aun así los ejes no forman un DAG: 23 de los 32 son un solo nudo de 788 de los
  1.013 archivos.
- `operacion` (370 archivos) no es una unidad: es fachada.
- `enlaces` (12 archivos) es "capacidad sin superficie": nadie la necesita. `adaptadores` y `mcp`
  tampoco los necesita nadie, y hay una deuda declarada `adaptador-sin-uso`.
- La herramienta dice que el núcleo se parte cortando 4 aristas, y que mientras existan las
  aristas débiles "reorganizar carpetas es cosmético".

Casos vistos al escribir las páginas que calzan con la hipótesis: dos funciones que recorren una
ruta dentro de un documento (`payload_path_reading.deep_get` con puntos y
`segments/payload_values.value_at` con barras); `docs update` que no pasa por
`save_document_payload`; y la contención, que da identidad a un ítem, junto a la dirección por
posición que la ignora.

## Mecanismos

- [Los anillos](mecanismos/anillos.md): reparto de los 32 ejes del repo, confirmado por JP el 2026-11-27.

## Principios

- [Metodología para destilar los principios](principios/metodologia.md): aprobada por JP el
  2026-11-27. Las fichas por grupo de fuentes van en `principios/fichas/`.
