## REFORMULACION

Encargo: hacer que el endpoint POST /save de `sldb serve` devuelva, en su respuesta 422 por validación, un campo `details` con `exc.errors()` de pydantic. Resultado esperado: ruta save modificada en `src/sldb/cli/serve/` y un test que verifique el 422 con esos details. Límites: solo la ruta save y su test; fuera queda el resto de serve. Tipo `task.code`, nodo `ritual-execution`, ejecutable (no agregado). Repo: sldb.

## AMBIGUEDADES

1. «la respuesta 422 trae details con exc.errors() de pydantic» — no fija la forma exacta: ¿`details` es la lista de `exc.errors()` o un objeto que la contiene? Obliga a inventar el contrato de respuesta.
2. «save con un campo invalido» — no identifica campo, modelo ni payload. Obliga a inventar el fixture del test.
3. «La ruta save de src/sldb/cli/serve/» — no nombra archivo ni función. Obliga a inventar la superficie exacta a tocar.
4. «un test» frente a la ruta concreta `tests/test_serve_save_422.py` — no aclara si el archivo ya existe o se crea. Obliga a inventar su estado inicial.
5. El bundle invoca «los rituales enrutados por el Board», pero `desk/tasks/Board.md` no está incluido. Obliga a inventar qué tareas están activas o si esta lo está.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout/phase, Board (ausente), `src/sldb/cli/serve/` (ruta save y manejo de errores), tests existentes de serve, versión de pydantic/FastAPI. Cambios previstos: capturar `RequestValidationError`, responder 422 con `details=exc.errors()`; añadir `tests/test_serve_save_422.py`. Dependencias: cliente de test, modelo del documento, handler actual. Validaciones futuras: el comando pytest indicado; luego ritual testing y closeout con deskops. Sin ejecutar nada.

## FUTURO

Un humano o nodo de contexto debe fijar el contrato exacto de `details`, el campo inválido de prueba y confirmar la ruta/archivo; el nodo de cierre decide commit, CHANGELOG y retirada del Board.
