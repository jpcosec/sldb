# Tester deskops-t-5182291d0393: veredicto PASA

Tarea: `task-referrers-y-rewrite-references-aceptan-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-duplican-men`.
Base: HEAD `7cd8a5e3` más el diff sin commitear del ejecutor `deskops-e-ca9ebf095f85`, incluida su Corrección 1.
Las salidas completas están en `validation.log`, en esta misma carpeta.
`uv run --frozen --extra code --extra dev` funcionó, así que no usé el fallback de `uvx`.

## Validation (la corrí yo)

| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py` | **PASA**: 12 passed, rc 0 |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py` | **PASA**: 21 passed, rc 0 |

## Done When, punto por punto

1. **"Los dos archivos pasan con los tres casos nuevos": PASA.**
   - H-a: `test_a_graph_built_in_process_gives_the_mentions_the_store_does_not_declare`. Usa el desk mínimo del pill, sin `project_graph` en `store.yaml`. Sin `graph` devuelve `[]`; con `ProjectGraph(root, DESK_CONFIG)` devuelve la mención `desk/tasks/task-ref.md:3`.
   - H-c: `test_a_declared_field_is_one_schema_referrer_not_also_a_frontmatter_mention`. Primero comprueba que el grafo sí tiene la arista de mención desde `task-b.md`, así que la duplicación existiría sin el filtro. Después comprueba que `depends_on` sale una sola vez, como `schema`.
   - H-b: `test_an_excluded_source_is_left_byte_for_byte_and_the_rest_is_rewritten`, parametrizado con `Task:task-b` y con `desk/tasks/task-b.md`. Compara `read_bytes()` antes y después del archivo excluido. Hay además un caso negativo: `..._names_no_tracked_document_is_refused`.
   - Los tres están dentro de los dos archivos de Validation que pasan.
2. **"Sin graph ni excluded_sources el comportamiento es el de hoy": PASA.**
   - En el código, `graph if graph is not None else optional_graph(...)` deja el camino de antes intacto.
   - El filtro de `excluded_sources` solo actúa si `excluded` no está vacío.
   - Todos los tests existentes de los dos archivos siguen verdes.
   - Mi caso `test_graph_none_is_same_as_omitting` comprueba que `graph=None` da lo mismo que no pasarlo.
   - Ojo con H-c: el filtro sí cambia el resultado sin `graph`, si el store declara un grafo con menciones en el frontmatter. Ese cambio es el que pide el contrato. `EXPECTED` y los tests de la CLI de `test_referrers.py` no cambiaron y siguen verdes.
3. **CHANGELOG: PASA.** Hay una línea en español bajo `## 0.1.13 — not released yet`, primera de la lista, con el estilo de las entradas vecinas.
   **Commit y aviso a deskops: PENDIENTES.** No son del ejecutor: los hace el coordinador con `deskops closeout commit` y `deskops message send --to deskops`. No los evalúo. El ejecutor dejó propuesto el texto del aviso.

## Corrección 1 (`a2_changes`), lo que pidió el coordinador: PASA

- **El valor sale del payload, no de un hash copiado.** `pinned = world.payload("Review:r1")["subject"]` se lee del documento ya creado. En el archivo no hay ningún hash literal (lo revisé con grep en el diff).
  - El helper además exige la forma `doc:Card:card-a@sha256:` seguida de 64 caracteres. Si `create_document` dejara de pinnear, el test fallaría por esa aserción y no pasaría en silencio.
  - El valor se lee del documento, no del informe de `rewrite_references`. Por eso la comprobación no es circular: el `before` que reporta la API se compara contra lo que hay en disco.
- **Los 5 tests comprueban lo mismo que antes, salvo el pin.** El diff de esos 5 tests solo sustituye `A2_CHANGES` por `expected = a2_changes(reference_world)`. El resto de cada aserción queda igual: `skipped`, payloads, digests, `calls` y conteos.
  - `a2_changes` toca solo el `before` de la entrada `Review:r1`. Las otras 4 entradas y todos los `after` salen idénticos; el `after` de Review sigue siendo `doc:Card:card-a2`.
  - `A2_CHANGES` no cambió.
  - En `test_with_the_index_and_the_graph_warm_...`, `expected` se calcula antes de `count_walks`. Así la lectura del payload no se cuenta como recorrido y la aserción `{"walk": 0, ...}` mantiene el mismo rigor.
  - En `test_removing_...`, `expected[:3]` con `after: None` equivale a lo de antes.
