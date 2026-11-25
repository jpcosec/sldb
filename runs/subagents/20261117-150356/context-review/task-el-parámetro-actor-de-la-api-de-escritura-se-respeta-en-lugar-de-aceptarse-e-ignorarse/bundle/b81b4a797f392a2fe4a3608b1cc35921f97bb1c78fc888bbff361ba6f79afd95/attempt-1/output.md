## REFORMULACION

Encargo del nodo `task.code` en `/mnt/ssd/proyectos/SLDB_1`: conseguir que toda función pública de escritura de `src/sldb/api` que acepta `actor` lo propague hasta el sello de procedencia (`sldb.by`), sin cambiar el formato del sello. Resultado: código corregido, tests en `tests/api/test_provenance.py`, inventario y excepciones en `result-summary.md`, `CHANGELOG` y commit. Límites: `docs/architecture/provenance.md` solo se lee; `actor=None` conserva el sello actual; `write_anchor` gana `actor` como último parámetro y lo pasa a `create_document` y `save_document_payload`.

## AMBIGUEDADES

1. “cuenta toda función sin _ inicial que escribe documentos o el índice”: no define qué operaciones constituyen “escribir el índice” ni ofrece lista; obligaría a inventar el criterio de inventario.
2. “Toda función pública de escritura que acepta actor” frente a “sin _ inicial”: no fija si “pública” significa exportada, documentada o solo sin guion bajo; obligaría a inventar el criterio de publicidad.
3. “por ejemplo src/sldb/api/anchors/anchor_docs.py:47 llama save_document_payload con actor=None” frente a “write_anchor gana actor…”: no aclara si `record_reconnection`, que descarta `actor`, también debe aceptarlo; obligaría a decidir su alcance.
4. “actor=None deja el sello exactamente como hoy (el valor por defecto actual de sldb.by)”: no explicita si “hoy” es el literal `agent` o `current_actor()`/`SLDB_ACTOR`; obligaría a inventar la semántica de `None`.
5. “Si alguna no puede respetarlo, se documenta en su docstring”: no da criterios de excepción; obligaría a inventar cuándo una función “no puede”.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, los rituales, `docs/architecture/provenance.md`, `anchor_docs.py`, `test_provenance.py`, tests de anchors/API y el código que forma el sello. Haría grep de `actor` en `src/sldb/api`, inventariaría funciones no privadas que escriben documentos o índice, seguiría cada camino hasta `save_document_payload`/`create_document`, añadiría `actor` a `write_anchor` y lo propagaría. Añadiría tests, actualizaría `CHANGELOG` y `result-summary.md`. Dependencias: formación del sello, `current_actor`, APIs de documentos e índice. Validaciones futuras: los cinco comandos listados, empezando por `pytest -q tests/api/test_provenance.py` y terminando en `bash tools/check.sh --fast`. No se ejecuta nada aquí.

## FUTURO

Otro nodo ejecutará la implementación y producirá inventario, excepciones, tests, changelog y commit. Un humano o el coordinador resolverá las ambigüedades y validará el alcance; `deskops`/closeout actualizará Board y verificará gates.
