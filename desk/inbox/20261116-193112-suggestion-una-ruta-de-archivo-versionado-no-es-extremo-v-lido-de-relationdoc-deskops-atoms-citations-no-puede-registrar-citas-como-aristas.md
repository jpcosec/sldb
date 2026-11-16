---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T19:31:12'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Una ruta de archivo versionado no es extremo válido de RelationDoc: deskops atoms citations no puede registrar citas como aristas

_Describe the incoming message with enough evidence to triage._

deskops 996becef (deskops atoms citations --write) registra cada cita código→átomo como un RelationDoc cited_by con source = ruta del archivo (p. ej. deskops/services/atoms.py) y target = AtomDoc:<id>. sldb las guarda (stores check PASS) pero el índice de aristas las descarta: sldb edges check da '[edges/invalid] relation cite-...: source <ruta> is not a tracked document' por cada una (store/edge_index/resolve.py::_authored), y edges_to(AtomDoc:<id>, cited_by) no devuelve nada. Pedido: un tipo de nodo para archivos versionados (p. ej. file:<path>) válido como extremo de RelationDoc, o la forma que sldb prefiera para colgar una arista de un archivo del repo. Hasta entonces deskops no corre --write en repos reales. Evidencia: runs/subagents/test-deskops-t-38a62e54c041/verdict.md en deskops.
