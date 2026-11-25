## REFORMULACION

Encargo ejecutable de depuración: corregir `undo_changes` de sldb MCP. Propósito: (a) documentar que deshacer es una escritura nueva que re-sella procedencia y hashes; (b) hacer que el guard stale compare contenido sin procedencia; (c) hacer `steps=N` atómico, validando toda la cadena antes de escribir. Resultado: dos tests nuevos que fallan antes y pasan después, suite de sldb en verde y aviso a IR con el commit. Repo implícito: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: no cambiar formato de procedencia ni `source_hash`; specIR/IR04b fuera; tocar `src/sldb/mcp`, `src/sldb/api`, tests, CHANGELOG y doc de undo.

## AMBIGUEDADES

1. «IR/tests/test_mcp_undo.py» y «IR/runs/subagents/deskops-e-674fcb14989b-a2/»: no se define la base de esas rutas; obligaría a inventar dónde está IR.
2. «src/sldb/mcp y src/sldb/api, donde están el guard y la pila»: no identifica archivos ni símbolos; obligaría a inventar ubicaciones.
3. «reutilizar la función de sldb que ya calcula el hash de contenido si existe»: no consta que exista ni su nombre; obligaría a inventar API o duplicar lógica.
4. «donde está la doc de undo_changes»: no nombra archivo; obligaría a inventar destino documental.
5. «escribe bajo el cerrojo del store»: no especifica API de cerrojo ni alcance; obligaría a inventar mecanismo.
6. «la suite completa de sldb pasa (la integrate)» frente a la validación limitada a `tests/mcp`: no hay comando de suite completa ni se define quién integra.
7. «avisar a IR por deskops message send con el commit»: faltan destinatario, formato y rama/mensaje de commit; obligaría a inventarlos.

## DRY-RUN

Lecturas: TaskDoc, artefactos IR citados, código del guard y pila, tests existentes, doc y CHANGELOG, y búsqueda de hash de contenido. Cambios previstos: tests reproducibles primero; guard basado en hash sin procedencia; validación encadenada en memoria y escritura única bajo cerrojo; documentación y CHANGELOG. Dependencias: acceso a IR, store y entorno pytest. Validaciones futuras: ejecutar `tests/mcp`, comprobar fallo/paso, ejecutar suite completa y enviar aviso. Nada se ejecuta aquí.

## FUTURO

Un humano o nodo integrador debe resolver rutas de IR, comando de suite completa y destinatario del aviso. Otro ejecutor aplica cambios, ejecuta tests y hace commit. IR04b se reanuda tras recibir la nota con el commit.
