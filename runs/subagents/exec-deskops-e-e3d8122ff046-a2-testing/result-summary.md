# Informe del tester independiente — main de sldb en verde (job store, un solo build)

**Veredicto: PASA** — el contrato de `--keep` se cumple (pass/fail conservan la copia; DIR no vacío da rc 2 e intacto; sin `--check` rc 2; reporte equivalente salvo `kept`), los tests nuevos pasan en `7cf254f6` (35/35) y fallan al aplicarlos al código padre (8 fallos), y el job store de CI queda con un solo build de sldb; la limitación de `selfdoc` con `--pythonpath` externo se describe en §3 y no afecta al comando exacto del CI.

## 0. Entorno, alcance y método

- El path del encargo `/mnt/ssd/proyectos/SLDB_1/sldb` no existe en este contenedor. El checkout disponible es **`/workspace/sldb`**, con el commit `7cf254f6` y su padre `8420dd3a` en el historial (`git show -s`). Escribí el informe y los logs en el run dir de ese repo.
- Commit probado: `7cf254f65ee322e041bf600347bbddacbcfb091b`; padre: `8420dd3aeab873b0ca7928cc44c381f97dc09113`.
- No modifiqué el checkout principal ni commiteé. En el worktree temporal del padre superpuse el archivo de tests nuevos solo para la comprobación de regresión de §2; ese worktree se eliminó al terminar.
- No corrí builds del sldb real ni la suite completa. Los fixtures de §1 y §3 son proyectos pequeños en `/tmp` con `stores build`/`selfdoc` de verdad.
- Entorno: Python 3.13.18, pytest 9.1.1. El venv del repo tiene shebangs a rutas que no existen (`/home/robocop/...`, `/mnt/ssd/...`), así que ejecuté con el Python 3.13 de uv y `PYTHONPATH=<worktree>/src:/workspace/sldb/.venv/lib/python3.13/site-packages`. Es un detalle del contenedor, no del commit.
- `TMPDIR=/tmp` en todas las corridas.

## 1. Contrato de `--keep`

### Lectura del código (commit `7cf254f6`)

- `src/sldb/cli/parsers/stores.py:90`: define `--keep DIR` en `stores build`.
- `src/sldb/cli/commands/stores_build.py:41-44`: si `args.keep` y no `args.check`, imprime `Error: --keep only works with --check` por stderr y devuelve **2**, antes de resolver el store. Por tanto no crea ni toca DIR.
- `src/sldb/cli/commands/stores_build_check.py:41-54` (`check_command`):
  - con `--keep`, `scratch = _keep_directory(Path(keep))`; si devuelve `None`, rc **2**;
  - llama al mismo `check_build(store, root, scratch)` que sin `--keep` y solo añade `"kept": str(_copy_path(root, scratch))` al reporte;
  - sin `--keep` usa `tempfile.TemporaryDirectory`, como antes.
- `src/sldb/cli/commands/stores_build_check.py:57-64` (`_keep_directory`): resuelve DIR; si existe y no es directorio o tiene cualquier entrada, imprime `Error: --keep ... is not empty (or not a directory); give a new or empty directory` y devuelve `None`. Si no existe o está vacío, hace `mkdir(parents=True, exist_ok=True)`. No borra nada.
- `src/sldb/cli/commands/stores_build_check.py:67-69` (`_copy_path`): `scratch.joinpath(*root.resolve().parts[1:])`, es decir DIR + ruta absoluta del proyecto.
- `src/sldb/cli/commands/stores_build_check.py:72-83` (`check_build`): la lógica del veredicto (`integrity`, `undeclared`, `missing`, `differences`, `ok`) no se modificó; el `kept` se agrega fuera, en `check_command`.
- `src/sldb/cli/commands/stores_build_check.py:117-124`: `_copy_sources` copia `git ls-files --cached --others --exclude-standard`; `127-133`: `_link_siblings` deja los enlaces hermanos alcanzables con symlinks.

### Evidencia independiente (no son los tests del ejecutor)

Fixture en `/tmp` con `.sldb` real, docs selfdoc, git y un link declarado a un store ausente (`ghost`) para que el reporte también tenga una alerta. Log completo: `manual-keep-contract.log`.

**a) `--check` sin `--keep` vs `--check --keep` (paso correcto).** Ambos rc 0 y JSON idénticos salvo la clave `kept`:

