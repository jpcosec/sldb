REFORMULACION
Propósito: que POST /save de sldb serve, al rechazar un documento por validación pydantic, devuelva un 422 cuyo JSON incluya `details` con la lista `exc.errors()`. Resultado: cambio en el manejador de save y un test nuevo. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo la ruta save de `src/sldb/cli/serve/` y `tests/test_serve_save_422.py`; fuera el resto de serve.

AMBIGUEDADES
1. «además de lo que ya devuelve»: no se describe el body actual del 422; obliga a inventar el esquema y campos existentes.
2. «exactamente la lista exc.errors() (serializable: loc, msg, type)»: `exc.errors()` puede incluir `ctx`/`input` no serializables; «exactamente» frente a «serializable» obliga a inventar si se filtra o se transforma.
3. «siguiendo cualquier test existente de serve»: no identifica cuál; obliga a inventar cliente de test, fixtures y convenciones.
4. «un modelo minimo con un campo int»: no dice cómo se registra o expone ese modelo en serve; obliga a inventar la API de prueba.
5. «Correr solo ese test»: contradice el ritual de testing cuando el cambio afecta comportamiento compartido («then the full suite when shared behavior changed»); obliga a decidir el alcance de validación.

DRY-RUN
Lecturas previstas: TaskDoc, Board, rituales, pills/átomos (vacíos en el frontmatter), `grep -rn 'save' src/sldb/cli/serve/`, captura de `ValidationError`, tests existentes de serve. Cambios previstos: crear `tests/test_serve_save_422.py` y modificar el manejador para añadir `details` serializando `exc.errors()`. Dependencias: versión de pydantic, cliente/fixtures de test de serve y `TMPDIR=/mnt/ssd/tmp/sldb1`. Validaciones futuras: el pytest indicado; según ritual, suite completa o checks si cambia comportamiento compartido; closeout con commit atómico.

FUTURO
Un nodo ejecutor implementará y ejecutará las pruebas. El ritual de closeout decidirá commit y cierre. Un humano debe resolver las ambigüedades 1–5 antes de ejecutar, conforme al pre-gate del ritual de ejecución.
