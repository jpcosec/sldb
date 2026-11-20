---
sldb:
  by: agent
  at: '2026-11-20T06:46:34Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta@sha256:dc4b12c8d64ba2ad796b93c678388500d34cf443b5d2d9edfb91c78b3778ac17
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: sldb
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-064420/context-review/task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta/preflight/e30bc820845abee12769571ef5d1155438f28916fb005f24096000f4645aba16/attempt-1
input_sha256: e30bc820845abee12769571ef5d1155438f28916fb005f24096000f4645aba16
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 6cb537863b112df14bde871cd1f0d8836f14fa3236d118b23629ffd78959b486
output_sha256: 3e309601df6a36a0cc674bb4b663727f3ff7fd303dff1b36ab447f54da6d25ad
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. 1) y bundle 6) Tests en tests/store/test_merge_driver_auto.py,
  archivo nuevo. 2) y bundle 5) El hallazgo va en src/sldb/api/stores/store_surroundings.py,
  en una función _merge_driver(store_path) sumada a surroundings_findings, con el
  mismo esquema que _gitignore: alert(''stores/merge_driver_missing'', ''.gitattributes'',
  ''<qué falta>'', ''sldb stores merge-driver --install''). alert es el nivel de aviso
  que ya usa cache_not_ignored. 3) y bundle 1) ''En un repo git'' significa que ''git
  rev-parse --show-toplevel'' corrido desde store_path.parent sale con 0, como hace
  install_merge_driver; worktrees y submódulos cuentan como repo. Si sale distinto
  de 0, o no hay git, no se hace nada. 4) Si git falla al instalar, se imprime una
  línea por stderr (''merge driver no instalado: <motivo>''), el comando sigue y su
  código de salida no cambia. ''Git falla'' es CalledProcessError u OSError de install_merge_driver.
  Bundle 2) Las tres líneas son las de install_merge_driver: ''<rel>/core/store_index.yaml
  merge=sldb'', ''<rel>/core/models/*.yaml merge=sldb'' y ''<rel>/store.yaml merge=sldb'',
  con <rel> la ruta del store relativa a la raíz del repo. Bundle 3) Las claves son
  merge.sldb.name y merge.sldb.driver, con los valores DRIVER_NAME y DRIVER de merge_driver_install.py;
  el chequeo reusa esas constantes y no las duplica. 6) CHANGELOG.md de la raíz, una
  viñeta en la sección sin publicar. 7) y bundle 7) El gate es: TMPDIR=/tmp python
  -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto.py tests/store/test_stores_build.py
  tests/api/test_api_stores.py y tests/test_clean_code_rules.py, más bash tools/check.sh
  --fast. La suite completa la corre integrate. Bundle 8) Commit con trailer ''Task-Id:
  <id de esta tarea>'' y rutas nombradas.'
# ISO 8601 timestamp
created_at: '2026-11-20T06:44:29.112637+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T06:46:13.227595+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-064420/context-review/task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta/preflight/e30bc820845abee12769571ef5d1155438f28916fb005f24096000f4645aba16/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1) y bundle 6) Tests en tests/store/test_merge_driver_auto.py, archivo nuevo. 2) y bundle 5) El hallazgo va en src/sldb/api/stores/store_surroundings.py, en una función _merge_driver(store_path) sumada a surroundings_findings, con el mismo esquema que _gitignore: alert('stores/merge_driver_missing', '.gitattributes', '<qué falta>', 'sldb stores merge-driver --install'). alert es el nivel de aviso que ya usa cache_not_ignored. 3) y bundle 1) 'En un repo git' significa que 'git rev-parse --show-toplevel' corrido desde store_path.parent sale con 0, como hace install_merge_driver; worktrees y submódulos cuentan como repo. Si sale distinto de 0, o no hay git, no se hace nada. 4) Si git falla al instalar, se imprime una línea por stderr ('merge driver no instalado: <motivo>'), el comando sigue y su código de salida no cambia. 'Git falla' es CalledProcessError u OSError de install_merge_driver. Bundle 2) Las tres líneas son las de install_merge_driver: '<rel>/core/store_index.yaml merge=sldb', '<rel>/core/models/*.yaml merge=sldb' y '<rel>/store.yaml merge=sldb', con <rel> la ruta del store relativa a la raíz del repo. Bundle 3) Las claves son merge.sldb.name y merge.sldb.driver, con los valores DRIVER_NAME y DRIVER de merge_driver_install.py; el chequeo reusa esas constantes y no las duplica. 6) CHANGELOG.md de la raíz, una viñeta en la sección sin publicar. 7) y bundle 7) El gate es: TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto.py tests/store/test_stores_build.py tests/api/test_api_stores.py y tests/test_clean_code_rules.py, más bash tools/check.sh --fast. La suite completa la corre integrate. Bundle 8) Commit con trailer 'Task-Id: <id de esta tarea>' y rutas nombradas.