```text
alerts plain: [{'code': 'build/link-missing', 'subject': 'ghost', ...}]
alerts kept : [{'code': 'build/link-missing', 'subject': 'ghost', ...}]
result equal except 'kept': True
kept copy: /tmp/keep-contract-fgdb7474/keep-pass/tmp/keep-contract-fgdb7474/project
kept copy has .sldb/store.yaml: True
stores check on kept copy rc: 0
```

**b) DIR nuevo y DIR existente vacío conservan la copia.** El nuevo se creó y el existente vacío funcionó; en ambos quedó `.../.sldb/store.yaml` y `stores check` sobre la copia devolvió 0. El caso con check fallido se cubre en (e).

**c) DIR no vacío: error claro, rc != 0 y DIR intacto.**

```text
$ python -m sldb stores build --check --keep .../keep-nonempty
rc=2
stderr: Error: --keep /tmp/keep-contract-fgdb7474/keep-nonempty is not empty (or not a directory); give a new or empty directory
non-empty rc: 2 intact: True entries: ['stale.txt']
```

Comparé hashes SHA-256 de las entradas antes y después: sin cambios. El código también rechaza un DIR que sea un fichero en la misma rama (`not keep.is_dir()`), sin escribirlo.

**d) `--keep` sin `--check` es error de uso.**

```text
$ python -m sldb stores build --keep .../keep-no-check
rc=2
stderr: Error: --keep only works with --check
no-check rc: 2 dir created: False
```

**e) El veredicto no cambia con o sin `--keep` en un check fallido.** Con `include=[]` (los documentos rastreados quedan sin declarar):

```text
plain rc: 1 kept rc: 1
plain undeclared: [] kept undeclared: []
plain missing: [] kept missing: []
plain only-local: ["only local: ('CliCommandDoc', ...)", "only local: ('SurfaceDoc', ...)"]
kept only-local : ["only local: ('CliCommandDoc', ...)", "only local: ('SurfaceDoc', ...)"]
alerts equal: True
failure result equal except 'kept': True
failed check left copy: True
```

Conclusión de §1: el contrato se cumple; el único cambio en el resultado es la clave adicional `kept` (y la línea `kept:` en texto), no rc, `undeclared`, `missing`, `only local`, `errors` ni `alerts`.

## 2. Tests nuevos contra `7cf254f6` y `7cf254f6^`

Worktrees: `/tmp/wt-7cf` en `7cf254f6` y `/tmp/wt-prev` en `8420dd3a`. Comando desde cada worktree:

```bash
TMPDIR=/tmp PYTHONPATH=<worktree>/src:/workspace/sldb/.venv/lib/python3.13/site-packages \
  python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py
```

Resultados:

- `7cf254f6`: **35 passed**, rc 0 (`pytest-stores-7cf.log`).
- `7cf254f6^` ejecutando literalmente su propio archivo: **27 passed**, rc 0 (`pytest-stores-prev.log`). **Esto no demuestra nada sobre la regresión**: el archivo de `7cf254f6^` todavía no contiene los tests nuevos; por eso no puede fallar.
- Para hacer la comprobación correcta, copié el `tests/store/test_stores_build.py` de `7cf254f6` al worktree padre y corrí el mismo comando: **8 failed, 27 passed**, rc 1 (`pytest-stores-prev-with-new-tests.log`). Fallan:
  - `test_keep_leaves_the_rebuilt_copy_with_a_usable_store_after_a_passing_check`
  - `test_keep_leaves_the_copy_when_the_check_fails`
  - `test_keep_without_check_is_a_usage_error`
  - `test_keep_refuses_a_directory_that_is_not_empty`
  - `test_keep_accepts_an_existing_empty_directory`
  - `test_keep_does_not_change_what_the_check_reports`
  - `test_selfdoc_check_on_the_kept_copy_equals_the_one_after_an_in_place_build[clean]`
  - `test_selfdoc_check_on_the_kept_copy_equals_the_one_after_an_in_place_build[stale-reference]`

Los seis primeros fallan porque el parser padre no conoce `--keep`; los dos últimos porque no se crea la copia. El informe del ejecutor dice “7 tests nuevos”; en realidad son 7 funciones, una parametrizada en dos casos: 8 casos en total. No es un fallo del cambio, solo una imprecisión del conteo.

## 3. Equivalencia de `selfdoc` (condición del coordinador)

### ¿El test compara de verdad rc y todos los hallazgos?

Sí, para los dos casos que cubre. En `tests/store/test_stores_build.py:525-546`, el test:

