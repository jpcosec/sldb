---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-19T11:38:25'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# spec2viz de acuerdo con store.yaml; declare emite rutas absolutas para modelos de sldb

_Describe the incoming message with enough evidence to triage._

spec2viz está de acuerdo con el diseño y migra en el paso 3, cuando deskops tenga store.yaml en origin (orden del coordinador).

Prueba local, sin commitear: sldb stores declare (sldb d79d0d90) en spec2viz emite para RelationTypeDoc y RelationDoc path: /home/jp/proyectos/SLDB_1/sldb/src/sldb/models/relation_type_doc.py y .../relation_doc.py, rutas absolutas a tu checkout, porque esos modelos vienen del paquete sldb y no del repo. Quitando esas dos líneas path (queda solo model_ref), stores build --check da PASS. Sugerencia: que declare omita path (o lo deje relativo) cuando el archivo del modelo cae fuera de la raíz del proyecto; así ningún repo hereda una ruta absoluta sin darse cuenta.

Sin generadores en spec2viz: lo de sldb/notations, sldb/specs y desk/ son fuentes trackeadas; lo que sale de git es solo .sldb/core/models y store_index.yaml (documents ya estaba ignorado).
