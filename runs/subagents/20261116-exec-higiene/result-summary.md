# result-summary: task-higiene-del-desk-de-sldb-cerrar-con-closeout-resolved-by-citando-el-sha-las-tareas-abiertas-cuyo-tra

Ejecutor deskops-e-93fa3c35f7e4 (sldb-executor). origin/main = `4bcd1918` (main local `1a36c78d`, un commit de desk por delante).

## Estado: BLOQUEADO en el paso de cierre (el análisis está completo)

De las 13 tareas evaluables, **1 está cumplida en origin/main**:
`task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e`, resuelta por `9668e881`.
**No la cerré.** `deskops closeout resolved-by` no puede respetar a la vez la aclaración (4) del coordinador ("No hagas commit") y el "no stagees cambios ajenos" del brief:

- `close_resolved_by` → `_close` (deskops `services/closure.py`, ~l.280-420 y ~l.740-800) **siempre hace un commit de cierre** ("It makes exactly one closing commit"). No tiene opción para cerrar sin commit.
- Antes de commitear corre `git add -A -- .sldb`. En el árbol hay cambios ajenos sin commitear en `.sldb/` (`.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml`, `.sldb/core/documents/RunDoc/run-deskops-e-93fa3c35f7e4.yaml`, el RunDoc de este run), y entrarían en ese commit.

Cuando el `.sldb/` del coordinador esté commiteado o asumido, se cierra con un solo comando (desde la raíz de sldb; ya verifiqué sus refs y tests):

```
TMPDIR=/dev/shm deskops closeout resolved-by --root . \
  --task task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e \
  --reason "H1-H3 entraron a main en 9668e881 (fix) tras la causa raíz commiteada en 3b6786cc; informe runs/subagents/h1-worker-report.md" \
  --ref 9668e881 --ref 3b6786cc \
  --test tests/store/test_doc_invalid_check.py --test tests/store/test_doc_invalid_writes.py \
  -m "closeout: stores check no aborta ante un documento que su modelo rechaza (resolved-by 9668e881) [skip ci]"
```

Las dos refs son ancestros de origin/main (`git merge-base --is-ancestor`). Los dos tests existen y pasan (2 y 8 passed, ver validation.log).

## Criterio

- Lista: `deskops list tasks --root . --format json` → 80 tareas abiertas (todas `draft`).
- Exclusión (aclaración 2): una tarea cuyo archivo `desk/tasks/<id>.md` entró al repo el 2026-11-16 o el 2026-11-17 (`git log --diff-filter=A`) cuenta como creada por el coordinador en las últimas 48 h. Eso deja fuera 67 tareas (serie SW, las 7 del análisis, las del inbox, decisiones de JP, C3 TS, la del triaje del 16-11 `37b2b26c`, etc.). Quedan 13 evaluables.
- "Cumplida" (aclaración 3): goal y done_when verificables en el código de origin/main (extraído con `git archive origin/main` a /dev/shm) más un sha concreto. En la duda, queda abierta.

## Tabla de las 13 evaluables

