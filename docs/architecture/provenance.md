# Procedencia: quién escribió cada cosa, con qué autoridad, y dónde está su historia

Estado (2026-10-20): **propuesta pendiente del dueño, sin implementar.** Nace de su corrección
del mismo día: la heurística de errores y reparaciones de sldb es demasiado estricta porque
no sabe de quién es cada documento ni qué tan estable es su modelo. Este documento declara
esas tres cosas en cada documento y hace que `stores check`, `lint`, `selfdoc check` y el
anclaje las lean en vez de aplicar una tabla fija. Reemplaza la sección 10 de
[code-anchoring.md](code-anchoring.md) como criterio; mantiene su salida (error/alerta,
`warnings` del envelope, annotations) tal cual.

## 1. Lo que se declara

Tres cosas, en el frontmatter de cada documento, bajo una sola clave reservada `sldb`:

```yaml
---
sldb:
  by: agent:deskops-30        # quién: human:<id> | agent:<id>
  at: 2026-10-20T11:30:12Z    # cuándo (UTC); 0 cuando no se sabe
  via: deskops retire         # con qué: la operación o herramienta que escribió
  authority: authored         # nivel de autoridad (sección 2)
  from: [code:src/sldb/cli/main.py::main]   # opcional: de qué deriva (theorem, generated)
---
```

- La clave es `sldb` y no `provenance` porque `AtomDoc` de deskops ya usa `provenance` para
  la URL de la fuente de un átomo (`deskops/models/atom.py`); un nombre con namespace no
  choca con ningún modelo ajeno.
- **Si el bloque no está, se asume `by: agent`, `at: 0`, `authority: generated`** (regla del
  dueño). Un documento escrito a mano sin bloque se lee como generado por un agente en el
  instante cero: lo menos autoritativo posible, hasta que alguien lo firme.
- El esquema es un modelo pydantic, `Provenance`, declarado junto al modelo base
  `StructuredNLDoc` (`src/sldb/models/structured_doc.py`); cada documento leído expone
  `.provenance`. El modelo lo **declara**; el store lo **lleva** (sección 4).

## 2. Niveles de autoridad

De más a menos autoridad sobre lo que dice un humano:

| nivel | qué es | quién lo escribe | un cambio es |
|---|---|---|---|
| `source_raw` | material de afuera: un correo pegado, una transcripción, una spec recibida | un humano, una vez | **error**: la fuente no muta; otra versión es otro documento |
| `authored` | escrito con intención: specs, decisiones, notas, tareas, átomos | humano o agente | la vida normal: alerta a lo sumo; la política decide (sección 5) |
| `theorem` | derivado de fuentes por una regla enunciada: teoremas de pron, conclusiones de un lint, anclajes | un agente o un comando, con `from:` | alerta `verify` si cambió sin que cambiara su `from:` |
| `generated` | producido por un generador desde código o desde el store: `CliCommandDoc`, `PythonSymbolDoc`, surfaces | un comando | viejo respecto de su fuente: alerta `regenerate`; editado a mano: **error** (se va a pisar) |
| `cache` | desechable, se reconstruye: runtime, shards, embeddings | sldb | nada; ni siquiera es un hallazgo |

Los nombres `source_raw` y `theorem` son los del dueño y los de pron (`TheoremDoc`,
`source/`). Cada modelo declara su nivel por defecto con `__authority__` en la clase
(`CliCommandDoc` → `generated`, `TheoremDoc` → `theorem`, `InboxNoteDoc` → `authored`); el
bloque de un documento puede subirlo o bajarlo. Sin declaración, `generated`.

El nivel y el autor se cruzan: un humano que edita un `generated` está escribiendo donde lo
van a pisar (error, y el arreglo es declararlo `authored` o escribir en la fuente); un
agente que toca un `source_raw` está alterando evidencia (error); un agente que reescribe un
`authored` de otro autor es lo que hoy nadie ve y debería ser alerta `by-changed`.

## 3. La historia vive en git

No se inventa la rueda: el pasado de un documento es su historia en git, y el bloque `sldb`
de cada versión dice quién la escribió. sldb pone las ruedas para buscar ahí:

- `sldb docs history <Model:doc> [--since] [--format json]` <!-- gone -->: por cada commit
  que tocó el archivo: sha, fecha de git, los `by`, `at` y `authority` del bloque `sldb` de esa versión, su
  `source_hash` y `content_hash`, y qué campos cambiaron respecto de la anterior (los dos
  payloads extraídos y comparados por campo, como `field_hashes`). Se apoya en
  `text_history.py` (`src/sldb/store/diagnostics_models/text_history.py`), que ya recorre
  `git log --follow` y hashea cada versión.
- Lo que dice la identidad de git no se usa para `by`: en este repo los commits locales salen
  como `github-actions[bot]`. El autor está en el documento, no en el commit.
- Esto responde la nota de inbox 20261019-011009 (qué guarda el pasado del árbol): es la
  opción **(c)** de [journal-authority.md](journal-authority.md), con el quién y el cuándo
  que se perdían ahora dentro del documento. El journal sigue congelado y no gana ningún
  escritor; se retira cuando `docs history` exista. Queda como decisión del dueño confirmarlo.

## 4. Cómo lo lleva el store

Medido con un sondeo (2026-10-20) sobre el renderizador y el extractor actuales:

