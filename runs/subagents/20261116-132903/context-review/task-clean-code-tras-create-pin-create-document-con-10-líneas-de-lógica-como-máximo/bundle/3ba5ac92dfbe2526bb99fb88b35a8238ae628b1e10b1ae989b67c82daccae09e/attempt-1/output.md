REFORMULACION

Propósito: eliminar la violación de clean code introducida por task-create-document-pinnea (commit e82d62ba) en `src/sldb/api/documents/create_document.py`, donde `create_document` tiene 12 líneas de lógica y el máximo es 10. Resultado: extraer funciones privadas o clases a módulos nuevos junto al original, en el mismo paquete, sin cambiar comportamiento ni API pública (reexport); que pasen `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast`; añadir una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`; commit. Repo: sldb. Límites: no cambiar comportamiento ni tests de comportamiento; otras violaciones se anotan en `result-summary.md` y no se tocan.

AMBIGUEDADES

1. "12 líneas de lógica (máximo 10)": no se incluye `tests/test_clean_code_rules.py`; habría que inventar qué cuenta como lógica y cómo se miden las "80 líneas efectivas".
2. "en el mismo archivo si este sigue bajo 80 líneas": falta el conteo actual y no se concreta qué extraer; obliga a inventar el criterio y el corte.
3. "o en un módulo vecino": no se da nombre ni ruta del módulo nuevo; obliga a inventar.
4. "Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet'": no se incluye el CHANGELOG; no se puede verificar que exista esa sección ni el texto exacto.
5. "los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport)": no se listan consumidores ni imports; obliga a inventar los reexports.
6. "los tests de la tarea original siguen verdes sin cambios": no se nombra el conjunto exacto; los tres tests de Validation son una suposición.

DRY-RUN

Lecturas: `create_document.py`, `tests/test_clean_code_rules.py`, `CHANGELOG.md`, los tres tests de Validation, `git show e82d62ba`, `tools/check.sh`.
Cambios previstos: extraer el paso de pin/render/escritura a función privada o módulo vecino; reexportar nombres; una línea en CHANGELOG. No tocar tests.
Dependencias: `uv --frozen`, extras `code` y `dev`, `TMPDIR=/dev/shm`.
Validaciones futuras: los cinco comandos de Validation.

FUTURO

Un nodo ejecutor aplica el refactor y la validación; deskops y el ritual de closeout cierran la tarea (commit, Board, tree limpio); un humano decide qué hacer con otras violaciones anotadas.
