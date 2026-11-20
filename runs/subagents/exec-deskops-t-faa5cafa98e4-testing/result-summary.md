FALLA

# Testing — on_write: `save_document_payload` devuelve las alertas y la regla ve las aristas del payload nuevo

## Veredicto

**FALLA** por la puerta rápida: `bash tools/check.sh --fast` termina con **rc 1** porque falla `identidad`
(`directorio versionado sin clasificar en la raíz: workbench_demo`). Es una roja **preexistente y ajena a
este cambio** (ya está en el commit padre `5900a3eb`, comprobado en un worktree limpio), y el ejecutor
registra que el coordinador autorizó commitear con ella; aun así, la regla del rol de testing es explícita:
rc distinto de 0 en `check.sh --fast` ⇒ FALLA.

**El comportamiento pedido sí está implementado y todos los tests aplicables pasan.** Si el coordinador
acepta formalmente la roja preexistente como excepción, el veredicto funcional es **PASA**, con una salvedad
de contrato anotada abajo (`with_payload` vs. `with_edges`).

## Trabajo localizado

- Commit del ejecutor: `0f91540dfbaee9a0eae95b2c0a20b71db0ad1d78`
  ("on_write: save_document_payload devuelve las alertas y la regla ve las aristas del payload nuevo",
  con `Task-Id: task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el`).
- HEAD actual: `eb42a49e`; los archivos de la tarea no tienen cambios posteriores a `0f91540d`.
- El commit mezcla cambios de otras tareas que estaban en el índice compartido (matching, notations,
  store_check/diagnostics y sus tests), como el propio ejecutor reconoce en su informe. Eso no rompe los
  tests ejecutados, pero ensucia el commit.

Archivos efectivos de esta tarea:

- `src/sldb/api/documents/document_reference.py` (`alerts: list[dict[str, Any]] = Field(default_factory=list)`)
- `src/sldb/api/documents/payload_save.py` y `payload_save_steps.py` (devuelven y propagan las alertas)
- `src/sldb/api/rules/rules_on_write.py` (`check_on_write` devuelve `Finding.as_dict()` de nivel alert; `payload_edges`)
- `src/sldb/api/rules/rule_graph.py` (`with_edges` y vista declarada)
- `tests/api/test_rules.py`, `tests/api/test_on_write_entering.py`
- `CHANGELOG.md` (ver salvedad abajo)

## Qué se verificó

- `check_on_write` devuelve solo las alertas (`split(...)` → segundo elemento) como `Finding.as_dict()`;
  `route(alerts)` sigue ejecutándose antes de devolverlas. Probe con listener instalado: la alerta aparece
  tanto en `DocumentReference.alerts` como en el listener (`rules/closed`, `X:x1`).
- `save_document_payload` rellena `DocumentReference.alerts`; sin reglas devuelve `[]`. El test nuevo de
  `tests/api/test_rules.py` lo comprueba con `_LISTENERS` vaciado por monkeypatch.
- El test de `tests/api/test_on_write_entering.py` usa
  `count(depends_on: title != "") > 0`: guardar con `depends_on: X:x2` pasa, quitarla da `rules/linked`, y
  el documento conserva la referencia previa porque el error no escribe. Cubre alta y retirada de aristas.
- Las aristas nuevas se construyen con `declared_reference_edges` + `doc_anchor_edges` sobre el payload
  nuevo (`payload_edges`) y reemplazan las salientes `references`/`contains` del documento; las demás
  aristas del índice quedan.

## Salvedad de contrato

El Scope/Precisiones pide que **`RuleGraph.with_payload`** devuelva el grafo con las aristas salientes del
payload nuevo reemplazadas. La implementación lo separa: `with_payload` solo cambia el payload, y el
reemplazo ocurre en `with_edges`, que `check_on_write` llama antes. Probe directo:

    rule_graph(store).with_payload("X:x1", payload_con_depends_on)
      -> count(depends_on: title != "") > 0  == false
    rule_graph(store).with_edges("X:x1", payload_edges(...)).with_payload(...)
      -> count(depends_on: title != "") > 0  == true

El comportamiento observable de `save_document_payload`/`on_write` es correcto y los tests exigidos pasan,
pero `with_payload` por sí solo no cumple la letra de la Precisión. Si la aceptación incluye un test directo
sobre `with_payload`, fallaría.

También: la línea de CHANGELOG de esta tarea **no está en el commit del ejecutor**; aparece en HEAD añadida
por `07450d10` (commit con el `Task-Id` de la tarea de `stores check`). El árbol final sí tiene la entrada
bajo `## 0.1.13 — not released yet`, en español, pero no quedó en el commit que cita esta tarea.

## Tests ejecutados (de a uno)

No existía `/tmp/ws-venv` en este contenedor; se usó el Python del venv del repo,
`/workspace/sldb/.venv/bin/python` (3.13.18), con `TMPDIR=/tmp` salvo donde se indica.

| Archivo | Resultado |
|---|---|
| `tests/api/test_rules.py` (archivo del commit) | **14 passed** |
| `tests/api/test_on_write_entering.py` (archivo del commit) | **8 passed** |
| `tests/api/test_rules_evaluation.py` (validación explícita) | **12 passed** |
| `tests/api/test_rules.py` + `test_on_write_entering.py` con `TMPDIR=/dev/shm` | **22 passed** |
| `tests/matching/test_matching_refs.py` (archivo del commit) | **11 passed** |
| `tests/notations/test_notations_from_graph_cli.py` (archivo del commit) | **9 passed** |
| `tests/store/test_diagnostics.py` (archivo del commit) | **17 passed** |
| `tests/notations/test_component_spec_graph.py` (módulo tocado) | **16 passed** |
| `tests/test_serve_stores_check.py` (módulo tocado) | **2 passed** |
| `tests/api/test_rewrite_references.py` (regresión de `check_rules_on_write`) | **21 passed** |

No se corrió la suite completa: la integra el host, según la instrucción del rol.

## Gate rápido

    PATH=/workspace/sldb/.venv/bin:$PATH bash tools/check.sh --fast  -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

La violación de identidad no proviene de este commit: `workbench_demo` está versionado desde `562847e2`,
ya es ancestro del commit del ejecutor, y este no toca `contracts/identity.toml` ni `workbench_demo`.
Comprobado también sobre el commit padre `5900a3eb` en un worktree aparte: falla igual.

## Observaciones de proceso

- El ejecutor no envió el aviso `deskops message send --to deskops` que pide el contrato; queda pendiente.
- El commit `0f91540d` arrastra archivos de otras tareas; conviene separarlo o dejarlo documentado en closeout.
