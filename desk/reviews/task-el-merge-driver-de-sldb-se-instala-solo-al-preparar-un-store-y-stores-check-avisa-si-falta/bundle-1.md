---
sldb:
  by: agent
  at: '2026-11-20T06:47:04Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261120-064456/context-review/task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta/bundle/c55e67432bb131a7479789109090fa545b6f297dfd1390ce34ea9b982c7f366e/attempt-1
input_sha256: c55e67432bb131a7479789109090fa545b6f297dfd1390ce34ea9b982c7f366e
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 96a62fbe219ee1d090535cc9cc5654d6e77caa9986282fc3e21e9215f4d53966
output_sha256: ffc831ece74859372ed5a110940c17efef93aceffda7f8c47c14674252e0b882
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
created_at: '2026-11-20T06:45:13.930145+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T06:46:42.890642+00:00'
disposed_by: sldb
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-064456/context-review/task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta/bundle/c55e67432bb131a7479789109090fa545b6f297dfd1390ce34ea9b982c7f366e/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1) y bundle 6) Tests en tests/store/test_merge_driver_auto.py, archivo nuevo. 2) y bundle 5) El hallazgo va en src/sldb/api/stores/store_surroundings.py, en una función _merge_driver(store_path) sumada a surroundings_findings, con el mismo esquema que _gitignore: alert('stores/merge_driver_missing', '.gitattributes', '<qué falta>', 'sldb stores merge-driver --install'). alert es el nivel de aviso que ya usa cache_not_ignored. 3) y bundle 1) 'En un repo git' significa que 'git rev-parse --show-toplevel' corrido desde store_path.parent sale con 0, como hace install_merge_driver; worktrees y submódulos cuentan como repo. Si sale distinto de 0, o no hay git, no se hace nada. 4) Si git falla al instalar, se imprime una línea por stderr ('merge driver no instalado: <motivo>'), el comando sigue y su código de salida no cambia. 'Git falla' es CalledProcessError u OSError de install_merge_driver. Bundle 2) Las tres líneas son las de install_merge_driver: '<rel>/core/store_index.yaml merge=sldb', '<rel>/core/models/*.yaml merge=sldb' y '<rel>/store.yaml merge=sldb', con <rel> la ruta del store relativa a la raíz del repo. Bundle 3) Las claves son merge.sldb.name y merge.sldb.driver, con los valores DRIVER_NAME y DRIVER de merge_driver_install.py; el chequeo reusa esas constantes y no las duplica. 6) CHANGELOG.md de la raíz, una viñeta en la sección sin publicar. 7) y bundle 7) El gate es: TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto.py tests/store/test_stores_build.py tests/api/test_api_stores.py y tests/test_clean_code_rules.py, más bash tools/check.sh --fast. La suite completa la corre integrate. Bundle 8) Commit con trailer 'Task-Id: <id de esta tarea>' y rutas nombradas.
