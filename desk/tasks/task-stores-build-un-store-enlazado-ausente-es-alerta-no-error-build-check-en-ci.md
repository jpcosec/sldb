---
sldb:
  by: agent
  at: '2026-11-10T04:50:17Z'
  authority: generated
  via: save_document_payload
id: task-stores-build-un-store-enlazado-ausente-es-alerta-no-error-build-check-en-ci
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/stores/apply_declaration.py
- src/sldb/api/stores/build_store.py
- src/sldb/cli/commands/
- tests/store/test_stores_build.py
- tests/api/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-stores-build-check-falla-con-un-store-enlazado-ausente-build-no.md
---

# stores build: un store enlazado ausente es alerta, no error (build --check en CI)

## Rationale

_Explain why this task exists or the business driver behind it._

CI de deskops rojo en sldb stores build --check porque el runner no tiene los repos hermanos que .sldb/store.yaml enlaza (desde 1b89114c). Decisión revisable del coordinador de proyecto (b): un link ausente es alerta, no error.

## Goal

_Describe the concrete result this task must produce._

build y build --check toleran un store enlazado ausente, con una alerta que nombra el link y la ruta; el resto de los errores de link no cambia.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/apply_declaration.py, build_store.py, src/sldb/cli/commands/stores_build*.py, tests/api/ y CHANGELOG.md. Fuera: link_store para links presentes, deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (sldb origin/main): src/sldb/api/stores/apply_declaration.py:24 apply_links llama a link_store por cada link declarado que no está en el índice o que cambió de ruta. link_store (link_store.py:50, _check_other_exists) lanza SLDBStoreError «No store at <ruta>» si el destino no tiene store. build --check (src/sldb/cli/commands/stores_build_check.py) reconstruye una copia sin .sldb/core, así que siempre llama a apply_links, y en un CI sin los repos hermanos falla. stores build sobre el store local no falla porque el store_index versionado ya trae los links.

DECISIÓN (coordinador de proyecto, 2026-11-10, revisable): un store enlazado ausente es alerta, no error.
s1: apply_links salta el link cuyo destino no tiene store (store_exists sobre root/path) y lo devuelve aparte. build_store (src/sldb/api/stores/build_store.py) lo reporta en una clave nueva, links_missing (lista de {name, path}), tanto en el build como en el plan (apply=False).
s2: build --check no falla por eso: agrega una alerta por link ausente, con código build/link-missing, subject = nombre del link y what = la ruta declarada y que el store no existe, y la reporta como las demás alertas (alert_sink). ok no cambia por los links ausentes.
s3: sldb stores build (sin --check) imprime la misma alerta en su resumen.
s4: un link cuyo destino existe pero no es un store válido, o que apunta al propio store, sigue siendo error (link_store sin cambios).
s5 (tests): un test nuevo en tests/api/ (por ejemplo test_build_store_missing_link.py). Store con un link declarado a una ruta sin store: build_store no lanza, reporta links_missing con nombre y ruta, y el índice no queda con el link. check_build da ok y una alerta build/link-missing que nombra link y ruta. Con el link presente, todo queda igual que hoy. Además, de a uno: los tests existentes de stores build y build --check (grep stores_build en tests/) y tests/test_clean_code_rules.py.
s6 (prueba del consumidor): sobre un clon limpio de deskops wt/main-en-verde-2 en /dev/shm, sin repos hermanos, con PYTHONPATH a esta rama de sldb, sldb stores build --check --store .sldb termina con exit 0 y con las 4 alertas build/link-missing.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-10), alineadas con lo implementado en wt/link-missing-alert 40221f7a:
b1 (store_exists): es la existente, sldb.store.layout.store_exists(path), la misma que usa link_store en _check_other_exists. Un destino sin store es exactamente lo que hoy hace fallar link_store con «No store at».
b2 (ausente contra inválido): apply_links solo salta lo que store_exists da por ausente. Lo demás pasa por link_store como hoy: el link al propio store (_check_not_self) y el alias inválido (_check_link_name) siguen siendo error.
b3 (forma de links_missing): una lista de {"name": str, "path": str} con la ruta tal como la declara store.yaml. Está en el reporte con apply=True y con apply=False (va en _pending), entre «missing» y «scaffold». La línea «built:» del resumen no la cuenta, así que la salida normal no cambia.
b4 (alerta): severidad alert (sldb.core.finding.alert), código build/link-missing, subject el nombre del link, what «declared link path <ruta> has no store; the build goes on without it» y fix «check out the linked repository next to this one». build --check la agrega a report["alerts"], que _report_alerts ya emite por alert_sink. build la imprime como línea «alert: [build/link-missing] ...» en su resumen. Helper en src/sldb/cli/commands/stores_link_alert.py.
b5 (los 4 links): .sldb/store.yaml de deskops declara exactamente sldb, spec2viz, pron y scion (desde 1b89114c). En un clon sin hermanos, los 4 están ausentes.
b6 (clon): git clone del repo de deskops, git fetch del branch wt/main-en-verde-2 y checkout de 7bd88006 en /dev/shm/mv2-clone, sin repos hermanos al lado; sldb con PYTHONPATH=<esta rama>/src.
b7 (tests existentes): tests/store/test_stores_build.py (actualiza REPORT_KEYS y dos expectativas exactas del reporte con links_missing: [], y agrega los dos tests nuevos), tests/api/test_api_stores.py y tests/test_clean_code_rules.py. Por eso tests/store/ entra en files.

## Validation

_List the checks required before this task can close._

- Test nuevo de s5
- Tests existentes de stores build/build --check y test_clean_code_rules de a uno
- Clon limpio de deskops sin hermanos: sldb stores build --check exit 0 con 4 alertas (s6)

## Done When

_Name the observable condition that makes the task complete._

build y build --check pasan con un link ausente y emiten la alerta build/link-missing con nombre y ruta; tests de s5 verdes; prueba del consumidor de s6 con exit 0.