1. construye el proyecto `a` en sitio con `stores build` y ejecuta `_selfdoc_check(in_place)`;
2. construye el proyecto `b` con `stores build --check --keep`, entra en `_kept_copy(keep, kept_from)` y ejecuta `_selfdoc_check(copia)`;
3. compara `got == expected`.

`_selfdoc_check` (`tests/store/test_stores_build.py:446-451`) devuelve la tupla `(rc, json.loads(reporte))`; por tanto `got == expected` compara **el rc y el JSON completo**, no solo un campo. El JSON de `selfdoc check` incluye `ok`, `documents`, `missing`, `changed`, `untracked`, `stale_indexes`, `removed`, `renamed`, `semantic_gaps`, `graph_stale`, `graph_errors`, `undeclared`, `unexplained`, `unresolved_references`, `purpose_conflicts`, `metadata_errors`, `written`, `errors` y `alerts`. Además exige `changed != []` exactamente en el caso `stale-reference`. Los dos casos (`clean` y `stale-reference`) pasan en `7cf254f6` (2 passed; `pytest-selfdoc-equivalence-7cf.log`).

Límites del test, no bloqueantes para el comando CI:

- compara hallazgos, no bytes ni mtimes de los documentos generados;
- en la línea 541 no hace `assert` del rc del `stores build --check --keep` (aunque el test solo tiene sentido si la copia existe);
- usa un factory local del proyecto (`selfdoc_test_factory`) y no el factory por defecto `sldb.cli.parser:build_parser` que usa el CI; no cubre `--pythonpath`, `--store` ni `--output`.

### Caso que se le escapa (encontrado)

Probé un `--pythonpath` relativo que apunta a un symlink fuera del proyecto: `project/ext -> ../external`, con el factory en `external/ext_factory.py`, y `selfdoc sync/check --pythonpath ext --factory ext_factory:build`. En sitio funciona; en la copia de `--keep` no:

```text
$ (cd .../project && python -m sldb selfdoc check --factory ext_factory:build --pythonpath ext --system widget)
rc=0
... JSON completo, ok=true, documents=2, errores=[] ...

$ (cd .../keep/tmp/.../project && python -m sldb selfdoc check --factory ext_factory:build --pythonpath ext --system widget)
rc=1
stderr: Unexpected: No module named 'ext_factory'
expected parsed: {..., "documents": 2, "errors": [], "ok": true, ...}
got parsed: null
equal: False
```

Log: `selfdoc-escape-pythonpath.log`. Causa: `_copy_sources` copia el symlink tal cual (`../external`), pero dentro del árbol `keep` ese `../external` resuelve a una ruta distinta (no existe); `load_parser` lo usa como `pythonpath`. El test no lo detecta porque su factory está dentro del proyecto y se copia como archivo normal.

**Impacto:** el job CI ejecuta `sldb selfdoc check` sin `--pythonpath` y con el factory por defecto (`ci.yml:73`), así que este caso no afecta al job tal como está configurado. Si la condición “mismo rc y mismos hallazgos” se interpreta para cualquier invocación de `selfdoc check`, este es un contraejemplo real; queda como limitación conocida, no como bloqueo del cambio.

## 4. `.github/workflows/ci.yml`

En `7cf254f6`, el job `store` termina así:

```yaml
- name: Rebuild sldb's store from its sources
  working-directory: sldb
  run: sldb stores build --check --keep "$RUNNER_TEMP/sldb-built"
- name: Check generated CLI reference
  working-directory: sldb
  run: cd "$RUNNER_TEMP/sldb-built$PWD" && sldb selfdoc check
```

- Hay **un solo build de sldb** (`ci.yml:68`). La línea 59 es el build condicional de deskops; `make world` de pron está en 64; ninguno es un build de sldb. El anterior `sldb stores build && sldb selfdoc check` desapareció: `selfdoc check` ya no construye nada (`ci.yml:69-73`).
- `_copy_path` (`stores_build_check.py:67-69`) es `scratch + partes absolutas del root`. Comprobé la coincidencia con la expansión del shell:

```text
$ python - <<'PY'
from pathlib import Path
from sldb.cli.commands.stores_build_check import _copy_path
root = Path('/tmp/wt-7cf')
scratch = Path('/tmp/runner-temp/sldb-built')
print(_copy_path(root, scratch))
print(scratch.joinpath(*root.resolve().parts[1:]))
PY
/tmp/runner-temp/sldb-built/tmp/wt-7cf
/tmp/runner-temp/sldb-built/tmp/wt-7cf

$ RUNNER_TEMP=/tmp/runner-temp PWD=/tmp/wt-7cf bash -c 'printf "%s\n" "$RUNNER_TEMP/sldb-built$PWD"'
/tmp/runner-temp/sldb-built/tmp/wt-7cf
```