- Un bloque `sldb` en un documento cuyo template no lo declara **se extrae ignorándolo** y
  **el ruido estructural no lo ve**, pero `refuse_undeclared_frontmatter`
  (`src/sldb/api/documents/frontmatter_keys.py`) lo rechaza al trackear y el re-render lo
  pierde.
- Un template con `sldb: ⸢optrev,dict•sldb⸥` dentro de su frontmatter lo renderiza y lo
  extrae idéntico, y lo omite entero cuando el valor es `None`.

Dos formas de llevarlo; se propone la segunda:

1. **Campo del modelo.** `StructuredNLDoc` declara el campo `sldb` e inyecta el marcador en
   el frontmatter de cada template. Costo: cambia el `contract_hash` de todos los modelos
   una vez (el template y el esquema de campos lo firman), el bloque entra en `content_hash`
   y cada firma mueve `hash_d` (un sello se leería como mutación de datos), y hay que
   enseñar a `template_literals`, `create_model` y `models validate` a no escribir ni exigir
   lo inyectado.
2. **Bloque del store, esquema del modelo** (propuesta). El modelo declara `Provenance` y
   `__authority__`; el camino de escritura del store lo sella y el de lectura lo lee, fuera
   del payload de campos:
   - escritura (`payload_save_steps.write_rendered_document`, `create_document`): se renderiza
     el payload y se **adjunta** el bloque al frontmatter (creándolo si el template no tiene);
   - lectura (`runtime_document`, `extract_model_data`): el bloque se lee a `.provenance` y
     el extractor sigue ignorándolo; `refuse_undeclared_frontmatter` exime la clave `sldb`;
   - hashes: el bloque está en el texto, así que **mueve `source_hash`** (como cualquier
     escritura) y **no mueve `content_hash`**: un sello es un cambio de texto, no de datos.
     El contrato de los modelos no cambia; ningún store necesita `stores update` por esto.
   - índice: `DocumentEntry` gana `by`, `at` y `authority` (aditivo, `None` en stores viejos)
     para que `find --where`, el export semántico y el grafo los vean sin abrir el archivo.

Quién firma `by`: `--actor` (hoy solo en `sldb semantic`) pasa a ser un flag global, con
`SLDB_ACTOR` como variante de entorno; sin ninguno, `agent`. `via` es el comando que
escribió. **Se sella solo cuando algo cambió**: si el texto sin bloque es igual al que está
en disco, el bloque anterior se conserva. Esto evita que un generador mueva `at` en cada
corrida y rompa comparaciones como el `docs-check` de pron sobre su README generado.
`docs track` no escribe el archivo y no sella: un archivo trackeado a mano queda con los
defaults hasta que alguien lo guarde por la API.

## 5. Política: el hallazgo se lee con la autoridad, no con una tabla

`diagnose_store` sigue produciendo hechos (`source_hash`, `content_hash`, contrato, roster).
La capa que los interpreta deja de ser fija y pasa a consultar, en orden: el bloque del
documento, el `__authority__` del modelo, y la política del store:

```yaml
# .sldb/store.yaml
policy:
  InboxNoteDoc: {data_mutation: reindex, structural_noise: allow}
  ArchitectureNarrativeDoc: {structural_noise: allow}
  "*": {missing: error, model_unresolved: error, link_broken: error}
```

Respuestas: `ignore`, `allow`, `reindex` (un `stores update` acotado a ese documento),
`alert`, `error`, `hook: <comando>` (recibe el hallazgo en JSON; deskops puede mover una
tarea o avisar por inbox). Defaults de sldb, sin declaración alguna:

- **error** solo lo roto: archivo trackeado ausente, modelo que no importa, store declarado
  sin construir, enlace a nada, y las dos cruces de la sección 2 (humano sobre `generated`,
  agente sobre `source_raw`).
- **alerta** todo movimiento de fuente: contrato movido, raíz o roster atrasados,
  `data_mutation`, documento generado viejo, ancla cambiada, ruta citada ausente (`lost`).
- **allow** el ruido estructural en modelos de cuerpo narrativo (un solo campo `body`) y en
  `authored`; **alerta** en los demás. La escritura deja de rechazarlo cuando la política lo
  permite: hoy `docs track` y `docs create` lo rechazan sin mirar el modelo.

La salida no cambia respecto de lo ya diseñado: una alerta nunca es silenciosa (texto,
`errors`/`alerts` en el JSON, `warnings` del envelope, `::warning` en CI) y el exit code sale
solo de los errores. Lo que cambia es de dónde sale el nivel.

## 6. Etapas propuestas

1. `Provenance` y `__authority__` en el modelo base; sello en escritura y lectura a
   `.provenance`; exención de la clave `sldb`; `--actor` global. Tests: round-trip con y sin
   bloque, defaults, `content_hash` quieto ante un sello, sello solo si cambió algo.
2. `DocumentEntry` con `by`/`at`/`authority`; `find --where` y export los exponen.
3. `docs history` sobre git.
4. La política de la sección 5 con sus defaults, y la salida de error/alerta ya escrita
   (tipo `Finding`, emisor único, `warnings` del envelope) conectada a ella. Avisar por inbox
   a deskops, spec2viz y graph_ui antes de subir, porque cambia `stores check`.
5. El anclaje a código ([code-anchoring.md](code-anchoring.md)) encima: un ancla es un
   documento `theorem` con `from:` y sus fingerprints.

Pendiente del dueño: confirmar la forma 2 de la sección 4, los cinco niveles y sus nombres, y
la lectura de la nota 20261019-011009 como opción (c).
