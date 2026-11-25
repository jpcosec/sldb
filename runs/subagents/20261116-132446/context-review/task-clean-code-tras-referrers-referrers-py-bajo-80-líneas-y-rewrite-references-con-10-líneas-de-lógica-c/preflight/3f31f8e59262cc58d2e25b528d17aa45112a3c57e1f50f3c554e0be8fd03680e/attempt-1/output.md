## REFORMULACION

**Propósito:** corregir las violaciones de clean code introducidas por `task-referrers-y-rewrite-references` (3772a1fa), que hacen fallar `tools/check.sh`.

**Resultado:** `src/sldb/api/edges/referrers.py` con ≤80 líneas efectivas y `rewrite_references` con ≤10 líneas de lógica, sin cambiar comportamiento ni API pública; una línea en `CHANGELOG.md` y commit.

**Repo:** `/mnt/ssd/proyectos/SLDB_1`, paquete `src/sldb/api/edges`.

**Límites:** no alterar tests de comportamiento ni otras violaciones (solo anotarlas); extraer a módulos nuevos del mismo paquete con reexport desde el original.

## AMBIGUEDADES

1. «Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet'»: falta el texto exacto y confirmar que el encabezado existe; obliga a inventar redacción y ubicación.
2. «dentro de rewrite_references.py o en un módulo vecino»: obliga a inventar la estructura elegida y los nombres de los pasos.
3. «Mover document_paths, frontmatter_lines y _in_frontmatter […] (reexportar document_paths y frontmatter_lines)»: no dice si `_in_frontmatter` se reexporta; obliga a inventar.
4. «se anotan en result-summary.md»: no indica ruta ni formato; obliga a inventar ubicación y plantilla.
5. «CHANGELOG y commit»: no especifica mensaje de commit; obliga a inventarlo.

## DRY-RUN

**Lecturas:** `referrers.py`, `rewrite_references.py`, `tests/test_clean_code_rules.py`, `tests/api/test_referrers.py`, `tests/api/test_rewrite_references.py`, `CHANGELOG.md`.

**Cambios previstos:** crear `referrer_frontmatter.py` con las tres funciones movidas; reexportar `document_paths` y `frontmatter_lines`; extraer pasos con nombre en `rewrite_references`; añadir línea al CHANGELOG.

**Dependencias:** existencia del encabezado `## 0.1.13`, imports actuales de los nombres públicos.

**Validaciones futuras:** los cuatro comandos de Validation (`pytest` de referrers, rewrite_references y clean_code_rules; `tools/check.sh --fast`) y `git diff` sobre tests.

Sin ejecutar nada.

## FUTURO

El nodo tester/validador ejecuta los comandos de Validation y confirma el cierre. Un humano decide la redacción final del CHANGELOG/commit y si abre tareas para las demás violaciones anotadas.
