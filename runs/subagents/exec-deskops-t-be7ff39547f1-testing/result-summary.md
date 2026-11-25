PASA

# Tester deskops-t-be7ff39547f1: resultado

Task: `task-sldb-responde-que-documentos-aplican-a-un-archivo-o-a-un-simbolo-sea-porque-lo-anclan-directo-o-porq`
Commit revisado: `f68074750918eb74b262ff15f27f1fc9be1e2e9e` — `feat: anchors_resolve answers which documents cover a file or symbol, and which code a document or tag covers`

Archivos del commit:
`contracts/layers.toml`, `src/sldb/api/__init__.py`, `src/sldb/api/anchors/__init__.py`,
`src/sldb/api/anchors/resolve_pointers.py` (nuevo), `src/sldb/api/anchors/tag_reach.py` (nuevo),
`src/sldb/mcp/read/tools.py`, `src/sldb/mcp/registry.py`, `src/sldb/models/code_anchor_doc.py`,
`tests/mcp/test_read_tools.py`, `tests/test_where_pointers_resolve.py` (nuevo).
El commit no lleva `Task-Id`.

## Veredicto

**PASA.** `anchors_resolve` responde en las dos direcciones y en la dirección de tag:

- `target=path` o `path::Symbol` (con `code:` opcional) -> `{target, documents: [{doc, via}], unresolved}`,
  con `via` = `direct` o `tag:<tag>`, ordenado por `doc`.
- `document=Model:id` -> `{document, code: [{path, symbol, via}], unresolved}`, ordenado.
- `tag=<tag>` -> `{tag, documents, code, unresolved}`: el tag, su subárbol transitivo del DAG y sus
  equivalencias (`tag_reach`), que es lo que exige el Done When para "el tag padre".

La cobertura por tag compone `CodeAnchorDoc.ref` (vía `parse_code_ref`) con `load_semantic_dag` y
`semantic_dag_graph.under`; no hay un segundo índice. Un tag que ningún documento declara va a
`unresolved` como `{tag, doc}` y no levanta error. La operación es de solo lectura: el test compara
los bytes de todos los archivos del store antes y después, y la herramienta MCP se registra en
`READ_TOOLS` con las anotaciones `READ_ONLY`. El nombre canónico es uno solo (`anchors_resolve`) en
`sldb.api` y en MCP. `docs/architecture/command-taxonomy.md` no existe, así que la propuesta de
taxonomía queda en este result-summary (operación de lectura, nivel 0).

## Validación ejecutada

Directorio de trabajo: `/workspace/sldb`. Temporales en `/tmp` con
`PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-be7ff39547f1` y `TMPDIR=/tmp`.
No se corrió la suite completa.

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q tests/test_where_pointers_resolve.py` | 0 | 5 passed |
| `python -m pytest -q tests/mcp/test_read_tools.py` | 0 | 14 passed |
| `python -m pytest -q tests/api/test_anchors.py` | 0 | 22 passed, 1 skipped |
| `python -m pytest -q tests/api/test_api_semantic.py` | 0 | 8 passed |
| `python -m pytest -q tests/api/test_doc_anchors.py` | 0 | 24 passed |
| `bash tools/check.sh --fast` (con el venv en `PATH`) | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_resolve_pointers.py` ni `tests/test_tag_reach.py`; el test del módulo es
`tests/test_where_pointers_resolve.py`, ya corrido, y los tests de la familia de anclas son
`tests/api/test_anchors.py` y `tests/api/test_doc_anchors.py`, también corridos.

### Entorno

`/tmp/ws-venv` no existe en este contenedor. Usé `/workspace/sldb/.venv` (Python 3.13.18, tree-sitter
disponible) para la API y las puertas. Ese venv no tiene `anyio`/`mcp`, así que para
`tests/mcp/test_read_tools.py` usé `/workspace/IR/.venv`, que sí los tiene y resuelve el mismo
árbol fuente (mismo inodo que `/workspace/sldb/src`). La suite MCP pasa allí; sin ese extra el
archivo falla en el `import anyio` del fixture, un límite del venv y no del commit.

## Comprobaciones adicionales

- **Done When, caso hijo:** probé un documento etiquetado con un tag nieto
  (`layer.interface.panel.deep`) y resolver el tag padre (`layer.interface`) lo devuelve con
  `via: tag:layer.interface.panel.deep`; el código del ancla también aparece.
- **Equivalencias:** probé una equivalencia local -> global en el DAG y el alcance del tag local
  incluye el equivalente (y viceversa), como pide la aclaración.
- **Tercero sin relación:** el documento con `layer.other` no aparece al preguntar por el archivo
  ni al resolver `layer.interface`.
- **Sin escritura:** además del test del commit, `open_store(..., mode="readonly")` y la
  comparación de bytes cubren el caso; el árbol de trabajo de `src/`, `tests/`, `contracts/` y
  `docs/` no tiene cambios sin commitear.
- **Modelo:** `CodeAnchorDoc` gana `tags` opcional (`optrev`), necesario para que un ancla pueda
  llevar categorías; `tests/api/test_anchors.py` sigue pasando sin cambios.
- **MCP:** el tool aparece en la superficie de lectura y se llama igual que la API; el test de
  herramientas de lectura lo verifica.

## Observaciones no bloqueantes

- La aclaración de revisión nombraba dos argumentos (`target`, `document`); el ejecutor agregó un
  tercero, `tag`, porque el Done When pide explícitamente resolver un tag padre y un tag no es un
  documento. Queda como una sola operación y un solo nombre.
- Para `target` y `document`, `unresolved` recorre todos los punteros del store, no solo los
  relacionados con la consulta. El Done When solo pide informar el puntero inexistente; el ruido
  adicional no contradice el contrato, pero conviene tenerlo presente si un consumidor filtra.
- Un documento que apuntara directamente a un tag global de una equivalencia que no sea nodo del
  DAG local se trataría como `unresolved`; los documentos apuntan a tags locales (el patrón de
  `gse.` resuelve local -> global), así que no afecta los casos aceptados.
