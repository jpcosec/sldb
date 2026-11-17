# Tester deskops-t-69a960ddb28e — sldb.api.code.code_facts + write_anchor público (C1, C2, C5)

**Veredicto: PASA.** Las dos fallas que aparecen (`check.sh --fast`: identidad, y `tests/test_store_seams.py`) también están en HEAD a3a091ee y no tienen que ver con este cambio.

## Validation (salida completa en validation.log)
| Comando | rc | Veredicto |
|---|---|---|
| `pytest -q tests/api/test_anchors.py` | 0 (22 passed) | PASA |
| `pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 (14 passed) | PASA |
| `pytest -q tests/test_clean_code_rules.py` | 0 (1193 passed; `-k` sobre los 3 archivos nuevos: 3 passed) | PASA |
| `bash tools/check.sh --fast` | 1 | PASA para esta tarea: núcleo, capas, **ejes** (963 archivos, 0 violaciones; con el desvío de `contracts/layers.toml`) y superficie pasan. El **único** FAIL es identidad: `archivo versionado sin clasificar en la raíz: AGENTS.md`. Se reproduce en un clon limpio de HEAD a3a091ee (/dev/shm/test-k1-clone): sale el mismo FAIL. Viene de j02 (7dbb6bc9) y es ajeno. |

No corrí la suite completa ni `sldb stores build --check`: los corre el integrador.

## Done When, punto por punto
- Los comandos de Validation pasan: **PASA**, con la salvedad de la puerta identidad de arriba (preexistente y ajena).
- `from sldb.api.code import code_facts`: **PASA** (`__all__ == ['code_facts']`).
- `from sldb.api.anchors import write_anchor`: **PASA** (`'write_anchor' in __all__`, y el test ya importa desde ahí).
- Cada fact trae span y source_hash no vacíos: **PASA**. Los tests lo cubren, `_require_anchor` lanza RuntimeError si falta alguno, y lo comprobé además en el fixture real de IR (ver más abajo).
- CHANGELOG: **PASA** (entrada en 0.1.13).
- Commit y aviso a IR: **no se pueden verificar todavía**. Son del coordinador.

## Aclaraciones del coordinador
1. El cambio son `src/sldb/api/code/` (3 archivos nuevos), `src/sldb/api/anchors/__init__.py`, `tests/api/test_anchors.py`, `CHANGELOG.md` y el desvío autorizado `contracts/layers.toml`. Los otros cambios del árbol son bookkeeping de deskops: `.sldb/*` registra los RunDoc de exec-k1 y test-k1, y `desk/inbox/...211648` está acusado y cerrado. No vi nada más fuera del contrato.
2. `check.sh --fast`: identidad (AGENTS.md) es el único fallo y las otras 4 puertas pasan. Es preexistente (comprobado en el clon de HEAD).
3. `tests/test_store_seams.py`: 1 failed, 1 passed (`io/derived_guard.py: sldb.core.exceptions`). Falla **igual en HEAD** (git archive en /dev/shm/test-k1-head). El archivo es `src/sldb/store/io/derived_guard.py`, de j02, y no `api/code`. El paquete nuevo no agrega ningún offender. `tests/test_api_surface*` no existe. La puerta superficie de check.sh pasa (0 violaciones).
4. Rutas repetidas: se aceptan una vez, sin error. Está testeado (`src/x.py`, `./src/x.py`, `src/../src/x.py`).
5. Fixture de IR `/mnt/ssd/proyectos/SLDB_1/IR/tests/fixtures/blog_app` (12 .py y 1 .sql): 33 facts de 13 archivos, `skipped=[]` y **0 facts sin span o source_hash**. Todos los spans son base 1 con fin ≥ inicio. Cada `source_hash` es igual a `sha256` de los bytes del archivo. Están todas las claves (path, span, source_hash, kind, qualified_name, signature, doc, relations, attrs). Los kinds incluyen table, column e index del SQL. El conjunto es idéntico a `scan_tree` ordenado por id.

## Regresiones vecinas
Módulos de `src/` cambiados: `sldb.api.anchors` (`__init__`) y el paquete nuevo `sldb.api.code`. El único archivo de `tests/` que los importa por nombre es `tests/api/test_anchors.py` (`grep -rlE 'api\.anchors|api\.code|anchor_docs|write_anchor|code_facts' tests`), y pasa. Por cercanía corrí además `tests/api/test_doc_anchors.py` (24 passed) y `tests/selfdoc/test_docstring_metadata.py` (14 passed). No hay fallas nuevas respecto de HEAD.

## Casos no cubiertos por el ejecutor (script /dev/shm/test-k1-scripts/edges.py)
- `root` como str relativo y un directorio como path: funciona.
- `.jsx`, `.ts` y `.js` (fuera del árbol de los tests): dan facts (component, function, module).
- Archivo `.py` vacío: un fact module con span 1–1 y el source_hash de los bytes vacíos.
- `.txt` pedido explícitamente: va a `skipped`. `paths=[]` da `{facts: [], skipped: []}`.
- Un symlink dentro de root que apunta fuera (`link_out/hosts` → /etc) lanza ValueError "outside root". Correcto.
- Dos archivos con el mismo qualified_name dan ids distintos (`a.m.f`, `b.m.f`). Los ids de un subconjunto son subconjunto de los del árbol.
- **Observación, no bloquea:** `code_facts(root, "a/m.py")`, con un str en vez de una lista, itera los caracteres y lanza `ValueError: /: absolute path`, y el mensaje nombra `/` y no la ruta. El contrato tipa `paths` como lista, así que no es FALLA, pero conviene un guard (`isinstance(paths, str)`) o un mensaje más claro. Una ruta con NUL lanza un ValueError de `lstat` sin el formato "<ruta>: ...". También es menor.

## Árbol
No edité el repo, no hice stage, commit ni stash. Las bases de HEAD están en /dev/shm (test-k1-head y test-k1-clone).