| tarea | resultado | sha / motivo |
|---|---|---|
| `task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e` | **cumplida, cierre pendiente (bloqueo arriba)** | `9668e881` (fix H1-H3, CHANGELOG 0.1.13, docs/user-manual.md §5) y `3b6786cc` (causa raíz antes del arreglo). El informe `runs/subagents/h1-worker-report.md` nombra la causa de H2 ("ningún commit lo arregló": se arregla en 9668e881). Los tests `tests/store/test_doc_invalid_check.py` y `test_doc_invalid_writes.py` pasan. |
| `task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la` | abierta | Código en main (`bb0e0e9a`, `29ed522b`, `b106f4c0`, `44a55226`, merge `b51e9667`), pero el goal pide que `rules check` exponga la evaluación estructurada en JSON y el worker lo dejó solo en `tags check` (desvío declarado en h47-worker-report.md, sin decisión registrada). Además, el done_when pide dar de baja las notas H4 y H5-H7 y el ítem del drawer, y las notas siguen en `desk/inbox/`. Se cierra con resolved-by `b51e9667` si el coordinador acepta el desvío y da de baja las notas. |
| `task-reglas-rule-graph-no-compone-la-federación-entera-de-stores-enlazados-27-s-por-comando-de-deskops` | abierta | El goal está en main (`84eb7f75`: ya no compone la federación entera; findings idénticos en los 6 desks). El done_when pide rule_graph < 1 s y en stores grandes no se cumple (1,59-2,05 s en frío, rg-worker-report.md). El residuo está en `task-rule-graph-en-frío-y-deskops-show-task-...` (creada el 16-11). Candidata a supersede o resolved-by `84eb7f75` si el coordinador da por trasladado el residuo. |
| `task-v0-benchmark-fijo-de-velocidad-sldb-bench-y-punto-de-partida` | abierta | `sldb bench` está en main (`5f0d5a19`…`531beed4`, tests `tests/test_bench_*.py`). Falta `reports/velocidad-baseline-20261115.md` en origin/main: el worker lo escribió en `/mnt/ssd/proyectos/SLDB_1/reports/`, fuera del repo, y el done_when no es verificable en main. Se cierra con resolved-by `531beed4` si se acepta el informe fuera del repo o se versiona. |
| `task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024` | abierta | `gh run list --branch main`: los últimos 5 runs de CI en main están en `failure` (p. ej. 44077903890 del 2026-11-17). |
| `task-sldb-views-run-board-en-menos-de-1-s-caché-de-disco-de-los-shards-de-documentos-para-select-document` | abierta | No hay caché de disco de shards de documentos ni recorte del import de sldb.api en main después de `d8992c43` (solo el promote de desk). La meta de < 1 s no tiene evidencia. |
| `task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430` | abierta | `apply_batch(store, changes, pythonpath)` en main no tiene `dry_run`. |
| `task-apply-batch-aristas-validadas-antes-de-escribir-alertas-on-write-en-batchreport-rules-check-sobre-re` | abierta | Depende de dry_run (abierta). `BatchReport` no tiene `alerts`; `apply_batch` no acepta `via` ni `authority`. |
| `task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2` | abierta | `src/sldb/api/edges/check_edges.py:29` sigue clasificando con `s.count(":") == 2`. |
| `task-api-pública-búsqueda-rankeada-escrituras-recientes-y-store-hash-como-precondición-atómica-brechas-de` | abierta | No hay puntaje ni orden en search, `store_hash` no es precondición de escritura y no hay decisión registrada para ninguna de las tres brechas. |
| `task-sldb-escucha-suscripciones-y-stream-de-eventos-de-escritura-inbox-20261114-115028` | abierta | No hay documento de decisión (eventos, suscripciones, SSE) en docs/ ni tareas de implementación creadas. |
| `task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia` | abierta | El documento existe (`docs/architecture/evidence-model-family.md`), pero el done_when exige la decisión del dueño y dice "PENDIENTE: decide el dueño". |
| `task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field` | abierta | `docs/architecture/bootstrap-model-set.md` existe, pero los 9 puntos dicen "Decisión del dueño: PENDIENTE". |

## Tabla de las 67 excluidas

