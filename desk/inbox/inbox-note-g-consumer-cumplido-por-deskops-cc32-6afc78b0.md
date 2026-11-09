---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-09T16:13:02'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# G_CONSUMER cumplido por deskops (CC32, 6afc78b0)

_Describe the incoming message with enough evidence to triage._

G_CONSUMER cumplido por deskops (plan deskops-como-config, nodo CC32): squash 6afc78b0, closeout 2ce88abd, en main de deskops el 2026-11-09.

deskops ya consume el grafo operable de sldb tal como lo entregan GO06, GO07, GO08 y GO09:
- Siete RuleDoc on_transition, una por tipo de tarea de fábrica, con subject "model <= <TaskXDoc>" y where current_node = "ritual-execution". Viven en desk/lifecycle/rule-activation-*.md de cada desk, las siembra deskops desk update --apply y se registran con sldb.api.add_model("sldb.models.rule_doc:RuleDoc").
- Las condiciones usan any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>") sobre ReviewDoc.__doc_anchors__ = ["subject"], más all(depends_on: status = "closed").
- deskops advance llama a edges_holding(store, "RitualDoc:ritual-execution", payload, include_linked=False, document="<Model>:<task>"). Cuando la arista está bloqueada, llama a edges_blocked y muestra los Finding tal como vienen. show y next usan transition_findings.
- Test de integración en tres pasos (tests/test_activation_rules.py de deskops): sin recibos, advance falla y nombra la cláusula; con los recibos pinneados, activa; con goal editado, bloquea con anchor_state = changed.
- Depende del arreglo de sldb 5d4e0771: el rollback restaura .sldb_cache/rules/dirty.json.

Hipótesis para sldb (no bloquean):
1. El testigo de un any falso es el primer elemento alcanzado. Para que el finding muestre anchor_state = changed hubo que poner anchor_state como primera hoja de la conjunción. Sería más útil que el testigo fuera el elemento que llega más lejos, o que seen incluyera todas las hojas evaluadas.
2. (H-CC32-2) create_document no pinnea anclas: un recibo creado y nunca reescrito queda lost aunque su destino exista. deskops lo resuelve con create + update en la misma transacción, y review record pinnea en dispose. Convendría que create pinnee, o que exista una operación pin.
3. sldb anchors check sobre un índice anterior a GO07 devuelve doc_anchors: [], mientras que el lenguaje ya lee esos subject sin hash como lost. Conviene que avise o que calcule al vuelo.
4. sldb stores check tarda ~28 s en un store recién creado por deskops init, y deskops desk update lo corre en cada ejecución.
5. rule_graph cuesta ~3,2 s por llamada en un store de ~30 documentos. deskops lo cachea en su ReadSnapshot; un caché por store_fingerprint en sldb evitaría que cada consumidor lo reinvente.
6. children no existe como campo de TaskDoc, así que la regla de task.aggregate queda pendiente (es de deskops; no pide nada a sldb).
