## REFORMULACION
Encargo ejecutable (no agregado): en el repo sldb, commit 7b9b1e6d, cerrar el resto de la seguridad de lectura de documentos trackeados. Propósito: que ninguna operación del store abra un documento trackeado que sea symlink o resuelva fuera de la raíz, usando `sldb.store.source_read` como único punto. Resultado: r1 lecturas con `unreadable_reason` + `read_source_text` y hallazgo nombrado; r2 `track` rechaza symlinks/fuera; r3 inventario archivo:línea y grep final; r4 tests de regresión con audit hook de `open` en subproceso; r5 límites de clean code, `layers.toml`, docs y CHANGELOG. Límites: fuera el comportamiento stale/rebuild (a2) y la forma de los hallazgos existentes; no subir límites; el worker no corre los 7 pasos.

## AMBIGUEDADES
1. “toda lectura del texto de un documento trackeado (o por trackear desde un path del store)”: no define qué paths del store son “documento por trackear”; obligaría a inventar criterio (extensión, ubicación, frontmatter).
2. “la extracción de campos que siguen a track/update”: no dice qué campos ni módulos; obligaría a inventar alcance.
3. “el informe trae la tabla de cada lectura”: no indica archivo, ruta ni formato del informe; obligaría a inventar el artefacto.
4. “el comando lo nombra con el hallazgo existente (store/path-outside-root o store/symlink-not-read)”: no mapea qué hallazgo corresponde a symlink dentro de raíz, symlink saliente o ruta fuera; obligaría a inventar el mapeo.
5. “stores build, build --check”: no aclara si “build --check” es el mismo comando que “stores build --check”; obligaría a inventar la CLI exacta.

## DRY-RUN
Lecturas: TaskDoc, `source_read` (`unreadable_reason`/`read_source_text`), módulos citados (`index_refresh`, `scan_rewrite_loss`, `scan_structural_noise`, `ops`, `section_rebuild`, `semantic_doc_tags`, `edge_rebuild`), `tests/store`, `tests/api`, `contracts/layers.toml`, CHANGELOG/docs. Cambios previstos: sustituir `open`/`read_text` por la guarda; rechazo temprano en `track`; inventario; tests con audit hook; docs/CHANGELOG/layers. Dependencias: `source_read` existente, hallazgos, CLI y audit hook. Validaciones futuras: tests dirigidos de store/api, `test_live_stale_security`, `test_clean_code_rules`, `check.sh --fast`; luego los 7 pasos.

## FUTURO
El coordinador ejecuta los 7 pasos del workflow en clon limpio y valida el informe; el overlord prioriza. No es ambigüedad.
