# Tester deskops-t-a70c5f5c6081 — task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable

**Veredicto global: PASA.** Salida completa en `validation.log`. `uv` funcionó; no hizo falta el fallback con `uvx`.

## Validation (corrido por mí)
| comando | resultado | veredicto |
|---|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py` | 43 passed, rc 0 | PASA |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_envelope.py` | 10 passed, rc 0 | PASA |
| `TMPDIR=/dev/shm PYTHONPATH=src uv run ... python -m sldb --version` | `sldb 0.1.13 (archive/wt/h47-70-gf4d7c828-dirty at /mnt/ssd/proyectos/SLDB_1/sldb)`, rc 0 | PASA |

## Done When
- **Los tests pasan**: PASA (ver arriba). Los tres tests nuevos cubren lo que pide el Scope: rc 0 y empieza con `sldb `; con `source_revision`→None la línea es exactamente `sldb <versión>` sin paréntesis; con `'v0.1.13-1-gabc'` aparece `(v0.1.13-1-gabc at `.
- **`python -m sldb --version` desde el checkout imprime la versión con el describe entre paréntesis**: PASA. El describe coincide con `git describe --tags --always --dirty` corrido a mano (`archive/wt/h47-70-gf4d7c828-dirty`).
- **CHANGELOG**: PASA. Una línea en español, primera bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`, con el estilo de las vecinas.
- **Commit**: no aplica al tester. Según las Convenciones, lo hace el coordinador con `deskops closeout commit`; hoy no hay commit.

## Scope / Precisiones (revisado en el diff)
- `source_revision()`: llama a `_source_checkout_dir()`, que es nueva y hace el mismo recorrido; `_source_checkout_version` no cambia (lo pide el pill). Comprueba `.git` con `exists()`, así acepta archivo o carpeta. Con un spy confirmé el comando y los kwargs exactos: `['git','-C',<dir>,'describe','--tags','--always','--dirty']`, `capture_output=True, text=True, timeout=2, check=False`. Devuelve None si rc≠0, si la salida está vacía, con FileNotFoundError y con TimeoutExpired.
- `--version` está en `build_parser` de `src/sldb/cli/parsers/core.py` como `argparse.Action` propia. El contrato nombra `src/sldb/cli/parser.py`, pero el pill (Where/How) manda `parsers/core.py`. `parser.py` no se tocó. Es un desvío autorizado.
- `version_line()` es un helper extra dentro de un archivo del contrato y no amplía el comportamiento.

## Casos borde no cubiertos por el ejecutor (script `/dev/shm/sldbver-test/edge.sh`, sin editar el repo)
1. Copia del checkout **sin `.git`** → `sldb 0.1.13`, rc 0. PASA.
2. **`.git` como archivo** (`git worktree add` en /dev/shm con el src del árbol copiado; `.git` = `gitdir: ...`) → `sldb 0.1.13 (archive/wt/h47-70-gf4d7c828-dirty at /dev/shm/sldbver-test/wt)`, rc 0. PASA. Quité el worktree al terminar (`git worktree list` ya no lo muestra). El primer intento sobre HEAD sin copiar el src dio rc 2, como era de esperar, porque HEAD no tiene `--version`; no es un fallo del cambio.
3. **`.git` roto** (carpeta vacía; git describe rc≠0) → sin paréntesis, rc 0. PASA.
4. **git fuera del PATH** (FileNotFoundError) → `sldb 0.1.13`, rc 0. PASA.
5. **Parches**: TimeoutExpired → None, y `version_line` = `sldb 0.1.13`; stdout solo con espacios → None; rc 128 → None. PASA.
6. Entrypoint **`sldb --version`** (no solo `python -m`) → rc 0, y `sldb --version ls` también imprime la versión y sale con 0. PASA.

## Observaciones (no bloquean)
- `sldb --help` muestra una ayuda curada (`SHORT_ARGPARSE_HELP`, dispatcher/main) que no menciona `--version`. Queda fuera del contrato.
- Igual que dice el ejecutor: con `--tags`, el describe toma el tag ligero `archive/wt/h47` en lugar de `v0.1.13`. Cumple el comando exacto de las Precisiones; si se quiere `v0.1.13-…`, haría falta `--match 'v*'` en otra tarea.

## Archivos tocados (git status)
Del ejecutor: `src/sldb/store/package_version.py`, `src/sldb/cli/parsers/core.py`, `tests/test_cli_v2.py`, `CHANGELOG.md` (además de su run dir). Todos están en el contrato o el pill. Nada más fuera de eso, aparte de los cambios ajenos que lista el brief. `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` y los `RunDoc/run-deskops-{e-95afccc5d347,t-a70c5f5c6081}.yaml` son el registro de los runs (`include` de los run.md de este despacho) y los hizo el coordinador, no el ejecutor. Por mi parte solo escribí en `runs/subagents/20261116-test-sldb-version/` y en /dev/shm.
