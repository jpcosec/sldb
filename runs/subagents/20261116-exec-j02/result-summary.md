# Resultado: deskops-e-d029d60e0080 (merge de dos .sldb sin detenerse)

Estado: LISTO, rc 0 en los tres comandos de Validation, en `tests/test_clean_code_rules.py` y en `tools/check.sh --fast`. No hice commit ni mandé avisos (aclaración 4 del coordinador).

## Qué cambié (archivo y función)

- `src/sldb/store/io/derived_guard.py` (nuevo): `has_conflict_markers`, `unmerged_index_error` y `guarded_load`. Un índice derivado con marcadores `<<<<<<<`/`|||||||`/`=======`/`>>>>>>>`, o que no parsea (YAML, pydantic o un valor que no es mapping), lanza `SLDBStoreError("<ruta> is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)")`. Un archivo que falta conserva su `FileNotFoundError`.
- `src/sldb/store/io/__init__.py`: `load_store_index` y `load_models_index` pasan por `guarded_load`. Es un import y 2 líneas más.
- `src/sldb/api/stores/conflict_sides.py` (nuevo): `conflict_sides(text) -> (ours, theirs)` reconstruye cada lado desde los hunks (descarta la base diff3), y `union_by(ours, theirs, key)`.
- `src/sldb/api/stores/store_file_merge.py` (nuevo): `merge_index_data` une stores, models y predicates por nombre; `merge_declaration_data` une links y models por nombre, predicates por clave e `include` con `merge_includes`. Esta última junta las paths por modelo sin repetir ruta, salta un glob que ya está y agrega una regla nueva. En todos los casos gana la rama actual.
- `src/sldb/api/stores/derived_recovery.py` (nuevo): `recovered_data(path, merge)`. Un archivo que parsea se usa tal cual; uno con marcadores da la unión de sus dos lados; uno que no parsea y no tiene marcadores sale de `git show HEAD:`. Si nada de eso sirve, da un error que dice cómo restaurarlo.
- `src/sldb/api/stores/rebuild_index.py` (nuevo): `rebuild_index(store)` y `locate_store(store)`. `locate_store` encuentra el store sin leer su índice. Los pasos, bajo el lock del store: (1) repara `store.yaml` si tiene marcadores; (2) repara `store_index.yaml`; (3) repara cada `models/*.yaml`, tomando el lado actual; (4) recién ahí llama a `open_store`, que lee los índices; (5) recalcula cada nodo de modelo: el roster con `documents_hash._hash_b` sobre los shards de `compose_documents_entries`, el contrato con `stamp_model_node` (→ `hash_model_contract`/`hash_model_layer`) y `documents_count`; (6) llama a `ops.cascade_store_hash`. Devuelve `{repaired, models}`.
- `src/sldb/api/stores/merge_driver.py` (nuevo): `store_file_kind(%P)` y `merge_driver(%O, %A, %B, %P)`. Para `models/*.yaml` deja `%A` y sale 0. Para `store_index.yaml` deja `%A` más los modelos, links y predicados que solo registró `%B`, y sale 0. Para `store.yaml` une con `merge_declaration_data` y sale 0. Cualquier otro archivo sale 1.
- `src/sldb/api/stores/merge_driver_install.py` (nuevo): `install_merge_driver(store_path)` escribe las 3 líneas que falten en `.gitattributes` (rutas relativas al toplevel de git) y en `git config` pone `merge.sldb.name` y `merge.sldb.driver = sldb stores merge-driver %O %A %B %P`. Es idempotente.
- `src/sldb/api/stores/branch_stores.py` (nuevo): `branches_with_store(root)` devuelve las ramas locales, menos la actual, cuyo árbol (`git ls-tree --full-tree`) tiene `.sldb/store.yaml` o `.sldb/core/store_index.yaml`.
- `src/sldb/cli/parsers/stores_merge.py` (nuevo): `add_merge_parsers` define los subparsers `rebuild-index` (`--store`) y `merge-driver` (`files` %O %A %B %P, `--install`, `--store`), con help y description que explican cuándo usar cada uno.
- `src/sldb/cli/parsers/stores.py`: llama a `add_merge_parsers(sub)`.
- `src/sldb/cli/commands/stores_merge.py` (nuevo): `rebuild_index_command` y `merge_driver_command`.
- `src/sldb/cli/commands/stores.py`: `run` despacha `rebuild-index` y `merge-driver` a la nueva `_merge`.
- `src/sldb/cli/commands/store_init.py`: `_alert_other_branches` imprime por stderr `alert: branch '<rama>' already has a store at .sldb/; merge that branch instead of creating a second store (one store per repository)` y después crea el store igual.
- `AGENTS.md` (nuevo, raíz) y `docs/versionado-y-colaboracion.md`: sección «Merge de .sldb» con los tres comandos, cuándo correr cada uno, el procedimiento y el error exacto.
- `CHANGELOG.md`: entrada en 0.1.13.
- Tests nuevos:
  - `tests/store/test_merkle_shards.py`: `test_rebuild_index_turns_conflicted_indexes_into_the_clean_ones` y `test_merge_driver_joins_the_include_rules_of_store_yaml`.
  - `tests/store/test_update_fault_tolerance.py`: `test_a_conflicted_derived_index_says_which_command_to_run`, `test_merge_driver_install_is_idempotent` y `test_stores_init_alerts_when_another_branch_already_has_a_store`.

