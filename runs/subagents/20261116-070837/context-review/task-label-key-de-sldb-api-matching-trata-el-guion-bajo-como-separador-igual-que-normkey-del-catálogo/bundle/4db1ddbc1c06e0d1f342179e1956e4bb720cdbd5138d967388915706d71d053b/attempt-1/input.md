FILE:desk/tasks/task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo.md
---
sldb:
  by: agent
  at: '2026-11-16T05:31:04Z'
  authority: generated
  via: save_document_payload
id: task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-214942-suggestion-ir13b-label-key-no-separa-y-normkey-del-cat-logo-s-matching-label-key-underscore.md
depends_on: []
pills: []
files:
- src/sldb/api/matching/atom_keys.py
- tests/matching/test_matching_explicit.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# label_key de sldb.api.matching trata el guion bajo como separador, igual que normKey del catálogo

## Rationale

_Explain why this task exists or the business driver behind it._

sldb.api.matching.label_key (src/sldb/api/matching/atom_keys.py) normaliza con re.sub(r"[^\w\s]+", " ", ...); \w incluye "_", así que label_key("post_published") da "post_published". normKey de la plantilla JS del catálogo usa /[^\p{L}\p{N}\s]+/gu y da "post published". Un elemento sin label se dibuja con su id; si el id lleva "_", el mapa de átomos explícitos queda con una clave que el navegador nunca busca y el átomo no se encuentra. Lo reportó IR13b. Origen: desk/inbox/20261115-214942-suggestion-ir13b-label-key-no-separa-y-normkey-del-cat-logo-s-matching-label-key-underscore.md.

## Goal

_Describe the concrete result this task must produce._

label_key("post_published") devuelve "post published" y, en general, label_key produce la misma clave que normKey para letras, dígitos, espacios, guiones bajos y puntuación.

## Scope

_State what is in scope and what is out of scope._

Entra: cambiar la expresión de label_key en src/sldb/api/matching/atom_keys.py para que "_" cuente como separador con exactamente re.sub(r"[\W_]+", " ", texto), conservando el resto del pipeline (minúsculas, espacios colapsados, strip). Tests nuevos en tests/matching/test_matching_explicit.py: uno con "post_published" -> "post published" y test_label_key_matches_normkey parametrizado con estos pares exactos: ("post_published", "post published"), ("Año_2024", "año 2024"), ("a-b_c.d", "a b c d"), ("  x__y  ", "x y"). Entrada en CHANGELOG.md. No entra: cambiar normalize_key ni _title_aliases del mismo archivo, tocar la plantilla JS del catálogo (vive en el repo IR), cambiar el emparejamiento difuso, ni la tarea task-el-emparejamiento-de-átomos-de-sldb-api-matching-pasa-a-su-propio-eje-y-recuperacion-vuelve-a-ser-un.

Precisiones (preflight-1): la equivalencia con normKey se exige solo para los cuatro pares listados y para letras, dígitos, espacios, guion bajo y puntuación ASCII; símbolos y emoji quedan fuera. Si algún golden de tests/matching/ cambia, se compara su diff: si las únicas diferencias son "_" convertido en espacio, se actualiza el golden; si hay cualquier otra diferencia, no se toca y la tarea se detiene con el diff en el informe.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/matching/atom_keys.py (label_key, línea 14-16) y sus usos con grep "label_key" en src/sldb. 2) Cambiar el regex a [\W_]+. 3) Agregar los tests en tests/matching/test_matching_explicit.py. 4) Correr tests/matching/ completo para ver que ningún golden de emparejamiento dependía del guion bajo; si alguno cambia, ajustar el golden solo si el cambio es exactamente la separación de "_".

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/

## Done When

_Name the observable condition that makes the task complete._

TMPDIR=/dev/shm pytest -q tests/matching/ pasa, incluido el test nuevo label_key("post_published") == "post published"; CHANGELOG.md tiene la entrada; commit con esos archivos.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:src/sldb/api/matching/atom_keys.py
"""Claves y alias de un átomo: `label_key` (la de `normKey` del template del catálogo),
`normalize_key` y los alias por título y etiquetas.

Migrado de `spec2viz.deskops` (`label_key`, `_normalize_key`, `_alias_candidates`). No se
sustituye por `normalize` de difflib_matcher: ese quita acentos y deja la puntuación, y
`label_key` debe seguir coincidiendo con `normKey`.
"""

from __future__ import annotations

import re


