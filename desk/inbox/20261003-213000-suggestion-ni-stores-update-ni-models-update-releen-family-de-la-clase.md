---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AgentsKBs
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-03T21:30:00'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:44:56'
---

# Ni `stores update` ni `models update` releen `__family__` de la clase

_Describe the incoming message with enough evidence to triage._

Cambiar `__family__` en un modelo ya registrado no tiene forma soportada de
llegar al store. El valor queda congelado al momento de `models add`.

## Reproducción

Store: `knowledge_antonia-cobranza` (AgentsKBs, rama `kb/cobranza`).
Modelo: `kb_models.knowledge:CampaignDoc`, registrado con `__family__ = "cobranza"`.

1. Editar la clase: `__family__ = "cobranza"` → `__family__ = "outbound"`.
2. `sldb stores update --store knowledge_antonia-cobranza/.sldb --pythonpath .`
   → `Updated store`, 113 docs reindexados, **`family: cobranza` intacta**.
3. `sldb models update CampaignDoc --store ... --pythonpath .`
   → `Updated 'CampaignDoc'`, **`family: cobranza` intacta**.
4. `sldb models show CampaignDoc` sigue reportando `family: cobranza`.

El store queda declarando una familia que la clase ya no declara, sin que ningún
comando lo señale. `stores check` pasa.

## Causa

`family` se escribe en un solo lugar, al registrar:

- `src/sldb/api/model_registry/model_index_writes.py:47` —
  `ModelsIndex(..., family=model_family(model_type), ...)`
- `src/sldb/cli/commands/model_add.py:95` — ídem

La ruta de update no la toca:

- `src/sldb/cli/commands/model.py:103` `update()` → `_rehash_and_save()` →
  `rehash_documents()` + `stamp_model_node()`. Rehashea documentos y sella el
  nodo; **no reconstruye el `ModelsIndex` desde la clase**.

Las demás rutas (`models_list`, `describe_model`, `export`, `edge_index`,
`graph/ingest`) solo **leen** `m_idx.family`, así que propagan el valor viejo al
grafo y a los índices derivados.

`semantics` y `base_models` se escriben junto a `family` en `model_add` y
probablemente tengan el mismo problema; no lo verificamos.

## Por qué importa

`family` no es metadato inerte: agrupa la materialización. En nuestro caso
`kb.yaml` declara

```yaml
materialize:
  order: [self, conversation, domain, gate, user, cobranza, kb]
```

Si la clase dice `outbound` y el store dice `cobranza`, el orden de
materialización depende de cuál de los dos lea el consumidor. Eso es
comportamiento observable del asistente, no cosmética.

Además bloquea una corrección de contrato legítima: `__family__ = "cobranza"`
estaba en un paquete de modelos compartido por cuatro KBs de clientes distintos
(viola el I8 de nuestro spec 11: el vocabulario de un cliente no va en el
esquema compartido). Queremos renombrarlo a algo genérico y no hay camino por
sldb.

## Qué esperábamos

Una de estas:

1. `models update <M>` reconstruye `family`, `semantics` y `base_models` desde la
   clase, igual que `model_add`. Es lo que el nombre del comando sugiere.
2. Si cambiar `family` debe ser explícito (porque reordena la materialización de
   quien la use), que exista `models update <M> --refresh-contract` o similar, y
   que `stores check` **marque la divergencia** entre
   `model_family(model_type)` y `m_idx.family` en vez de callarla.

Lo que no esperábamos es que el único camino sea editar
`.sldb/core/models/<M>.yaml` a mano (que además invalida `hash_b`) o
des-registrar y re-registrar el modelo, que en un store con documentos
trackeados obliga a re-trackear todo.

## Workaround que vamos a usar mientras tanto

Ninguno nos convence. Las opciones son:

- editar el YAML a mano y correr `models update` para re-sellar los hashes
  (frágil, deja el store en un estado que ningún comando produjo);
- `untrack` + `models add` + `track` de los 2 documentos afectados
  (más invasivo, pero todo pasa por sldb).

Preferimos la segunda si confirman que es el camino previsto. Si hay un tercero
que no vimos, mejor.

## Resolución

Resuelto (2026-10-18, sldb-04). 7280701a94: stamp_model_node (src/sldb/store/model_node.py) relee `__family__` de la clase cada vez que firma el modelo con la clase importada, y la copia a la entrada del store_index; `stores update` y `models update` pasan por ahí. Test: tests/store/test_family_follows_the_class.py. Task: task-releer-family-de-la-clase-en-stores-update-y-models-update.