- Los 21 tests pasan.

## Casos que el ejecutor no cubrió (script en `/dev/shm/tester-referrers/edge.py`, sin versionar): 8/8 PASAN

| Caso | Qué comprueba | Resultado |
|---|---|---|
| `test_frontmatter_mention_in_doc_without_schema_hit_is_kept` | H-c no filtra de más: una mención en el frontmatter (campo `note`, que no es referencia) de un documento **sin** hit schema se conserva (línea 8) | PASA |
| `test_body_mention_in_doc_with_schema_hit_is_kept` | H-c solo actúa sobre el frontmatter: en un documento con hit schema, la mención en el cuerpo se conserva | PASA |
| `test_frontmatter_mention_on_other_line_of_doc_with_schema_hit` | En un documento con hit schema, una mención en **otra** línea del frontmatter (`note`) también se descarta | PASA, según la letra del Scope (ver Observación 1) |
| `test_exclude_by_bare_name_and_slash_form_and_generator[task-b / Task/task-b]` | La exclusión funciona con un nombre a secas y con `Model/name`, pasados como generador (`Iterable`) | PASA |
| `test_exclude_without_graph_works_on_fields_and_dry_run_writes_nothing` | `excluded_sources` sin `graph` y con `dry_run`: excluye el campo y no escribe ningún byte (fuera de `.sldb_cache`) | PASA |
| `test_untracked_file_as_excluded_source_is_refused_and_nothing_written` | Una ruta existente pero sin trackear (`task-ref.md`) como fuente excluida lanza `SLDBDocumentTargetError` y no escribe nada | PASA |
| `test_graph_none_is_same_as_omitting` | `graph=None` da lo mismo que omitirlo | PASA |

## Alcance de archivos: PASA

- El ejecutor tocó solo los 5 archivos del contrato: `src/sldb/api/edges/referrers.py`, `src/sldb/api/edges/rewrite_references.py`, `tests/api/test_referrers.py`, `tests/api/test_rewrite_references.py` y `CHANGELOG.md`. Además dejó su entrega en `runs/subagents/20261116-exec-referrers/`.
- Los cambios en `.sldb/` son el registro de los RunDoc de este despacho, que hace el coordinador:
  - `store.yaml` y `store_index.yaml`: se añaden `run-deskops-e-ca9ebf095f85` y `run-deskops-t-5182291d0393`.
  - `RunDoc.yaml`: `documents_count` pasa de 26 a 28.
  - No son del ejecutor.
- El resto de cambios son ajenos y figuran en la lista del brief: `apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/` y `.herdr-coordination.md`. No los revisé.
- `uv.lock` ya figuraba como modificado al empezar; mis comandos usaron `--frozen`.
- No toqué ni stageé nada del repo. Solo escribí los dos archivos de entrega en esta carpeta.

## Observaciones (no bloquean)

1. **Pill frente a Scope en H-c.**
   - El pill dice que se descarta "solo la mención que repite, en el mismo documento y la misma línea del frontmatter, un hit schema".
   - El Scope y las Precisiones del contrato dicen que se descartan las mentions "cuya línea cae dentro del frontmatter de ese documento", sea cual sea la línea.
   - La implementación sigue el contrato: también descarta una mención en otra línea del frontmatter, como `note`, en un documento que ya tiene hit schema. Ese caso queda sin reportar por ninguna de las dos vías.
   - El pill subordina sus indicaciones a las Precisiones, así que no lo cuento como falla. Lo dejo anotado por si deskops espera la lectura estricta de "misma línea".
2. **Excluir con un archivo de menciones sin trackear.** Una fuente excluida que es un archivo con menciones pero sin trackear (como `task-ref.md`) no se puede excluir: lanza `SLDBDocumentTargetError`. Es lo que fijan las Precisiones ("a un documento trackeado"), pero deskops no podrá excluir así un archivo de tareas sin trackear.
3. **Fuentes excluidas en el informe.** Las fuentes excluidas no aparecen en `skipped` del `RewriteReport`. El contrato no lo pide y el formato no cambia.
