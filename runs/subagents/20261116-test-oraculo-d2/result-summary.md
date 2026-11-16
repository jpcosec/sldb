# Resultado: tester deskops-t-f05daf60b7c9

Task: `task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations`. Pills: ninguno. Salida completa en `validation.log`.

**Veredicto global: PASA**

## Validation
| Comando | Resultado | Veredicto |
|---|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q -rs tests/notations/test_component_spec_python.py` | 5 passed, 0 skips (`-rs` vacío), rc=0 | PASA |
| `! grep -n 'import.*spec2viz\|importorskip("spec2viz' tests/notations/test_component_spec_python.py` | sin coincidencias, rc=0. `grep -n spec2viz` solo encuentra docstring (l.3-5), la constante `SPEC2VIZ_GOLDEN` (l.20) y el nombre del test (l.50) | PASA |

`uv` funcionó; no hizo falta el fallback `uvx`.

## Done When, punto por punto
1. **El test pasa sin spec2viz importable** — PASA. `uv run ... python -c "import spec2viz"` → `ModuleNotFoundError`, rc=1; ningún `sys.path` contiene spec2viz; con `PYTHONPATH=src`, `importlib.util.find_spec('spec2viz')` → `None` y el archivo pasa 5/5 igualmente.
2. **El grep no encuentra imports de spec2viz** — PASA (ver tabla).
3. **Golden y CHANGELOG listos para commit** — PASA como estado previo al closeout: `tests/notations/goldens/component_spec_python_spec2viz.json` existe (sin trackear, carpeta nueva: el closeout debe incluirla explícitamente) y `CHANGELOG.md` tiene una línea en español bajo `## 0.1.13 — not released yet`, con el estilo de las vecinas. El commit lo hace el coordinador.

## Forma del golden (Scope)
- Claves exactamente `_source`, `classes`, `defines`, `modules`; `defines` como lista ordenada de pares `[from, to]`. PASA.
- `_source` = `91ba1d0ccc14716c7ad63538a1757639ab9e8c94` = `git -C /mnt/ssd/proyectos/SLDB_1/spec2viz rev-parse HEAD` actual. PASA.
- Serialización: el archivo es idéntico byte a byte a `json.dumps(g, sort_keys=True, indent=2)` (más el `\n` final). PASA.

## Casos propios (no cubiertos por el ejecutor)
1. **Regeneración independiente** (`/dev/shm/tester-oraculo/check.py`): extraje `TREE` del test con `ast`, lo escribí en `/dev/shm`, corrí `spec2viz.generators.python_ast.generate_python_ast_spec` con `PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/spec2viz` y normalicé por mi cuenta → `regenerated == golden: True`. El golden no se ajustó a mano: coincide con spec2viz.
2. **Mutaciones del golden (caso negativo)** (`/dev/shm/tester-oraculo/mutate.sh`, sobre una copia del test y del golden en /dev/shm, sin tocar el repo):
   - control → pasa;
   - quitar un módulo, añadir un `defines` (`Inner`), cambiar la etiqueta de una clase → **falla** (el oráculo detecta deriva de verdad);
   - golden ausente → **falla** (no se salta en silencio, como hacía el `importorskip`);
   - cambiar solo `_source` → pasa (esperado: `_source` es metadato, no se compara).

## Fuera de contrato
- Archivos tocados por la tarea: `tests/notations/test_component_spec_python.py`, `CHANGELOG.md` y el golden nuevo (que el Scope pide). Nada más en `src/`, `tests/` ni `desk/`.
- Resto del árbol: los cambios ajenos listados en el brief (`apply_batch.py`, `lock.py`, `tests/api/test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`), sin revisar. También hay cambios en `.sldb/` (`core/models/RunDoc.yaml`, `core/store_index.yaml`, `store.yaml` y dos RunDoc nuevos `run-deskops-e-4b91d6885d4e` / `run-deskops-t-f05daf60b7c9`): el diff solo registra los `run.md` del ejecutor y de este tester, así que es el registro de despacho de los runs, no un cambio del ejecutor. No los toqué.

## Observaciones menores (no bloquean)
- La línea del assert nuevo es larga (~170 columnas); si el repo limita la longitud de línea en `tests/`, el linter podría quejarse. No está en la Validation.
- Aviso de pytest `Unknown config option: asyncio_default_fixture_loop_scope`, preexistente y ajeno.
