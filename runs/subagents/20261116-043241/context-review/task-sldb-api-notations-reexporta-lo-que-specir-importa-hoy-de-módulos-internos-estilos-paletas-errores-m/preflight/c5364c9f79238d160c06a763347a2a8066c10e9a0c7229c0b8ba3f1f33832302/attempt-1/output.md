## REFORMULACION

Propósito: que `specIR` dependa solo de `sldb.api`, reexportando desde `sldb.api.notations` nombres hoy importados de módulos internos. Resultado: imports y entradas en `__all__` de `src/sldb/api/notations/__init__.py`, un test `test_api_notations_exports` en `tests/notations/test_notation_models_and_builtins.py` y una entrada en `CHANGELOG.md`. Repo: SLDB; no tocar el repo IR. Límites: no mover ni renombrar módulos, no guardar `entity` u otros datos en `SpecDoc`, no modificar el repo IR.

## AMBIGUEDADES

1. “Los tres comandos de Validation pasan”: Validation solo enumera dos comandos; el tercero parece ser el `python -c` de Done When. Obliga a decidir si ese `python -c` es validación obligatoria y cuál es el tercer comando.
2. “en orden alfabético dentro de su grupo”: no define “grupo”. Obliga a elegir el criterio de agrupación (por módulo origen, por espacio de nombres o alfabético global).
3. “AmbiguousPathError, UnknownReferenceError, UnknownNotationError (src/sldb/notations/errors/)”: da el directorio, no los módulos exactos. Obliga a inferir o localizar desde qué archivo se importa cada error.

## DRY-RUN

Lecturas previstas: `src/sldb/api/notations/__init__.py` (imports y `__all__`, líneas 49-88), ubicación de cada nombre mediante búsqueda, test existente y `CHANGELOG.md`. Cambios previstos: agregar imports y `__all__` sin mover nombres; añadir el test que importe cada nombre desde `sldb.api.notations`, compruebe pertenencia a `__all__` e identidad con el objeto original; agregar entrada de changelog. Dependencias: que los módulos y nombres existan, que `api` pueda importar de `notations` y `models` según `tools/check.sh --fast`, y que no se introduzcan ciclos. Validaciones futuras, sin ejecutar: `TMPDIR=/dev/shm pytest -q tests/notations/test_notation_models_and_builtins.py`, `bash tools/check.sh --fast` y el `python -c` de importación indicado; después, commit con los tres archivos.

## FUTURO

El repo IR debe quitar sus excepciones de import y verificar que no cambia comportamiento. Un humano decide si el commit y el cierre de la tarea son aceptables.
