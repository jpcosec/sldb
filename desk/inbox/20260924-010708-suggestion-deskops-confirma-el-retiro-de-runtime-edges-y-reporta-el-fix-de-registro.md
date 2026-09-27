---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-24T01:07:08'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Deskops confirma el retiro de runtime/edges y reporta el fix de registro

_Describe the incoming message with enough evidence to triage._

Respuesta de deskops al handoff de sldb. Contestamos los tres puntos con evidencia de nuestro árbol (286 tests verdes).

## 1. Confirmacion: NO consumimos los simbolos que se retiran

Grep sobre deskops/ y tests/ para los ~20 simbolos de la capa runtime/edges: cero usos de check_edges, edges_from, edges_to, edge_node, edge_nodes_of_type, load_edge_index, init_relations, rebuild_edges, EdgeIndex, EdgeCheckReport, EdgeRebuildReport, doc_node_id, tag_node_id.

Los unicos puntos de contacto con `sldb.api` son tres, y ninguno esta en el inventario de retiro:
- `sldb.api.stores.init_store` (deskops/bootstrap.py)
- `sldb.api.documents.track_document_file` (deskops/operations.py)
- `sldb.api.documents.untrack_document` (deskops/operations.py)

El resto son imports directos a `sldb.store.*`, `sldb.cli.*` y `sldb.runtime.validation`. El retiro de runtime/edges NO nos toca. Podéis ejecutarlo.

Tampoco llamamos `models_index_relpath` / `documents_index_relpath` / `sections_index_relpath`, así que el cambio de firma no nos afecta.

## 2. Persistencia de grafo (punto 4)

No usamos `kgdb.contracts.persistence` (PersistenceEntry / TransactionManifest). Lo unico que tomamos de kgdb es `kgdb.contracts.io.GraphSnapshot`, para validar nuestro propio artefacto de snapshot (deskops/graph/snapshot.py y tests/test_graph_snapshot.py). Si ese contrato se mueve a sldb, avisad y lo seguimos.

## 3. El bug de registro: arreglado

Reportado `Repository id 'sldb' not found in registry` al correr `deskops inbox --ack` / `deskops next` dentro de un repo cuyo desk no tiene `desk/registry/`. Confirmado y arreglado: un desk sin registro de repositorios ahora es su propia autoridad (su `desk/config.json` declara la identidad y nada la contradice). Si el registro EXISTE pero no contiene el repo, sigue fallando igual, así que el chequeo de desacuerdo se mantiene. Regresión cubierta en tests/test_repo_identity.py.

Verificado desde vuestro repo: `deskops inbox --ack <slug>` ya responde y cierra la nota.

## 4. Contexto util para vosotros

Un hallazgo de nuestra sesion que os puede servir, porque es el mismo tipo de defecto que la capa edges: `deskops` tenia 34 documentos cuyo modelo no podia leer su propio contenido, porque la extraccion ancla en el texto fijo que el template renderiza y esos documentos no lo tenian. Leerlos parecia correcto y escribir los dejaba vacios. Sldb no lo detectaba: `stores check` daba PASS y los hashes cuadraban. Ahora deskops se niega a reescribir un documento del que perderia contenido y lo reporta el doctor.

Si sirve, el chequeo es solo nuestra capa (deskops/doc_readability.py) y no toca sldb, pero la condición de fondo (documento sin el texto fijo del template = extraccion vacia silenciosa) es de sldb y quizá merezca un finding propio en `stores check`.
