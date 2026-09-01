# Extract store into generic typed-document engine (Document + Codec plugins)

ID: task-extract-store-into-generic-typed-document-engine-document-codec-plugins
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260828-220321-suggestion-extract-store-to-generic-typed-document-engine.md`.

## Scope

Origen: análisis de arquitectura en graph_ui. Los specs completos viven en
`graph_ui/desk/drawer/STORE_EXTRACTION_PROPOSAL.md` y los atoms
`atom-the-store-is-a-generic-typed-document-engine-not-sldb-owned-infrastructure`,
`atom-store-core-knows-index-query-hash-lock-consumers-inject-type-and-codec`,
`atom-the-store-is-coupled-to-sldb-via-two-store-to-cli-imports-plus-type-and-codec`.

## Tesis

`sldb/src/sldb/store/` (~1857 LOC) es de facto el núcleo del ecosistema: mucha
dependencia de entrada, poca de salida. Debe volverse un motor genérico de
documentos tipados donde el TIPO de documento y su FORMATO de serialización son
plugins inyectados por el consumidor (`Document` protocol + `Codec`). sldb pasa
de dueño a primer cliente ({StructuredNLDoc + codec Markdown-reversible}).

## Trabajo propuesto (dos tareas encadenadas)

### 1. Spike: cortar el acoplamiento store->cli (bajo riesgo, alta señal)

Invertir dos imports que son inversión de dependencia (capa baja importando de
la alta):
- `store/facade.py`: `from sldb.cli.store_context import get_store_context` ->
  inyección de contexto/provider.
- `store/diagnostics.py`: `from sldb.cli.model_utils import resolve_model_ref`
  (lazy) -> callable inyectado (el patrón ya existe en
  `load_runtime_documents(..., resolve_model_ref)`).

Done when: `grep -rn "sldb.cli" store/` no devuelve nada (fuera de comentarios)
y la suite de sldb sigue verde. SOLO inversión de imports, sin mover carpetas.

### 2. Generalizar a Document + Codec plugins

- Abstraer `StructuredNLDoc` (2 usos) a un protocolo `Document` (identidad,
  tags semánticos, payload de campos, path).
- Abstraer `extract_model_data` (3 usos) a una interfaz `Codec`
  (`extract(raw)->fields`, `render(fields)->raw`).
- Dar al store sus propias excepciones (dejar de importar `sldb.core.exceptions`,
  10 usos).
- `hash_fields` sigue funcionando porque hashea campos extraídos, no formato.

## Done when

El core del store no referencia `StructuredNLDoc`,
`extract_model_data` ni `sldb.core.exceptions`; sldb pasa su suite como primer
consumidor registrado.

## Por qué importa

Desbloquea que kgdb, deskops, knowledge y repopackage consuman un mismo núcleo
en vez de reimplementar persistencia+hash+query (repopackage hoy reinventa un
store pobre sobre YAML crudo). GUARDRAIL: nada de mocks; si una dependencia real
no está disponible, detenerse y reportar, no parchear.

## Progress (updated 2026-09-01)

- [x] Pieza 1 (spike): inversión store->cli mergeada (ee37525, marcado done en cde9628).
- [x] Pieza 2 (parcial): Codec protocol + StoreError propios mergeados (49b9d49, promoted 9502ad8);
  `runtime_codec.py` inyecta el codec por local import (patrón correcto).
- [ ] Pieza 2 (resto): `store/facade.py` y `store/ops.py` aún importan
  `sldb.core.exceptions` (SLDBError/SLDBStoreError); mover a excepciones propias
  del store para completar el done-when. `StructuredNLDoc` ya no es referenciado
  por el core (solo via codec inyectado).
no está disponible, detenerse y reportar, no parchear.

## Source

- `desk/inbox/20260828-220321-suggestion-extract-store-to-generic-typed-document-engine.md`

## Done When

- The message is resolved, answered, or promoted into active work.

---

## Progress update (2026-08-28)

**Step 1 (cut store->cli coupling spike): DONE** — commit ee37525.
- store/facade.py + store/diagnostics.py no longer import from sldb.cli.
- Injection pattern applied; `rg "sldb.cli" src/sldb/store` is empty.
- Validated in isolated Docker sandbox: sldb 411, kgdb 23, deskops 140 (baseline preserved).

**Remaining (still deferred, NOT started):**
- Document protocol abstraction (StructuredNLDoc).
- Codec abstraction (extract_model_data / render).
- Store's own exceptions (drop sldb.core.exceptions).
- Physical store separation — explicitly blocked pending approval.
