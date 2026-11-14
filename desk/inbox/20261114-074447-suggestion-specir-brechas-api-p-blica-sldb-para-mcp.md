---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-14T07:44:47'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# [specIR] Brechas API pública SLDB para MCP

_Describe the incoming message with enough evidence to triage._

## Capacidad 4: seleccionar por predicados con sldb.api.select_documents y buscar texto rankeado con sldb.api.search
Necesidad: select_documents: Actor: agente MCP de specIR operando un store SLDB; Entrada: selector con predicados; Resultado esperado: filas {export_id, model, name, path}. search: Actor: agente MCP de specIR operando un store SLDB; Entrada: término obligatorio y where opcional; Resultado esperado: resultados textuales ordenados por relevancia.
Rutas/símbolos revisados: src/sldb/api/documents/select_documents.py::select_documents; src/sldb/api/search.py::search; src/sldb/api/records/matches.py::search_records; docs/architecture/selectors.md.
Brecha: select_documents está disponible. search requiere term y busca coincidencias literales, regex o fuzzy, pero no calcula puntaje ni ordena por relevancia; where se aplica después de la coincidencia textual.
Pregunta al desk: ¿Puede SLDB exponer o documentar un puntaje de relevancia y el orden de resultados por ese puntaje en search mediante la API pública para soportar seleccionar por predicados con sldb.api.select_documents y buscar texto rankeado con sldb.api.search?
TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp

## Capacidad 9: consultar journal e historial de documento/procedencia
Necesidad: Actor: agente MCP de specIR operando un store SLDB; Entrada: consulta de eventos recientes o identidad de documento; Resultado esperado: escrituras/cambios con fecha y procedencia.
Rutas/símbolos revisados: src/sldb/api/journal.py::journal; src/sldb/api/documents/document_history.py::document_history; docs/architecture/journal-authority.md; docs/architecture/provenance.md.
Brecha: el historial por documento está disponible desde Git, pero journal retorna siempre una lista vacía y no informa eventos recientes de escritura del store.
Pregunta al desk: ¿Puede SLDB exponer o documentar la consulta de escrituras recientes del store con fecha y procedencia mediante la API pública para soportar consultar journal e historial de documento/procedencia?
TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp

## Capacidad 10: leer StoreFingerprint.store_hash y usar la huella global como precondición atómica de escritura, rechazando mismatch
Necesidad: Actor: agente MCP de specIR operando un store SLDB; Entrada: huella global observada y solicitud de escritura; Resultado esperado: escritura solo si la huella aún coincide, con rechazo atómico de mismatch.
Rutas/símbolos revisados: src/sldb/api/stores/store_fingerprint.py::store_fingerprint; src/sldb/api/documents/transaction.py::Transaction.update; src/sldb/api/documents/payload_save.py::save_document_payload; src/sldb/api/documents/create_document.py::create_document.
Brecha: la API lee StoreFingerprint.store_hash, pero ninguna operación de escritura acepta ese hash global y lo compara atómicamente; las guardas documentadas son por documento o payload.
Pregunta al desk: ¿Puede SLDB exponer o documentar una escritura que acepte StoreFingerprint.store_hash como precondición y rechace atómicamente el mismatch mediante la API pública para soportar leer StoreFingerprint.store_hash y usar la huella global como precondición atómica de escritura, rechazando mismatch?
TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp

## Capacidad 11: detectar operación pública SLDB que cumpla la capacidad de deshacer escritura confirmada de kb_undo/forma undo
Necesidad: Actor: agente MCP de specIR operando un store SLDB; Entrada: solicitud de deshacer una escritura de nivel 1 o 2 evaluada con éxito (outcome: done); Resultado esperado: reversión equivalente a (undo) de pron §4.
Rutas/símbolos revisados: src/sldb/api/documents/transaction.py::transaction; ../pron/source/spec/14-superficie-mcp.md §4.
Brecha: transaction revierte archivos solo si el bloque lanza una excepción; no hay operación pública que revierta una escritura ya confirmada de nivel 1 o 2.
Pregunta al desk: ¿Puede SLDB exponer o documentar la reversión de una escritura confirmada de nivel 1 o 2 mediante la API pública para soportar detectar operación pública SLDB que cumpla la capacidad de deshacer escritura confirmada de kb_undo/forma undo?
TaskDoc: task-ir01-auditoría-de-la-api-pública-de-sldb-frente-a-la-superficie-mcp
