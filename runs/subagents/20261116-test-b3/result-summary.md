# Tester deskops-t-b4736317f0b4 — task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3

**Veredicto: PASA.** La salida completa está en `validation.log`, en esta misma carpeta.

## Validation (corrida por mí)

| Comando | Resultado |
|---|---|
| `pytest -q tests/api/test_api_graph_analysis.py` | PASA: 10 passed, rc 0 |
| `pytest -q tests/store/test_graph_analysis.py` | PASA: 16 passed, rc 0 |
| `pytest -q tests/store/test_graph_backend.py` | PASA: 9 passed, rc 0 |
| `pytest -q tests/test_serve.py` | PASA: 61 passed, rc 0 |
| `pytest -q tests/test_clean_code_rules.py` (obligatorio por el brief) | PASA: 1173 passed, rc 0 |
| `bash tools/check.sh --fast` (obligatorio por el brief) | PASA: "TODAS LAS PUERTAS PASAN", rc 0 |

- Todo se corrió con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, y `uv` no falló.
- No corrí la suite completa ni `sldb stores build --check`: quedan delegados al integrador.

**check_claims sobre CHANGELOG.md** (aclaración del coordinador):

| Árbol | Afirmaciones comprobadas | Falsas |
|---|---|---|
| Árbol de trabajo | 282 | 3 |
| HEAD (`git archive HEAD` en `/dev/shm/tb3-head`) | 274 | 3 |

- Las 3 falsas son las mismas en los dos árboles: `docs/missing`, `docs/ambiguous` y `sldb query`. **Confirmado: vienen de antes**, no de esta entrada.
- La entrada nueva suma 8 afirmaciones y ninguna es falsa.

## Done When, punto por punto

- **Los comandos de Validation pasan**: PASA (ver la tabla).
- **`graph_path(..., explain=True)` sobre el índice del propio repo**: PASA, comprobado con mi propio script (`/dev/shm/tb3/edge_cases.py`).
  - Llamada: `<repo>/.sldb` con `include_linked=False`, de `RitualDoc:ritual-execution` a `RitualDoc:ritual-closeout`.
  - Camino devuelto: execution → testing → closeout.
  - Tramos:
    - `task_activates`, forward, `{origin: relation_doc, relation_doc: execution-task_activates}`;
    - `task_hands_to_closeout`, forward, `{origin: relation_doc, relation_doc: testing-task_hands_to_closeout}`.
  - El `path` con explain coincide con el que devuelve la llamada sin explain.
- **Goldens intactos**: PASA. `git status` y `git diff HEAD` sobre `tests/fixtures/graph_goldens/` salen vacíos, y `test_graph_backend` pasa.
- **`sldb graph path --explain`**: PASA. Lo corrí sobre el repo (`--local`), con y sin `--all --limit 2`: rc 0 y la salida trae `steps`.
- **GET `?explain=1`**: PASA. Llamé a `path_payload` con un handler simulado sobre el repo (no levanté ningún servidor):
  - `explain=1` y `explain=true` → 200 con `{path, steps}`;
  - `explain=0` y sin el parámetro → 200 con solo `{path}`;
  - explain sin camino → 404.
- **CHANGELOG**: PASA. La entrada está en 0.1.13 y check_claims no le encuentra afirmaciones falsas.
- **Commit**: no hay commit todavía. El brief del ejecutor y el del tester lo prohíben, así que queda para el closeout o el integrador; no lo cuento como falla de esta etapa.
- **Aviso a IR**: el ejecutor dejó el texto sugerido en su result-summary y lo envía el coordinador al cerrar. Texto: «sldb.api.graph.graph_path/graph_paths aceptan explain=True: {path, steps[{source,target,edges[{relation,direction,provenance{origin,relation_doc|field,from_store}}]}]}; CLI `sldb graph path --explain`, serve `/graph/path?explain=1`».

## Casos que el ejecutor no cubrió (`/dev/shm/tb3/edge_cases.py`, todos OK)

