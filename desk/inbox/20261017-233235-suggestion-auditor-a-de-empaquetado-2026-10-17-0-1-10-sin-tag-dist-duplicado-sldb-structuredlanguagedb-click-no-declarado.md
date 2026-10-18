---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-17T23:32:35'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Auditoría de empaquetado 2026-10-17: 0.1.10 sin tag, dist duplicado sldb/structuredLanguageDB, click no declarado

_Describe the incoming message with enough evidence to triage._

Auditoría read-only de empaquetado (2026-10-17). Hallazgos en sldb:
1. pyproject.toml:3 = 0.1.10 (HEAD 546a726 'release: 0.1.10') sin tag v0.1.10; publish.yml solo dispara con tags v*, así que 0.1.10 no está publicado. Último tag de versión: v0.1.9 (git describe v0.1.9-11-g546a726).
2. Entorno base (anaconda py3.13) tiene DOS dists editables sobre sldb/src: structuredLanguageDB 0.1.9 y un sldb 0.1.0 parásito (__editable__.sldb-0.1.0.pth). Ninguno está en 0.1.10.
3. src/sldb/store/export.py:99 usa version("sldb") (nombre de dist equivocado); hoy devuelve 0.1.0 del dist parásito y si no existiera cae al fallback hardcodeado '0.1.0' (:101). Termina en producer.version del export.
4. sldb/.venv tiene sldb 0.1.0 editable apuntando a /home/jp/proyectos/hum-ecosystem/tools/sldb (otro proyecto); no tiene structuredLanguageDB ni click.
5. click importado en src/sldb/selfdoc/click_scanner.py:8 y no declarado en pyproject.toml:21-29 (módulo no alcanzable desde otros imports).
6. src/sldb/examples/pandoc_cv/ (cv_model.py, cv.input.md) sin __init__.py ni package-data -> fuera de la rueda. cli/commands/help_texts.json no cubierto por pyproject.toml:53-56 (nada lo lee).
7. dist/sldb-0.1.0-py3-none-any.whl (2026-07-26) es el único artefacto: nombre de dist viejo, 115/611 módulos, contiene nldb/. build/lib y src/sldb.egg-info (0.1.0) igual de desfasados.
8. sldb/kgdb/ no es paquete (solo relation_types/*.md); el kgdb importable es kgdb 0.1.0 instalado desde git jpcosec/kgdb@1247139, no index.
CI: ci.yml verde en la última corrida (2026-10-17 15:28Z).