| tarea | resultado | motivo |
|---|---|---|
| `task-decisión-de-jp-arreglar-en-sldb-las-referencias-por-ruta-que-no-resuelven-a-través-de-un-store-enlaz` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-dónde-vive-un-hook-que-bloquea-write-edit-sobre-rutas-trackeadas-por-un-store-de-sldb` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-publicar-sldb-0-1-13-fechar-el-changelog-tag-v0-1-13-y-aviso-a-los-consumidores-cuand` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-python-sync-o-stores-build-destrackean-los-pythonsymboldoc-cuyo-símbolo-desapareció` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-qué-de-las-vistas-de-deskops-h1-h8-de-cc34-expresa-la-viewdoc-de-sldb-y-qué-queda-com` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-decisión-de-jp-si-sldb-agrega-un-ast-intermedio-entre-marcador-y-campo-y-clases-anidadas-en-un-docum` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-declaredfiletargets-lee-campos-lista-y-no-aplica-las-exclusiones-a-lo-que-se-declara-para-que-un-des` | excluida | creada el 2026-11-17 (02ea724e), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for` | excluida | creada el 2026-11-17 (02ea724e), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-el-emparejamiento-de-átomos-de-sldb-api-matching-pasa-a-su-propio-eje-y-recuperacion-vuelve-a-ser-un` | excluida | creada el 2026-11-16 (02da5686), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com` | excluida | creada el 2026-11-17 (479b32b2), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari` | excluida | creada el 2026-11-17 (479b32b2), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-higiene-del-cli-para-sldb-ui-fields-update-append-con-string-y-format-inbox-show-con-error-por-stder` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-higiene-del-desk-de-sldb-cerrar-con-closeout-resolved-by-citando-el-sha-las-tareas-abiertas-cuyo-tra` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-limpieza-de-cáscaras-vacías-de-la-api-y-de-los-residuos-de-kgdb-graph-parser-help-texts-graph-ingest` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con` | excluida | creada el 2026-11-16 (02da5686), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-matching-attach-atom-edges-deja-de-recomponer-live-stale-y-los-mapas-del-índice-federado-en-cada-edg` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-on-write-save-document-payload-devuelve-las-alertas-de-la-escritura-y-la-regla-ve-las-aristas-que-el` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-pron-contra-sldb-deshacer-restaura-el-hash-del-mundo-untrack-track-recupera-el-documento-y-find-con` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-r6-el-tokenizer-y-el-parser-del-lenguaje-de-reglas-bajan-a-core-para-cerrar-la-arista-de-capas-model` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared` | excluida | creada el 2026-11-17 (479b32b2), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-reproducir-si-sldb-docs-update-reescribe-índices-de-documentos-ajenos-al-que-actualiza-reviewdoc-de` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-rule-graph-en-frío-y-deskops-show-task-perfilar-de-nuevo-y-bajar-el-costo-de-leer-el-índice-local-me` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-separar-el-store-en-sldb-store-todo-lo-versionado-store-yaml-y-core-y-sldb-cache-todo-lo-regenerable` | excluida | creada el 2026-11-16 (2eb386df), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-api-expone-render-con-roundtrip-renderizar-el-payload-de-un-modelo-a-markdown-y-validar-que-vue` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-api-notations-reexporta-lo-que-specir-importa-hoy-de-módulos-internos-estilos-paletas-errores-m` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-code-publica-facts-genéricos-de-ts-tsx-js-y-jsx-llamadas-entre-símbolos-llamadas-http-como-llam` | excluida | creada el 2026-11-16 (e024b14a), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-docs-track-canonical-un-markdown-escrito-a-mano-se-lleva-a-su-render-canónico-con-el-diff-a-la` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-models-validate-importa-los-modelos-de-deskops-models-como-lo-hacen-extract-y-render-no-module` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-notations-from-graph-elige-el-campo-del-label-el-campo-que-da-kind-o-estilo-y-un-campo-de-agrup` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-notations-validate-valida-una-notación-una-paleta-o-un-spec-por-nombre-o-ruta-e-imprime-finding` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sldb-stores-remove-quita-el-enlace-también-de-la-declaración-store-yaml-así-otra-sesión-no-lo-reintr` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos-data-entity-y-afines-y-el-style-llega-a-la` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-store-index-yaml-no-guarda-rutas-absolutas-de-máquina-para-los-modelos-que-vienen-de-un-paquete-mode` | excluida | creada el 2026-11-16 (da04f911), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-surface-dev-prosa-generada-con-marca-y-hash-de-sus-átomos-de-origen-y-extractor-externo-de-átomos-pr` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw1-documentación-y-arranque-de-surface-al-día-con-el-workbench-readme-maqueta-histórica-tareas-t7-t` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw10-la-cabecera-del-workbench-muestra-la-ruta-del-documento-en-el-disco-como-carpetas-desplegables` | excluida | creada el 2026-11-17 (479b32b2), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw11-el-panel-izquierdo-del-workbench-muestra-el-grafo-de-documentos-relacionados-con-el-abierto-al` | excluida | creada el 2026-11-17 (479b32b2), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw2-la-edición-en-el-lugar-confirma-con-enter-o-falla-cerrada-sin-autoridad-conocida-y-muestra-la-op` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw3-las-referencias-abren-la-vista-que-corresponde-a-su-modelo-el-árbol-enfoca-en-vez-de-navegar-y-l` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw4a-sldb-serve-expone-escribir-un-anclaje-y-leer-su-estado-y-la-cobertura-por-fuente-sobre-la-api-p` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw4b-surface-ancla-de-verdad-por-las-rutas-de-sldb-serve-borra-el-cálculo-local-de-anclajes-y-muestr` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw5-el-dueño-de-un-modelo-sale-de-describe-model-model-ref-y-los-modelos-de-deskops-dicen-gestionado` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw6-el-workbench-vuelve-a-la-ui-de-deskops-y-muestra-gates-y-evidencia-de-la-tarea-desde-deskops-vie` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw7-model-studio-edita-campos-existentes-crea-modelos-deja-que-sldb-compruebe-los-slots-de-la-planti` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw8-decisión-de-jp-qué-queda-de-la-superficie-anterior-de-surface-vistas-legacy-stores-demo-y-caso-l` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw9-aceptación-del-workbench-sobre-el-desk-real-vistas-flujos-atajos-colores-y-enlace-desde-deskops` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-sw9-primera-pasada-capturas-y-tiempos-de-las-cuatro-vistas-del-workbench-sobre-df3903db-para-que-jp` | excluida | creada el 2026-11-17 (d50dd6a9), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |
| `task-átomos-del-catálogo-sin-rutas-absolutas-atom-payload-y-store-documents-emiten-la-ruta-relativa-al-pr` | excluida | creada el 2026-11-16 (37b2b26c), dentro de las 48 h del coordinador: trabajo nuevo, no se evalúa |