## Done When, punto por punto

- Los tres comandos de Validation pasan con los tests nuevos: 8 passed, 6 passed y 27 passed, todos con rc 0 (ver `validation.log`).
- Prueba a mano de dos ramas, con y sin driver: está abajo; el script quedó en `manual-two-branches.sh`.
- `AGENTS.md` y `docs/versionado-y-colaboracion.md` tienen la sección «Merge de .sldb». `check_claims.py` sobre los dos: PASS, 24 afirmaciones y 0 falsas.
- `sldb stores --help` lista `rebuild-index` y `merge-driver`; la salida está abajo.
- CHANGELOG: hecho. El commit **no lo hice**, porque el brief y la aclaración 4 del coordinador lo prohíben; queda para el integrador/closeout.
- Nota a mepu: **no la mandé** (aclaración 4). Texto sugerido para el closeout: «Ya existe el merge driver de sldb. Una vez por clon: `sldb stores merge-driver --install`. Después de cada merge o rebase que toque `.sldb/`: `sldb stores rebuild-index` y `sldb stores check`. Sin el driver, sldb falla con un mensaje que nombra `sldb stores rebuild-index`: córrelo y seguí. `stores init` avisa si otra rama ya tiene store; en ese caso mergeá esa rama en vez de crear un segundo store.»

## Comandos corridos (rc)

- `pytest -q tests/store/test_update_fault_tolerance.py` → rc 0, 8 passed
- `pytest -q tests/store/test_merkle_shards.py` → rc 0, 6 passed
- `pytest -q tests/store/test_stores_build.py` → rc 0, 27 passed
- `pytest -q tests/test_clean_code_rules.py` → rc 0, 1190 passed
- `bash tools/check.sh --fast` → rc 0, TODAS LAS PUERTAS PASAN
- `python tools/check_claims.py AGENTS.md docs/versionado-y-colaboracion.md` → PASS. Sobre `CHANGELOG.md` da 3 falsas (`docs/missing`, `docs/ambiguous`, `sldb query`), pero ya estaban en HEAD: `git show HEAD:CHANGELOG.md` las tiene y mi diff no.
- `python -m sldb selfdoc check` → rc 0, `ok: true`, solo alertas: faltan `knowledge/commands/cmd-sldb-stores-{merge-driver,rebuild-index}.md` y `surface-sldb-stores.md` está desactualizado. `sldb selfdoc sync` escribe en `knowledge/` y `.sldb/`, que no tengo permitido tocar, así que **queda para el integrador**.
- La suite completa y `sldb stores build --check` no figuran en Validation y no los corrí.

