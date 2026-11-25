**REFORMULACION**

Encargo ejecutable (`task.code`) en el repo SLDB_1, paquete `sldb`: corregir la regresión de B2 (600b51a9) que hace que `component_spec_from_python` recorra `.ts/.tsx/.js/.jsx` vía `scan_tree`. Propósito: que ese generador construya el spec solo desde archivos `.py` y que ningún otro lenguaje produzca hallazgos. Resultado: filtro por extensión en el generador, test nuevo en `tests/notations/test_component_spec_python.py` que compare un árbol con `.js` minificado ilegible frente al mismo árbol sin él (mismo spec, cero hallazgos), entrada en `CHANGELOG.md` y aviso a IR. Límites: no modificar `scan_tree` para los demás consumidores (`code_facts`, anclas); no excluir `vendor/` ni `*.min.js` de `scan_tree` en general. Archivos nombrados: `component_spec_python.py`, el test, `CHANGELOG.md`.

**AMBIGUEDADES**

1. "filtrar por extensión los archivos que recorre, o pedir a `sldb.code` un escaneo limitado a Python con la API que ya existe": dos rutas alternativas sin criterio de elección; obligaría a inventar cuál API usar y dónde aplicar el filtro.
2. "como antes de B2": no define el comportamiento exacto previo; obligaría a inventar la semántica histórica sin consultar git.
3. "un .js minificado ilegible": no aclara si "ilegible" es contenido no UTF-8, sintaxis inválida o solo minificado; obligaría a inventar el fixture y su ubicación.
4. "el spec de src/sldb no cambia respecto de HEAD": falta el método de comparación (¿archivo generado?, ¿comando?); obligaría a inventar el procedimiento.
5. "fallan, de forma determinista, dos pruebas de paridad de IR" frente a una sección Validation que no las incluye: obligaría a decidir si deben pasar o quedan fuera de alcance.
6. "aviso a IR": canal y destinatario no especificados; obligaría a inventar el mecanismo.

**DRY-RUN**

Lecturas: `src/sldb/api/notations/component_spec_python.py`, `sldb.code.scan` (`scan_tree`, `scan_file`), `files.py` (`find_files`), el test y `CHANGELOG.md`. Cambios previstos: limitar el recorrido a `.py` antes o después de `scan_tree` (según la ruta elegida); añadir el test comparativo; entrada de CHANGELOG. Dependencias: extra `[code]` (tree-sitter), `uv --frozen`. Validaciones futuras: los cuatro comandos de Validation y, si se define, la comparación del spec de `src/sldb` contra HEAD. Sin ejecutar nada.

**FUTURO**

El ejecutor implementa y commitea `fix(notations): ...`; `deskops closeout` cierra la tarea y actualiza el Board; un humano decide la ruta de filtrado si persiste la ambigüedad 1, el método de comparación (4), el alcance de las pruebas de IR (5) y el canal del aviso (6). IR recibe la notificación.