def label_key(value: str) -> str:
    """Misma normalizacion que `normKey` del template (minusculas, sin puntuacion)."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]+", " ", (value or "").strip().lower())).strip()


def normalize_key(value: str) -> str:
    """La clave de un título: minúsculas, puntuación a espacios, espacios colapsados."""
    value = (value or "").strip().lower()
    value = re.sub(r"[^\w\s]+", " ", value)
    return re.sub(r"\s+", " ", value)


def _title_aliases(title: str) -> list[str]:
    """El título normalizado, sus palabras de 3+ letras y cada par de palabras contiguas."""
    normalized_title = normalize_key(title)
    if not normalized_title:
        return []
    words = [word for word in normalized_title.split() if len(word) >= 3]
    return [normalized_title, *words, *[f"{a} {b}" for a, b in zip(words, words[1:])]]


def _tag_aliases(tags: list[str]) -> list[str]:
    """Por cada etiqueta `namespace:valor`, el valor normalizado y sus palabras de 3+ letras."""
    aliases: list[str] = []
    for tag in tags or []:
        if ":" not in tag:
            continue
        _namespace, value = tag.split(":", 1)
        normalized_value = normalize_key(value.replace("-", " ").replace("_", " "))
        if normalized_value:
            aliases.append(normalized_value)
            aliases.extend([word for word in normalized_value.split() if len(word) >= 3])
    return aliases


def alias_candidates(title: str, tags: list[str]) -> list[str]:
    """Los alias de un átomo, sin repetidos y en orden: los del título y luego los de las etiquetas."""
    seen: set[str] = set()
    result: list[str] = []
    for alias in [*_title_aliases(title), *_tag_aliases(tags)]:
        if alias and alias not in seen:
            seen.add(alias)
            result.append(alias)
    return result

FILE:tests/matching/test_matching_explicit.py
"""`atoms: [id]` por elemento del spec -> vinculacion explicita, alias y filtro por tags.

