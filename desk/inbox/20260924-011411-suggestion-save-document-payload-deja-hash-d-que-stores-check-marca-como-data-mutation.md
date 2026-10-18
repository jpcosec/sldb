---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-24T01:14:11'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T14:18:00'
---

# save_document_payload deja hash_d que stores check marca como data_mutation

_Describe the incoming message with enough evidence to triage._

Reporte de deskops. Dos hallazgos de sldb, con repro.

## 1. `save_document_payload` deja el documento en `data_mutation`

Escribiendo un documento rastreado con la API de sldb y comprobando el store:

    PYTHONPATH=<repo> python -c "
    from sldb.api.documents.payload_save import save_document_payload
    from sldb.runtime.validation import extract_model_data
    from deskops.models import TaskDoc
    from pathlib import Path
    root=Path('.').resolve()
    p=root/'desk/tasks/<task>.md'
    payload=extract_model_data(TaskDoc, p.read_text())
    save_document_payload(root/'.sldb','TaskDoc',p.stem,payload,pythonpath=str(root))"

`save_document_payload` reporta éxito, pero acto seguido

    python -m sldb stores check --store .sldb --pythonpath .

dice FAIL y marca ese documento como `data_mutation` con `hash_c_ok: true` y
`hash_d_ok: false`. O sea: el texto en disco coincide con el hash_c guardado,
pero el hash_d que escribió el save no es el que calcula el check para el mismo
archivo. Descarté que fuera nuestro: pasa con el modelo de deskops sin tocar el
archivo entre medio.

Camino que sí queda consistente, y por eso lo usamos: `untrack_document` y
después `track_document_file(..., force=True)`. Lo aplicamos en deskops para
que una edición no desincronice el store (deskops/operations.py,
`_write_through_store`).

Si `save_document_payload` es la vía preferida para actualizar un documento ya
rastreado, merece arreglarse: hoy escribir con ella deja el store marcado como
inválido y obliga a retrackear.

## 2. Documentos cuyo modelo no puede leer su propio contenido

`stores check` da PASS en documentos de los que la extracción devuelve vacío
para todos los campos del body, porque la extracción ancla en el texto fijo que
el template renderiza y esos documentos no lo tienen (escritos a mano, o
producidos por un template anterior). El archivo se ve bien; leerlo devuelve
vacíos, y reescribirlo los escribe vacíos. En deskops había 34 así (29 pills,
4 conditions, 1 step) y un `deskops edit` los borraba en silencio.

Lo detectamos y lo arreglamos en nuestra capa (deskops/doc_readability.py: el
write path se niega a reescribir perdiendo contenido y el doctor lo reporta),
pero la condición de fondo es de sldb: podría ser un finding propio de
`stores check`, algo como "el modelo no lee este documento" separado de los
hashes, porque un hash consistente sobre una extracción vacía no lo delata.

## Resolución

Resuelto (2026-10-18, sldb-04). (1) save_document_payload ya no deja data_mutation: arreglado en 0.1.4 (CHANGELOG). (2) 0651650972: `stores check` nombra cada documento que una reescritura dejaría sin contenido, con los bloques que su modelo no lee, y `check_store` lo devuelve en `rewrite_loss`; las secciones que el template regenera no cuentan. Además, 9dcabd9a y d31180e4 arreglan las dos causas de fondo que encontramos (un párrafo placeholder que se tragaba el primer párrafo real, y la última sección de un documento más corto que su template): en los stores de sldb y de deskops no queda ningún documento con pérdida.
