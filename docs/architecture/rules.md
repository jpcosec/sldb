# Reglas de sldb: RuleDoc, `rules check` y `rules explain`

Estado (2026-11-06): contrato e implementación de los nodos GO06 (§1-§8) y GO08 (§9-§10) del
plan `desk/drawer/plans/grafo-operable`. sldb evalúa reglas declaradas; los consumidores las
escriben como documentos. El lenguaje de predicados es el de
[`rules-language.md`](rules-language.md) y la evaluación entra por la costura
[`GraphBackend.eval`](graph-backend.md). Las anclas `doc:` son las de
[`anchoring.md`](anchoring.md) §6 (GO07) y las transiciones las de [`edges.md`](edges.md)
(GO09). Fuera: el retiro de los shims (GO10).

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
| `moment` | `on_write` \| `on_transition` \| `on_check` | Cuándo se evalúa (§9). `rules check` sin `--subject` corre solo `on_check`. |
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
| `what` | `<clause> (seen: <seen>)`, con `seen` en JSON compacto (claves ordenadas, `ensure_ascii=False`). Con `message`: `<message> \| <clause> (seen: <seen>)`. Si la cláusula que decidió es un cuantificador de nivel superior con testigo, sigue ` (witness: <Model:name> <seen del testigo>)` (§9.5). |
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
- GO08 (§9): `rules_on_check(store) -> list[Finding]`, `on_check_findings(store, pythonpath=None)`
  y `transition_findings(store, document, subject, pythonpath=None)`; en `sldb.api`, además,
  `edges_blocked`.

Piezas: `rule_graph.py` (el índice cargado una vez en el backend del store y qué documentos
son locales), `rule_subjects.py` (qué reglas hay, a qué aplican y cómo se resuelven las
referencias), `rules_check.py`, `rules_explain.py` y `rule_writes.py`; de GO08,
`rules_on_write.py`, `rules_on_transition.py`, `rules_on_check.py`, `rule_cache.py`,
`dirty_set.py` y `fixpoint.py`.

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

## 9. Evaluación en su momento (GO08)

Los findings son los de §4 (`rule_finding`): mismo `level`, `code`, `subject`, `what`,
`document`. Todo finding sale por `sldb.cli.alert_sink`: los alerts en `warnings` del envelope,
los errores en `error`/`errors`. Una regla aplica como en §3.

### 9.1 `on_write`

Un paso propio de `save_document_payload` (`payload_save_steps.check_rules_on_write`),
inmediatamente después del pinneado de anclas (GO07) y antes de renderizar y escribir:

- La regla lee el payload **ya pinneado**, con `<campo>__anchor_state` de cada campo
  `__doc_anchors__` calculado como lo compondría el índice. El documento conserva su modelo y sus
  aristas del índice **anterior** a la escritura (H-GO08-3).
- Reglas: las `on_write` del store, en orden de export id (`RuleDoc:<nombre>`).
- Al menos un finding `error`: `SLDBRuleViolationError` (`sldb.core.exceptions`), con los errores
  en `findings` y un `message` de una línea por error, `<code>: <what>`. Nada se escribe. En el
  envelope es `error.type = "rules/violation"`, exit 1.
- Los alerts salen siempre (pase o no la escritura) por `sldb.core.finding_route.route`; la CLI
  instala `alert_sink` como oyente al arrancar (`warnings` del envelope y una línea por alert en
  stderr). Un programa que use la API sin instalar oyente no los recibe (H-GO08-2).
- Un store que no registra `RuleDoc` (ni un modelo construido sobre él) no lee ninguna regla:
  la escritura se comporta exactamente como antes.

### 9.2 `on_transition`

`edges_holding(store, node, subject, relation=None, include_linked=True, exclude_tags=(), document=None)`
y la nueva `edges_blocked` con la misma firma. `document` es la referencia del documento que
transiciona (`Model:name`, `store:Model:name` o ruta); las reglas `on_transition` que le aplican
se evalúan sobre `subject`, el mismo payload que leen las condiciones (los extremos de la arista
son estados, no sujetos).

- Sin error: `edges_holding` devuelve las aristas que se cumplen, cada `EdgeRecord` con `effects`
  (GO09, intacto) y `findings` (lista de `Finding`, solo alerts; `[]` si no hay).
  `edges_blocked` devuelve `[]`.
- Con un error: ninguna arista se cumple (`edges_holding` = `[]`) y `edges_blocked` devuelve las
  que se habrían cumplido, cada una con `findings` = todos los findings (errores y alerts).
- Las reglas son del sujeto, no de la arista: los mismos findings valen para toda arista que
  sale de `node` (H-GO08-4).
- Sin `document` no corre ninguna regla y `findings` queda `None`: como `effects`, no aparece en
  ningún dump mientras no tiene valor. `sldb edges show NODE --holds-for DOC` pasa `DOC` como
  `document`.

### 9.3 `on_check`

`sldb stores check` (y `check_store`, `GET /stores/check`) agrega a sus findings, a su propio
nivel y después de los del diagnóstico, los de `on_check_findings`: las reglas `on_check` de
`rules_on_check` y los alerts de `check_doc_anchors` (GO07). Exit 1 solo si hay un error; los
alerts salen en `alerts` del JSON y en `warnings` del envelope.

### 9.4 Caché derivada y dirty set

