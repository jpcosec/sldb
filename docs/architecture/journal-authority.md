# El árbol guarda, el journal es una vista

Estado (2026-10-19): diseño entregado, sin implementar. El journal queda **congelado**: no
se le agregan campos ni escritores nuevos. La implementación espera una decisión del dueño
(sección 4). Entregable de `task-congelar-journal-autoridad-arbol`.

## 1. Decisión tomada

El dueño decidió congelar el journal y rediseñar su relación con el árbol Merkle: el
**árbol es la autoridad** y el **journal es una interfaz de lectura** sobre él, como
`git log`/`git diff` sobre el object database de git, no un segundo almacén.

## 2. Estado actual (medido el 2026-10-19)

- `JournalEntry` (`src/sldb/store/journal/entry.py`) guarda `operation`, `address`, `field`,
  `actor` y `timestamp`; los valores `previous_value`/`new_value`; los hashes del documento
  y del store antes y después (`hash_c_*`, `hash_d_*`, `hash_a_*`); y la cadena
  (`previous_hash`/`entry_hash`). Los nombres con letra se quedan porque `entry_hash` firma
  el `model_dump()` de la entrada: renombrarlos rompe `verify_chain` en todo journal escrito.
- Escribe por `sldb.api.journal.record`, con 14 llamadas en 15 módulos de `sldb.api`
  (documentos: create, save, track, untrack, delete, backfill; modelos: add, create,
  inherit, reindex, remove, drafts de campos y de template, promote).
- Vive en `.sldb/runtime/journal/`, un YAML por escritura, sin rotación (en el store de
  este repo: unas 5.900 entradas, 24 MB). Es ignorado por git y opcional:
  `SLDB_JOURNAL_OFF=1` apaga las escrituras.
- Hoy solo audita: no hay replay ni inversa. Un save completo se podría deshacer a mano
  desde `previous_value`; create, track y untrack no guardan lo necesario
  ([versionado-y-colaboracion.md, (b)](../versionado-y-colaboracion.md)).

El problema: guarda los mismos hashes que el árbol ya calcula y además los valores, así
que es una segunda fuente de verdad. Como es opcional e ignorado por git, tampoco puede
ser la autoridad.

## 3. Dirección

1. **Árbol = autoridad.** Hoy el árbol solo tiene los hashes del estado actual. Para que el
   journal sea una vista, el árbol tiene que guardar el pasado: snapshots
   contenido-direccionados, no necesariamente completos (los shards que no cambiaron se
   comparten, como los blobs de git).
2. **Journal = lista fina de punteros:** `(timestamp, actor, operation, address,
   raíz_antes → raíz_después)`. Sin valores y sin hashes de documento.
3. **El diff se calcula** comparando dos árboles; no se guarda.

El punto que no se puede esquivar: una vista necesita un árbol con memoria. Sin el pasado
en el árbol, el journal no puede reducirse a una interfaz, y los campos de valores son lo
único que hoy permite ver qué cambió.

Mientras tanto (congelado): no se agregan campos ni escritores, no se lo usa como fuente
de verdad del estado, y `verify_chain` sigue siendo su único contrato.

## 4. Decisión pendiente del dueño

**Qué mecanismo guarda el pasado del árbol**, o si se descarta el journal. Opciones:

- **(a) Snapshots propios:** el store guarda shards y raíces viejas, contenido-direccionados,
  en `.sldb/`. Es lo más fiel a la dirección, pero agrega almacenamiento y una política
  de poda.
- **(b) Apoyarse en git:** la historia del árbol es la historia de git de los shards. Depende
  de que `.sldb/core/` siga versionado, lo opuesto a la decisión pendiente de sacarlo de git
  (nota del inbox 20261007-133032), y no cubre escrituras sin commit.
- **(c) Descartar el journal:** se borra la capa y la auditoría queda en git del markdown.
  Es lo más simple; se pierde el quién y el cuándo por escritura.

Con (a) o (b): se implementa el journal de punteros detrás de una versión de formato que
re-encadena las entradas, y se migra el lector (`sldb journal`, `sldb.api.journal`).
