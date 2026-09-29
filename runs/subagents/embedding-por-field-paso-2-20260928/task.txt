# Embedding por field en la capa derivada (paso 2 de field-level indexing)

ID: task-embedding-por-field-en-la-capa-derivada-paso-2-de-field-level-indexing
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260928-225002-suggestion-embedding-por-field-en-la-capa-derivada-paso-2-de-field-level-indexing.md`.

## Scope

_Describe the incoming message with enough evidence to triage._

Paso 2 de field-level indexing. El paso 1 (hash por field) ya esta hecho y
cerrado: commit 9976efc, `DocumentEntry.field_hashes` en produccion.

NOTA DE PROCESO: esta task existia como la mitad no ejecutada de
`task-hash-por-field-embedding-por-field-en-capa-derivada`, declarada solo como
prosa ("NO INCLUYE (tarea siguiente)") dentro del scope de aquella. Al cerrarse
esa task el bundle se borro y el paso 2 se perdio con el. Se recrea aqui como
artefacto propio.

## Estado habilitante (ya existe en main)

- `DocumentEntry.field_hashes: dict[str, str]`, poblado en todos los write-sites.
- `hash_field_map_of` / `hash_fields_with_map` en `store/hashing.py`.
- `api/matching/document_index.py` ya keyea por hash y cachea vectores en un
  archivo derivado fuera de git:

```python
def _unchanged(self, key: str, h: str) -> bool:
    prev = self._entries.get(key)
    return prev is not None and prev.get("hash") == h
```

La arquitectura correcta (hash invalida, embedding indexa) ya esta construida.
Solo opera a nivel documento.

## Tesis

Un field (`scope`, `why`, `body`) es una unidad semantica legitima. Buscar sobre
el documento entero diluye esa senal: `document_type.document` da una semantica,
el field da otra mas fina.

`DocumentIndex.index()` ya recibe `(key, hash, text)`. Un field es
`key = "Model/doc#field"` con `hash = field_hashes[field]`. La clase soporta
granularidad arbitraria; nadie le dijo que la key deba ser un documento.

## Trabajo propuesto

1. Proyeccion de fields a items indexables: de un documento y su modelo, emitir
   `(f"{model}/{doc}#{field}", field_hashes[field], texto_del_field)`. Decidir
   que fields se indexan (probablemente no `id`, no hashes, no listas de tags).
2. Alimentar `DocumentIndex` con esos items. `_partition` ya hace lo correcto:
   re-embebe solo los fields cuyo hash movio.
3. Exponer ranking por field. Hoy ni siquiera `Corpus.rank()` (nivel documento)
   esta expuesto en el CLI ni exportado en `sldb.api` (ver limite en
   docs/user-manual.md seccion 14): resolver eso es parte del alcance o su
   dependencia.
4. Cuantizacion int8 al persistir.

## Costos medidos (corpus real del repo, ~989 fields simulados)

- storage fp32: 1483 KB
- storage int8:  371 KB  <- usar este, despreciable
- hash por field: 0.77 us/field (ya pagado, el paso 1 lo dejo hecho)

## NO-GOAL (heredado del analisis del paso 1, sigue vigente)

NO reemplazar hashes por embeddings en la capa de identidad. Evaluado y
descartado por razones estructurales, no de costo:

- No es exacto: dos textos distintos pueden dar vectores a distancia ~0. Para un
  Merkle que decide que reprocesar, un falso negativo es corrupcion silenciosa.
- No es determinista entre versiones: cambiar de modelo de embedding, de version
  de lib o de backend BLAS mueve todos los vectores -> invalidacion total del
  store. sha256 es estable para siempre.
- No compone: `model_hash = hash(contract_hash + roster_hash)`. Promediar
  embeddings de hijos no produce identificador del padre, produce ruido.
- ~1000x mas caro: 0.77 us vs ~1-3 ms por field.

Los hashes se quedan en la capa de identidad y cambio. Los embeddings van solo
en la capa derivada de busqueda.

## Precaucion de diseno (del atom del paso 1)

Ausencia de dato no es dato. `field_hashes` vacio significa "no se pudo
calcular" (store viejo, o documento que ya no extrae), nunca "ningun field
cambio". Un indexador que vea mapa vacio debe caer al documento entero, no
concluir que no hay nada que re-embeber.
Ver: desk/atoms/atom-un-mapa-de-hashes-vacio-significa-no-se-pudo-calcular-nunca-nada-cambio.md

## Source

- `desk/inbox/20260928-225002-suggestion-embedding-por-field-en-la-capa-derivada-paso-2-de-field-level-indexing.md`

## Done When

- The message is resolved, answered, or promoted into active work.
