# Result summary — retiro de `incomplete`
run_id: exec-deskops-e-5cfcba8143e9 · session: (claude agent, sin path de sesión hijo) · session_sha256: n/a

## Decisión: RETIRAR (con evidencia)
- Productores de `incomplete` en src: `predicate_reach._element` (solo si `edge["unavailable"]`), de ahí `predicate_eval.evaluate`/`predicate_paths._from`/`predicate_explain` (None) y consumidores `fixpoint`, `rules_check`, `rules_explain`, `rule_subjects`.
- La arista `unavailable` solo la escribía `predicate_view.graph_view` (dict de tests de spec) o la leía `index_view._edge` de `metadata["unavailable"]`; `grep unavailable src/sldb/store/edge_index` = vacío: ningún código escribe esa metadata. El único test "real" (`tests/api/test_rules.py`) la inyectaba con monkeypatch.
- Caso real intentado (store enlazado con `far`, `near` lo referencia, `shutil.rmtree` del enlazado, índice recompuesto): `compose_edge_index` descarta la arista; no queda ninguna `unavailable`; `where` y `rules check` dan false/error. Ningún camino público da incomplete.

## Cambios (todo en el worktree, SIN commit, ver bloqueo)
Código: predicate_reach, predicate_paths, predicate_eval, predicate_explain, predicate_view, backend/index_view, api/rules/{fixpoint,rule_subjects,rules_check,rules_explain}, api/where, cli/commands/rules, cli/parsers/rules, models/rule_doc (docs/strings).
Comportamiento: rules check sin `rules/<n>/incomplete`; rules explain exit 0/1/3 (ya no 2).
Tests: tests/api/test_rules_evaluation.py (+test de alcance/retiro), tests/api/test_rules.py (quita test incomplete y helper `_unavailable`), tests/test_rules_language_spec.py (2 tests ahora esperan true/false). tests/test_predicates_cli.py no nombra incomplete: sin cambios.
Docs: docs/architecture/rules-language.md (§3 reescrita, tablas Kleene fuera, H4, §4, §9), docs/architecture/rules.md, CHANGELOG.md.
Revisar: el cambio de exit 2 de `rules explain` y la eliminación del código `rules/<n>/incomplete`.

## Bloqueo
`bash tools/check.sh --fast` rc 1 por `identidad: workbench_demo` sin clasificar en la raíz (versionado desde 562847e2, ajeno a esta tarea). No toqué contratos; por eso no commiteé ni ejecuté `deskops advance`. Tests de Validation pasan.

## Excepción autorizada (coordinador)
`check.sh --fast` rc 1 solo por la puerta `identidad` (workbench_demo sin clasificar, preexistente, decisión aparte f055723d); las demás puertas y los tests pasan. Commit hecho en el worktree con `git commit -- <rutas>` y trailer Task-Id.
