## REFORMULACION

Propósito: que specIR pueda importar todo desde `sldb.api` sin tocar módulos internos. Resultado: `src/sldb/api/notations/__init__.py` reexporta los nombres del Scope (modelos de diagrama, estilos/paletas, errores, rutas de catálogo) y los incluye en `__all__`; nuevo `test_api_notations_exports` comprueba import, pertenencia a `__all__` e identidad de objeto; una línea en `CHANGELOG.md`. Repo: SLDB_1, con los tres archivos citados. Límites: no mover renombrar módulos, no tocar el repo IR, no guardar entity en SpecDoc.

## AMBIGUEDADES

1. "Validation tiene tres comandos (los dos pytest y tools/check.sh --fast)": Validation solo lista un pytest. Obliga a inventar cuál es el segundo comando pytest.
2. "en orden alfabético dentro de su grupo" (Implementation Path) frente a "en __all__ los nombres nuevos se agregan en orden alfabético al final de la lista existente" (Precisiones). Obliga a inventar la disposición final de `__all__`.
3. "El commit lo hace el coordinador con deskops closeout commit" frente a Done When "commit con los tres archivos". Obliga a decidir si el ejecutor commitea o no.
4. "Un aviso con deskops message send --to <repo>": `<repo>` no se define. Obliga a inventar el destinatario del aviso.

## DRY-RUN

Lecturas: `src/sldb/api/notations/__init__.py` (imports y `__all__`), los módulos origen citados en Scope, `tests/notations/test_notation_models_and_builtins.py`, `CHANGELOG.md`. Cambios previstos: añadir bloques de import por módulo origen, ampliar `__all__`, crear `test_api_notations_exports`, añadir entrada de CHANGELOG. Dependencias: que cada nombre exista en la ruta indicada y que `sldb.notations` reexporte los errores; que las capas permitan api→notations/models. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/notations/test_notation_models_and_builtins.py`, `tools/check.sh --fast`, y el `python -c` de Done When.

## FUTURO

Decide un humano o ejecuta otro nodo: el commit de cierre (coordinador), el envío del aviso a IR, la resolución de las ambigüedades 2-4, y la retirada de excepciones en el repo IR (fuera de alcance).
