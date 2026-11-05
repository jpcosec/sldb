# El árbol guarda, git recuerda: el journal fue retirado

Estado (2026-11-04): **implementado.** El dueño decidió el 2026-10-29 la opción (b) de la
propuesta del 2026-10-19: el pasado del árbol es la historia de git de sus shards. Con
`.sldb/core/` versionado entero ([derived-store-boundary.md](derived-store-boundary.md)), el
journal no tiene función y se retira: ninguna escritura lo produce, `sldb stores migrate-layout`
borra el que un store tenía (sin archivarlo) y `sldb journal show` responde

```
El journal fue retirado el 2026-11-04; el pasado del store se consulta con sldb docs history <doc>.
```

y sale con exit 0 (`journal verify` imprime lo mismo). Cierra
`task-congelar-journal-autoridad-arbol`: el journal quedó congelado el 2026-10-19 y retirado
ahora, en vez de rediseñado.

## 1. Qué decía la propuesta y qué quedó

La dirección era que el **árbol es la autoridad** y el journal una interfaz de lectura sobre él,
como `git log`/`git diff` sobre el object database de git, no un segundo almacén. El punto que no
se podía esquivar: una vista necesita un árbol con memoria. Las opciones eran snapshots propios
(a), apoyarse en git (b) o descartar el journal (c). Con (b), git es la memoria del árbol: cada
commit guarda los shards de `core/` tal como quedaron, y el diff entre dos commits es el diff
entre dos árboles, calculado, no guardado. El journal de punteros que (b) preveía
(`timestamp, actor, operation, address, raíz_antes → raíz_después`) no se implementa: `git log`
ya da el cuándo y el quién del commit, y `sldb docs history <doc>` lo proyecta por documento.

Lo que se pierde respecto del journal viejo, y se acepta: el quién y el cuándo **por escritura
sin commit** (varias escrituras entre dos commits se ven como una), y los valores
`previous_value`/`new_value` de cada operación. El Markdown versionado tiene el diff del
contenido; el shard versionado, el de los hashes.

## 2. Qué se retiró (2026-11-04)

- El escritor: `sldb.api.journal.record` y `sldb.store.journal.append_entry`, con su lock y su
  cadena de hashes. Los 14 puntos de escritura de `sldb.api` (documentos: create, save, track,
  untrack, delete, backfill; modelos: add, create, inherit, reindex, remove, drafts de campos y
  de template, promote; DAG semántico) ya no calculan `hash_a_before/after` ni valores previos.
- Los lectores `read_entries`/`verify_chain` y el layout `.sldb/runtime/journal/`.
  `sldb.api.journal()` devuelve `[]` y `sldb.api.verify_journal()` un reporte válido con 0
  entradas, para que quien los importe siga funcionando; `JournalEntry` y
  `JournalVerifyReport` quedan como modelos de ese contrato vacío.
- `SLDB_JOURNAL_OFF`: no hay nada que apagar.
- Los parámetros `actor` de la API se conservan. Donde sellan la procedencia del documento
  (`create_document`, `save_document_payload`, `backfill`, `delete_document`) siguen
  usándose; en el resto se aceptan por compatibilidad y no se registran.

## 3. Cómo se consulta el pasado ahora

- `sldb docs history <doc> [--since FECHA] [--format json]`: las versiones commiteadas del
  documento, quién firmó cada una y qué campos se movieron.
- `git log -- .sldb/core/documents/<Model>/<doc>.yaml`: cada commit que movió el hash de ese
  documento; `git log -- .sldb/core/store_index.yaml`, cada movimiento de la raíz.
- `git diff <a> <b> -- .sldb/core/`: el diff entre dos árboles.

Nada de esto cubre escrituras sin commit: el store refleja el estado actual del árbol y git su
historia; entre commits, `sldb stores check` dice qué se movió contra lo indexado.
