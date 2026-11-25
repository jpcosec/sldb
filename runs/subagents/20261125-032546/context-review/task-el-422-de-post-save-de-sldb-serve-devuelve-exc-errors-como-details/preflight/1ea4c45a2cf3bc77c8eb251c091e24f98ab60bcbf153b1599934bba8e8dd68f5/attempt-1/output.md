## REFORMULACION

Tarea `task.code` ejecutable, no agregado. Propósito: que `POST /save` de `sldb serve`, al rechazar un documento por validación, devuelva un 422 cuyo `details` contenga `exc.errors()` de pydantic. Resultado esperado: modificar la ruta `save` de `src/sldb/cli/serve/` y añadir un test; el test debe pasar. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb` (según cwd y validación). Límites: solo la ruta `save` y un test; fuera “lo demas de serve”. Validación prevista: únicamente el comando pytest indicado, con `TMPDIR` y venv dados.

## AMBIGUEDADES

1. “La ruta save de src/sldb/cli/serve/ y un test.” No identifica módulo, función ni si el test es nuevo. Obliga a inventar la superficie exacta y el archivo de test, aunque la validación sugiere `tests/test_serve_save_422.py`.
2. “save con un campo invalido” no especifica modelo, campo ni payload. Obliga a inventar el caso concreto de validación.
3. “details con exc.errors() de pydantic” no fija la clave exacta (`details` frente a `detail`), el envoltorio ni cómo se serializa. Obliga a inventar el contrato HTTP.
4. “Partida en 4 tareas chicas al replanificar en DAG” no aporta referencias ni dependencias. Obliga a inventar si existe contexto de tareas hermanas relevante.

## DRY-RUN

Lecturas hipotéticas: TaskDoc; módulo de `save` bajo `src/sldb/cli/serve/`; tests y fixtures existentes de serve. Cambios previstos: crear `tests/test_serve_save_422.py` con un payload inválido que espere 422 y `details`; ajustar la captura de `ValidationError` para incluir `exc.errors()`. Dependencias: pydantic, framework HTTP usado por serve, pytest y entorno `.venv`/`TMPDIR`. Validación futura: ejecutar exactamente el pytest indicado y comprobar 422 y forma de `details`. No se ejecuta nada ahora.

## FUTURO

Un humano debe confirmar el contrato exacto de `details` y el campo inválido de prueba si no está ya fijado. Otro nodo podrá integrar, commitear o cerrar la tarea tras el test; las tareas hermanas del DAG no se infieren desde este input.
