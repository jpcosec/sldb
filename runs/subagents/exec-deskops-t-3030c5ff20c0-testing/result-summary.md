PASA

# Tester deskops-t-3030c5ff20c0: `model_tag("T")` sobre el DAG semántico

Task: `task-una-regla-puede-preguntar-por-los-tags-semanticos-del-modelo-de-un-documento-y-por-los-de-sus-ancest`
Commit revisado: `66fbb00002272f85d54747672c165646f1e66201` — `feat: rules language predicate model_tag("T") over the semantic DAG`
Archivos del commit: `src/sldb/api/rules/rule_writes.py`, `src/sldb/store/graph/backend/{index_semantics,index_view}.py`, `src/sldb/store/graph/language/{predicate_ast,predicate_atoms,predicate_leaves,predicate_view,semantic_scope}.py`, `docs/architecture/{rules-language,rules}.md`, `tests/test_rules_semantic_tag_predicate.py`.

Nota: el commit no lleva `Task-Id` (como pedía el encargo), así que el `git log --grep "Task-Id: ..."` de «Como probar» no lo encuentra; se localizó por el asunto del commit y por `git log --oneline` (esconde el commit hijo `run: deskops-t-3030c5ff20c0`).

## Veredicto

**PASA.** El lenguaje de reglas tiene un predicado `model_tag("T")` cuyo valor es verdadero cuando el modelo del documento declara un tag que es `T`, que desciende de `T` en el DAG semántico (aristas `semantic_parent`, a cualquier profundidad) o equivalente a cualquiera de ellos (equivalencia simétrica). La dirección es la pedida: preguntar por el padre casa a los hijos, preguntar por el hijo no casa al padre. La validación al escribir una `RuleDoc` rechaza un tag que el DAG no conoce, nombrando el tag, tanto en `where` como en `condition`. `rules-language.md` describe el predicado con ejemplos y `rules.md` documenta la validación.

## Validación ejecutada

