# Reglas de sldb: RuleDoc, `rules check` y `rules explain`

Estado (2026-11-06): contrato e implementación del nodo GO06 del plan
`desk/drawer/plans/grafo-operable`. sldb evalúa reglas declaradas; los consumidores las
escriben como documentos. El lenguaje de predicados es el de
[`rules-language.md`](rules-language.md) y la evaluación entra por la costura
[`GraphBackend.eval`](graph-backend.md). Fuera de este nodo: la evaluación incremental y el
cableado de `on_write` y `on_transition` (GO08), las anclas `doc:` (GO07), las transiciones
como datos (GO09) y el retiro de los shims (GO10).

## 1. El documento `RuleDoc`

`sldb.models.rule_doc.RuleDoc` es un modelo builtin. Se registra como cualquier modelo
(`sldb models add sldb.models.rule_doc:RuleDoc`) y una regla se escribe y se registra como
cualquier documento (`sldb docs create RuleDoc ...` o `sldb.api.create_document`).

| Campo | Tipo | Significado |
|---|---|---|
| `title` | texto | El título (H1). |
| `subject` | texto | La familia de la regla: `model <= X`, o una conjunción de nivel superior de términos `model <= X` (la intersección de sus familias, `rules-language.md` §6). |
| `where` | texto, opcional | Predicado que se evalúa sobre cada miembro de la familia antes de la condición. `false` o `incomplete` = la regla no aplica a ese documento. |
| `condition` | texto | El predicado que debe cumplir cada documento al que la regla aplica. |
| `severity` | `error` \| `alert` | El nivel del finding cuando la condición da `false`. |
| `moment` | `on_write` \| `on_transition` \| `on_check` | Cuándo se evalúa. `rules check` sin `--subject` corre solo `on_check`; GO08 cablea los otros dos. |
| `message` | texto, opcional | Texto con el que empieza `Finding.what`. |

La familia de `model <= X` sale de la herencia de modelos que sldb ya conoce: `base_models`
de los nodos de modelo del índice, transitivamente (la misma que usan `source_types` y
`target_types` de `RelationTypeDoc`).

El hash de una regla es el `content_hash` de su documento; GO08 lo incluye en la clave de su
caché derivada. Nada del resultado de una regla se persiste.

## 2. Validación al escribir

Las invariantes de un documento son del modelo; las que dependen del store, de la escritura.

- **Validadores de `RuleDoc`** (pydantic): `condition` parsea; `where`, si no está vacío,
  parsea; `subject` parsea y es exactamente `model <= X` o una conjunción de nivel superior de
  esos términos (una comparación, un camino, un `or` o un `not` se rechazan: los filtros van en
  `where`); `severity` y `moment` son `Literal`. Construir o escribir una RuleDoc mal formada
  levanta el `ValidationError` del modelo con el campo y el motivo, y no se escribe nada.
- **Contra el store** (`sldb.api.rules.refuse_unknown_family`): cada `X` de `subject` debe
  ser un modelo registrado. Si no, la escritura se rechaza con el error existente de sldb para
  modelo desconocido, `SLDBStoreError: Model 'X' not registered.`. Lo comprueban
  `create_document`, `save_document_payload` y `sldb docs update`, después de validar el
  payload y antes de escribir.

## 3. Qué reglas hay y a qué documentos aplican

- Las reglas son las `RuleDoc` (o documentos de un submodelo de `RuleDoc`) del **store
  local**, leídas de la proyección del índice de aristas (`graph-backend.md`, GO04): no se
  re-extrae ningún documento.
- Una regla **aplica** a un documento si el `subject` da `true` sobre él (el documento está en
  la familia) y, si hay `where`, el `where` da `true`.
- El grafo sobre el que se evalúa es el índice compuesto con sus stores enlazados, de modo que
  los caminos cruzan links y un documento de un store enlazado se puede evaluar.

## 4. `sldb rules check [--subject DOC]`

```
sldb rules check [--subject DOC] [--store S] [--pythonpath P] [--format text|json|yaml]
```

- **Con `--subject`:** evalúa sobre ese documento todas las reglas que le aplican, de
  cualquier momento. `DOC` es `Model:name`, `store:Model:name` (un store enlazado) o una ruta
  (relativa a la raíz del proyecto o absoluta; también `name`, `Model/name` y `alias:ruta`).
- **Sin `--subject`:** evalúa las reglas `on_check` sobre cada documento **local** al que
  aplican (los stores enlazados no se recorren).
- Solo los resultados `false` e `incomplete` se convierten en `Finding` de
  `sldb.core.finding`, que sale por el canal de siempre (`sldb.cli.alert_sink`):

