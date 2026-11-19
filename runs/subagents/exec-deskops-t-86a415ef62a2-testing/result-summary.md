PASA

# Tester deskops-t-86a415ef62a2: resultado

Task: `task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar`
Commit revisado: `1398def0224c0185922ad3709050c1966fa5aed3` — `Fix accionable en los hallazgos builtin tag_namespace`
Archivos del commit: `src/sldb/api/rules/builtin_tag_findings.py`, `tests/api/test_tags.py`, `CHANGELOG.md`.

## Veredicto

**PASA.** Los hallazgos de `builtin:tag_namespace:<name>` ya no salen con `fix` vacío. El fix cubre los dos desvíos que produce la regla:

- Namespace no declarado: nombra el namespace y la clave exacta a declarar en `.sldb/store.yaml` (`tag_namespaces`, `- name: <name>`), y lista los namespaces declarados como alternativa.
- Namespace declarado con anclas faltantes: nombra el modelo y el campo que anclan (`CrossroadDoc.path`, `Anchor.tag`, etc.) y los tags que faltan por anclar.

No se cambió qué detecta la regla. Es la única familia builtin de tags (`PREFIX = "builtin:tag_namespace:"`); no hay otra regla builtin de tags con `fix` vacío que completar.

## Validación ejecutada

`/tmp/ws-venv` no existe en este entorno; se usó el venv del proyecto (`/workspace/sldb/.venv/bin/python`, que es el mismo árbol que `/mnt/ssd/proyectos/SLDB_1/sldb`). No se corrió la suite completa.

| Comando | rc | Resultado |
|---|---|---|
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/api/test_tags.py` | 0 | 37 passed |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/api/test_rules_evaluation.py` | 0 | 12 passed |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q tests/test_clean_code_rules.py` | 0 | 1212 passed |
| `PATH=/workspace/sldb/.venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast` | 0 | todas las puertas PASAN |

No existe `tests/test_builtin_tag_findings.py` ni otro `tests/test_<modulo>.py` para el módulo tocado; su cobertura está en `tests/api/test_tags.py`. El test nuevo (`test_an_undeclared_namespace_finding_names_the_namespace_to_declare`) y el assert actualizado de `test_tags_check_finds_a_document_created_without_its_anchor` cubren las dos ramas del fix.

## Comprobación contra el caso reportado (sldb-ui)

Se ejecutó `sldb stores check --store /workspace/UIs/sldb-ui/.sldb --format json --pythonpath /workspace/UIs/sldb-ui`. El store sigue teniendo los 5 errores `rules/builtin:tag_namespace:domain` reportados, y los 5 traen `fix` no vacío; por ejemplo:

- `domain:sldb` → `Create a CrossroadDoc document whose `path` anchors it for each of: domain:sldb; or change the tags domain:sldb of AtomDoc:atom-quien-usa-sldb-ui to anchored ones.`
- `domain:sldb-ui, domain:sldb` → nombra ambos tags faltantes y el mismo modelo/campo.

El rc del comando es 1 porque el store tiene errores preexistentes (190 errores y 216 alertas en total), no por el cambio; ningún hallazgo `tag_namespace` quedó con `fix` vacío.

## Observaciones no bloqueantes

- El fix de anclas faltantes no enumera todos los tags ya anclados del namespace; indica el modelo/campo y los tags que faltan, que es la acción concreta pedida por el Goal.
- El `CHANGELOG.md` documenta el cambio y remite al test correcto.
