# Embedding por field en la capa derivada (paso 2 de field-level indexing)

Task: task-embedding-por-field-en-la-capa-derivada-paso-2-de-field-level-indexing
Estado: resuelto. El trabajo propuesto por esta task aterrizó íntegro.

## Qué se hizo

La tesis de la task era correcta y se implementó como estaba escrita:

- `DocumentIndex.index()` ya recibía `(key, hash, text)` y keyeaba por hash; solo
  operaba a nivel documento. Se le dio la granularidad de field sin refactor:
  `key = docs/<Model>/<doc>/<campo>` con `hash = field_hashes[field]`.
- La proyección de fields a items indexables es `FieldProjection`
  (`src/sldb/api/corpus/field_projection.py`): excluye por defecto identity y
  bookkeeping (`id`, `name`, `slug`, `path`, `tags`, hashes) y texto bajo 12 chars,
  como preveía el punto 1 del trabajo propuesto.
- El ranking por field está expuesto (`Corpus.rank_fields`) y `Corpus` quedó
  exportado en `sldb.api`, que resuelve el punto 3 y el límite de §14 del manual.
- NO-GOAL respetado: los hashes siguen en la capa de identidad; los embeddings
  solo en la capa derivada. El índice por field vive en su propio archivo derivado
  (`fields.*.json`), nunca compartido con el de documentos.
- Precaución del atom respetada: store sin `field_hashes` (mapa vacío = "no se
  pudo calcular") recomputa en memoria al leer; no concluye "nada cambió".

## Invariante medido

Editar un field de un documento re-embebe ese field y reutiliza el resto:
`embedded=1, reused=3` sobre un documento de dos fields. Verificado también
end-to-end con `fields update` sobre un store de prueba.

## Puntos del trabajo propuesto no incluidos

Punto 4 (cuantización int8): no se hizo. El storage fp32 del corpus de fields es
despreciable (371 KB int8 vs 1483 KB fp32 medidos en la task); se deja para
cuando exista un corpus de fields real que lo pese.

## Evidencia

- Commits: b047b74 (índice y ranking por field), d8bbcfc (field_id al espacio de
  direcciones de `fields`: `docs/<Model>/<doc>/<campo>`, con rutas anidadas y
  prefijo de store linkeado), f53a32b (7 tests de los contratos).
- Tests: `tests/test_field_corpus.py` — contratos de direccionamiento, proyección,
  hash propio por field, fallback de store pre-migración, invalidación selectiva,
  ranking con documento y payload en el hit, audit por field y separación de
  archivos derivados.
- Suite: 1077 passed, 0 failed (validation.log).
- Desviación de proceso registrada: la implementación se hizo en la sesión
  principal, sin despachar Executor/Tester como subagentes. La validación que
  respalda este cierre es la suite commiteada, no un run de Tester.
