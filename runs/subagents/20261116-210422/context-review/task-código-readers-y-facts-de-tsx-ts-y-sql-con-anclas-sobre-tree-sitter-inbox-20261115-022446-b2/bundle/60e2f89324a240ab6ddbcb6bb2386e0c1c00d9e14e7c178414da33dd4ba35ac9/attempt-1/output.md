## REFORMULACION

Encargo ejecutable (no agregado): ampliar el paquete `sldb.code` de structuredLanguageDB, en `/mnt/ssd/proyectos/SLDB_1`, para leer `.ts`, `.tsx`, `.js` y `.jsx` con un reader único sobre `tree-sitter-typescript`, publicando hechos de fuente con la misma forma que Python y soportando anclas `code:<ruta>.<ext>::<símbolo>`. Resultado: `lang_ts.py`, runtime multi-gramática, dispatch en `scan.py`, extensiones en `code_ref.py` y `record_anchor.py`, dependencia en el extra `code`, fixtures y tests. Límites: SQL queda para la tarea hermana; nada de mapeo de dominio; fuera de `sldb.code` solo los dos registros nombrados; el lock lo decide el coordinador si hay cambios ajenos.

## AMBIGUEDADES

1. «cuyo cuerpo contiene al menos un nodo JSX en cualquier punto»: no define qué nodos cuentan (`jsx_element`, `jsx_self_closing_element`, fragmentos) ni si JSX dentro de funciones anidadas vale. Obliga a inventar la lista y el alcance.
2. «el comentario /** ... */ cuyo final está en la línea inmediatamente anterior a la declaración, o a su export»: con varios `/** */` seguidos o un `export default` en línea aparte, no dice cuál cuenta ni qué línea es «su export». Obliga a inventar precedencia y tratamiento del `export_statement`.
3. Enumera `export function X` y `export default function X`, pero no `export default function() {}` ni `export default memo(...)`: obliga a inventar si crean hecho y con qué nombre.
4. «Hechos en la misma forma que los de Python» y «los imports de TS/TSX»: no define el formato de `signature` ni de los targets de imports. Obliga a inventar formato.
5. «recorded_with informa la gramática del archivo»: no fija la cadena (¿versión?, ¿typescript o tsx?). Obliga a inventar formato.
6. «find_files incluye .ts/.tsx/.js/.jsx solo si la gramática está»: no dice qué gramática ni si exige el paquete completo. Obliga a inventar la condición.
7. «deskops message send --desk-root a su desk»: no da la ruta del desk de IR. Obliga a inventar destino.

## DRY-RUN

Lecturas: TaskDoc, rituales, `pyproject.toml`, `uv.lock`, `runtime.py`, `scan.py`, `code_ref.py`, `record_anchor.py`, `ids.py`, readers/imports/facts/fingerprints y los tests listados. Cambios: dependencia y `uv lock`; runtime por extensión; `lang_ts.py` nuevo con query, JSDoc e imports; dispatch y `find_files`; `parse_code_ref`; `recorded_with`; fixtures y tests de intact/changed/lost/reconnected; CHANGELOG. Dependencias: gramática instalada y lock regenerado. Validaciones futuras: los siete comandos del TaskDoc.

## FUTURO

Si `uv.lock` trae cambios ajenos, decide el coordinador. La tarea SQL depende de esta; el aviso a IR y el commit/closeout los ejecuta el nodo de cierre.
