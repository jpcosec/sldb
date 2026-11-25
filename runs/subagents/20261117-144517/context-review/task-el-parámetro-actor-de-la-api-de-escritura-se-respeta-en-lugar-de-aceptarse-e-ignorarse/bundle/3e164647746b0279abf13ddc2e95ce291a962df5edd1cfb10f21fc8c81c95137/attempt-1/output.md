REFORMULACION
Propósito: que el parámetro `actor` de la API de escritura deje de aceptarse e ignorarse. Resultado: toda función pública de escritura que recibe `actor` lo propaga hasta el sello de procedencia (`sldb.by`), de modo que un documento escrito con `actor=X` quede firmado por X; las excepciones se documentan en docstring y `result-summary.md`. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambiar el formato del sello; superficie nombrada: `src/sldb/api/anchors/anchor_docs.py`, `tests/api/test_provenance.py`, `CHANGELOG.md`; validaciones: los cinco comandos listados. No es un agregado: es una `task.code`, aunque el ritual de ejecución exige atomizarla antes de implementar.

AMBIGUEDADES
1. “unas 15 tienen actor: str | None = None, y algunas lo pisan”: no hay inventario ni nombres; obliga a inventar qué funciones cuentan como “pública de escritura” y cuáles son las afectadas.
2. “incluido anchor_docs.write_anchor”: `write_anchor` no acepta `actor` y llama a `save_document_payload` sin él; obliga a inventar si se añade el parámetro, con qué valor por defecto y cómo se mantiene compatibilidad.
3. “Si alguna no puede respetarlo, se documenta en su docstring y en result-summary.md”: no se define ubicación ni formato de `result-summary.md`, ni el criterio de “no puede respetarlo”; obliga a inventar ambos.
4. “docs/architecture/provenance.md” no está en el bundle; además se anuncian “pills ligadas, los átomos ligados” pero el TaskDoc trae `pills: []` y `atoms: []`; obliga a inventar el mecanismo de sellado y el contexto faltante.

DRY-RUN
Lecturas: TaskDoc y rituales; `anchor_docs.py`; `test_provenance.py`; `provenance.md` (ausente); `test_anchors.py`, `test_api_documents.py`, `tools/check.sh` y `Board.md` (no incluidos); `CHANGELOG.md`. Cambios previstos: grep de `actor` en `src/sldb/api`; seguimiento hasta el sello; propagación de `actor` en cada camino; posible cambio de firma en `write_anchor`/`record_reconnection`; tests; docstrings/result-summary; CHANGELOG. Dependencias: inventario, `provenance.md`, Board/pills/átomos. Validaciones futuras: los cinco comandos, sin ejecutarlos ahora.

FUTURO
Decide un humano u otro nodo: el inventario exacto, si `write_anchor` cambia de firma, dónde vive `result-summary.md`, la entrada de CHANGELOG y el commit. El nodo de ejecución deberá atomizar la tarea según `ritual-execution` antes de tocar código.
