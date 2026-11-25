REFORMULACION
Propósito: implementar en SLDB_1 (task.code, nodo ritual-execution) una ampliación genérica de los facts de Python de `sldb.code` para que specIR derive después rutas, campos, serializers y cadenas de llamadas Django/DRF. Resultado: facts con bases de clase (`extends`), decoradores con argumentos, llamadas entre símbolos y un kind `assignment` para asignaciones de módulo/clase con llamada, lista/tupla o literal; fixture Django/DRF mínimo, tests, CHANGELOG y validaciones. Repo/rutas: `src/sldb/code/scan.py`, `readers.py`, `tests/selfdoc/test_treesitter_symbols.py`, `CHANGELOG.md`. Límites: no interpretar Django/DRF ni resolver tipos/imports; no TS/JS; este revisor no ejecuta nada.

AMBIGUEDADES
1. “NORMALIZATION: si cambia la forma de los facts existentes, se sube” no fija versión actual ni destino: obligaría a inventar número y criterio de compatibilidad.
2. “attrs.decorators: lista de {name, args, kwargs}” no define si `args` es lista ordenada, dict o texto único: obligaría a inventar el esquema.
3. “contenido en su clase o módulo” no indica relación/campo de pertenencia: obligaría a inventar el edge o atributo padre.
4. “Fixture de Django/DRF mínimo ... y tests” no fija archivos, nombres ni cobertura exacta: obligaría a inventar el fixture y casos.
5. “aviso a IR” no define canal ni formato: obligaría a inventar la notificación.
6. “módulos nuevos ... (por la regla de 80 líneas)” no nombra módulos: obligaría a inventar el despiece.

DRY-RUN
No es agregado ni paquete no ejecutable: es una tarea code. Un ejecutor futuro leería `readers.py`, `scan.py`, `facts.py`, `fingerprints.py` y los tests citados; escribiría módulos nuevos de `sldb.code`, integraría `scan_file` para `.py`, añadiría fixture y tests, actualizaría CHANGELOG. Dependencias: tree-sitter Python, `py_norm`/`signature`, modelo de facts y fingerprints existentes. Validaría con los pytest listados y `tools/check.sh --fast`, además de anclas, agreement y fingerprints. Sin ejecutar.

FUTURO
Un humano/coordinador decide versión de normalización, nombres de módulos y alcance exacto del fixture; otro nodo (IR) consume los facts y los interpreta como Django/DRF; el commit/merge y el aviso quedan fuera de este preflight.