En `<.sldb_cache>/rules/` del store (`layout.cache_dir`), JSON, leída y escrita bajo el bloqueo
de store existente (`store_lock`, en espera):

- Un archivo por regla, `<content_hash de la RuleDoc>.json`: `results` (export id → finding como
  `Finding.as_dict()`, o `null` si se cumple o no aplica) y `stamps` (de qué se calculó cada
  resultado). La familia es `subject` sin aplicar `where`. Cambiar la regla cambia su hash: la
  familia entera se recalcula; los archivos de hashes que ya no existen se borran.
- `dirty.json`: el dirty set. Escribir un documento D (`on_write`, con RuleDoc en el store) agrega
  D y todo documento con una arista entrante o saliente hacia D en el índice. `rules_on_check`
  recalcula los documentos sucios y lo vacía al terminar.
- Una regla **ancha** (una clausura `+`, un camino de más de un paso o un cuantificador anidado)
  recalcula su familia entera si el dirty set no está vacío.
- Cuenta como sucio (se recalcula): un documento sin entrada, uno cuyo stamp cambió (el
  documento y sus vecinos a un salto, o el store entero para una regla ancha: `source_hash` y
  payload compuesto, anclas incluidas) y todo, si `dirty.json` falta, es ilegible o de otra
  versión. Así una escritura que no pasa por `save_document_payload` (un `create`, un `delete`,
  un archivo editado y reconstruido) no deja un resultado viejo (H-GO08-5).
- La caché nunca es autoridad: borrarla da los mismos findings. Un recálculo es una llamada a
  `rules_on_check.recompute` por par regla-documento; `check_doc_anchors` no se cachea.

### 9.5 Punto fijo y testigo

Los únicos hechos derivados son los conjuntos de una clausura `+`. El evaluador de GO05 ya los
calcula semi-naive (`predicate_reach._closure`: cada ronda expande solo los elementos nuevos; uno
ya visto no se vuelve a expandir), así que termina con ciclos; viven en memoria y nunca se
persisten. GO08 lo reutiliza (`fixpoint.py`).

Como `seen` del lenguaje no nombra elementos (rules-language.md §4, H16), el `what` de un
finding decidido por un cuantificador de nivel superior agrega el **testigo**:
` (witness: <Model:name> <su seen>)`, el primer elemento alcanzado que falsea un `all`, cumple
el `any` interno de un `none` o, en un `any` falso, el primero alcanzado (todos lo falsean);
en un `incomplete`, el primero incompleto. Sin elementos no hay testigo.

### 9.6 `sldb edges check`

Además de lo existente, falla (exit 1) si la condición de una arista (la suya o la heredada de su
tipo) no parsea: `edge <origen> -[<tipo>]-> <destino>: condition does not parse: <motivo>`.

## 10. Ejemplo end-to-end

`tests/api/test_rules_end_to_end.py`. Un store temporal con:

- `Task` (`__contract__ = ["title", "goal"]`), `Review` (`__doc_anchors__ = ["subject"]`,
  campo `verdict`) y `State`; dos estados `State:doing` y `State:done` y un `RelationDoc`
  `moves_to` entre ellos sin condición.
- La regla:

```yaml
title: reviewed
subject: model <= Task
condition: any(^subject: anchor_state = "intact" and verdict = "accepted")
severity: error
moment: on_transition
```

1. **Task sin Review.** `edges_holding(store, "State:doing", task, "moves_to", document="Task:t")`
   es `[]`; `edges_blocked(...)` devuelve la arista con el finding
   `rules/reviewed`, cuyo `what` empieza por `any(^subject: ...)` (sin testigo: nada alcanzado).
2. **Review accepted con `subject: doc:Task:t`.** Al guardarla se pinnea
   (`doc:Task:t@sha256:...`); la arista está en `edges_holding`, con `findings = []`.
3. **Editar `goal` de la Task.** El ancla queda `changed`; la arista vuelve a `edges_blocked` y el
   `what` termina en `(witness: Review:r {"anchor_state":"changed"})`. `sldb stores check`
   reporta además el alert `anchors/doc_changed` de `Review:r` y sale 0.

## 11. Hipótesis de GO08

- **H-GO08-1. Testigo.** Nombrar el elemento (aceptación: "falla nombrando C"; "explicación
  anchor_state = changed") no cabe en `seen` sin cambiar el lenguaje (GO05); va al final de
  `what`, también en `rules check`.
- **H-GO08-2. Canal de los alerts de `on_write`.** La API no importa la CLI: los alerts viajan
  por `sldb.core.finding_route`, donde `sldb.cli.main` instala `alert_sink`.
- **H-GO08-3. Aristas en `on_write`.** La regla ve el payload nuevo pero las aristas del índice
  anterior; una referencia agregada en la misma escritura se ve en la siguiente evaluación.
- **H-GO08-4. Sujeto de `on_transition`.** Un payload suelto no dice qué documento es: el
  parámetro `document` lo nombra. Sin él no corre ninguna regla.
- **H-GO08-5. Stamps.** Además del dirty set del contrato, cada resultado guarda un stamp; un
  cambio que no pasó por una escritura con reglas también recalcula.
- **H-GO08-6. Solo `save_document_payload`.** `create_document`, `docs track` y el borrado no
  corren `on_write` ni marcan el dirty set (los stamps cubren su efecto en `on_check`).
