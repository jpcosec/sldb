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
