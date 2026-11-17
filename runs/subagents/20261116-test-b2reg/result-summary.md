# Resultado — tester deskops-t-4b0ad6f4233f (regresión de B2 en component_spec_from_python)

Veredicto: **PASA**

Todos los comandos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev` (uv funcionó, no hizo falta el fallback). La salida completa está en `validation.log`.

## Validation
| Comando | Resultado |
|---|---|
| pytest -q tests/notations/test_component_spec_python.py | PASA: 6 passed, rc=0 (incluye el nuevo `test_only_python_files_make_the_spec`) |
| pytest -q tests/notations/test_component_spec_graph.py | PASA: 16 passed, rc=0 |
| pytest -q tests/test_clean_code_rules.py | PASA: 1201 passed, rc=0 |
| bash tools/check.sh --fast | PASA: TODAS LAS PUERTAS PASAN, rc=0 |

## Done When
- Validation pasa con el test nuevo: **PASA**.
- El spec de src/sldb no cambia respecto de HEAD: **PASA**. Cargué el `component_spec_python.py` de HEAD (sacado con `git archive HEAD` a /dev/shm/b2reg-t/head) y el nuevo, los corrí sobre `src/sldb` y comparé `(spec, findings)` como JSON ordenado: idénticos sin `root_package` y con `root_package="sldb"`, sin findings en los dos casos.
- CHANGELOG: **PASA**. Hay una entrada en 0.1.13 y lo que afirma es correcto: `find_files` incluye `.ts/.tsx/.js/.jsx/.sql` y `scan_tree` no cambió.
- Commit y aviso a IR: **no aplican al tester**. Los hace el cierre, porque el brief prohíbe hacer commit.

## Aclaraciones del coordinador
1. **Caso real de IR: PASA.** Leí IR sin escribir en él. Con `component_spec_from_python(IR/src/specir, project_id="specir", title="specIR")`, que es el `PACKAGE` de `tests/visual/test_sync_generation_parity.py:189`:
   - HEAD da `[('component-spec/syntax-error', 'visual/templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js')]`.
   - El cambio da `[]`.
   - Sobre `IR/src` pasa lo mismo: HEAD da el syntax-error de `specir/visual/.../bpmn-navigated-viewer.production.min.js` y el cambio da `[]`.
2. **Spec de src/sldb idéntico a HEAD: PASA** (ver arriba).
3. **`code_facts` y las anclas siguen viendo .js/.ts: PASA.**
   - `src/sldb/code/` es idéntico a HEAD (`git diff` vacío y `diff -r` contra la base).
   - `scan_tree` sobre un árbol con a.py, b.js y c.ts devuelve los tres paths. `sldb.api.code.code_facts.code_facts` también devuelve facts de a.py, b.js y c.ts.
   - Las anclas (`src/sldb/api/anchors/reconnect.py:45`) siguen llamando a `scan_tree`, y `src/sldb/api/anchors` y `src/sldb/api/code` no cambiaron.

## Caso no cubierto por el ejecutor (script /dev/shm/b2reg-t/scripts/cmp.py)
El árbol tiene `pkg/{__init__,a,b}.py`. Le agregué:
- `pkg/a.js` (mismo stem que `a.py`, con `import from './b'`);
- un `.sql` roto, un `.tsx` roto y un `.jsx` roto;
- un directorio llamado `x.py/` con un `.js` roto adentro.

Resultados:
- **HEAD:** 4 syntax-error (sql, tsx, jsx, `x.py/inner.js`). Además mezcla `a.js` en el módulo `pkg.a` y aparece una arista espuria `module_pkg_a -> module_pkg_/b`.
- **Con el cambio:** `(spec, findings)` es igual al del árbol con solo los `.py` y sin findings.

El directorio `x.py/` no se confunde con un archivo Python, porque `find_files` solo lista archivos.

## Alcance
`git diff --name-only` muestra solo los 3 archivos del contrato (`src/sldb/api/notations/component_spec_python.py`, `tests/notations/test_component_spec_python.py`, `CHANGELOG.md`), más los cambios ajenos y preexistentes en `.sldb/` y los no trackeados `desk/inbox`, `desk/runtimes` y `.herdr-coordination.md`, que no revisé. Los archivos ajenos que nombra el brief (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`) no aparecen modificados en este momento.

## Regresiones vecinas
- El único módulo de `src/` cambiado es `sldb/api/notations/component_spec_python.py`.
- `grep -rl "component_spec_python|component_spec_from_python" tests/` encuentra solo `tests/notations/test_component_spec_python.py`. Lo corrí aparte: 6 passed, sin fallas nuevas.

## No corrido
No corrí la suite completa ni `sldb stores build --check`: los delega el brief al integrador y no figuran en Validation.