## Prueba a mano en /dev/shm (dos ramas que tocan documentos distintos)

Repo de prueba: modelo `Note`, documento base `n0`; `rama-a` crea `a`, `rama-b` crea `b`, cada rama hace `stores declare --write` y luego se corre `git merge rama-a` sobre `rama-b`. Git invoca el `sldb` del PATH (`~/.local/bin/sldb`, una versión instalada vieja que no conoce `merge-driver`), así que para esta prueba puse primero en el PATH un shim que corre el checkout (`uv run --project …`). Lo anoto en la doc: el `sldb` del PATH tiene que ser una versión que conozca el driver.

### Con driver
```
$ sldb stores merge-driver --install
merge driver installed: 3 .gitattributes lines added, 2 git config keys set
$ (otra vez)
merge driver installed: 0 .gitattributes lines added, 0 git config keys set
.sldb/core/store_index.yaml merge=sldb
.sldb/core/models/*.yaml merge=sldb
.sldb/store.yaml merge=sldb
$ git merge rama-a
Auto-merging .sldb/core/models/Note.yaml
Auto-merging .sldb/core/store_index.yaml
Auto-merging .sldb/store.yaml
Merge made by the 'ort' strategy.
 .sldb/core/documents/Note/a.yaml | 14 ++++++++++++++
 .sldb/store.yaml                 |  1 +
 docs/a.md                        |  9 +++++++++
 3 files changed, 24 insertions(+)
 create mode 100644 .sldb/core/documents/Note/a.yaml
 create mode 100644 docs/a.md
rc=0
$ sldb stores check
PASS: store integrity
alert: [store/roster-stale] Note: roster hash disagrees but all 3 documents present are clean: the list is incomplete or a document joined/left without reindexing — `stores update` recomputes it
    fix     : sldb stores update
rc=0
$ sldb stores rebuild-index
rebuilt 1 model indexes and the store index
rc=0
$ sldb stores check
PASS: store integrity
rc=0
$ grep include store.yaml
include:
- model: Note
  paths:
  - docs/n0.md
  - docs/b.md
  - docs/a.md
graph_backend: networkx
policy: {}
```

### Sin driver
```
$ git merge rama-a
Auto-merging .sldb/core/models/Note.yaml
CONFLICT (content): Merge conflict in .sldb/core/models/Note.yaml
Auto-merging .sldb/core/store_index.yaml
CONFLICT (content): Merge conflict in .sldb/core/store_index.yaml
Auto-merging .sldb/store.yaml
CONFLICT (content): Merge conflict in .sldb/store.yaml
Automatic merge failed; fix conflicts and then commit the result.
rc=1
A  .sldb/core/documents/Note/a.yaml
UU .sldb/core/models/Note.yaml
UU .sldb/core/store_index.yaml
UU .sldb/store.yaml
A  docs/a.md
$ sldb stores check
/dev/shm/j02/repo-nodriver/.sldb/core/store_index.yaml is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)
rc=1
$ sldb stores rebuild-index
repaired /dev/shm/j02/repo-nodriver/.sldb/store.yaml
repaired /dev/shm/j02/repo-nodriver/.sldb/core/store_index.yaml
repaired /dev/shm/j02/repo-nodriver/.sldb/core/models/Note.yaml
rebuilt 1 model indexes and the store index
rc=0
$ sldb stores check
PASS: store integrity
rc=0
$ grep include store.yaml
include:
- model: Note
  paths:
  - docs/n0.md
  - docs/b.md
  - docs/a.md
graph_backend: networkx
policy: {}
```

En los dos casos, `diff -r` entre `.sldb/core` tras `rebuild-index` y una copia del mismo árbol tras `sldb stores update && sldb stores build` no da diferencias: «driver: rebuild-index == update+build» y «nodriver: rebuild-index == update+build».

