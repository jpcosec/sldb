## REFORMULACION

**Propósito:** corregir el scan de enlaces de sldb para que no cuente como enlaces el contenido de bloques de código cercados (backticks o tildes) ni el código en línea, evitando falsos positivos como el ejemplo `target` de sldb-ui.

**Resultado:** comando `sldb links` y su API subyacente excluyen código fenced/inline; enlaces reales siguen detectándose; tests nuevos, CHANGELOG y commit.

**Repo/ruta:** `/mnt/ssd/proyectos/SLDB_1`; superficie: `src/sldb/cli/commands/links.py`, `tests/test_links.py`, `CHANGELOG.md`. Es un nodo ejecutable simple (`task.code`), no agregado.

**Límites:** entran fenced (backticks/tildes) e inline; no entran “otros tipos de referencia”.

## AMBIGUEDADES

1. “el parser de enlaces que usa src/sldb/cli/commands/links.py” — no identifica módulo ni función; obliga a inventar cuál es el parser real.
2. “excluir los bloques de código cercados (con backticks o tildes) y el código en línea” — no aclara anidamiento, fences sin cierre ni bloques indentados; obliga a decidir alcance.
3. “No entra: otros tipos de referencia” — no define cuáles; obliga a inventar la frontera.
4. “aviso a sldb-ui” — no indica canal, formato ni destinatario; obliga a inventar el mecanismo.
5. “CHANGELOG y commit” — no fija mensaje, formato ni granularidad; obliga a inventar convención.

## DRY-RUN

**Lecturas:** `links.py` y el parser importado; `tests/test_links.py`; `CHANGELOG.md`; posible referencia al inbox citado (solo lectura).

**Cambios previstos:** localizar el punto donde se extraen enlaces; filtrar rangos de código fenced/inline antes de contarlos, preservando enlaces reales; añadir casos de prueba con enlaces reales y ejemplos dentro de bloques; anotar en CHANGELOG.

**Dependencias:** parser Markdown existente y su API; utilidades de test presentes en el repo.

**Validaciones futuras (no ejecutadas):** `pytest tests/test_links.py`, `tests/test_links_batch_cli.py`, `tests/test_clean_code_rules.py`, `bash tools/check.sh --fast`.

## FUTURO

Un ejecutor decide el parser concreto y su estrategia de filtrado, implementa, ejecuta las validaciones, crea commit y notifica a sldb-ui. Un humano valida el cierre y el aviso.
