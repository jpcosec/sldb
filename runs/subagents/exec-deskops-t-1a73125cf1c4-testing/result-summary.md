PASA

# Tester deskops-t-1a73125cf1c4: campo con default en documentos existentes

Task: `task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p`
Commit revisado: `8074f488ab9a6d4575777f51af17c84b23943117` — `Un campo ausente toma el default del modelo al extraer` (trailer `Task-Id` correcto).

Archivos del commit:
- `src/sldb/runtime/validation.py` (+9/−1)
- `tests/test_campo_con_default.py` (nuevo, 69 líneas)

## Veredicto

**PASA.** `Validator.extract` ahora descarta las claves cuyo valor extraído es `None` cuando el
campo del modelo no es requerido, de modo que pydantic aplica el default declarado. Un documento
escrito antes de agregar `espera_segundos: int = 4` con su marcador `rev` deja de quedar en
`store/doc-invalid` y su payload extraído trae `espera_segundos == 4`. Los campos requeridos y
los valores presentes pero inválidos conservan el comportamiento anterior (siguen fallando), así
que el arreglo no oculta documentos realmente malformados.

## Validación ejecutada (detalle en validation.log)

Ejecutada de a un archivo, con `TMPDIR=/tmp` y
`PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-1a73125cf1c4`:

| Comando | rc | Resultado |
|---|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_campo_con_default.py` | 0 | 1 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_validation_semantics.py` | 0 | 2 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/store/test_doc_invalid_check.py` | 0 | 2 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/store/test_doc_invalid_writes.py` | 0 | 8 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_extraction_segments.py` | 0 | 6 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_section_body_extraction.py` | 0 | 5 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_runtime_cache.py` | 0 | 8 passed |
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_field_corpus.py` | 0 | 7 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_validation.py`; para el módulo tocado (`runtime/validation.py`) se corrieron
`tests/test_validation_semantics.py` y las suites de extracción y de `store/doc-invalid` que
ejercitan el mismo camino. No se corrió la suite completa.

## El test nuevo detecta el bug

Como control negativo, corrí el test nuevo contra el árbol del commit padre (`6eaac4e4`, sin el
arreglo, en una copia temporal en `/tmp`): **falla** con
`store/doc-invalid` — `Asistente rejects a.md: espera_segundos: Input should be a valid integer`.
Con el arreglo, el mismo test pasa. El test reproduce exactamente el síntoma reportado en la nota
del 21-nov.

## Nota de entorno

`/tmp/ws-venv` no existe en este host. Usé `/workspace/sldb/.venv/bin/python` (CPython 3.13.18,
pydantic 2.13.4, pytest 9.1.1); `/workspace/sldb/.venv` y `/mnt/ssd/proyectos/SLDB_1/sldb/.venv`
son el mismo inodo. `tools/check.sh --fast` se corrió con ese `.venv/bin` primero en `PATH`.
El árbol actual incluye commits posteriores de otras tareas, pero
`git diff 8074f488 HEAD -- src/sldb/runtime/validation.py tests/test_campo_con_default.py` está
vacío: el trabajo del ejecutor es el que se probó.

## Observaciones no bloqueantes

- El alcance se respeta: solo el cambio de extracción y su test. `fields update` y las migraciones
  sin default quedan fuera, como pide el encargo.
- El filtro usa `model_fields[k].is_required()`, así que también cubre defaults por
  `default_factory`; un campo requerido ausente sigue llegando como `None` y fallando.
