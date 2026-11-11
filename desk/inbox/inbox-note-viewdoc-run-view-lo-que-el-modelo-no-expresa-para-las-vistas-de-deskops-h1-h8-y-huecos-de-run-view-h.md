---
sldb:
  by: agent
  at: '2026-11-11T10:47:49Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T13:00:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# ViewDoc/run_view: lo que el modelo no expresa para las vistas de deskops (H1-H8) y huecos de run_view (H11 rendimiento, H12 caché borrada, H13 revision)

_Describe the incoming message with enough evidence to triage._

Hallado por CC34 de deskops (wt/cc34 ff4718b2, runs/subagents/cc34-worker-report.md, 2026-11-11). deskops view board|task salen de sldb.api.run_view proyectado al contrato de docs/deskops-ui.md. Lo que la ViewDoc no expresa hoy lo completa el CLI de deskops con operaciones de lectura existentes, marcadas 'pendiente de sldb Hn'. H9 (ViewDoc enlazada) y H10 (deskops) van aparte.

## Hipótesis para sldb (texto exacto enviado al coordinador)

- (H1) transitions.from_field necesita export id; current_node guarda 'ritual-execution' y edges_from no lo resuelve -> holding/blocked vacíos;
- (H2) transitions admite una sola relation y el ciclo tiene 3 (task_activates, task_hands_to_closeout, task_completes);
- (H3) gates con holds=false no aparecen (solo holding/blocked);
- (H4) closeout {declared,found,summary,implicit_code,alerts,evidence} no tiene fuente sin recibos evidence (hoy verify corre en lectura en cada render);
- (H5) next sale del spec yaml del paquete, no de documentos;
- (H6) effective_pills/atoms/validation por herencia no están en el índice;
- (H7) drawer markdown/excerpt (texto crudo) no está en las filas;
- (H8) revision por nota del inbox no existe por fila.

Además:

- (H9) run_view sobre un store que ENLAZA a otro con la ViewDoc da 'Unknown view'. El índice compuesto nombra el nodo enlazado '<link>:ViewDoc:<name>' y load_view busca 'ViewDoc:<name>'; además read_view resuelve semantics.path contra el project_root local, no contra el del store enlazado. Como sldb serve usa run_view, tampoco lo encuentra. Reproducción: `~/proyectos/SLDB_1/coord2-ccconfig/cc34/h9-repro/h9_repro.py` y `output.txt`; en deskops lo muestra `tests/test_view.py::test_a_store_without_the_viewdocs_is_an_error_envelope` y la medición c5 de abajo.
- (H10, de deskops) run_view solo ve documentos trackeados: desk/drawer/tasks no lo trackea ningún desk ni desk_declaration.yaml, desk/inbox no está en desk_declaration.yaml, y message send / promote escriben sin trackear.
- (H11, rendimiento) `run_view` compone en cada proceso el índice de aristas con todos los stores enlazados (`load_edge_index(include_linked=True)`: ~10 000 shards YAML de 6 stores en el desk de deskops), aunque las secciones de board solo seleccionan documentos locales; el índice compuesto no persiste entre procesos. Es el ~95 % del tiempo de `deskops view board` (perfil: run_view 38,4 s, proyección 0,6 s).
- (H13) en el proceso que escribió el store, `run_view` da otra `revision` para las mismas filas que un proceso nuevo o `sldb serve` (cachés de sldb en memoria); con datos iguales. El CLI y `sldb serve` son procesos propios, así que no afecta la guarda; el test c6 de graph_ui compara contra `sldb views run` en su propio proceso.
- (H12, menor) borrado `.sldb_cache`, `run_view` responde `Unknown view: board` (el índice sale vacío porque "reading never rebuilds") en vez de decir que el store no está construido; hace falta `sldb stores build`.

Esperado: que la ViewDoc exprese H1-H8 (o una decisión de que quedan como agregados del consumidor), que run_view no componga el índice entero en cada proceso (H11; meta caliente < 1 s, CC52 de deskops), que un store sin construir lo diga (H12) y que la revision no dependa de cachés del proceso (H13).