| Campo de `Finding` | Valor |
|---|---|
| `level` | La severidad de la regla si la condición da `false`; `alert` si da `incomplete`, sea cual sea la severidad. |
| `code` | `rules/<nombre>` si `false`; `rules/<nombre>/incomplete` si `incomplete`. `<nombre>` es el nombre del documento RuleDoc. |
| `subject` | El nodo evaluado: el `Model:name` del documento (`store:Model:name` si es de un store enlazado). |
| `what` | `<clause> (seen: <seen>)`, con `seen` en JSON compacto (claves ordenadas, `ensure_ascii=False`). Con `message`: `<message> \| <clause> (seen: <seen>)`. |
| `fix` | `""`: la regla no prescribe remedio. |
| `document` | La ruta del documento relativa a la raíz de su proyecto, como la guarda el registro. |

El nodo viaja en `subject` y la cláusula en `what`; `Finding` no gana campos.

- **Exit:** 1 si hay al menos un finding `error`; 0 en otro caso (los alerts nunca fallan).
- **Salida:** en texto, una línea por finding y el recuento. Con `--format json`,
  `{"findings": [<Finding.as_dict()>...]}`. Con `sldb --envelope rules check --format json`,
  `data` es ese objeto, los alerts van además en `warnings` y un exit 1 es
  `error.type = "rules/failed"`.

## 5. `sldb rules explain RULE SUBJECT`

```
sldb rules explain RULE SUBJECT [--store S] [--pythonpath P] [--format text|json|yaml]
```

`RULE` es `RuleDoc:<nombre>`, `<nombre>` o la ruta de la regla; `SUBJECT`, como `DOC` en
`rules check`. Imprime el finding de eval tal como lo devuelve `GraphBackend.eval`, también
cuando se cumple. Con `--format json` (y por tanto en `data` del envelope):

```json
{"rule": "RuleDoc:needs-owner", "subject": "TaskDoc:task-a",
 "finding": {"node": "TaskDoc:task-a", "holds": "false", "clause": "has(owner)", "seen": {"owner": ""}}}
```

La clave `finding` cierra la hipótesis H10 de `rules-language.md` para `rules explain`.

Cuando la regla no aplica al sujeto, no hay finding de eval, solo el motivo:

```json
{"rule": "RuleDoc:needs-owner", "subject": "TaskDoc:task-a", "applies": false,
 "reason": "where", "detail": "status = \"open\""}
```

`reason` es `subject` si el documento no está en la familia (`detail` = el `subject` de la
regla) o `where` si el `where` dio `false` o `incomplete` (`detail` = la `clause` del `where`
que lo decidió).

| `holds` | exit |
|---|---|
| `true` | 0 |
| `false` | 1 |
| `incomplete` | 2 |
| la regla no aplica | 3 |

La severidad no afecta el exit de `explain`.

## 6. Referencias que no resuelven

Una regla o un documento que no resuelve es el error existente de documento desconocido:
`SLDBDocumentTargetError: Unknown document target: <ref>`, que en el envelope es
el tipo `docs/missing` <!-- gone --> con exit 1 (un tipo de error, no una ruta).

## 7. API

`sldb.api.rules` (también en `sldb.api`):

- `rules_check(store, subject=None, pythonpath=None) -> list[Finding]`
- `rules_explain(store, rule, subject, pythonpath=None) -> dict` y `explain_exit(answer) -> int`
- `refuse_unknown_family(store_path, model_type, payload, pythonpath=None)`

Piezas: `rule_graph.py` (el índice cargado una vez en el backend del store y qué documentos
son locales), `rule_subjects.py` (qué reglas hay, a qué aplican y cómo se resuelven las
referencias), `rules_check.py`, `rules_explain.py` y `rule_writes.py`.

## 8. Hipótesis

- **R1. Payload de evaluación.** La condición se evalúa sobre la proyección del índice
  (`graph-backend.md`, GO04): un campo que no se proyecta (un diccionario, una tabla) no se
  ve desde una regla.
- **R2. Arista `models → store`.** Los validadores de `RuleDoc` importan el parser del
  lenguaje, que vive en el almacén, de forma diferida; `contracts/layers.toml` la cuenta como
  la reparación pendiente R6 (bajar el parser a la capa 0).
- **R3. `sldb docs track`.** Registrar un archivo RuleDoc ya escrito valida el modelo al
  extraerlo, pero no comprueba que los modelos de `subject` estén registrados; una regla así
  no aplica a ningún documento.
- **R4. Formato.** `rules check` y `rules explain` imprimen texto por defecto, como el resto
  de la CLI; el JSON del envelope pide `--format json`.