Con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-3030c5ff20c0`. `/tmp/ws-venv` no existía en el contenedor; usé el `.venv` del repo (`/workspace/sldb/.venv`, Python 3.13.18), que es el que resuelve `sldb` al checkout.

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q tests/test_rules_semantic_tag_predicate.py` | 0 | 5 passed |
| `python -m pytest -q tests/store/test_predicate_language.py` | 0 | 16 passed |
| `python -m pytest -q tests/test_predicates_cli.py` | 0 | 4 passed |
| `python -m pytest -q tests/api/test_rules.py` | 0 | 13 passed |
| `python -m pytest -q tests/api/test_rules_evaluation.py` | 0 | 13 passed |
| `python -m pytest -q tests/api/test_rules_end_to_end.py` | 0 | 1 passed |
| `python -m pytest -q tests/api/test_rules_linked_reach.py` | 0 | 4 passed |
| `python -m pytest -q tests/store/test_semantic_dag_walk.py` | 0 | 8 passed |
| `python -m pytest -q tests/store/test_graph_backend.py` | 0 | 9 passed |
| `python -m pytest -q tests/api/test_tags.py` | 0 | 37 passed |
| `python -m pytest -q tests/api/test_tags_scope.py` | 0 | 11 passed |
| `python -m pytest -q tests/test_rules_language_spec.py` | 0 | 52 passed |
| `python -m pytest -q tests -k rules` | 1 | 1339 passed, 2 failed, 2 errors — los 4 idénticos en el commit padre (ver observaciones) |
| `python -m pytest -q tests/test_clean_code_rules.py::…[index_semantics.py] …[semantic_scope.py]` | 0 | 2 passed |
| `bash tools/check.sh --fast` (con `.venv/bin` en PATH) | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_semantic_scope.py` ni `tests/test_index_semantics.py`; los tests de módulo tocado existentes son `tests/store/test_predicate_language.py` (lenguaje de predicados) y `tests/store/test_graph_backend.py`/`tests/store/test_semantic_dag_walk.py` (vista del índice y DAG), corridos arriba. No se corrió la suite completa.

## Cobertura del Done When

- **Casa al modelo con el tag propio:** `test_the_parent_tag_matches_its_own_model_its_child_and_an_equivalent_but_not_the_unrelated` (Parent), y la fila «el propio» de la tabla de `rules-language.md`.
- **Casa al hijo:** el mismo test (Child) y `test_a_child_tag_does_not_match_the_parent_model` en el sentido inverso. Verifiqué además, con probes fuera del repo, una jerarquía de tres niveles (`concept.base.child.grand`): pedir `concept.base` casa padre/hijo/nieto; pedir el nieto casa solo al nieto.
- **No casa sin relación:** el mismo test (Alien queda fuera; `Alien:alien` recibe `holds: false`).
- **Equivalencia:** el mismo test (Twin, `other.same` ↔ `concept.base`) y un probe que declara la equivalencia en el otro sentido (`concept.base.child` → `weird.thing`): se lee en ambos sentidos, y un equivalente a un descendiente también entra en el alcance del ancestro.
- **Tag desconocido al validar, con el nombre:** `test_an_unknown_tag_is_refused_when_the_rule_is_written_naming_the_tag` (`SLDBStoreError` con `concept.nope`). Verifiqué además que se rechaza en `where` y en `condition`, en `create_document` y en `save_document_payload`, y que no se escribe el archivo. El mensaje es `Unknown semantic tag 'T': …`.
- **Sintaxis:** `test_the_argument_must_be_a_quoted_tag` (`model_tag(x)` → `WherePredicateError`); probé también que un número (`model_tag(3)`) y una comilla simple no parsean, y que `model_tag ("x")` sí (espacio no significativo).
- **Evaluador puro:** `test_the_predicate_is_pure_over_a_test_graph` (vista `{nodes, semantic:{model_tags,parents}}`); el DAG de la vista sale de las tablas dadas, sin recalcular jerarquía por prefijos.
- **Docs:** `rules-language.md` §1 (gramática y regla de forma), tabla de §7 (5 filas y un ejemplo YAML con `where: model_tag(...)`), y `rules.md` §2 (validación por el store).

## Pruebas independientes (fuera del repo, en `/tmp/probe`)

12 probes verdes (`probe_model_tag.py`) más 2 de caché (`probe_cache.py`):

- `where:` con `model_tag` en vez de `condition:` filtra correctamente y `rules explain` informa `reason: "where"` para el no casado.
- Una regla `on_write` con `model_tag` en `where` evalúa bien un documento que el índice todavía no tiene (tags del nodo de modelo): bloquea a Grandchild y deja pasar a Alien.
- `where_findings` sobre el store devuelve `true/false` por documento; `where_matches` sobre un payload suelto devuelve `false` sin romper; `sldb find --where 'model_tag("concept.base.child")'` responde `ok`.
- El `seen` del finding trae `model` y `model_tags` (incluidos los tags heredados de `StructuredNLDoc`).
- `subject: model_tag(...)` se rechaza por el validador de `RuleDoc` (`ValidationError`), como dice `rules-language.md`.
- Cambiar el DAG después de una corrida cacheada (`add_semantic_parent`/`remove_semantic_parent`) recalcula y no deja resultados viejos: la caché no se vuelve autoridad con este predicado.

## Observaciones no bloqueantes

- `tests -k rules` da rc 1 por 4 fallos **preexistentes y ajenos**: `test_clean_code_rules.py` sobre `sldb/api/documents/batch_edges.py` y `sldb/notations/notation_spec.py`, y 2 errores de fixture en `tests/mcp/test_mutability.py` (`test_level_1_refuses_rules…`). Los reproduje en un worktree del padre `66fbb0000^` con el mismo comando: idénticos. La selección aporta 7 tests nuevos (5 del predicado y 2 de clean-code de los módulos nuevos), todos verdes.
- Un tag declarado solo por `__semantics__` de un modelo registrado, sin ningún documento de ese modelo todavía, se rechaza como desconocido: el DAG crece con los tags de los documentos, así que el tag aún no existe en él. Es coherente con «un tag que no existe en el DAG es error», pero el mensaje dice «no document, model or DAG entry carries it» y ahí sí lo lleva el modelo; convendría un mensaje que no afirme eso.
- `docs/architecture/rules.md` §2 tiene una frase mal editada: «Lo primero: Si no, la escritura se rechaza…». Se entiende, pero sobra «Lo primero:».
- El docstring de `semantic_scope.dict_semantics` remite al «formato de los grafos de test de rules-language.md §8», pero §8 (H2) no se actualizó para documentar la clave `semantic: {model_tags, parents, equivalents}` del grafo de test.
- No se añadieron filas de `model_tag` a `tests/test_rules_language_spec.py`, aunque el encabezado de `rules-language.md` dice que los ejemplos del documento son esa suite; los ejemplos nuevos están cubiertos por `tests/test_rules_semantic_tag_predicate.py`.
- `sldb find --where` acepta también `model_tag` (funciona), pero ni `FIND_HELP` (`src/sldb/cli/commands/help_texts_find.py`) ni el docstring de `src/sldb/api/where.py` lo listan. No lo pedía el encargo (docs en `docs/architecture/`).
- Al correr varios archivos con un mismo `--basetemp` compartido aparecieron dos ERROR por colisión de temporales; con basetemp fresco por archivo (y en el commit padre) salen verdes. No es del cambio.
