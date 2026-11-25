## REFORMULACION

Encargo ejecutable (`task.code`): hacer que toda función pública de escritura de `sldb.api` que acepta `actor` lo propague hasta el punto donde se forma el sello de procedencia (`sldb.by`), de modo que un documento escrito con `actor=X` quede firmado por X y ninguna función lo descarte. Repo: SLDB_1. Superficie declarada: `src/sldb/api/anchors/anchor_docs.py`, `tests/api/test_provenance.py`, `CHANGELOG.md`; referencia `docs/architecture/provenance.md`. Fuera de alcance: cambiar el formato del sello. Cierre: pasan los cinco comandos de Validation, ningún escritor público descarta `actor`, CHANGELOG y commit.

## AMBIGUEDADES

1. "unas 15 tienen actor: str | None = None": el inventario exacto no está dado; obliga a inventar la lista o a fijarla por grep.
2. "Toda función pública de escritura": no define qué cuenta como pública ni como escritura (¿helpers, clases, `_private`?); obliga a inventar el criterio de inclusión.
3. "algunas lo pisan (por ejemplo src/sldb/api/anchors/anchor_docs.py:47...)": el número de línea puede no coincidir; obliga a inventar si el ejemplo sigue vigente.
4. "Si alguna no puede respetarlo, se documenta en su docstring y en result-summary.md": no indica ruta, formato ni esquema de `result-summary.md`; obliga a inventarlos.
5. "un documento escrito con actor=X queda firmado por X": no define qué sello corresponde cuando `actor` es `None` u omitido; obliga a inventar el fallback.
6. Validation incluye `tests/api/test_anchors.py` y `tests/api/test_api_documents.py`, ausentes en `files`; no aclara si deben modificarse o solo ejecutarse.
7. "CHANGELOG y commit": no fija formato de entrada ni mensaje/alcance del commit; obliga a inventarlos.

## DRY-RUN

Lecturas: `docs/architecture/provenance.md`, `anchor_docs.py`, grep de `actor` en `src/sldb/api`, tests citados, `CHANGELOG.md`. Cambios previstos: propagar `actor` por cada camino hasta `save_document_payload`/formador del sello; ajustar firmas y docstrings; añadir tests en `test_provenance.py`; entrada en CHANGELOG. Dependencias: firma de `save_document_payload`, helper que materializa `sldb.by`, y el inventario real de funciones. Validaciones futuras: los cinco comandos listados, sin ejecutarlos ahora.

## FUTURO

Un nodo de ejecución confirma el inventario y decide qué funciones no pueden cumplir; un humano valida el criterio de "pública de escritura", el tratamiento de `actor=None`, la ubicación/formato de `result-summary.md` y el commit final.
