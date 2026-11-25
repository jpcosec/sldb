## REFORMULACION
Es una tarea ejecutable `task.code`, no un agregado. Propósito: que el scan de enlaces de sldb no cuente como enlaces el contenido de bloques de código cercados ni de código en línea, evitando falsos rotos. Resultado: parser/API usado por `src/sldb/cli/commands/links.py` corregido, tests en `tests/test_links.py` con enlaces reales y ejemplos en código, y CHANGELOG. Repo: SLDB_1. Límites: solo referencias de enlace; no otros tipos; archivos declarados links.py, tests/test_links.py y CHANGELOG; validaciones del TaskDoc.

## AMBIGUEDADES
1. Scope dice “excluir los bloques de código cercados (con backticks o tildes) y el código en línea”, pero los tests incluyen “test_parse_links_indented_code_in_list_item” y “fenced, indented and inline code”: obliga a decidir si el código indentado entra o si se ajustan tests.
2. “files: ... src/sldb/cli/commands/links.py” y “encontrar el parser de enlaces que usa...”: el parser parece estar en `src/sldb/links.py`, no listado; obliga a inventar si `files` es exhaustivo.
3. “los cuatro casos de runs/subagents/20261116-test-lk-c1/result-summary.md”: no está en el bundle; obliga a inventar los casos o a leer fuera.
4. “un cierre indentado sin apertura vista no abre un bloque nuevo que se trague el resto del archivo”: no fija columnas exactas; obliga a inventar el algoritmo.
5. “CHANGELOG y commit; aviso a sldb-ui”: no define canal ni destinatario; obliga a inventar el aviso.

## DRY-RUN
Lecturas: TaskDoc, rituales, links.py, tests/test_links.py, CHANGELOG y, si existen, src/sldb/links.py y result-summary. Cambios: localizar parse_links/recover_links; ignorar fences backticks/tildes —incluida apertura tras marcador de lista y columna de contenido—, inline code y, si se confirma, código indentado; conservar enlaces reales; añadir/ajustar tests y CHANGELOG. Dependencias: markdown-it-py opcional para contraste y fixtures CLI/store. Validaciones futuras: los cuatro comandos pytest y `check.sh --fast`. Sin ejecutar nada.

## FUTURO
Un ejecutor futuro implementa y corre validaciones. Humano/deskops decide commit, closeout, retirada del Board y aviso a sldb-ui. La disponibilidad de markdown-it-py la determina el entorno.
