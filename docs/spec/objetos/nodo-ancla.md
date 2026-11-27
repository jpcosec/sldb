---
clase: objeto
tipo: nodo            # nodo | arista
nombre: nodo-ancla
estado: borrador
---

# Ancla

## Qué es

Anclar es fundamentar una afirmación en su fuente y guardar lo que se vio de ella, para saber
después si la fuente cambió (`docs/architecture/anchoring.md` §1). Hoy "ancla" nombra tres
cosas distintas en el código, y solo una es un nodo `anchor` del grafo:

1. `AnchorDoc`: un alias de léxico, `symbol` + `kind` + `ref` (`model:`, `doc:`, `edge:`...).
   Resuelve a qué apunta, pero no guarda lo que vio. Es el único que da un nodo
   `sldb://anchor/<symbol>` (`src/sldb/store/edge_index/doc_kinds.py:60-65`).
2. `CodeAnchorDoc`: un ancla a código, `code:<ruta>::<nombre>`, con una huella por nodo
   (firma, forma, docstring, cuerpo). En el grafo es un documento común: el constructor de
   anclas lo descarta porque no tiene `symbol` (`doc_kinds.py:61`).
3. Ancla a documento: no es un documento ni un nodo, es un valor de campo
   `doc:Modelo:nombre@sha256:<hash>`, en un campo de `__doc_anchors__` o en el `from:` de la
   procedencia (`src/sldb/models/doc_anchor_value.py:19`).

## Cómo se nombra

- Ancla a código: `code:<ruta>::<nombre calificado>`, con `::` vacío para el módulo y `~2`, `~3`
  para nombres repetidos; la ruta termina en `.py`, `.ts`, `.tsx`, `.js`, `.jsx` o `.sql`
  (`src/sldb/models/code_ref.py:13-24`).
- Ancla a documento: `doc:Modelo:nombre` o con huella, `doc:Modelo:nombre@sha256:<64 hex>`
  (`src/sldb/models/doc_anchor_value.py:19`).
- `AnchorDoc.ref` usa otra forma, `doc:<nombre>` sin modelo (`src/sldb/models/anchor_doc.py:48`),
  que no coincide con la de las anclas a documento.
- El documento ancla se nombra como cualquier documento (ver `nodo-documento`); el nodo
  `anchor` por su `symbol`. Con la gramática propuesta (borrador) el documento sería
  `[store:]st/<Modelo>/<doc>` y el valor ancla un fragmento de él.

## Dónde se guarda

- `CodeAnchorDoc` y `AnchorDoc`: un Markdown rastreado, como cualquier documento. La autoridad
  de `CodeAnchorDoc` es `theorem`: se deriva de una fuente que nombra
  (`src/sldb/models/code_anchor_doc.py:18-19`).
- Ancla a documento: el texto del campo del documento que la contiene; nada aparte.
- El estado (`intact`, `changed`...) no se guarda: se calcula al leer
  (`src/sldb/store/edge_index/doc_anchor_states.py:44`).
- En el store de sldb, `AnchorDoc` está registrado como `pron.models:AnchorDoc`
  (`.sldb/store.yaml:68-69`), un modelo de `pron`, que está archivado.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | Código: `anchors record <ref> --write <ruta> [--claim --name]` crea un `CodeAnchorDoc`; sin `--write` solo imprime el bloque. Documento: se crea al escribir un valor `doc:...`; el guardado le agrega la huella. `AnchorDoc`: sin comando propio, se crea como cualquier documento (`docs create --model AnchorDoc`) | `src/sldb/cli/commands/anchors.py:21-29`, `src/sldb/api/anchors/anchor_docs.py:50`, `src/sldb/api/documents/doc_anchor_pinning.py:19`, `src/sldb/api/documents/create_document.py:54` | **Sin confirmar:** crear es registrar qué destino ve la afirmación y guardar su huella actual |
| Leer | Código y documento: `anchors check` (solo lectura). `anchors record <ref>` sin `--write` lee un símbolo. `anchors_resolve` (qué documentos cubren un código o un tag) existe en la API y en MCP, no como comando de CLI. `AnchorDoc`: `edges show` | `src/sldb/cli/commands/anchors.py:31`, `src/sldb/api/anchors/check_anchors.py:21`, `check_doc_anchors.py:29`, `src/sldb/api/anchors/resolve_pointers.py:24`, `src/sldb/mcp/read/tools.py:64`, `src/sldb/cli/parsers/anchors.py:16-27` | **Sin confirmar:** leer es resolver el destino y decir su estado contra lo guardado |
| Cambiar | Código: `anchors record --write` sobre el mismo archivo vuelve a grabar y conserva `claim` e `history`; `anchors check --record` escribe las reconexiones. Documento: no hay comando; la huella se fija en el próximo guardado, y un ancla `changed` o `lost` queda así hasta que alguien reescribe el valor | `src/sldb/api/anchors/anchor_docs.py:37,50`, `src/sldb/api/anchors/check_anchors.py:28`, `docs/architecture/anchoring.md` §6 | **Sin confirmar:** cambiar es aceptar lo que cambió (volver a grabar la huella) o apuntar a otro destino; son dos cambios distintos |
| Borrar | Sin comando propio. Como un ancla a código es un documento: `docs untrack` o `docs delete`. Un ancla a documento se borra con `fields remove` o `fields update` del campo. Busqué un subcomando `anchors` de borrado: solo hay `record` y `check` | `src/sldb/cli/parsers/anchors.py:16-27`, `src/sldb/cli/commands/fields_mutate.py:20` | **Sin confirmar:** borrar quita la afirmación anclada, no la fuente |

