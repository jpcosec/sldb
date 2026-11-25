PASA

# Tester deskops-t-79041272f6a9: docs create -o relativa contra el cwd

Task: `task-sldb-docs-create-o-resuelve-la-ruta-contra-el-cwd-o-avisa`
Commit revisado: `c5a5e2b02171db74a13ba64ea4b63590d8e0f3e0` — `docs create -o resuelve la ruta relativa contra el cwd`
Archivos del commit: `src/sldb/cli/commands/doc.py`, `tests/test_cli_v2.py`, `tests/test_docs_create_output_path.py`.

## Veredicto

**PASA.** `DocCLI.add` resuelve `args.output` con `Path(...).resolve()` antes de llamar a
`create_document`, de modo que una `-o` relativa se interpreta contra el cwd del proceso y no
contra la raíz del store/proyecto. El test nuevo reproduce exactamente el contrato: con cwd en
`<repo>/sub`, `docs create -o sub.md` deja el archivo en `<repo>/sub/sub.md` y no en
`<repo>/sub.md`. El test habría fallado antes del arreglo, porque `create_document._resolve_path`
resuelve las rutas relativas contra `project_root`.

## Validación ejecutada (detalle en validation.log)

Se corrieron de a un archivo, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-79041272f6a9`:

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider tests/test_docs_create_output_path.py` | 0 | 1 passed |
| `python -m pytest -q -p no:cacheprovider tests/test_cli_v2.py` | 0 | 50 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existe un `tests/test_doc.py` específico para `src/sldb/cli/commands/doc.py`; el test de
módulo que ejerce ese CLI es `tests/test_cli_v2.py`, que fue incluido en el commit y corrido.
No se corrió la suite completa.

## Comprobaciones adicionales

- El test nuevo usa un store temporal y un cwd en un subdirectorio, y además verifica que la
  ruta antigua (`<repo>/sub.md`) **no** existe, no solo que la nueva existe.
- `Path.resolve()` se aplica también a rutas absolutas sin alterar su destino, y conserva la
  detección de symlinks de `create_document` (que recibe la ruta ya resuelta).
- Los dos tests preexistentes de `test_cli_v2.py` afectados pasan `-o` como ruta absoluta; el
  cambio no altera su intención (escribir en el store temporal), y la suite de ese archivo pasa.
- Sin cambios fuera de los tres archivos del commit; los cambios en `.sldb/`, `desk/` y
  `.deskops.log` son del despacho, ajenos al ejecutor.

## Observaciones no bloqueantes

- El docstring de `create_document` sigue diciendo que una ruta relativa es relativa a la raíz
  del proyecto. Sigue siendo cierto para esa API de bajo nivel; el contrato del CLI es quien
  resuelve contra el cwd antes de llamarla. No afecta al comportamiento pedido.