## Done When

- "Cada tarea cerrada cita un sha de origin/main que la resuelve": no se cerró ninguna (bloqueo). La única cerrable tiene listo su comando con `9668e881`, ancestro de origin/main.
- "result-summary.md tiene la tabla completa": sí, 13 evaluadas más 67 excluidas, que suman las 80 abiertas.
- "deskops graph missing da 0": rc 0, "No missing graph references found."
- "commit de desk con [skip ci]": no lo hice (aclaración 4). Lo hace el coordinador, o el closeout de arriba, que lleva [skip ci] en el asunto.

## Comandos (salida completa en validation.log)

| comando | rc |
|---|---|
| `cd .. && TMPDIR=/dev/shm deskops graph missing --root sldb` | 0 |
| `cd .. && TMPDIR=/dev/shm deskops list tasks --root sldb` | 0 |
| `uv run ... pytest -q tests/store/test_doc_invalid_check.py` (2 passed) | 0 |
| `uv run ... pytest -q tests/store/test_doc_invalid_writes.py` (8 passed) | 0 |
| `uv run ... pytest -q tests/test_clean_code_rules.py` (1202 passed) | 0 |
| `uv run ... bash tools/check.sh --fast` | 0 |

Otros comandos de solo lectura: `git log/show/merge-base` sobre origin/main, `git archive origin/main` a `/dev/shm/higiene-main` y `gh run list --repo jpcosec/sldb --branch main --limit 5`.

## Archivos tocados

- `runs/subagents/20261116-exec-higiene/validation.log` (nuevo)
- `runs/subagents/20261116-exec-higiene/result-summary.md` (nuevo)

No toqué `desk/`, `.sldb/` ni `src/`. No hice stage ni commit.

## Desvíos y dudas

1. La aclaración (1) autoriza `closeout resolved-by` y la (4) prohíbe commitear, pero resolved-by siempre commitea y stagea todo `.sldb/`. Me detuve antes del cierre en lugar de elegir entre las dos.
2. Exclusión por fecha de alta en git (≥ 2026-11-16). Incluye las del triaje `37b2b26c` del 16-11 (inbox y drawer), que podrían tener origen más viejo. Si el coordinador quiere evaluarlas, hay que correr el mismo criterio sobre ellas.
3. El brief lista `desk/tasks/Board.md` como archivo del contrato. Solo lo cambiaría el closeout (saca la tarea del Board).