Sobre un índice sintético con ids `sldb://`:

- `source == target` devuelve `{"path": [a], "steps": []}`.
- Sin camino: `None`, y `explained_paths` devuelve `[]`.
- El filtro `relations=["r1"]` saca del tramo la arista `r2` paralela.
- Un tramo que solo se recorre al revés sale `backward`.
- `evidence` no entra en `provenance`.
- Empate de precedencia: `r1` va antes que `r2`.
- `directed=True` sin camino devuelve `None`.
- Ningún tramo de un camino encontrado queda con `edges` vacío: lo comprobé para todos los pares y filtros.
- `field` y `from_store` vacíos (`""`) no se emiten.

## Notas (no son fallas)

- **Arista sin `origin`**: sale con `provenance: {}`. El contrato no lo precisa, y las aristas reales siempre traen `origin`.
- **Ids sin el prefijo `sldb://`**: `explain_path` lee las aristas con `index.edges_from`, que pasa el id por `as_node_id` y le antepone `sldb://document/`. Por eso, en un índice armado con ids que no empiezan con `sldb://`, los tramos saldrían sin aristas mientras `path_between`, que trabaja con los ids tal cual, sí encuentra el camino.
  - Me pasó en un primer intento del script, que usaba ids desnudos; queda en el log como un artefacto mío.
  - En un índice real todos los ids empiezan con `sldb://`, así que no afecta a esta tarea.

## Alcance de archivos

| Archivo | Situación |
|---|---|
| `src/sldb/api/graph/analyze.py` | modificado, en el contrato |
| `src/sldb/store/graph/backend/networkx_backend.py` | modificado, en el contrato |
| `src/sldb/cli/parsers/graph_analysis.py` | modificado, en el contrato |
| `src/sldb/cli/commands/graph_analysis.py` | modificado, en el contrato |
| `src/sldb/cli/serve/graph_routes.py` | modificado, en el contrato |
| `tests/api/test_api_graph_analysis.py` | modificado, en el contrato |
| `CHANGELOG.md` | modificado, en el contrato |
| `src/sldb/store/graph/analysis/path_steps.py` | nuevo; lo autorizan el Implementation Path y el coordinador |
| `src/sldb/cli/commands/graph_path_print.py` | nuevo; lo autorizan el Scope y el coordinador |

- **Sin cambios ajenos a la tarea en `src/` ni en `tests/`.**
- Los cambios en `.sldb/` y `desk/` (los ReviewDoc y la TaskCodeDoc de la tarea b2, `store.yaml`), `uv.lock` y los RunDoc son ajenos o del coordinador.
- **Incidente `.sldb/core/core`** que contó el ejecutor:
  - `.sldb/core/core` ya no existe.
  - El diff de `.sldb/core/store_index.yaml` contra HEAD es solo la línea `store_hash`.
  - Su valor actual, `5a610f20…`, difiere del `b780a36c…` que anotó el ejecutor. Lo atribuyo a la actividad ajena posterior sobre los modelos (ReviewDoc y otros), no a esta tarea.
  - Mis corridas no tocaron `.sldb`: comparé `git status --short .sldb` antes y después y es idéntico.
- Clean code: `path_steps.py` tiene 66 líneas brutas y `graph_path_print.py` 29; `test_clean_code_rules` pasa para todos los archivos tocados.

## Regresiones vecinas

Corrí cada archivo de `tests/` que importa los módulos cambiados, uno por uno, con rc 0 en todos:

| Archivo | Resultado |
|---|---|
| `tests/api/test_api_edges.py` | 16 passed |
| `tests/api/test_api_graph.py` | 2 passed |
| `tests/api/test_graph_source_parity.py` | 13 passed |
| `tests/store/test_payload_projection.py` | 40 passed |
| `tests/store/test_predicate_language.py` | 16 passed |

`test_api_graph_analysis`, `test_graph_backend` y `test_serve` ya están en Validation. Como no hubo ninguna falla, no hizo falta compararlos contra HEAD.