### Aviso de stores init (rama huérfana `dev`, con store en `main`)
```
alert: branch 'main' already has a store at .sldb/; merge that branch instead of creating a second store (one store per repository)
Initialized store at /dev/shm/j02/init-test/.sldb
rc=0
```

### sldb stores --help (extracto)
```
    rebuild-index       Regenerate the derived store indexes from the shards
                        (after a merge).
    merge-driver        Git merge driver for .sldb/ files; --install registers
                        it in this clone.
```

## Archivos tocados (lista exacta)

Modificados: `CHANGELOG.md`, `docs/versionado-y-colaboracion.md`, `src/sldb/cli/commands/store_init.py`, `src/sldb/cli/commands/stores.py`, `src/sldb/cli/parsers/stores.py`, `src/sldb/store/io/__init__.py`, `tests/store/test_merkle_shards.py`, `tests/store/test_update_fault_tolerance.py`.

Nuevos: `AGENTS.md`, `src/sldb/api/stores/{branch_stores,conflict_sides,derived_recovery,merge_driver,merge_driver_install,rebuild_index,store_file_merge}.py`, `src/sldb/cli/commands/stores_merge.py`, `src/sldb/cli/parsers/stores_merge.py`, `src/sldb/store/io/derived_guard.py`.

Más la evidencia en `runs/subagents/20261116-exec-j02/` (`validation.log`, `result-summary.md` y `manual-two-branches.sh`).

No toqué `.sldb/`: los cambios en `RunDoc.yaml`, `store_index.yaml`, `store.yaml` y el RunDoc nuevo son del coordinador. Tampoco toqué `desk/` ni `.herdr-coordination.md`, y `src/sldb/api/stores/update_store_indexes.py` no hizo falta tocarlo.

## Desvíos y dudas

1. **Archivos fuera de la lista del contrato.** Son todos módulos nuevos que el Scope autoriza (API en `src/sldb/api/stores/`, comando en `src/sldb/cli/commands/`, `AGENTS.md`) y que exige la regla de 80 líneas: `parsers/stores.py` ya tenía 78 líneas efectivas, de ahí `parsers/stores_merge.py`. La guarda está en `src/sldb/store/io/derived_guard.py` para no engordar `io/__init__.py`.
2. **El driver en `store_index.yaml` no deja `%A` puro.** Le suma lo que solo registró `%B` (modelos, links y predicados, por nombre). Con `%A` puro, un modelo que agregó la otra rama quedaba con su `models/X.yaml` y sus shards, pero sin entrada en el índice. Del mismo modo, en `store.yaml` uno también links, modelos y predicates por nombre, además de los `include`: un include de un modelo que la otra rama declaró, sin su declaración, rompe el build.
3. **«Sin leer los índices derivados actuales».** Lo interpreté así: no se confía en ningún hash ni conteo, todos se recalculan desde los shards y los contratos. Lo registrado (qué modelos, links, predicados, `model_ref` y `semantics`) sí se lee de los índices, reparados primero (unión de lados o `HEAD`). Reconstruirlo desde cero obligaría a re-registrar cada modelo (`add_model` / `inherit_model`). El resultado coincide byte a byte con `stores update` + `build` en la prueba a mano.
4. **`rebuild-index` también repara `store.yaml` cuando tiene marcadores**, con la misma unión que el driver. Sin eso, un merge hecho sin el driver no terminaba con un solo comando.
5. **Después de un merge con el driver, los hashes quedan viejos** hasta correr `rebuild-index`. `stores check` lo muestra como alerta `store/roster-stale` con PASS. Correr `rebuild-index` automáticamente tras el merge sería un hook post-merge, que es H1 y está fuera de alcance; el procedimiento documentado lo incluye.
6. **Commit, aviso a mepu y `selfdoc sync` quedan para el integrador/closeout.**