Portado de spec2viz (`tests/test_explicit_atoms.py`, `tests/test_atoms_matching.py` y los de
`parse_atoms` de `tests/test_deskops.py`) contra las funciones puras de `sldb.api.matching`: la
vista es un `SpecView` con el spec ya cargado y los atomos salen de `--atoms-dir` (sin store), en
vez de construir el HTML del catalogo.
"""
import json
from pathlib import Path

import pytest
import yaml

from sldb.api.matching import (
    SpecView, UnknownAtomError, alias_candidates, build_explicit_atoms, filter_atoms_payload, label_key, parse_atoms, raw_atoms_by_view,
)


def _atom(d: Path, atom_id: str, title: str, q="what"):
    (d / f"{atom_id}.md").write_text(
        f"---\ntitle: {title}\nfive_wh_one_plus: {q}\nid: {atom_id}\n---\nCuerpo de {atom_id}.\n", encoding="utf-8"
    )


def _project(tmp_path, state_atoms_a, state_atoms_b):
    atoms = tmp_path / "atoms"
    atoms.mkdir()
    _atom(atoms, "atom-uno", "Uno")
    _atom(atoms, "atom-dos", "Dos", "why")
    _atom(atoms, "atom-ruido", "Otro tema")
    spec = {
        "id": "ciclo", "title": "Ciclo", "type": "state", "version": "1.0",
        "data": {
            "entity": "OC", "initial": "nueva",
            "states": [
                {"id": "nueva", "label": "4 Nueva", **({"atoms": state_atoms_a} if state_atoms_a is not None else {})},
                {"id": "cerrada", "label": "Cerrada", **({"atoms": state_atoms_b} if state_atoms_b is not None else {})},
            ],
            "transitions": [{"from": "nueva", "to": "cerrada", "on": "cierra"}],
        },
    }
    (tmp_path / "ciclo.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    return atoms


def _build(tmp_path, atoms, strict=False):
    """Lo que `catalog build --atoms-dir` resolvia: atomos de la vista y su resolucion explicita."""
    spec = yaml.safe_load((tmp_path / "ciclo.yml").read_text(encoding="utf-8"))
    views = [SpecView(key="v1", id="v1", specs=[spec], source=str(tmp_path / "f.mmd"), base_dir=str(tmp_path))]
    raw, _ = raw_atoms_by_view(views, atoms)
    return build_explicit_atoms(views, raw, strict=strict)


def test_build_exposes_explicit_map_by_label_and_id(tmp_path):
    atoms = _project(tmp_path, ["atom-uno", "atom-dos"], None)
    explicit, _complete, findings, _linked = _build(tmp_path, atoms)
    assert findings == []
    view = explicit["v1"]
    assert [a["id"] for a in view["4 nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert [a["id"] for a in view["nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert "cerrada" not in view


def test_unknown_atom_is_warning_unless_strict(tmp_path):
    atoms = _project(tmp_path, ["atom-uno", "no-existe"], None)
    explicit, _complete, findings, _linked = _build(tmp_path, atoms)
    assert [(f.level, f.code) for f in findings] == [("warning", "matching/unknown-atom"), ("warning", "matching/unknown-atom")]
    assert all("no-existe" in f.what for f in findings) and findings[0].fix == "crear el átomo o corregir el id"
    assert {f.subject for f in findings} == {"v1#4 nueva", "v1#nueva"}
    assert [a["id"] for a in explicit["v1"]["4 nueva"]["list"]] == ["atom-uno"]
    with pytest.raises(UnknownAtomError) as raised:
        _build(tmp_path, atoms, strict=True)
    assert "no-existe" in str(raised.value)
    assert {f.level for f in raised.value.findings} == {"error"}


def test_fully_explicit_view_embeds_no_fuzzy_payload(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], ["atom-dos"])
    explicit, complete, _findings, _linked = _build(tmp_path, atoms)
    # la vista queda entre las completas: el catalogo no embebe payload difuso para ella
    assert complete == {"v1"}
    bodies = {a["body"] for entry in explicit["v1"].values() for a in entry["list"]}
    assert bodies == {"Cuerpo de atom-uno.", "Cuerpo de atom-dos."}


def test_partially_explicit_view_keeps_fuzzy_payload(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], None)
    _explicit, complete, _findings, _linked = _build(tmp_path, atoms)
    assert "v1" not in complete


def test_atoms_linked_from_explicit_are_embedded_one_level(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], ["atom-dos"])
    (atoms / "atom-uno.md").write_text(
        "---\ntitle: Uno\nfive_wh_one_plus: what\nid: atom-uno\n---\nVer [depende:: [[atom-ruido]]] y [[atom-lejano]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano", "Lejano")
    (atoms / "atom-ruido.md").write_text(
        "---\ntitle: Otro tema\nfive_wh_one_plus: what\nid: atom-ruido\n---\nSigue [[atom-lejano2]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano2", "Nivel dos")
    _explicit, _complete, findings, linked = _build(tmp_path, atoms)
    assert findings == []
    assert set(linked) == {"atom-ruido", "atom-lejano"}  # un nivel: no atom-lejano2


def _two_atoms(tmp_path):
    d = tmp_path / "atoms"
    d.mkdir()
    for i, (title, tags) in enumerate([("Uno", ["dominio:oc"]), ("Dos", ["dominio:stock"])]):
        (d / f"a{i}.md").write_text(
            f"---\ntitle: {title}\nfive_wh_one_plus: what\nid: a{i}\ntags: {json.dumps(tags)}\n---\nCuerpo {i}.\n",
            encoding="utf-8",
        )
    return d


def test_filter_atoms_payload_by_full_tag_or_value(tmp_path):
    payload = json.loads(parse_atoms(_two_atoms(tmp_path)))
    assert set(filter_atoms_payload(payload, ["dominio:oc"])) == {"uno"}
    assert set(filter_atoms_payload(payload, ["stock"])) == {"dos"}
    assert set(filter_atoms_payload(payload, None)) == {"uno", "dos"}
    assert filter_atoms_payload(payload, ["nada"]) == {}


def test_parse_atoms_handles_missing_dir(tmp_path):
    assert parse_atoms(tmp_path / "missing") == "{}"


def test_parse_atoms_builds_index_and_skips_bad_files(tmp_path):
    atoms_dir = tmp_path / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "good.md").write_text("---\ntitle: Architecture\nfive_wh_one_plus: what\nid: atom-1\n---\nBody text.\n", encoding="utf-8")
    (atoms_dir / "bad.md").write_text("---\n: bad yaml\n---\nBroken.\n", encoding="utf-8")
    findings = []
    payload = json.loads(parse_atoms(atoms_dir, findings))
    assert payload["architecture"]["title"] == "Architecture"
    assert "architecture" in payload["architecture"]["aliases"]
    assert payload["architecture"]["atoms"]["what"]["id"] == "atom-1"
    assert payload["architecture"]["atoms"]["what"]["body"] == "Body text."
    assert [f.code for f in findings] == ["matching/atom-parse-failed"]
    assert "Failed to parse atom" in findings[0].what


def test_aliases_by_title_and_tags():
    aliases = alias_candidates("Evaluación de órdenes", ["dominio:orden-compra", "sin-namespace"])
    assert aliases == [
        "evaluación de órdenes", "evaluación", "órdenes", "evaluación órdenes", "orden compra", "orden", "compra",
    ]


def test_label_key_matches_template_normkey():
    # normKey: minusculas, puntuacion a espacio, espacios colapsados; los acentos se conservan
    assert label_key("  HOMOLOGACIÓN de producto (R1) ") == "homologación de producto r1"
    assert label_key("4 Nueva") == "4 nueva"

FILE:instruccion
Cold-bundle de la tarea task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/matching/

