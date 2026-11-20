FALLA

# Testing — raw_atoms_by_view: atoms_dir manda para todas las vistas

## Veredicto

**FALLA** por la puerta rápida: `bash tools/check.sh --fast` termina con **rc 1** porque falla `identidad`
por un directorio preexistente sin clasificar (`workbench_demo`, incorporado en `562847e2`, anterior al
commit del ejecutor y ajeno a este cambio). La regla del rol es explícita: rc distinto de 0 en
`check.sh --fast` ⇒ FALLA. Las demás puertas pasan y los tests de la tarea pasan; el comportamiento pedido
está implementado. Si el coordinador acepta formalmente esta roja preexistente como excepción (como se hizo
en `runs/subagents/exec-deskops-t-81480618a15e-testing`), el veredicto funcional es PASA.

## Trabajo localizado

- Commit con el trailer de la tarea: `eb42a49ef62a74a9250f2157e1c93dc3d34d1b3e`
  (`raw_atoms_by_view: atoms_dir manda para todas las vistas (el código quedó en 0f91540d)`).
  Ese commit es **vacío**: `git show --name-only eb42a49e` no lista archivos.
- Los cambios de esta tarea están en `0f91540dfbaee9a0eae95b2c0a20b71db0ad1d78` (commit de otra tarea,
  `Task-Id: task-on-write-...`), que mezcló los tres archivos de esta tarea. Es un incidente de índice
  compartido ya reportado por el ejecutor; el código sí está en HEAD.
- Archivos efectivos:
  - `src/sldb/api/matching/atoms_by_view.py`
  - `tests/matching/test_matching_refs.py`
  - `CHANGELOG.md`

## Qué se verificó

- `raw_atoms_by_view` (líneas 19-30): con `atoms_dir` truthy hace
  `payload = json.loads(parse_atoms(atoms_dir, findings))` y asigna ese mismo payload a **todas** las vistas
  (`atoms_by_view = {view.key: payload for view in views}`), sin ejecutar `reader.atoms`; la rama sin
  `atoms_dir` conserva el comportamiento anterior (store por vista).
- Docstring actualizada para decir que con `atoms_dir` no se consulta ningún store.
- Test nuevo `tests/matching/test_matching_refs.py::test_raw_atoms_by_view_atoms_dir_rules_every_view_and_no_store_is_read`
  (línea 133): dos vistas, una con store (`matching_store` con `atomo y`) y otra sin store, más un
  `atoms_dir` con `atomo z`; con directorio ambas vistas traen solo `atomo z` y un `StoreReader` inyectado
  queda vacío (`reader._docs == {}`); sin directorio la vista con store trae `atomo y`, no `atomo z`, y la
  vista sin store queda vacía.
- Línea de CHANGELOG bajo `## 0.1.13 — not released yet` presente (línea 10), en español y con el test citado.
- No existe `tests/test_<modulo>.py` para `atoms_by_view`; el archivo de test del cambio y el resto de
  `tests/matching/` son la cobertura aplicable.

## Tests ejecutados (de a uno, con TMPDIR=/tmp)

Base: `/workspace/sldb/.venv/bin/python -m pytest -q` (`/tmp/ws-venv` no existe en este contenedor).

| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm python -m pytest -q tests/matching/` | 32 passed, rc 0 |
| `TMPDIR=/tmp python -m pytest -q tests/matching/test_matching_refs.py` | 11 passed, rc 0 |
| `TMPDIR=/tmp python -m pytest -q tests/matching/test_matching_refs.py -k atoms_dir_rules` | 1 passed, rc 0 |
| `TMPDIR=/tmp python -m pytest -q tests/matching/test_matching_explicit.py` | 15 passed, rc 0 |

Detalle completo en `validation.log`.

## Gate rápido

`bash tools/check.sh --fast` → **rc 1**, únicamente por:

    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"

`workbench_demo` está versionado desde `562847e2` y la tarea de decisión es
`task-clasificar-workbench-demo-en-contracts-identity-toml-...`; este cambio no toca
`contracts/identity.toml` ni `workbench_demo`. Las puertas `núcleo aislado`, `capas`, `ejes` y `superficie`
pasan.

## Aviso

Aviso a IR: `raw_atoms_by_view` ahora respeta `atoms_dir` para todas las vistas y no consulta stores
(código en `0f91540d`; commit con trailer `eb42a49e`). No se envió `deskops message send`.