`ci-path-check.log` contiene la corrida. En el runner de GitHub `PWD` es `/home/runner/work/sldb/sldb`; la misma aritmética da `$RUNNER_TEMP/sldb-built/home/runner/work/sldb/sldb`.

**Salvedad de robustez:** `_copy_path` usa `root.resolve()` (path físico), mientras que el `cd` usa `$PWD` (path lógico del shell). En `ubuntu-latest` no hay componentes symlink en el workspace, pero en un runner con workspace symlinkado el `cd` podría no coincidir. No es el caso del CI actual; lo dejo anotado.

## 5. Comandos de la validación pedida

Ejecutados de a uno en worktrees de `7cf254f6` (luego eliminados), con `TMPDIR=/tmp`: `check.sh --fast` en `/workspace/sldb-7cf-check` y los pytest en `/tmp/wt-7cf`.

```bash
bash tools/check.sh --fast
# rc=0; TODAS LAS PUERTAS PASAN
# superficie: 2 de 4 consumidores presentes (deskops, spec2viz); faltan hum-scrapper y ontology
# la cifra total no se comprueba, 0 violaciones

python -m pytest -q -p no:cacheprovider tests/store/test_stores_build.py
# 35 passed, rc=0

python -m pytest -q -p no:cacheprovider tests/selfdoc/test_sync.py
# 5 passed, rc=0

python -m pytest -q -p no:cacheprovider tests/selfdoc/test_preflight.py
# 4 passed, rc=0
```

Log: `check-fast-7cf-workspace.log`, `pytest-stores-7cf.log`, `pytest-selfdoc-sync-7cf.log`, `pytest-selfdoc-preflight-7cf.log`. Los pytest emiten un warning de configuración (`Unknown config option: asyncio_default_fixture_loop_scope`), preexistente por la versión de pytest; no afecta al resultado.

También corrí `check.sh --fast` en el worktree `/tmp/wt-7cf`: rc 0, pero la puerta de superficie se omitió porque el padre `/tmp` no tiene los consumidores. La corrida primaria es la de `/workspace/sldb-7cf-check` (`check-fast-7cf-workspace.log`), donde sí se evaluó parcialmente.

## 6. Artefactos generados

- `pytest-stores-7cf.log` — 35 passed en 7cf.
- `pytest-stores-prev.log` — 27 passed ejecutando el archivo del padre (los tests nuevos no existen allí).
- `pytest-stores-prev-with-new-tests.log` — 8 failed, 27 passed al aplicar los tests de 7cf al código padre.
- `pytest-selfdoc-sync-7cf.log` — 5 passed.
- `pytest-selfdoc-preflight-7cf.log` — 4 passed.
- `pytest-selfdoc-equivalence-7cf.log` — 2 passed (clean, stale-reference).
- `manual-keep-contract.log` — contrato de `--keep` con fixture propio y alerta de link ausente.
- `selfdoc-escape-pythonpath.log` — contraejemplo de `--pythonpath` con symlink externo.
- `check-fast-7cf.log` y `check-fast-7cf-workspace.log` — `check.sh --fast`.
- `ci-path-check.log` — aritmética de `_copy_path` vs `$RUNNER_TEMP/sldb-built$PWD`.
- `git-commit-info.log` — SHA, padre y stat del commit.

## 7. Salvedades finales

1. **No bloqueante:** la instrucción literal “corre el archivo en `7cf^`” no puede demostrar el fallo porque ese archivo no contiene los tests nuevos; la comprobación correcta se hizo copiando los tests nuevos al código padre y da 8 fallos.
2. **No bloqueante para el CI:** `selfdoc check` con `--pythonpath` relativo a un symlink externo diverge (rc 1 en la copia, rc 0 en sitio). El comando del job no usa ese flag.
3. **Entorno:** el path del encargo `/mnt/ssd/...` no estaba montado; usé `/workspace/sldb`, que contiene el commit y el padre correctos. El venv del repo apunta a rutas ausentes; ejecuté con Python 3.13 de uv y `PYTHONPATH` explícito.
4. No se ejecutó ningún build del sldb real ni la suite completa; la validación de tiempos y la suite completa quedan para el integrador, como pide el encargo.