Lo que verifiqué y no coincide con lo escrito:

- `docs/architecture/anchoring.md` §6 dice que `create_document` no fija la huella. El código
  sí: llama a `pin_payload` (`src/sldb/api/documents/create_document.py:54`, docstring
  líneas 48-50). La doc está atrasada.
- `docs update` no fija las huellas, a diferencia de `save_document_payload`
  (`src/sldb/cli/commands/doc.py:63-73`): un ancla a documento escrita con ese comando queda
  sin huella.
- El registro de ejes dice "tipo de relación, ancla: como documento" en los cuatro verbos. Es
  cierto solo para `AnchorDoc` y `CodeAnchorDoc`; el ancla a documento es un valor y el
  estado del ancla a código no se escribe en ningún verbo genérico.

## Aristas que le llegan y que salen

- `names` (alias), del nodo `anchor` a lo que su `ref` nombra: modelo, campo, documento o tipo
  de relación (`doc_kinds.py:65`, `src/sldb/store/edge_index/anchor_targets.py:15-32`).
- `references`, del documento que contiene un campo `__doc_anchors__` al documento destino,
  sin el sufijo de huella (`src/sldb/store/edge_index/doc_anchor_edges.py:17`). Un destino
  inexistente no genera arista. `from:` de la procedencia nunca genera arista.
- Un `CodeAnchorDoc` no tiene arista hacia el código: el código no es un nodo. Se cruza con
  documentos y tags por `anchors_resolve` (`resolve_pointers.py:24`).
- Que una arista termine en una sección o un valor lo fijó el dueño; un ancla a sección o
  valor no existe porque no hay hash de sección ni de subcampo (ver `nodo-seccion`).

## Qué lo mantiene correcto

- Estados `intact`, `changed`, `reconnected`, `lost`, `renormalize`, `unparseable`, `invalid`,
  `unavailable` (`src/sldb/models/anchor_state.py:13-21`). Las alertas no hacen fallar el
  comando; solo los errores (`anchoring.md` §4).
- Huellas de código: `NORMALIZATION = 1` (`src/sldb/code/fingerprints.py:18`); la forma de un
  valor ancla la validan el modelo base y `Provenance` (`doc_anchor_value.py:51,59`).
- La definición del modelo se valida al cargarla (`doc_anchor_value.py:67`).
- Huella de documento: hash de contrato del destino (`doc_anchor_states.py:36`).

## Abierto

1. ¿Un ancla es un tipo de nodo, o una arista que recuerda la huella de su destino? (El
   registro de ejes lo plantea como lectura sin confirmar.) De eso depende si los tres casos
   de arriba son uno solo.
2. ¿"Cambiar" un ancla `changed` es aceptar el cambio (regrabar la huella) o reapuntar?
   Hoy el código lo resuelve con comandos distintos y el documento no tiene ninguno.
3. ¿Puede una ancla a documento reconectarse cuando el destino se renombra, como la de código?
   Hoy queda `lost`.
4. ¿`AnchorDoc` (alias sin huella) queda como modelo de sldb, o desaparece junto con `pron`?
5. ¿Se ancla una sección o un valor? Haría falta una huella por sección y por subcampo.

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es una propiedad de un nodo: el anclaje de referencia a su soporte (por ejemplo un blob de git), junto al hash que detecta si cambió.

## Fuentes

`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`,
`desk/drawer/plans/spec-de-producto-de-sldb/README.md`,
`docs/architecture/anchoring.md`, `docs/architecture/code-anchoring.md`,
`docs/architecture/provenance.md`, `docs/architecture/one-address-grammar-two-spaces.md`;
`src/sldb/models/` (`anchor_doc.py`, `code_anchor_doc.py`, `doc_anchor_value.py`, `code_ref.py`,
`anchor_state.py`); `src/sldb/api/anchors/`; `src/sldb/cli/parsers/anchors.py`,
`src/sldb/cli/commands/anchors.py`; `src/sldb/store/edge_index/` (`doc_kinds.py`,
`anchor_targets.py`, `doc_anchor_edges.py`, `doc_anchor_states.py`, `node_ids.py`);
`src/sldb/api/documents/create_document.py`, `doc_anchor_pinning.py`; `.sldb/store.yaml`.
