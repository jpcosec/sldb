# gd27b-worker: GD27 para deskops (anchored_by value bare, tag_models, tag_folder estricto)

TaskDoc: `task-gd27-para-deskops-anchored-by-con-valor-sin-namespace-y-alcance-de-las-reglas-de-tags-por-modelos-h1`
(task.code). Rama `wt/gd27-deskops`, base origin/main `b49b7259`. Origen: H1-H3 de CC35d de deskops.

## Diseño (antes del código)

### g1: `anchored_by.value`

Esquema de una entrada de `tag_namespaces`:

```yaml
- name: domain
  anchored_by:
    model: CrossroadDoc
    field: path
    value: bare        # opcional: tag (por defecto) | bare
```

- `anchored_by` es `{model, field}` o `{model, field, value}`; `value` solo `tag` o `bare`.
  Otra clave, un `value` distinto o un model/field en blanco: `ValidationError`. Se vuelca tal
  como se escribió (sin `value` si no lo trae), así que las declaraciones de hoy no cambian.
- `TagNamespace.anchor_tag(field_value) -> str | None` decide qué tag ancla el campo de un
  documento ancla:
  - `tag`: el valor mismo si su namespace es `name` (comportamiento de hoy);
  - `bare`: `f"{name}:{valor}"`; un valor que ya trae `name:` delante, uno en blanco o uno que
    no es str no ancla nada (disposición de pi).
- `anchors_of` (y por él `evaluate`, `tag_tree`) usa `anchor_tag`; las claves de `anchors` son
  siempre tags completos, así que `required`, `_missing`, `_nested` no cambian.

### g2: `tag_models`

```yaml
tag_models: [AtomDoc]     # opcional, a nivel store, junto a tag_namespaces
tag_namespaces: [...]
```

- `StoreDeclaration.tag_models: list[str]`, por defecto `[]`; vacío o ausente = todo como hoy
  (y no se vuelca, como las demás claves opcionales).
- En alcance: un documento cuyo `model` está en `tag_models` o tiene uno de ellos en
  `base_models` (lo que lee `RuleGraph.located`). Helper `in_scope(graph, models, node)` en
  `builtin_tag_rules.py`; `tag_scope(store_path)` lee la declaración una vez.
- Solo filtra la familia `builtin:tag_namespace`: `family_findings` evalúa solo los nodos en
  alcance (cubre `on_write`, `on_check`/`stores check`, `rules check`, `tags check`).
  `rules explain builtin:tag_namespace:<ns> DOC` sobre un documento fuera de alcance responde
  `holds: true` con `clause: "model in tag_models"` y `seen: {model, tag_models}`.
- Las anclas NO se filtran: `anchors_of` sigue leyendo todos los documentos locales del modelo
  ancla.
- `tag_tree` con `tag_models`: `used_tags` (y por él `orphans`, `unplaced` y, sin
  `anchored_by`, `roots`) cuenta solo documentos en alcance; las raíces y anclas de un
  namespace anclado, como hoy.
- No se valida que los nombres de `tag_models` estén registrados (hipótesis abajo).

### g3

Sin cambio de código en `tag_folder`: sigue `ValueError` ante segmentos vacíos. Una línea en
`docs/architecture/tags.md` que dice que el consumidor debe evitar esos tags (deskops lo hace
en 'CC35d resto').

### g4: tests

`tests/api/test_tags_scope.py` (nuevo): (a) CrossroadDoc.path `a.b` + anchored_by bare:
`tag_tree` da la raíz y `tag_check` sin hallazgos; un path `domain:a` no ancla; (b)
`tag_models: [AtomDoc]`: tareas con `workspace:x` sin hallazgos, átomo (y descendiente) con
namespace no declarado sí; explain fuera de alcance; tag_tree acotado; (c) los existentes de
`tests/api/test_tags.py` sin cambios.

### Presupuesto de líneas

`store_declaration.py` está en 80 líneas efectivas: el campo nuevo se compensa juntando el
`if` de `declared_graph_backend` en una expresión condicional.

## Hipótesis

- `tag_models` no se contrasta con los modelos registrados: un nombre mal escrito deja el
  alcance vacío (ningún hallazgo). Un `stores check` que lo avise sería el paso siguiente.

## Entrega

Hecho como el diseño, sin desvíos. Archivos: `tag_namespace.py` (`anchored_by.value`,
`anchor_tag`), `store_declaration.py` (`tag_models`; el `if` de `declared_graph_backend` pasa
a expresión para quedar en 80 líneas efectivas), `builtin_tag_rules.py` (`tag_scope`,
`in_scope`, filtro en `family_findings`, `explain` fuera de alcance, `anchors_of` por
`anchor_tag`; queda en 80), `tags/tag_tree.py` (`used_tags` acotado), `cli/commands/tags.py`
(`(bare)` en `tags namespaces`), `docs/architecture/tags.md` (g1, g2 y la línea de g3),
`CHANGELOG.md`, `tests/api/test_tags_scope.py` (nuevo, 11 tests). Sin archivos nuevos en `src/`
(no cambia `contracts/layers.toml`).

Validación (de a uno, con la guarda; intérprete `SLDB_1/.venv` con `PYTHONPATH=src`, porque
el worktree no tiene `python` en el PATH ni pytest en `sldb/.venv`):

| Archivo | Resultado |
|---|---|
| tests/api/test_tags_scope.py | 11 passed |
| tests/api/test_tags.py (sin cambios) | 34 passed |
| tests/test_clean_code_rules.py | 954 passed |
| tests/api/test_api_stores.py, test_policy.py, test_project_graph.py, test_project_graph_config.py, test_referrers.py, test_replace_text.py, test_scaffold_store.py, test_rules_linked_reach.py | 7, 14, 13, 11, 10, 16, 20, 4 passed |
| tests/store/test_stores_build.py | 27 passed |
| tests/test_serve.py | 61 passed |
| `bash tools/check.sh --fast` | TODAS LAS PUERTAS PASAN |

Pendiente del coordinador: los 7 pasos de `.github/workflows/ci.yml` en clon limpio.
