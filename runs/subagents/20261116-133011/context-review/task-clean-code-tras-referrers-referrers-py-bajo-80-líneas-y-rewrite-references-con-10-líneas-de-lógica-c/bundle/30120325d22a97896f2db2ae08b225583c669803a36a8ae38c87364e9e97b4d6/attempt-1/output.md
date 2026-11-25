## REFORMULACION
- **Propósito:** eliminar la violación de clean code introducida en el repo **sldb** por `task-referrers-y-rewrite-references`: `referrers.py` supera 80 líneas efectivas y `rewrite_references` tiene 15 líneas de lógica.
- **Resultado:** `referrers.py` bajo 80 líneas efectivas; `rewrite_references` con máximo 10 líneas de lógica; misma API pública y comportamiento; tests originales verdes sin cambios; una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`; commit.
- **Repo/archivos:** `sldb`; `src/sldb/api/edges/referrers.py`, `src/sldb/api/edges/rewrite_references.py`, `CHANGELOG.md`.
- **Límites:** extraer a módulos nuevos del mismo paquete; mover `document_paths`, `frontmatter_lines` y `_in_frontmatter` a `referrer_frontmatter.py`; reexportar `document_paths` y `frontmatter_lines` desde `referrers.py`; partir `rewrite_references` en pasos con nombre; no cambiar comportamiento, tests de comportamiento ni otras violaciones. Es un nodo ejecutable, no un agregado.

## AMBIGUEDADES
1. Cita: “si check.sh muestra otras, se anotan en result-summary.md y no se tocan” frente a “Todos los comandos de Validation pasan”. Obligaría a inventar si la tarea bloquea por fallos ajenos, dónde vive `result-summary.md` y si `check.sh --fast` debe pasar pese a ellos.
2. Cita: “80 líneas efectivas por archivo” frente a “partir rewrite_references ... dentro de rewrite_references.py o en un módulo vecino”. Obligaría a inventar si todo `rewrite_references.py` debe quedar bajo 80 líneas o solo la función bajo 10.
3. Cita: “Una línea en CHANGELOG.md ... que diga que es un arreglo de clean code”. Obligaría a inventar el texto exacto y confirmar que existe el encabezado 0.1.13.
4. Cita: “los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport)” y solo se reexportan dos nombres públicos. Obligaría a inventar si `_in_frontmatter` u otros nombres privados también deben reexportarse.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, átomo, fuentes citadas, `tests/test_clean_code_rules.py`, tests de referrers y rewrite, `tools/check.sh`, `CHANGELOG.md`. Cambios previstos: crear `referrer_frontmatter.py`; mover `document_paths`, `frontmatter_lines`, `_in_frontmatter`; ajustar imports y reexportar; refactorizar `rewrite_references` en helpers —resolver grafo/exclusiones, planificar payload/texto, escribir— preservando orden, transacción y `RewriteReport`; añadir línea de CHANGELOG. Dependencias: `ProjectGraph`, `transaction`, `replace_text`, validaciones y API pública. Validaciones futuras: ejecutar los cuatro comandos y comprobar con `git diff` que no cambian tests de comportamiento.

## FUTURO
El nodo tester/closeout ejecutará las validaciones y hará el commit; deskops/humano decidirá si las otras violaciones de `check.sh` se aceptan o se abren tareas, y cerrará Board/release.
