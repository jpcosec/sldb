FILE:desk/tasks/task-go07-anclas-a-documentos-con-hash-de-contrato.md
---
id: task-go07-anclas-a-documentos-con-hash-de-contrato
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
- src/sldb/models/structured_doc.py
- src/sldb/models/doc_anchor_value.py
- src/sldb/models/provenance.py
- src/sldb/store/model_contract.py
- src/sldb/store/edge_index/doc_contribution.py
- src/sldb/store/edge_index/compose.py
- src/sldb/store/edge_index/payload_projection.py
- src/sldb/api/documents/payload_save_steps.py
- src/sldb/api/anchors/__init__.py
- src/sldb/api/anchors/check_doc_anchors.py
- src/sldb/api/__init__.py
- src/sldb/cli/commands/anchors.py
- docs/architecture/anchoring.md
- CHANGELOG.md
- tests/api/test_doc_anchors.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO07: Anclas a documentos con hash de contrato

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO07 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK03. Hoy solo hay anclas de codigo (CodeAnchorDoc); Provenance.from_ acepta doc:<Model:name> pero el verify disenado nunca se implemento (alcance.md). GO07 agrega anclas a documentos pinneadas con el hash de contrato de GO02 y expone su estado al lenguaje de GO05 (alias anchor_state) sin tocar el shard de GO04.

## Goal

_Describe the concrete result this task must produce._

Campos __doc_anchors__ y from: de Provenance con la forma doc:Model:name@sha256:<hash>, validados al escribir y pinneados en el guardado; estados intact/changed/lost; check_doc_anchors(store) -> list[Finding] usado por anchors check; aristas references desde los campos __doc_anchors__; entrada derivada <campo>__anchor_state en la facet payload calculada al leer; docs/architecture/anchoring.md y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: el atributo __doc_anchors__ y su validacion en los modelos, Provenance.from_, el pinneado en payload_save_steps, las aristas references de los campos __doc_anchors__, la entrada derivada <campo>__anchor_state al componer o leer la proyeccion, check_doc_anchors y el comando anchors check, docs/architecture/anchoring.md, CHANGELOG.md, tests. Fuera: el cableado en stores check y la evaluacion incremental (GO08), cambios al lenguaje (GO05 ya define el alias anchor_state), cambios al formato del shard o a EDGE_INDEX_VERSION, reconnected para documentos.

PRINCIPIO DEL DUENO (2026-11-05): invariantes de UN documento = validadores pydantic del modelo; entre documentos = RuleDoc; los tests solo prueban rechazo. Aplicado aqui: (q1) la forma de un valor en un campo __doc_anchors__ y en from: (vacio/null o doc:Model:name[@sha256:<64 hex>]) es un validador pydantic (en el modelo base para los campos que el modelo declara en __doc_anchors__, y en Provenance para from:): escribir un valor malformado levanta el ValidationError del modelo con el campo y el motivo. Lo que depende de otro documento (que el destino exista, su hash actual, el estado intact/changed/lost) NO es validacion del modelo: es el pinneado al guardar y check_doc_anchors. Las invariantes de la definicion del modelo (__doc_anchors__ nombra campos str o list[str]; ningun campo termina en __anchor_state) se comprueban al cargar la definicion, como __indexed__ en GO04 (store/model_contract.py, SLDBModelError). (q2) Los tests de forma invalida prueban rechazo: texto no doc:, @sha256: vacio, hash que no es de 64 hex, tambien en from:; y la definicion de modelo invalida (campo no str/list[str], sufijo reservado).

HEREDADO: (h1) el hash de contrato es contract_hash(modelo, field_hashes) de src/sldb/store/graph/language/contract_hash.py (GO02 seccion 5, GO05 H12). (h2) El alias anchor_state ya existe en el lenguaje (GO05 p10): al atravesar el campo F lee F__anchor_state del payload del documento origen (lista alineada para list[str]); GO07 solo produce esa entrada. (h3) En el codigo actual Provenance.from_ es list[str] (alias from), no un escalar como dice el contrato: cada elemento que empieza por doc: es un ancla independiente; los que no (code:...) no se tocan. (h4) Los valores intact/changed/lost reutilizan el vocabulario de AnchorState (src/sldb/models/anchor_state.py) de las anclas de codigo; changed y lost son alertas.

PRECISIONES (preflight de GO07, 2026-11-06):
p1 (from: es lista): rige el codigo: Provenance.from_ sigue siendo list[str] (alias from); no hay migracion. Cada elemento se valida y trata por separado; donde el contrato dice "un from:" se lee "un elemento de from:".
p2 (que se rechaza): en from:, un elemento que no empieza por doc: (code:..., otros) se acepta como hoy y no se toca; un elemento que empieza por doc: debe tener la forma doc:Model:name[@sha256:<64 hex>] y si no la tiene (incluido @sha256: vacio o malformado) es error de validacion. En un campo __doc_anchors__, todo valor no vacio/null debe tener esa forma; cualquier otro texto es error.
p3 (Finding): check_doc_anchors devuelve sldb.core.finding.Finding (level, code, subject, what, fix, document) con level "alert". Codes: anchors/doc_changed y anchors/doc_lost para campos __doc_anchors__; anchors/provenance_changed y anchors/provenance_lost para elementos de from:. subject = Model:name del documento que contiene el ancla; what nombra el campo (o from), el destino y el estado; fix = ""; document = ruta del contenedor relativa a la raiz. Un ancla intact no emite Finding.
p4 (from: sin aristas): solo los campos __doc_anchors__ generan aristas references; from: no genera aristas (su estado lo reporta anchors check).
p5 (destino creado despues): un ancla guardada sin hash es lost mientras no tenga hash, aunque el destino se cree despues; la siguiente escritura del documento contenedor la pinnea. No hay reescritura automatica ni otro estado.
p6 (listas): en un campo list[str], cada elemento no vacio genera su propia arista references; <campo>__anchor_state es una lista alineada por indice con el valor del campo; un elemento vacio o null no genera arista y su posicion en __anchor_state es null.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO07 scope): Un ancla doc: es el valor de un campo: la forma doc:Model:name@sha256:<hash de contrato visto>. Los campos que llevan anclas son los que el modelo declara en el atributo de clase __doc_anchors__ (lista de nombres de campos de str o de list[str]) y el from: de Provenance, que pasa a admitir la forma con hash. Persistencia: en el propio documento, en el texto del campo; nada aparte. Pinneado: en los pasos de guardado de payload, un valor doc:Model:name sin @sha256 en un campo __doc_anchors__ o en from: se completa con el hash de contrato actual del destino (calculado como define GO02); si el destino no existe, se guarda sin hash. Estados: intact (hash igual), changed (hash distinto), lost (sin destino, o con destino pero sin hash); un ancla sin hash cuyo destino ya existe se pinnea en la siguiente escritura del documento que la contiene. GO07 expone check_doc_anchors(store) → list[Finding] y extiende el comando anchors check (src/sldb/cli/commands/anchors.py) para usarla; el cableado en stores check lo hace GO08 (dueño de api/stores); no hay reconnected para documentos. Severidad: changed y lost son alertas, nunca error, como las anclas de código. Un campo __doc_anchors__ solo admite vacío/null o valores con forma doc:Model:name[@sha256:<hash>]; otro texto es error de validación al escribir; <hash> son 64 caracteres hexadecimales y un @sha256: vacío o malformado es error, también en from:. from: de Provenance es escalar (str); un from: que no empieza por doc: (p. ej. code:) no es ancla de documento y este nodo no lo toca. Todo campo __doc_anchors__ se trata además como campo de __references__: genera aristas references con el nombre del campo, resolviendo doc:Model:name sin el sufijo @sha256; así ^subject existe en el grafo. El verify que provenance.md diseñó y nunca se implementó (alcance.md) es el mismo mecanismo aplicado a from:: Finding alert con code anchors/provenance_changed (destino con contrato distinto) o anchors/provenance_lost (sin destino o sin hash), emitido por anchors check por el canal de alertas; un from: sin hash se pinnea en la siguiente escritura igual que cualquier ancla. anchor_state se expone sin tocar el lenguaje ni el shard: al componer o leer la proyección, GO07 agrega a la facet payload, por cada campo __doc_anchors__, una entrada derivada <campo>__anchor_state (escalar para un campo str; lista alineada para list[str]) calculada en ese momento comparando el hash visto en el valor del campo con el hash de contrato actual del destino, que se calcula desde los field_hashes del destino ya presentes en el índice (GO04); no se persiste en el shard, así que editar el destino no exige invalidar al contenedor y EDGE_INDEX_VERSION no cambia; el sufijo __anchor_state queda reservado: un modelo que declare un campo con ese sufijo es error al cargar la definición del modelo. El lenguaje de GO05 la lee como cualquier campo y su alias genérico anchor_state (definido en GO05) la expone al atravesar el campo; ^subject es el recorrido inverso de las aristas references que el campo subject genera. Varias anclas en un campo lista = un estado por elemento. ACEPTACION: Un documento A con campo subject en __doc_anchors__ se guarda con doc:TaskDoc:b y queda pinneado con el hash de B; editar un campo del __contract__ de B deja el ancla changed; editar un campo fuera del contrato la deja intact; borrar B la deja lost; anchors check lo reporta como alertas (stores check lo hará vía GO08); con un modelo Review (campos subject en __doc_anchors__ y verdict) y una Task B como sujeto, la regla any(^subject: anchor_state = "intact" and verdict = "accepted") evalúa true cuando existe una Review con subject pinneado a B intacto y verdict accepted, y false sin Review, con verdict distinto o con el ancla changed; un valor no doc: en subject es rechazado al escribir; un documento con from: doc:B emite provenance_changed tras editar el contrato de B; docs/architecture/anchoring.md documenta __doc_anchors__, la forma con hash, el pinneado y la ausencia de reconnected; CHANGELOG. OUTPUT_SCOPE: src/sldb/api/anchors/, src/sldb/cli/commands/anchors.py, src/sldb/models/provenance.py, src/sldb/models/ (atributo __doc_anchors__ en el modelo base), src/sldb/api/documents/payload_save_steps.py (pinneado), src/sldb/store/edge_index/ (entrada derivada <campo>__anchor_state en la proyección), docs/architecture/anchoring.md, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla (anchor_state se calcula al leer); regla 6: ante un contrato ausente registrar la hipotesis, no inventar API). Lenguaje: docs/architecture/rules-language.md; proyeccion y costura: docs/architecture/graph-backend.md; reglas: docs/architecture/rules.md (GO06).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/api/test_doc_anchors.py sin fallos ni saltados
- A con subject en __doc_anchors__ guardado con doc:TaskDoc:b queda pinneado con el hash de B; editar un campo del __contract__ de B -> changed; editar fuera del contrato -> intact; borrar B -> lost; anchors check lo reporta como alertas
- modelo Review (subject en __doc_anchors__, verdict) y Task B: any(^subject: anchor_state = "intact" and verdict = "accepted") true con Review intacta y accepted; false sin Review, con verdict distinto o con el ancla changed
- valor no doc: en subject rechazado al escribir; un test de rechazo por forma invalida (tambien en from:) y por definicion de modelo invalida
- from: doc:B emite anchors/provenance_changed tras editar el contrato de B
- tests existentes de anclas de codigo, provenance, proyeccion (test_payload_projection) y lenguaje (test_predicate_language, spec GO02) sin cambios
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO07 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

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

FILE:src/sldb/models/structured_doc.py
from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel

class StructuredNLDoc(BaseModel):
    __authority__: str = "generated"
    __semantics__: dict[str, Any] = {"representation": ["markdown"], "source": ["document", "markdown"]}
    __template__: str = ""
    __compositions__: dict[str, dict[str, Any]] = {}
    __containment__: dict[str, list[str]] = {}
    __references__: list[str] = []

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if cls is StructuredNLDoc: return
        missing = sorted(n for n, i in cls.model_fields.items() if not i.description or not i.description.strip())
        if missing: raise TypeError(f"{cls.__name__} fields must define a non-empty description: {', '.join(missing)}")

    def render_payload(self, recorder: Any = None, ref_root: Path | None = None, field_resolver: Any = None) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        for name in self.__compositions__:
            payload[name] = self.compose_field(name, recorder=recorder, ref_root=ref_root, field_resolver=field_resolver)
        return payload

    def compose_field(self, name: str, recorder: Any = None, ref_root: Path | None = None, field_resolver: Any = None) -> str:
        """The composed field's text. `ref_root` resolves relative refs; the CWD is the fallback."""
        spec = self.__compositions__.get(name, {})
        refs = getattr(self, spec.get("source_field") or "", []) or []
        if not spec.get("source_field") or not isinstance(refs, list): return ""
        if spec.get("ref") == "field":
            return self._compose_by_field(refs, spec, recorder, field_resolver)
        return self._compose_by_doc(refs, spec, recorder, ref_root)

    def _compose_by_field(self, refs: list[Any], spec: dict[str, Any], rec: Any, res: Any) -> str:
        if res is None: return ""
        rendered = [t for i, r in enumerate(refs) if (t := self._render_field_ref(r, i, spec, rec, res))]
        return spec.get("separator", "\n").join(rendered)

    def _render_field_ref(self, raw_ref: Any, idx: int, spec: dict[str, Any], rec: Any, res: Any) -> str:
        ref_str = str(raw_ref).strip()
        try: resolved = res.resolve(ref_str)
        except Exception: return ""
        if (val := resolved.get("value")) is None: return ""
        text = _format_field_val(val, resolved.get("payload") or {}, spec.get("template", "{value}"))
        return _wrap_field_piece(rec, text, resolved, idx, ref_str) if rec is not None else text

    def _compose_by_doc(self, refs: list[Any], spec: dict[str, Any], rec: Any, ref_root: Path | None) -> str:
        if (model_type := self._resolve_composition_model(spec.get("model"))) is None: return ""
        rendered = [t for i, r in enumerate(refs) if (t := self._render_doc_ref(r, i, spec, model_type, rec, ref_root))]
        return spec.get("separator", "\n").join(rendered)

    def _render_doc_ref(self, raw: Any, idx: int, spec: dict[str, Any], m_type: type, rec: Any, root: Path | None) -> str:
        if not (p := self._payload_for_ref(raw, m_type, root)): return ""
        try: text = spec.get("template", "- {title}").format(**p)
        except Exception: return ""
        return _wrap_doc_piece(rec, text, m_type.__name__, idx, str(raw).strip()) if rec else text

    def _payload_for_ref(self, raw: Any, m_type: type, root: Path | None) -> dict[str, Any] | None:
        if not (path := self._resolve_ref(raw, root)).exists(): return None
        try: return self._extract_composed_payload(m_type, path)
        except Exception: return None

    @staticmethod
    def _resolve_ref(raw_ref: Any, ref_root: Path | None) -> Path:
        ref = Path(str(raw_ref).strip().strip("`"))
        return ref if ref_root is None or ref.is_absolute() else ref_root / ref

    def _resolve_composition_model(self, value: Any):
        if value is None or isinstance(value, type): return value
        if isinstance(value, str) and ":" in value:
            mod_name, _, attr_name = value.partition(":")
            obj: Any = import_module(mod_name)
            for attr in attr_name.split("."): obj = getattr(obj, attr)
            return obj
        return None

    def _extract_composed_payload(self, model_type: type[StructuredNLDoc], path: Path) -> dict[str, Any]:
        from sldb.runtime.validation import extract_model_data
        return extract_model_data(model_type, path.read_text(encoding="utf-8"))


def _format_field_val(val: Any, payload: dict[str, Any], template: str) -> str:
    try: return template.format(**{"value": val, "val": val, **payload})
    except Exception: return str(val)


def _wrap_field_piece(recorder: Any, text: str, res: dict[str, Any], idx: int, ref_str: str) -> str:
    source = {"doc": res.get("doc"), "path": res.get("path") or ref_str, "model": res.get("model"), "field": res.get("field")}
    return recorder.wrap(text, {"piece": True, "source": source, "ref_index": idx, "ref": ref_str})


def _wrap_doc_piece(recorder: Any, text: str, model_name: str, idx: int, ref_str: str) -> str:
    source = {"doc": None, "path": ref_str.strip("`"), "model": model_name, "field": None}
    return recorder.wrap(text, {"piece": True, "source": source, "ref_index": idx, "ref": ref_str})

M = TypeVar("M", bound="StructuredNLDoc")

FILE:src/sldb/models/provenance.py
"""Who wrote a document, when, through what, and with which authority (docs/architecture/provenance.md).

Carried by every document in a reserved `sldb` frontmatter block; declared here, next to the
base model, so every reader shares one schema. A document without the block reads as
`agent`, `0`, `generated`: the least authority possible, until someone signs it.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Authority = Literal["source_raw", "authored", "theorem", "generated", "cache"]
AUTHORITIES: tuple[str, ...] = ("source_raw", "authored", "theorem", "generated", "cache")
BLOCK_KEY = "sldb"


class Provenance(BaseModel):
    """The `sldb` block of a document; `declared` says whether the document carried one."""

    by: str = Field(default="agent", description="Who wrote this version: `human:<id>` or `agent:<id>`; bare `agent` when unknown.")
    at: str | int = Field(default=0, description="When, as an ISO-8601 UTC instant; 0 when unknown.")
    via: str | None = Field(default=None, description="The operation or tool that wrote: `save_document_payload`, `deskops retire`...")
    authority: Authority = Field(default="generated", description="How much the content is to be trusted and who may change it (docs/architecture/provenance.md §2).")
    from_: list[str] = Field(default_factory=list, alias="from", description="What this document derives from (theorem, generated): `code:<path>::<name>`, `doc:<Model:name>`.")
    declared: bool = Field(default=False, exclude=True, description="True when the document carried a block; False when these are the defaults.")

    model_config = {"populate_by_name": True}

    def as_block(self) -> dict[str, Any]:
        """The mapping written under the `sldb` key; `from` only when it names something."""
        block: dict[str, Any] = {"by": self.by, "at": self.at, "authority": self.authority}
        if self.via:
            block["via"] = self.via
        if self.from_:
            block["from"] = list(self.from_)
        return block

    @classmethod
    def of_model(cls, model_type: type) -> tuple[str, bool]:
        """`(authority, declared)` of a model class: its `__authority__`, and whether some class
        of its own (not the base) set it."""
        declared = any("__authority__" in vars(c) for c in model_type.__mro__ if c.__name__ != "StructuredNLDoc")
        return getattr(model_type, "__authority__", None) or "generated", declared

    @classmethod
    def from_block(cls, block: dict[str, Any] | None) -> Provenance:
        """A block as read, or the defaults when there is none (or it is not a mapping)."""
        if not isinstance(block, dict):
            return cls()
        known = {k: v for k, v in block.items() if k in ("by", "at", "via", "authority", "from")}
        return cls(**known, declared=True)

FILE:src/sldb/store/model_contract.py
"""What the store reads from a model class and from sldb's built-in vocabulary: the one seam.

The store is a typed-document engine that sldb's document models feed. Everything it needs to
know about them (a class's document bases, its declared family, how a field is described, the
relation types sldb ships) comes through here, so the store's other modules import nothing
from `sldb.models` directly, and a store packaged on its own replaces only this module
(task: desacoplar el store dentro de sldb). Imports are lazy where the store's import time
must not pull the document models in.
"""

from __future__ import annotations

from typing import Any

from sldb.models.builtin_relation_types import BUILTIN_RELATION_TYPES, builtin_payload  # noqa: F401 - plain data


def base_names(model_type: Any) -> list[str]:
    """Names of the document-model bases above this model, nearest first (not the root class)."""
    from sldb.models.structured_doc import StructuredNLDoc

    return [b.__name__ for b in model_type.__mro__[1:] if isinstance(b, type) and issubclass(b, StructuredNLDoc) and b is not StructuredNLDoc]


def declared_family(model_type: Any) -> str | None:
    """The class's `__family__`, the root branch it belongs to; None when it declares none."""
    value = getattr(model_type, "__family__", None)
    return str(value) if value else None


def describe_field(name: str, field: Any) -> Any:
    """How one field is described for the field nodes of the edge index."""
    from sldb.models.field_schema.describe import describe_field as describe

    return describe(name, field)


def indexed_fields(model_type: Any) -> list[str] | None:
    """The class's `__indexed__` names, checked; None when it declares none.

    Raises:
        SLDBModelError: A name is not a field of the model (own or inherited), or the field's
            declared type is neither a scalar nor a list of scalars.
    """
    names = getattr(model_type, "__indexed__", None)
    if names is None:
        return None
    for name in names:
        _check_indexed(model_type, name)
    return sorted(set(names))


def projected_fields(model_type: Any) -> list[str]:
    """Fields a payload filter may name: `__indexed__`, else every field whose declared type can
    hold a scalar or a list of scalars (`Any` included: known per value). [] without a class."""
    from sldb.store.edge_index.payload_types import opaque_annotation, projectable_annotation

    if model_type is None:
        return []
    indexed = indexed_fields(model_type)
    if indexed is not None:
        return indexed
    return sorted(n for n, f in model_type.model_fields.items() if projectable_annotation(f.annotation) or opaque_annotation(f.annotation))


def contract_signature(model_type: Any) -> str:
    """sha256 of the canonical JSON (sorted keys, UTF-8, no spaces) of the model's field names
    (inherited included) and its `__references__`, `__containment__`, `__compositions__` names;
    "" when the class could not be loaded."""
    import hashlib
    import json

    if model_type is None:
        return ""
    body = {"fields": sorted(model_type.model_fields), **{attr: sorted(getattr(model_type, f"__{attr}__", None) or []) for attr in _DECLARED}}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


_DECLARED = ("references", "containment", "compositions")


def _check_indexed(model_type: Any, name: str) -> None:
    from sldb.store.edge_index.payload_types import projectable_annotation
    from sldb.store.exceptions import SLDBModelError

    field = model_type.model_fields.get(name)
    if field is None:
        raise SLDBModelError(f"Model '{model_type.__name__}': __indexed__ names '{name}', which is not one of its fields.")
    if not projectable_annotation(field.annotation):
        raise SLDBModelError(f"Model '{model_type.__name__}': __indexed__ field '{name}' is declared {field.annotation!r}, not a scalar or a list of scalars.")

FILE:src/sldb/store/edge_index/doc_contribution.py
"""One document's whole contribution to the edge index, ready to be its shard."""

from __future__ import annotations

from functools import cache
from typing import Any, Callable

from sldb.store.edge_index.composition_edges import composition_edges
from sldb.store.edge_index.declared_references import declared_reference_edges
from sldb.store.edge_index.doc_kinds import special_contribution
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.edge_index.doc_structure import document_structure
from sldb.store.edge_index.payload_projection import with_projection
from sldb.store.edge_index.records import tag_nodes
from sldb.store.models import DocEdges, DocumentEntry, SectionContextRecord


def build_doc_edges(model_name: str, doc: DocumentEntry, sections: list[SectionContextRecord], payload_of: Callable[[], dict[str, Any] | None], model_type: Any | None = None) -> DocEdges:
    """A relation type, relation or anchor document contributes what it declares; any other
    document contributes itself, its sections, and the references its model declares. Either
    way its tags become nodes: a tag exists in the index because some document, model or DAG
    entry carries it.

    Args:
        model_name: Model the document is tracked under.
        doc: The document's index entry (name, path, hashes, tags).
        sections: The document's sections, from its sections shard.
        payload_of: Reads the document's field payload, at most once: for the special kinds,
            for the declared references, and for the document node's projection.
        model_type: The imported model class, or None when it cannot be imported; without it
            no declared reference is read, as in `build_model_edges`.

    Returns:
        The shard, not yet stamped with `source_hash` / `edges_version` (the caller's cache keys).
        Its document node carries the projection (`payload_projection`).
    """
    payload_of = cache(payload_of)
    special = special_contribution(model_name, doc, payload_of)
    part = special or document_structure(model_name, doc, sections)
    edges = part.edges + _declared_edges(model_name, doc, model_type, payload_of, special is not None)
    tags = set(doc.semantic_tags).union(*(s.semantic_tags for s in sections))
    nodes = with_projection(part.nodes, doc_node_id(f"{model_name}:{doc.name}"), doc, model_type, payload_of)
    return DocEdges(doc_name=doc.name, model_name=model_name, semantic_tags=sorted(set(doc.semantic_tags)), nodes=nodes + tag_nodes(tags), edges=edges)


def _declared_edges(model_name: str, doc: DocumentEntry, model_type: Any | None, payload_of: Callable[[], dict[str, Any] | None], is_special: bool):
    """The model's declared references, read only when it declares any: the payload is a file
    read per document, and most models declare none.

    A relation, relation type or anchor document is skipped: its id fields are the edge it
    already contributes (`RelationDoc.__references__` names the ends of that very edge), so
    reading them again would assert a second, untyped edge beside it.
    """
    if is_special or model_type is None:
        return []
    if not _declares_links(model_type):
        return []
    payload = payload_of()
    references = declared_reference_edges(model_name, doc.name, model_type, payload)
    return references + composition_edges(doc_node_id(f"{model_name}:{doc.name}"), model_type, payload)


def _declares_links(model_type: Any) -> bool:
    """Whether the model names other documents at all: otherwise its payload is not read."""
    dunders = ("__references__", "__containment__", "__compositions__")
    return any(getattr(model_type, name, None) for name in dunders)

FILE:src/sldb/store/edge_index/compose.py
"""Shards -> one EdgeIndex: every store's contributions merged (the same node id is one node,
the first contributor's), the cross-document rules applied. Composed once per state of the
shards: the result is kept while no shard file, and no store index, has moved."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.store.edge_index.composition_targets import resolve_composition_edges
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.federation import federated_stores, qualify
from sldb.store.edge_index.live_stale import ModelTypeOf, live_stale
from sldb.store.edge_index.resolve import resolve_edges_reporting
from sldb.store.edge_index.shard_reading import read_store_contributions
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.io import load_store_index
from sldb.store.models import EdgeContribution, EdgeNodeRecord, EdgeRecord, ModelEdges

_COMPOSED: dict[tuple, tuple[tuple, EdgeIndex]] = {}


def compose_edge_index(store_path: Path, include_linked: bool = True, exclude_tags: Iterable[str] = (), model_type_of: ModelTypeOf | None = None) -> EdgeIndex:
    """The store's edge index, read from its shards (never rebuilt here).

    Args:
        store_path: The store's `.sldb` directory.
        include_linked: Also read the linked stores' indexes, their ids qualified by name.
        exclude_tags: Documents carrying one of these tags are left out (their nodes, their
            sections, their edges); the index itself holds everything.
        model_type_of: Loads a model class (`(model_ref, project_root) -> class | None`), so
            `stale` also names documents built under another contract of their model.

    Returns:
        The composed index; shared between callers, so treat it as read-only. Its `stale` is
        checked on every call against the files on disk (`live_stale`), not only the shards.
    """
    stores = federated_stores(Path(store_path), include_linked)
    key = (str(stores[0][0]), include_linked, frozenset(exclude_tags))
    signature = tuple(shards_signature(path) for path, _ in stores)
    hit = _COMPOSED.get(key)
    if hit is None or hit[0] != signature:
        hit = _COMPOSED[key] = (signature, _compose(stores, frozenset(exclude_tags)))
    return _with_live_stale(hit[1], stores, model_type_of)


def _with_live_stale(index: EdgeIndex, stores: list[tuple[Path, str | None]], model_type_of: ModelTypeOf | None) -> EdgeIndex:
    moved, known = [f"{name}:{e}" if name else e for path, name in stores for e in live_stale(path, model_type_of)], set(index.stale)
    extra = [e for e in dict.fromkeys(moved) if e not in known]
    return index.model_copy(update={"stale": index.stale + extra}) if extra else index


def invalidate_composed_edge_indexes() -> None:
    """Forget every composed index (tests, or a caller that rewrote shards by hand)."""
    _COMPOSED.clear()


def _compose(stores: list[tuple[Path, str | None]], exclude_tags: frozenset[str]) -> EdgeIndex:
    nodes: dict[str, EdgeNodeRecord] = {}
    edges: list[EdgeRecord] = []
    stale: list[str] = []
    fields: dict[str, list[str]] = {}
    for path, name in stores:
        stale += _merge_store(path, name, exclude_tags, nodes, edges, fields)
    kept, problems, unresolved = resolve_edges_reporting(nodes, resolve_composition_edges(nodes, edges))
    return EdgeIndex(nodes=nodes, edges=kept, problems=problems, stale=stale, unresolved_references=unresolved, payload_fields=fields)


def _merge_store(path: Path, name: str | None, exclude_tags: frozenset[str], nodes: dict, edges: list[EdgeRecord], fields: dict[str, list[str]]) -> list[str]:
    parts, stale_here = read_store_contributions(path, exclude_tags)
    for part in parts:
        if isinstance(part, ModelEdges):
            fields.setdefault(part.model_name, part.projected_fields)
    _merge((qualify(p, name) for p in parts), nodes, edges, _source(path))
    return [f"{name}:{export_id}" if name else export_id for export_id in stale_here]


def _merge(parts: Iterable[EdgeContribution], nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord], source: dict) -> None:
    for part in parts:
        edges += part.edges
        for node in part.nodes:
            nodes.setdefault(node.id, _stamped(node, source))


def _stamped(node: EdgeNodeRecord, source: dict) -> EdgeNodeRecord:
    return node.model_copy(update={"facets": {**node.facets, "source": source}})


def _source(store_path: Path) -> dict:
    return {"generated_from": "sldb.store.edge_index", "store_path": str(store_path), "hash_a": load_store_index(store_path).hash_a}

FILE:src/sldb/store/edge_index/payload_projection.py
"""A document node's projection (GO04): its payload's scalar fields, its index entry's hashes and
the model's contract signature, stored on the node so a query reads them without re-extracting.

What is left out: a field holding a dict, or a list with any non-scalar item (a table, a nested
model), and every field outside the model's `__indexed__` when it declares one. A field the
extracted payload does not carry (null, so dropped by the extraction) is absent too.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from sldb.store.edge_index.payload_types import is_projectable
from sldb.store.exceptions import SLDBError
from sldb.store.models import DocumentEntry, EdgeNodeRecord

logger = logging.getLogger(__name__)


def project_payload(payload: dict[str, Any] | None, indexed: list[str] | None) -> dict[str, Any]:
    """The flat map field -> scalar / list of scalars; `indexed` (when given) picks the names."""
    if not payload:
        return {}
    names = sorted(payload) if indexed is None else indexed
    return {n: payload[n] for n in names if n in payload and is_projectable(payload[n])}


def with_projection(nodes: list[EdgeNodeRecord], node_id: str, doc: DocumentEntry, model_type: Any | None, payload_of: Callable[[], dict[str, Any] | None]) -> list[EdgeNodeRecord]:
    """`nodes` with the document's own node (`node_id`) carrying its projection; others untouched."""
    from sldb.store.model_contract import contract_signature, indexed_fields

    if not any(n.id == node_id for n in nodes):
        return nodes
    payload = {} if model_type is None else project_payload(_read(payload_of, doc), indexed_fields(model_type))
    update = {"payload": payload, "field_hashes": dict(doc.field_hashes), "source_hash": doc.source_hash, "contract_signature": contract_signature(model_type)}
    return [n.model_copy(update=update) if n.id == node_id else n for n in nodes]


def _read(payload_of: Callable[[], dict[str, Any] | None], doc: DocumentEntry) -> dict[str, Any] | None:
    """The payload, or None when the file no longer extracts (an edit from outside sldb broke it):
    the node is still contributed, without a projection, and the next rebuild tries again."""
    try:
        return payload_of()
    except (SLDBError, ValueError, OSError) as exc:
        logger.debug("edges: payload of %s not projected: %s", doc.name, exc)
        return None

FILE:src/sldb/api/documents/payload_save_steps.py
"""The steps of `save_document_payload`, moved here from `sldb.cli.commands.fields_save`."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBModelError, SLDBPayloadSaveError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store import documents_hash
from sldb.store.hashing import hash_fields_with_map, hash_text
from sldb.store.io import load_models_index, load_store_index, save_models_index, store_lock
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex
from sldb.store.model_node import stamp_model_node
from sldb.store.ops import cascade_store_hash
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes


def model_class(model_ref: str, pythonpath: str | None, root: Path) -> type:
    """The model class, imported with the caller's pythonpath first, then the store's own root.

    A linked store's models import from where that store lives.
    """
    try:
        return resolve_model_ref(model_ref, pythonpath)
    except SLDBModelError:
        return resolve_model_ref(model_ref, str(root))


def load_model_indexes(sp: Path, root: Path, model_name: str) -> tuple[StoreIndex, ModelEntry, ModelsIndex]:
    """The store index, the model's entry and its models index."""
    idx = load_store_index(sp)
    m_entry = next((m for m in idx.models if m.name == model_name), None)
    if m_entry is None:
        raise SLDBPayloadSaveError(f"Model '{model_name}' not registered.")
    return idx, m_entry, load_models_index(root / m_entry.models_index)


def load_document_entry(sp: Path, model_name: str, doc_name: str) -> DocumentEntry:
    """The document's index entry, from its shard."""
    doc_entry = load_document_shard(documents_shard_path(sp, model_name, doc_name))
    if doc_entry is None:
        raise SLDBPayloadSaveError(f"Doc '{doc_name}' not registered.")
    return doc_entry


def render_checked(model_type: type, payload: dict[str, Any], ref_root: Path) -> str:
    """The payload rendered to Markdown, refused unless it round-trips.

    `ref_root` is the project root, so a composed field resolves its refs against the project
    rather than against whatever directory the caller happens to run in.
    """
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBPayloadSaveError(f"Field mutation broke idempotency: {details}")
    return rendered


def write_rendered_document(root: Path, doc_entry: DocumentEntry, model_type: type, rendered: str, via: str = "save_document_payload", actor: str | None = None) -> None:
    """Write the rendered Markdown, signed with its provenance block (plus final newline), and
    record its source and content hashes."""
    from sldb.api.documents.provenance_stamp import stamped_file
    from sldb.models.provenance_block import index_block

    text = stamped_file(root / doc_entry.path, rendered + "\n", model_type, via, actor)
    (root / doc_entry.path).write_text(text, encoding="utf-8")
    doc_entry.source_hash = hash_text(text)
    doc_entry.content_hash, doc_entry.field_hashes = hash_fields_with_map(model_type, text)
    doc_entry.provenance = index_block(text)


def save_document_indexes(sp: Path, root: Path, idx: StoreIndex, m_idx: ModelsIndex, m_entry: ModelEntry, doc_entry: DocumentEntry, pythonpath: str | None, model_type: type | None = None) -> None:
    """Save the document shard and model hashes, then rebuild derived indexes, under the store lock.

    The model's roster hash covers its documents' hashes: a field write must move it, or
    `stores check` fails and consumers keyed on the model node never see the change.
    """
    with store_lock(sp):
        save_document_shard(documents_shard_path(sp, m_entry.name, doc_entry.name), doc_entry)
        documents_hash.note(sp, m_entry.name, doc_entry)
        stamp_model_node(m_idx, documents_hash.roster_hash_of(sp, m_entry.name), model_type)
        m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)
        rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_sections_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_edges_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_store_hash(sp, root, idx)

FILE:src/sldb/api/anchors/__init__.py
"""Code anchors (docs/architecture/code-anchoring.md): record what a symbol looks like, check
every anchor of a store against the code now, reconnect what moved by name.

`record_anchor` reads one symbol; `check_anchors` only reads unless asked to `record` the
reconnections (owner's decision 3). States are `sldb.models.anchor_state.AnchorState`.
"""

from sldb.api.anchors.check_anchors import check_anchors
from sldb.api.anchors.record_anchor import record_anchor

__all__ = ["check_anchors", "record_anchor"]

FILE:src/sldb/api/__init__.py
"""sldb's library API: the store, model and document operations the CLI performs, as functions.

Consumers (pron, deskops, graph_ui...) call these instead of instantiating `sldb.cli` command
classes with fake argparse namespaces. Each operation that names a store opens it the way a
CLI command does (`open_store`), returns a pydantic model instead of printing, and raises
`sldb.core.exceptions` errors instead of exiting. Layering: `sldb.cli` -> `sldb.api` ->
`sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`.
"""

from __future__ import annotations

from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents import document_ast, build_document_ir_json, leaf_paths, runtime_document, extract_document_payload, render_document_markdown, render_model_template
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.document_serialization import serialize_document
from sldb.api.documents.payload_path_reading import deep_get, ensure_list
from sldb.api.documents.payload_path_writing import deep_delete, deep_set
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.edges.check_edges import check_edges
from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to, load_edge_index
from sldb.api.edges.apply_effects import apply_effects
from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edges_holding import edges_holding
from sldb.api.model_registry.remove_model import remove_model
from sldb.api.model_registry.inherit_model import inherit_model
from sldb.models.structured_doc import StructuredNLDoc
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)
from sldb.api.notations import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    save_projection_view,
    sync_notation,
    sync_palette,
)
from sldb.api.edges.unresolved_references import unresolved_references
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_record, serialize_edge_records
from sldb.api.edges.init_relations import init_relations
from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.journal import journal, verify_journal
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.model_drafts.draft_validation import promote_model_draft, validate_model_draft
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.field_drafts import add_model_field, remove_model_field
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_drafts import edit_model_template
from sldb.api.model_drafts.metadata_drafts import edit_model_metadata
from sldb.api.model_create.create_model import create_model
from sldb.api.model_create.field_decl import FieldDecl
from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_registry.add_model import add_model
from sldb.api.search import search
from sldb.api.rules import refuse_unknown_family, rules_check, rules_explain
from sldb.api.where import where_matches
from sldb.store.query_engine.where_parse import WherePredicateError
from sldb.api.model_registry.describe_model import describe_model
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_description import ModelDescription
from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.model_registry.registered_model import RegisteredModel
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.schema.describe_field import describe_field, describe_model_fields
from sldb.api.schema.field_description import FieldDescription
from sldb.api.segments import CompositionPiece, CompositionSpec, DocumentSegments, FieldSegment, LiteralSegment, Segment, SourceRef, build_document_segments
from sldb.api.stores.doc_ref import split_doc_ref
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.doc_status import doc_exists, doc_status
from sldb.api.stores.tracked_documents import tracked_documents
from sldb.api.stores.ambiguous_document import AmbiguousDocument
from sldb.api.stores.resolve_indexed_document import indexed_model_bases, resolve_indexed_document
from sldb.api.stores.init_store import init_store
from sldb.api.stores.link_store import link_store
from sldb.api.stores.unlink_store import unlink_store
from sldb.api.model_registry.registration_query import is_model_registered, registered_models
from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.migrate_hash_names import migrate_store_hash_names
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_check import check_store
from sldb.api.stores.store_fingerprint import store_fingerprint
from sldb.api.stores.store_links import store_links
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.node_ids import anchor_node_id, bare, doc_node_id, field_node_id, kind, model_node_id, relation_type_node_id, section_node_id, tag_node_id
from sldb.store.journal import JournalEntry, JournalVerifyReport
from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord
from sldb.store.models.document_hashes import DocumentHashes
from sldb.store.models.store_fingerprint import StoreFingerprint
from sldb.api.corpus import (
    Corpus,
    CorpusEntry,
    FieldEntry,
    FieldHit,
    FieldProjection,
    Hit,
    IndexProjection,
    field_id,
    split_field_id,
)

__all__ = [
    "Corpus", "CorpusEntry", "FieldEntry", "FieldHit", "FieldProjection",
    "Hit", "IndexProjection", "field_id", "split_field_id",
    "CompositionPiece", "CompositionSpec", "DocumentSegments", "FieldSegment",
    "LiteralSegment", "Segment", "SourceRef", "build_document_segments",
    "DocumentHashes", "DocumentReference", "DraftDocumentCheck", "DraftValidationReport",
    "EdgeCheckReport", "EdgeIndex", "EdgeNodeRecord", "EdgeRebuildReport",
    "EdgeRecord", "FieldDecl", "FieldDescription", "JournalEntry",
    "JournalVerifyReport", "LinkedStore", "ModelCheck", "ModelDescription",
    "ModelDocumentSummary", "ModelDraft", "ModelFieldSummary", "ModelRegistration",
    "ModelSource", "RegisteredModel", "RelationsInitReport", "StoreFingerprint",
    "StoreLocation", "StoreUpdateReport", "add_model", "add_model_field",
    "create_model", "anchor_node_id", "bare", "check_edges", "check_store",
    "store_fingerprint", "create_document", "deep_delete", "deep_get", "deep_set",
    "delete_document", "describe_field", "describe_model", "describe_model_fields",
    "doc_node_id", "document_ast", "edge_node", "edge_nodes_of_type", "edges_from",
    "edges_to", "edit_model_metadata", "edit_model_template", "ensure_list", "extract_document_payload",
    "field_node_id", "init_relations", "init_store", "journal", "kind", "link_store", "unlink_store",
    "load_edge_index", "leaf_paths", "load_runtime_documents", "migrate_store_hash_names",
    "load_registered_model", "locate_model_source", "model_node_id", "open_store",
    "promote_model_draft", "rebuild_edges", "reindex_model", "relation_type_node_id",
    "remove_model_field", "render_document_markdown", "render_model_template",
    "resolve_model_ref", "runtime_document", "save_document_payload", "search",
    "section_node_id", "serialize_document", "serialize_edge_node_records",
    "serialize_edge_records", "tag_node_id", "track_document_file", "untrack_document",
    "update_store_indexes", "validate_model_draft", "verify_journal",
    "DocRefStatus", "doc_exists", "doc_status", "tracked_documents", "AmbiguousDocument", "indexed_model_bases", "resolve_indexed_document", "split_doc_ref", "store_links",
    "WherePredicateError", "apply_effects", "edges_holding", "effects_of", "refuse_unknown_family", "rules_check", "rules_explain", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
]

FILE:src/sldb/cli/commands/anchors.py
"""`sldb anchors record|check` handlers: alerts by every route, exit by the errors alone."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.anchors import check_anchors, record_anchor
from sldb.api.anchors.anchor_docs import write_anchor
from sldb.cli import alert_sink
from sldb.cli.output_format import emit
from sldb.cli.store_context import get_store_context
from sldb.models.anchor_state import AnchorState


class AnchorsCLI:
    def run(self, args: Any) -> int:
        return {"record": self._record, "check": self._check}[args.anchors_command](args)

    def _record(self, args: Any) -> int:
        _sp, root = get_store_context(args.store, mode="readonly")
        block = record_anchor(root, args.ref)
        if not args.write:
            emit(block, args.format, "\n".join(f"{k}: {v}" for k, v in block.items()))
            return 0
        written = write_anchor(args.store, args.pythonpath, _target(root, args.write), block, args.claim, args.name)
        emit({**block, "written": str(written.path)}, args.format, f"recorded {block['ref']} -> {written.path}")
        return 0

    def _check(self, args: Any) -> int:
        reports = check_anchors(args.store, args.pythonpath, record=args.record)
        findings = [f for r in reports if (f := r.finding())]
        emit({"anchors": [r.as_dict() for r in reports], "errors": [f.as_dict() for f in findings if f.level == "error"], "alerts": [f.as_dict() for f in findings if f.level == "alert"]}, args.format, _summary(reports, findings))
        alert_sink.report(findings, text=args.format == "text")
        return 1 if any(f.level == "error" for f in findings) else 0


def _target(root: Path, write: str) -> Path:
    return Path(write) if Path(write).is_absolute() else root / write


def _summary(reports: list, findings: list) -> str:
    counts = {state.value: sum(r.state is state for r in reports) for state in AnchorState}
    shown = ", ".join(f"{n} {name}" for name, n in counts.items() if n or name == "intact")
    return f"anchors: {len(reports)} checked — {shown} — {alert_sink.tally(findings) or 'no findings'}"

FILE:docs/architecture/anchoring.md
# Anclaje

Documento de autoridad de sldb sobre qué es anclar, sus vías, sus reglas y la distinción entre
error y alerta. Las reglas de las secciones 3 y 4 son decisiones del dueño y no se rediscuten;
el diseño técnico que las implementa está en [code-anchoring.md](code-anchoring.md).

## 1. Definición

**Anclar es fundamentar una afirmación en su fuente**: «esto lo digo porque está dicho allá».
Un anclaje une lo que se afirma con el lugar exacto que lo respalda, y **guarda lo que vio**
de esa fuente. Por eso detecta mutaciones: cuando la fuente cambia, lo guardado y lo actual
dejan de coincidir, y el anclaje lo sabe.

Un anclaje que solo resuelve (encuentra a qué apunta) sin guardar lo que vio no verifica nada:
puede decir dónde está su fuente, pero no si sigue diciendo lo mismo.

Esta es la definición de sldb. El `AnchorDoc` de pron la usa con otro sentido, el de **alias**:
una palabra del léxico y lo que nombra (`pron.models:AnchorDoc`). Un alias resuelve; no
fundamenta ni guarda lo que vio.

## 2. Las dos vías

1. **AnchorDoc**: un documento cuyo `ref` apunta a algo del store (un modelo, un campo, un
   documento, una relación; sldb lo resuelve en `src/sldb/store/edge_index/anchor_targets.py`).
   Hoy resuelve, pero no verifica: no guarda lo que vio.
2. **Código, con tree-sitter**: un anclaje a un símbolo de código, `code:<ruta>::<qualified_name>`,
   resuelto por nombre y no por línea, que guarda un fingerprint de cada nodo que vio
   (`CodeAnchorDoc`, `sldb anchors record|check`); su diseño está en
   [code-anchoring.md](code-anchoring.md).

## 3. Reglas del anclaje (decisión del dueño, 2026-10-19)

1. **Docstring y cuerpo son nodos distintos.** El anclaje guarda un fingerprint de cada uno por
   separado: el texto normalizado del nodo, no el hash del archivo. Los dos cuentan como
   mutación, pero el anclaje distingue cuál cambió: la docstring, el cuerpo o ambos (y la
   firma, si conviene).
2. **`changed` no es un error, es una alerta** (sección 4). La fuente se movió respecto de lo
   anclado; el estado es válido, pero hay que mirarlo.
3. **Una referencia rota se intenta reconectar.** Si el símbolo ya no está en su
   `qualified_name`, se busca dónde quedó, con la heurística de renombre de selfdoc adaptada
   a los fingerprints por nodo. Si se encuentra, se reporta «reconnected: de X a Y» y queda
   registrado; si no, se reporta «lost». Los dos casos son alertas explícitas, nunca
   silenciosas.

## 4. Error y alerta, en todo sldb (decisión del dueño, 2026-10-19)

- Un **error** es algo roto o que viola un contrato: no parsea, el store está corrupto, un
  documento es inválido, falta un archivo requerido, un modelo no importa.
- Una **alerta** es que la fuente se movió respecto de lo registrado: un anclaje cambió, un
  hash quedó atrás, un documento generado está viejo. El estado es válido, pero hay que
  mirarlo.

Reglas de salida:
- Una alerta no hace fallar el comando: si solo hay alertas, el exit code es 0.
- Una alerta **jamás es silenciosa**. Aparece en la salida de texto; con `--envelope`, en
  `warnings`; en el CI, como annotation; y en el resumen final, con su conteo.
- Un error sí hace fallar el comando.

La regla vale para todo sldb, no solo para los anclajes. Hoy varios comandos tratan un
movimiento de fuente como error (por ejemplo, `stores check` da FAIL por un hash atrasado).
La auditoría de cada caso y su reclasificación propuesta están en
[code-anchoring.md, sección 10](code-anchoring.md).

## 5. Decisiones del dueño sobre la implementación (2026-10-20)

1. **sldb tiene su propio modelo de anclaje.** Lleva la `ref`, un fingerprint por nodo
   (firma, docstring y cuerpo), el estado y la provenance. El `AnchorDoc` de pron sigue
   siendo un alias de léxico y **no se toca**: si algo quiere verificar, va al modelo de sldb.
2. **En `lint`, una ruta citada que ya no existe es la alerta `lost`**: exit 0 y siempre
   visible. El ruido estructural (headings que el modelo no declara) **sigue siendo error**,
   en `lint` y en `stores check`.
3. **`anchors check` solo lee.** `anchors check --record` es el único que escribe, y lo que
   registra son las reconexiones.

Regla general: el envelope lleva las alertas en `warnings` (antes era `[]` fijo) y
`--format json` no las omite. Una alerta nunca es silenciosa. La reclasificación de la
auditoría ([code-anchoring.md, sección 10](code-anchoring.md)) queda aprobada.

FILE:CHANGELOG.md
# Changelog

Version note (2026-09-13, updated 2026-10-18): `pyproject.toml` declares `0.1.12`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.13 — not released yet (no tag, not on PyPI)

- Transiciones como datos de la arista (GO09, plan grafo-operable; `docs/architecture/edges.md`):
  - Convención de `RelationDoc.attributes` para una transición: `sets` (mapa campo → escalar YAML o lista de escalares; `null` asignable) y `terminal` (booleano que sldb solo transporta); ausentes o `null` valen `sets = {}` y `terminal = false`; otras claves se conservan y no entran a los efectos. Es un validador pydantic de `RelationDoc` (`sldb.models.transition_attributes`): escribir un `RelationDoc` con `attributes` no mapa, `sets` no mapa, `terminal` no booleano o un valor de `sets` mapa o lista anidada se rechaza con `ValidationError`.
  - `EdgeRecord.effects` (nuevo, opcional): solo lo llena `edges_holding`, como `{sets, terminal}` con `{campo}` sustituido desde el sujeto (sintaxis de `where_subject`, escalar en su forma YAML: `true`/`false`, números, strings tal cual). Un `{campo}` ausente, `null` o no escalar hace que la arista no se cumpla. Con `effects = None` la clave no aparece en ningún dump: la salida de `edges_from`, `edges_to`, `sldb edges show` y los shards no cambia; `sldb edges show --holds-for` sí la muestra.
  - `sldb.api.effects_of(attributes, subject)` (la resolución) y `sldb.api.apply_effects(subject, effects, model)`: función pura que reemplaza o agrega las claves de primer nivel de `sets` en una copia del sujeto y valida el payload completo contra la clase `model` (levanta su `ValidationError`); nunca persiste.
- Reglas como documentos (GO06, plan grafo-operable; `docs/architecture/rules.md`):
  - `sldb.models.rule_doc.RuleDoc` (exportado en `sldb.models`): `subject` (`model <= X` o una conjunción de nivel superior de esos términos), `where` opcional, `condition`, `severity` (`error` | `alert`), `moment` (`on_write` | `on_transition` | `on_check`) y `message` opcional. Sus validadores pydantic rechazan una `condition` o un `where` que no parsean, un `subject` con otra forma y un valor fuera del vocabulario; escribir una RuleDoc cuyo `subject` nombra un modelo no registrado se rechaza con el error existente `Model 'X' not registered.` (`create_document`, `save_document_payload`, `sldb docs create|update`).
  - `sldb.api.rules` (`rules_check`, `rules_explain`, `explain_exit`, `refuse_unknown_family`; también en `sldb.api`): las reglas son las RuleDoc del store local, leídas de la proyección del índice y evaluadas con `GraphBackend.eval`.
  - CLI `sldb rules check [--subject DOC]`: cada resultado `false` es un `Finding` de core con la severidad de la regla y código `rules/<nombre>`; cada `incomplete`, un alert `rules/<nombre>/incomplete`. Sale 1 solo si hay algún error. Sin `--subject`, solo las reglas `on_check` sobre los documentos locales de su familia.
  - CLI `sldb rules explain RULE SUBJECT`: `data = {rule, subject, finding}` con el finding de eval (`node`, `holds`, `clause`, `seen`), también cuando se cumple; exit 0/1/2 por `holds` y 3 cuando la regla no aplica (`applies: false`, `reason: subject|where`, `detail`).
  - `contracts/layers.toml`: la arista `models → store` (el parser del lenguaje, importado de forma diferida por los validadores de `RuleDoc`) queda contada como R6 pendiente.
  - `docs/opsys/bridge_primitives/README.md`: la sección `Constraint` se marca como reemplazada por `RuleDoc`.
- Lenguaje de predicados unificado (GO05, plan grafo-operable; `docs/architecture/rules-language.md`):
  - `sldb.store.graph.language`: parser (`parse_predicate` → `Predicate`) y evaluador del lenguaje de GO02: `and`/`or`/`not` con paréntesis, caminos `campo`, `rel:<tipo>`, `^` y clausura `+` (pasos unidos por `.`), cuantificadores `any`/`all`/`none`, `count(...) cmp n`, sustitución `{campo}` desde el sujeto, `incomplete` (Kleene fuerte) en el borde de links y findings `{node, holds, clause, seen}`. `sldb.store.query_engine.rules` es la fachada de los tests de spec (52 verdes).
  - `GraphBackend.eval` evalúa caminos sobre el índice compuesto y, sin sujeto, el dominio entero (la proyección cargada, o todos los documentos). Al atravesar un campo `F` con `F__anchor_state` en el origen, cada elemento expone `anchor_state`.
  - API única: `where_matches`, `edges_holding`, `StructuredQuery` y `--where` evalúan con el lenguaje; nuevas `sldb.api.where.where_findings` (un store, sin re-extraer) y `where_records`.
  - CLI: `sldb find --where` acepta el lenguaje completo (caminos sobre el índice del store) y `--explain` agrega `findings` por documento evaluado. `sldb --envelope graph query` con filtros `FieldCondition` lleva un warning `deprecated/field-condition` que nombra el predicado de reemplazo; la salida no cambia.
  - Deprecados (GO10 los retira): `where_parse.compile_where`, `where_parse.where_parse` y construir `FieldCondition` emiten `DeprecationWarning`.
  - Cambios de resultado declarados (tabla de equivalencia, goldens en `tests/fixtures/where_goldens/`): `f != <número>` ya no cumple sobre un campo ausente; ordenar `None` o tipos mezclados da `false` en vez de `TypeError`; en `StructuredQuery`, `contains` sobre una cadena es subcadena e `is_null`/`is_not_null` tratan `""` como ausente.
- Transclusión de campos y segmentos ricos de diagramas y vistas en /document/segments (SV03):
  - `sldb.api.segments`:
    - `source_ref.py`: `SourceRef` incorpora el campo opcional `field: str | None = None`.
    - `composition_spec.py`: Soporta `ref: Literal["document", "field", "view", "spec"]`.
    - `composition_piece.py` y `field_segment.py`: incorporan los campos opcionales `projection: dict | None = None` y `table_data: dict | None = None`.
    - `field_ref_resolver.py`: `FieldRefResolver` resuelve referencias `Model:name#campo`, `docs/<Model>/<name>/<campo>` y `docs/<name>/<campo>` devolviendo `{model, doc, path, field, value, payload}`.
    - `segment_enrichment.py`: Enriquecimiento de segmentos con vistas resueltas (`resolve_view` / `evaluate_projection_view`) y tablas estructuradas (`table_data`).
    - `build_document_segments.py`: Inyecta `FieldRefResolver` en `render_with_spans` y enriquece los nodos con `projection` y `table_data`.
  - `sldb.models.structured_doc`: `StructuredNLDoc.compose_field` y `render_payload` aceptan `field_resolver`; cuando `ref == "field"`, resuelve campos remotos emitiendo `CompositionPiece` con `SourceRef(model, doc, path, field)`. Sin resolver inyectado, rinde vacío preservando la pureza del renderizador.
  - Documentación de arquitectura en `docs/architecture/segments-and-transclusion.md`.
  - Suite de tests en `tests/segments/test_field_transclusion_and_diagram_segments.py`.
- Visual notation and projection view resolver, store synchronization, CLI, and serve routes (SV02):
  - `sldb.api.notations`:
    - `notation_view.py`: `resolve_view` and `resolve_documents` resolving glyphs, compartments (`data.attributes`), template/keyword interpolation, edge ordering, UML fragments, and legends.
    - `projection_view.py`: `evaluate_projection_view`, `list_projection_views`, and `save_projection_view` evaluating node where-predicates, relation filters, layout, palette ink, and notation styling.
    - `notation_sync.py`: `sync_palette` and `sync_notation` writing `PaletteDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, and `RelationTypeDoc` into stores without intermediate YAML dependencies.
    - Re-exported in `sldb.api` and `sldb.api.notations`.
  - CLI: `sldb notations (list, sync, view, resolve)` with JSON output and envelope support (`sldb --envelope notations ...`).
  - HTTP serve routes in `sldb serve`: `GET /notations`, `GET /notations/view`, `POST /notations/resolve`, `GET /views/projection`, `GET|POST /views/projection/evaluate`, `POST /views/projection/save`.
  - Documentation updated in `docs/architecture/notations-and-views.md`.
  - Comprehensive test suite in `tests/notations/test_notation_view_and_routes.py`.
- Declaración y edición draft de containment, references, compositions, semantics y authority en modelos (SV04):
  - `sldb.api.create_model` y `ModelSource` aceptan `containment`, `references`, `compositions`, `semantics`, `authority`; validan que los campos referenciados existan y que las composiciones tengan marcador `⸢render•<name>⸥` en template (o lo generan en `default_template`), emitiendo las asignaciones correspondientes en el código Python generado.
  - `describe_model` y `ModelDescription` exponen `containment`, `references`, `compositions`, `semantics_map`, `authority`, `template`, `has_draft`, `draft_path`.
  - `sldb.api.edit_model_metadata` en `sldb.api.model_drafts` edita `__containment__`, `__references__`, `__compositions__`, `__semantics__` y `__authority__` en el `.draft.py` (`.py.temp`) mediante manipulación AST en `metadata_literals.py`, y sincroniza secciones de composiciones en el template.
  - `validate_template_contract` y `check_and_plan` validan coherencia de referencias/containment/compositions contra campos declarados y template, rechazando errores con `SLDBModelEditError`. `promote_model_draft(..., backfill=True)` re-renderiza documentos y reconstruye índices de modelo, semántico y de aristas.
  - Expuesto en CLI (`sldb models metadata edit`, `sldb models validate --promote --backfill`, y flags de creación) y HTTP serve (`POST /models/create`, `POST /models/metadata-edit`, `POST /models/promote` con `backfill`).
  - Documentación de arquitectura en `docs/architecture/model-authoring.md`.
- Visual vocabulary models, palettes and builtin notations absorbed from spec2viz (SV01):
  - 7 models in `sldb.models.notation_models` (re-exported in `sldb.models` and `sldb.api`):
    `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, and `ViewDoc`.
    `ViewDoc` adds optional `params: dict` and `sections: list` for GD25 convergence.
  - Submodule `sldb.notations` containing palette (`palette.py`), notation (`notation.py`),
    and styling (`styling.py`) engines, along with builtin `palettes/default.yml` and the 8 builtin
    notations in `builtin/` (`uml-class`, `statechart`, `component`, `deployment`, `uml-sequence`,
    `activity`, `component-view-matrix`, `reflection`).
  - `resolve_model_ref` maps legacy `spec2viz.sldb_models:<Model>` references to
    `sldb.models.notation_models:<Model>` for transparent backwards compatibility with existing stores.
  - Architecture documentation in `docs/architecture/notations-and-views.md`.
- Each document node of the edge index carries its projected payload (GO04): `EdgeNodeRecord`
  gains `payload` (top-level fields holding a scalar or a list of scalars; dicts and lists of
  non-scalars are left out; a model's `__indexed__` picks exactly those names), `field_hashes`
  (the entry's whole map), `source_hash` (hash_c) and `contract_signature` (sha256 of the model's
  field names and `__references__` / `__containment__` / `__compositions__` names), persisted in
  the shard; other nodes leave them empty. `EDGE_INDEX_VERSION` 4 -> 5: a version-4 shard reads
  as stale and is rebuilt on the next write or `stores build`. `EdgeIndex.stale` now also names
  a document whose Markdown was edited outside sldb and one built under another contract
  signature of its model (a new `__references__` entry). `StructuredQuery` filters on
  `FacetFilter(facet="payload", ...)` from the shard, with no re-extraction; a filter on a field
  no model projects raises `SLDBGraphArgumentError` naming it. An `__indexed__` name that is not
  a field or not scalar is `SLDBModelError` when the model loads. Existing queries answer as
  before. Edge index of this repo after `sldb stores build` (`du -sb` of the edges shards root,
  MB = 10^6; shards = `.yaml` files there; 2026-11-06): before (main 804f1ad4) 47.64 MB in
  3116 shards; after (wt/go04 on c1e50419, which tracks more documents) 58.54 MB in 3277 shards.
  `docs/architecture/graph-backend.md` documents the projection and what it leaves out.
- A bare id in a reference field that allows a model also names a document of one of its submodels
  (`depends_on: task-x` with `TaskDoc` allowed names `TaskCodeDoc:task-x`), read from `base_models`
  of the model nodes in the composed index (an inherited model's node takes them from its class, since
  its local index keeps none). The allowed model itself wins; several submodels with that
  name stay `ambiguous`. `resolve_indexed_document` also reads the bases of an inherited model from
  its owner store.
- `sldb.api.resolve_indexed_document(store_path, model, name)` finds `Model:name` when the document is
  tracked under a submodel of `Model` (`TaskDoc:task-x` finds `TaskCodeDoc:task-x`): an instance of a
  submodel is an instance of its bases, read from `base_models` in the model indexes, without importing
  any class. An exact match on the model wins; two submodels tracking the same name raise
  `AmbiguousDocument`. Consumers such as graph_ui resolve ids through it instead of comparing model names.
- The whole-graph analyses sit behind a `GraphBackend` seam (`load`, `eval`, `analyze`).
  `NetworkXBackend` wraps `sldb.store.graph.analysis` unchanged, so the six `sldb graph`
  analyses and the ten `api/graph/analyze.py` functions print the same output as before and
  can be given another backend by Python for tests. A store selects it with
  `graph_backend` in `.sldb/store.yaml`: absent means `networkx`; any other value fails on
  load with `graph_backend <value> no admitido; admitidos: ["networkx"]`. `eval` implements
  the GO02 subset without paths (finding shape in `rules-language.md` §4 and §6); a path
  raises `NotImplementedError` until GO05. `docs/architecture/graph-backend.md` fixes the
  seam: a future engine (Kùzu, Neo4j, Datalevin) enters behind it and the rules never see it.
- A project's declared-edge graph as a library (`sldb.api.edges.project_graph`): `ProjectGraph(root,
  ProjectGraphConfig)` reads the documents of configured surfaces and the files path rules
  classify as nodes, the schema edges and unresolved values of the project's own store from its
  cached composed edge index (`include_linked=False`), and from each document's text what its
  model does not declare (configured mapping fields, fenced YAML blocks, mentions under headings
  or on every line). `edges_from(node)` / `missing_from(node)` read one source alone and give
  what `extraction()` gives for it, so a reader asking about a few documents reads only those.
  The project owns only the configuration (deskops' desk is the first, `deskops/graph/desk_graph.py`).
  New `sldb.api.tracked_documents(store, refs)`: `doc_status` for many references from one read
  of the documents index.
- The store splits in two sibling directories: `.sldb/` (`store.yaml` and `core/`) is
  versioned whole, so that git holds the tree's past, and `.sldb_cache/` (edges, sections,
  semantic shards, graphs, locks; `.sldb/runtime/` until now) is regenerable and ignored
  (`docs/architecture/derived-store-boundary.md`; owner's decision, 2026-10-29).
  `sldb stores init` adds the line `.sldb_cache/` to the root `.gitignore` (idempotent, no
  other line touched); `sldb stores check` reports the error `stores/core_ignored` (exit 1)
  when git ignores `.sldb/core/` or `.sldb/store.yaml` and the alert `stores/cache_not_ignored`
  (exit 0) when the cache is not ignored; `stores build --check` leaves `.sldb_cache/` out of
  its copy. New `sldb stores migrate-layout [--store PATH] [--force]` moves the content of
  `.sldb/runtime/` to `.sldb_cache/` (refusing a non-empty cache unless `--force`, which
  deletes it first), deletes the journal without archiving it, removes `.sldb/runtime/` and
  rewrites the root `.gitignore`: only the lines whose pattern is `.sldb/core` or
  `.sldb/runtime` go, `.sldb_cache/` comes in, everything else stays verbatim. The
  `selfdoc python-sync` graph defaults to `.sldb_cache/graphs/python-source.graph.json`.
- The write journal is retired (2026-11-04): no write through `sldb.api` produces one, and
  `sldb journal show` (and `verify`) print `El journal fue retirado el 2026-11-04; el pasado
  del store se consulta con sldb docs history <doc>.` and exit 0. `sldb.api.journal()` answers
  `[]` and `verify_journal()` a valid, empty report, for importers; `SLDB_JOURNAL_OFF` is gone;
  the `actor` parameters stay (they still stamp a document's provenance where they did).
  `docs/architecture/journal-authority.md` records the decision: the tree is the authority
  and git is its memory.
- Edges can carry their evidence, on request: `sldb edges show --evidence` and
  `sldb.api.edges.edge_evidence.stamp_evidence` add `metadata.evidence` with `ref_hash` (the
  target's `content_hash`, a model's `model_hash`; for a section its document's, flagged
  `ref: document`, since sections have no hash of their own), `contract` (the source model's
  `contract_hash`) and `engine` (`{name, version}`) or, for an authored edge, `actor`
  (`relation_doc:<name>`). No timestamp. Computed on read, so the shards do not change, and
  `ref_hash` is the target's current hash: telling an edge went stale takes a caller that kept
  an earlier evidence to compare.
- `sldb --envelope <command> ...` prints one JSON value per run, `{ok, command, store,
  revision, data, warnings}` or `{ok: false, error: {type: "ns/name", message}, exit}`, and
  exits with a typed code: 0 ok, 1 missing, 2 ambiguous, 3 rejected input, 4 busy, 5 store or
  runtime failure, 6 usage, 70 unexpected (`docs/cli-envelope.md`). Opt-in: without the flag
  the CLI prints and exits as before, because callers parse that output today.
- `sldb stores declare` and `sldb stores build`. A store's source is `.sldb/store.yaml`: the
  models it registers (local, or inherited from a linked store), its links, its predicates,
  the generators that write derived documents (such as `selfdoc python-sync`), the paths
  they write, and `include` rules saying which file is tracked under which model and name.
  The index and the model and document indexes are rebuilt from it by `stores build`
  (idempotent); `stores build --check` rebuilds a scratch copy of the sources and fails when
  that copy does not pass `stores check`, a tracked document is not declared, or it tracks
  something other than the local store. `stores declare --write` writes the declaration the
  current index implies, to adopt the layout. Tracking or untracking a document through the
  API keeps the declaration current (a file outside the project is not declared), `stores
  check` notes a declared store whose `.sldb/core/` is versioned rather than ignored, and a
  declared file that is gone is reported by `build` as `missing`. `declare --write` writes
  the declaration the index implies: a model whose source is outside the project
  (sldb's own, from the installed package) is declared by `model_ref` alone, and a glob is
  written only for a folder with more than one tracked file, all of one model. Design:
  `docs/architecture/derived-store-boundary.md`.
- An inherited model whose owner uses a `src/` layout imports again. The import root was the
  owner's project root, so pron's models, which live under its `src/` directory, stayed unimportable in a
  store that inherits them; it is now the directory the owner's registered path puts the
  package in (`sldb.store.model_import_root`). sldb's own store inherits AnchorDoc,
  ProjectionDoc and MoveDoc from pron through a relative link (`../pron/.sldb`) instead of
  registering copies pinned to an absolute path that no longer existed.
- **Python 3.12 or newer is required** (`requires-python >=3.12`; it was `>=3.10`). Python
  3.10 reaches end of life this month, and the whole suite (sldb, deskops, spec2viz, graph_ui)
  moves to the same floor. CI tests 3.12 and 3.13. The compatibility code for 3.10 is gone:
  the `tomllib`/`tomli` fallback in the `tools/check_*.py` gates and the conditional `tomli`
  dev dependency. `uv.lock` is regenerated for the new floor.
- The pre-redesign singular groups `sldb store`, `sldb model` and `sldb doc` run again: they
  were parsed (and listed by `sldb doc --help`) but had no handler, so `sldb doc untrack`
  answered `Unknown command: doc`. The plural groups (`stores`, `models`, `docs`) remain the
  documented spelling.
- A change to a model's contract now rebuilds the edges of its documents. Adding
  `__reference_models__` to a model and running `stores update` used to reuse every document's
  edges shard (its hashes had not moved), so the new references never reached the index and
  `edges rebuild` walked nothing until the shards were deleted by hand. Each shard now records
  the contract it was built under; the first rebuild after upgrading rewrites every shard once.
- A store link can be removed or pointed elsewhere: `sldb.api.unlink_store(store, name)` /
  `sldb stores remove <name>`, and `link_store(..., replace=True)` / `stores add --replace`.
  Removing a link a model here is inherited from is refused (replace it instead). A link to a
  directory that is gone was only fixable by editing `store_index.yaml`; `stores check` now
  notes it (`broken_links` in `check_store`).
- A scalar list item reads back as written. An item whose text markdown reads as block syntax
  was lost or mangled on extract: `validation: ["```bash", "pytest", "```"]` came back as
  `["pytest"]` (so any rewrite of the document deleted the fence lines), and `# x`, `> x`,
  `- x`, `1. x`, `***`, `<b>` or a leading space lost their syntax. Such an item is now rendered
  with one leading backslash (a CommonMark escape) and extracted without it; only a value that
  opens its item (`- ⸢rev,list•x⸥`) is escaped. A hand-written item that already began with
  `\` before such syntax now reads without that backslash.
- Extracting and validating no longer re-parse the model's template each time: a template's
  recipes are computed once per template, `validate` renders once instead of twice, and the
  sections index reuses one markdown-it parser. On sldb's own store, extracting 153 documents
  went from ~420 ms to ~275 ms and their sections from ~205 ms to ~175 ms.
- The markdown AST keeps what a token carries beyond its text, in `SLDBNode.metadata`: a
  fence's language (`info`), its opening markup (`markup`) and its attributes.
- `sldb edges show <name>` with something that is no node of the index fails, and suggests the
  document's export id (`Did you mean PillDoc:pill-008?`), instead of printing `[]` as for a
  real node without edges.
- `models show`, `models template show` and `docs update` take `--format text|json|yaml`
  (`models show` keeps YAML as its default; the template comes wrapped as
  `{model, draft, path, template}`; `docs update` reports `{updated, model, path}`). An
  argument a subcommand does not know is reported with that subcommand's usage, not the
  root's.
- A model's `__family__` changed in the class reaches the store: `stores update` and
  `models update` re-read it (it was written only at `models add`).
- `sldb.api.registered_models(store)` and `is_model_registered(store, model)` (by name,
  `module:Class` or `module.Class`), and `sldb models check <model>...`, which reports each as
  registered or missing and exits 1 if any is missing.
- `stores check` notes ignore rules that break the store's split (`.sldb/core` ignored, or
  `.sldb/runtime` not ignored); `check_store` returns it as `gitignore_policy`.
- A registered model that does not import here no longer takes the store's AST down: it is
  listed with `resolved: false` and the error (a healthy model's entry is unchanged), so `models show` and `ast show` of the rest
  answer (in an environment without `pron`, `models show TaskDoc` failed).
- `models template show` (and every draft operation) finds a model's source by importing its
  `model_ref` when the recorded path is not a file here: a store copied without its models,
  an absolute path from another machine, or an inherited model, whose path is empty and
  failed with `Is a directory`. When neither works, the error names the model and the store.
- A template's literal paragraph (deskops' `_Describe the incoming message..._`) anchors only a
  paragraph with that text. A document written without the placeholder had its first real
  paragraph taken for it and dropped on extract, so any rewrite deleted it (the first
  paragraph of inbox notes; `why`, `goal` and `done_when` of a task). Documents that lacked
  the placeholder now extract more: `stores check` reports them as `data_mutation` until
  `sldb models update <Model>` re-extracts the model (`stores update` trusts a document whose
  text did not move). Headings still anchor by position.
- A document that ends before its template does keeps its last section: a field of a section
  the document does not have (`## When`, after a document that stops at `## Why`) no longer
  claims the last section's paragraph, which came out empty and was erased by any rewrite.
  Past a missing heading, only later headings end a section. The `purpose` of three of
  sldb's rituals came back (`models update RitualDoc`).
- `stores check` names the documents a rewrite would lose content from: blocks of the file
  that do not survive `render(extract(text))`, because the model does not read them (written
  by hand, or by an older template). Their hashes are consistent over the poor extraction, so
  nothing else showed it. Sections the template fills only with `render`/`py` markers are
  regenerated and not counted. `check_store` returns it as `rewrite_loss`.
- `stores check --quiet` prints the PASS/FAIL line alone, as documented: it printed the
  per-document notes too, and now also skips the scans behind them.
- A `data_mutation` over text that did not move (and an unchanged contract) is explained as
  what it is, sldb reading the same file differently after an upgrade, and points to
  `sldb models update <Model>`: `stores check` said `stores update` would accept it, but
  `stores update` trusts unchanged text and did nothing. It no longer asks for a decision.
- `stores check` says, for a document whose text disagrees with its index, where the indexed
  text sits in the file's git history: `stale` (an earlier committed version, with the commit:
  the index fell behind), `unmatched` (no committed version has it: an edit indexed and never
  committed, or damage), `orphan` (the file is gone) or `undetermined` (not a git work tree),
  with the `git log` command that shows it. The JSON report carries it as `history`.
- `sldb.store` imports the rest of sldb through three seams only: `store/exceptions.py`
  (errors), `store/runtime_codec.py` (extraction) and `store/model_contract.py` (what a model
  class declares, and the built-in relation types); it imports nothing from `sldb.api`, `cli`
  or `selfdoc`, and `tests/test_store_seams.py` keeps it so. `describe_field` and the field
  kinds moved to `sldb.models.field_schema` (still importable from `sldb.api.schema`), which
  closes the store → api edge R4 in `contracts/layers.toml`.
- `selfdoc python-check` and `python-sync` work again: a property with a setter (or an
  `@overload`) was two symbols with one document id, and both commands failed with "Python
  symbols collide". A name redefined in its scope is now one symbol.
- kgdb is part of sldb, and nothing invokes an external `kgdb` any more. `selfdoc python-sync`
  writes the source graph with sldb's own graph IO instead of running `kgdb ingest` (it failed
  once the separate package was gone). `--kgdb-command` and `--kgdb-output` were removed and
  are refused with a clear error; the graph goes to `--graph-output`, by default
  `.sldb/runtime/graphs/python-source.graph.json` (it was `.kgdb/python-source.graph.json`).
  `sldb.selfdoc.kgdb_sync` is now `sldb.selfdoc.source_graph_file` (`write_source_graph`), and
  the selfdoc report's `kgdb_stale` is `graph_stale`. The data contract
  `sldb_kgdb_semantic_export` keeps its name (see the entry on kgdb names below).
- Docstring metadata is parsed strictly (`sldb.selfdoc.docstring_metadata`, spec section 2):
  only an opening line exactly `---` starts it, a closing `---` is required, and the block is a
  YAML mapping with unique keys among `id` (required), `kind` and `tags` (`namespace:value`,
  deduplicated). Malformed metadata and an id declared twice are reported as `path:line:
  problem` in the selfdoc report's `metadata_errors`, and `selfdoc python-sync` writes nothing
  while any remain; they were silently ignored and the declaration lost its identity.
- The source graph gives every module and symbol node its `local_tags` and `effective_tags`,
  inherited along the lexical chain package -> module -> class/function -> nested declaration
  within the scan (spec section 3): `system:*` and `workspace:*` from the nearest declaration,
  `topic:*` as a union, any other tag local only; nothing through imports, base classes or
  siblings. Each effective tag names the declaration and `path:line` it comes from. Two
  `system:` (or `workspace:`) tags on one declaration are a metadata error.
- An import in the source graph follows explicit re-export chains to the definition
  (`from sldb.api import open_store` reaches `sldb.api.stores.open_store:open_store`), through
  module-level imports only, with the chain in the edge's `via`; `from pkg import submodule`
  reaches the submodule. A star import, a cycle or a module outside the scan stays
  unresolved. A relative import inside a package's `__init__.py` resolves against that
  package (it was resolved against the parent: `pkg.impl` for `pkg.inner.impl`).
- `stores check` reuses its per-document content scans (rewrite loss and structural noise)
  while a document's text, its model's contract and the sldb that reads it have not moved, in
  the user's cache directory; the rewrite-loss scan also reuses the extraction the check
  already has instead of extracting again. On sldb's store (2775 documents) a full check went
  from 43 s to 23 s cold and 7 s warm, with the same findings.
- The source graph keeps the condition an import lives under (`context`: `type_checking`,
  `conditional`, `try`), and marks an import a later same-scope binding shadows
  (`shadowed_at`); a reference after the shadowing no longer resolves to the import.
- `selfdoc python-check` reports, apart from errors and drift, the declarations without
  metadata (`undeclared`), the declared ones without an explanation (`unexplained`) and the
  annotation references nothing resolves (`unresolved_references`, which were dropped).
- A symbol document's `purpose` is generated from the first paragraph of its docstring when it
  is a placeholder or was generated before; an authored purpose is kept and listed in
  `purpose_conflicts` for a decision.
- `selfdoc python-sync` reports on what is on disk after writing: it reported the plans made
  before writing, so a sync that wrote everything returned 1.
- Deleting `.sldb/runtime/` and rebuilding brings the sections and semantic indexes back. The
  user cache (`~/.cache/sldb/runtime-cache-built/`) and the in-process dirty set vouched for
  shards that were gone, so a rebuild wrote only the edges and a graph snapshot lost
  `has_section` and `semantic_parent` (reported by graph-ui).
- The last kgdb names in sldb's public surface are sldb's now (kgdb merged into sldb):
  - `sldb.store.export.export_kgdb_semantic_payload` is `export_semantic_payload`;
  - the semantic export contract keeps its name, `sldb_kgdb_semantic_export` version 1, and so
    do its schema and fixture (`contracts/schemas/sldb_kgdb_semantic_export.schema.json`,
    `contracts/fixtures/sldb_kgdb_semantic_export.v1.json`). It is a frozen data identifier,
    like the `sldb://...` node ids: renaming a data contract breaks every reader of files
    already written, so a format change goes behind a new contract version, never a rename.
    Main wrote `sldb_semantic_export` for a while before release; an export under that name is
    still read, never written. `tests/store/test_export_contract_frozen.py` pins the contract,
    the ids and the keys of the store index and of the document entries. The reading function is `sldb_semantic_export_to_snapshot`;
  - `stores semantic-export --format kgdb` is `--format sldb`;
  - the `sldb serve` route `/kgdb/snapshot` is `/semantic-export`;
  - the store's tracked relation types moved from `kgdb/relation_types/` to
    `sldb/relation_types/`, where `edges init` already wrote the new ones.
- `stores init` fails cleanly: what a failed init wrote is removed, the message says where it
  failed and what to check (instead of `Unexpected: [Errno 13] ...`), and the exit code tells
  a caller what happened: 0 created or already there, 2 the place refused it (permissions),
  1 failed half-way. `init_store` raises `StoreInitError` (an `SLDBStoreError`).

## 0.1.12 - 2026-10-18 — declared references resolve bare ids and paths, and report what names nothing

- Declared references resolve bare ids and paths. A value of a `__references__` or
  `__containment__` field names its document as an export id, as the path a tracked document
  lives at, or as a bare id tried against the models the field allows — the new
  `__reference_models__ = {"field": ["Model", ...]}`, or the containment list; one match
  resolves, several are `ambiguous`. It is decided when the index is composed, so tracking the
  target later resolves it. What names nothing is reported, never an edge:
  `sldb.api.unresolved_references(store)` / `sldb edges unresolved` /
  `EdgeIndex.unresolved_references` (`UnresolvedReference`: source, model, field, target,
  target_export_id, relation, reason, source_path). A free reference field only reports export
  ids. `EDGE_INDEX_VERSION` is 4: shards rebuild. `__reference_models__` enters the contract
  hash only for a model that declares it.
- An edge sldb derives (structural, schema, alias) is checked against sldb's own definition of
  its builtin type, even where the store authored a type under that name (selfdoc's code
  `contains` / `references`).
- `edges check` of a store that links others fails only on its own edges: what only a linked
  store's edges commit (an owner's stale shards, its cardinality violations) is reported apart
  (`EdgeCheckReport.linked_errors`, `linked_stale`; a `note:` line in the CLI). Edges read
  from a linked store carry `metadata["from_store"]`.
- Inheriting a model into a store (`models inherit`, or `alias:Model` on first use) signs its
  empty roster, so `stores check` passes without a `stores update` first.
- A section no longer counts as the owner of a path: a bare composition or reference value
  equal to a heading path resolved to that section instead of a document.

## 0.1.11 - 2026-10-18 — models are defined once and inherited; a free `attributes` on relations

- `RelationDoc.attributes`: a free dict of the edge's own attributes (a multiplicity, a role, a
  transition's action), written in the frontmatter and copied to the index edge as
  `metadata["attributes"]`. A RelationDoc written before has none. Its contract moved: run
  `sldb stores update` in a store that tracks RelationDoc documents.
- `sldb.api.StructuredNLDoc`: the base class of models, from the public surface.
- `sldb.api.graph.query_snapshot(snapshot, query)`: a StructuredQuery over a GraphSnapshot held
  in memory, no store needed. `sldb.api.graph` also exports `Edge` and `SystemIdentity`.
- `models inherit` and the `stores check` note tell a copy by its class, not by the reference
  string: `deskops.models.atom:AtomDoc` is a copy of `deskops.models:AtomDoc` when the package
  re-exports it. A converted copy takes the owner's `model_ref`.
- `edges check` over linked stores: one edge that two stores both emit (a shared model's
  `has_field`) counts once for cardinality; `has_model` is many-to-many, since stores share a
  model they inherit; `links_to` is a builtin relation type. `sldb edges init` now also
  rewrites a tracked builtin relation type whose spec moved (`updated` in its report), and no
  longer writes a builtin over an authored relation type of the same name.
- Models are defined once, in the store that owns them, and inherited by the others.
  `sldb models inherit alias:Model` / `sldb.api.inherit_model` registers an inherited entry
  (`origin: <alias>`, no source path) or converts a local copy in place, keeping its documents,
  roster and signed contract. Using `alias:Model` as a model name now inherits instead of
  copying. An inherited model imports from the owner's project root, so no `--pythonpath` is
  needed and a moved owner is one link to update; with the owner unreachable the store keeps
  working on its own signature. `stores check` notes a local model under a name a linked store
  owns (a convertible copy, or an override to rename). The graph gains `links_to` between
  stores and `origin_store` on `has_model`. A store with no inherited models writes no
  `origin` key, so existing indexes do not change.
- `stores update` re-signs the roster of a model whose class does not import. It used to skip
  the model whole, so a stale roster (a merge that brought its shards in, say) stayed
  `roster stale` in `stores check`. Its documents are still not rehashed, it is still reported
  as skipped, and it keeps the contract it signed.
- `stores check` no longer reports a moved contract for a model with `extra="allow"` (deskops'
  TaskDoc) whose documents carry undeclared frontmatter keys. Such a key is still produced by
  the current class, so it is not a field the model dropped; the check only counts a key the
  current extraction of the same document no longer yields. `stores update` could never clear
  the old finding.
- A template whose frontmatter is one `dict` placeholder (`⸢rev,dict•frontmatter⸥`) declares
  every key: `docs track` and `docs create` no longer refuse a document's extra keys, which that
  dict carries back on re-render.
- `producer.version` in a semantic export is the real package version: read from the source
  checkout's `pyproject.toml`, else from the installed `structuredLanguageDB` metadata. It
  asked for a distribution named `sldb`, which never exists, and always fell back to `0.1.0`.
- `click` is an optional extra (`pip install structuredLanguageDB[click]`), imported only when
  `ClickScanner` is used; it was imported unconditionally without being declared.
- `sldb.examples.pandoc_cv` ships in the wheel, with its Markdown files.
- `tools/check_identity.py` reads `git ls-files -z`: a quoted non-ASCII path no longer shows
  up as a top-level entry named `"docs`.

## 0.1.10 - 2026-10-17 — references to a relation type reach it; a document by absolute path

- A `__references__` field that points at `RelationTypeDoc:<doc>` now lands on the
  `sldb://relation_type/<name>` node. The index stores relation types under that node, so the
  schema edge used to point at a document node that does not exist and was dropped silently
  while `doc_exists` said yes. `resolve_edges` moves that end to the relation-type node.
- `find_doc` (behind untrack and delete) accepts a document's absolute path as well as the path
  relative to the project root.
- Design notes for the surface in `docs/surface/`, with tests for the MachineDoc editor and an
  optimistic-lock client. The editor test compiles on Python 3.10/3.11 (no nested PEP 701
  f-string).

## 0.1.9 - 2026-10-16 — a dropped field is a contract move, and `stores update` fixes it

- A document whose `field_hashes` name a field its model no longer declares was signed under
  another contract. Any write of another document of the model re-stamps the model's contract,
  so the model looked unmoved: `stores check` blamed the untouched document (`data_mutation`,
  "confirm the change was intended") and `stores update` trusted its unchanged text and never
  re-extracted it, so the check stayed red. Now the model reads as `contract moved` (safe to
  run: `stores update`) and `stores update` re-extracts those documents.

## 0.1.8 - 2026-10-16 — a deleted model class no longer locks the store

- Derived-index rebuilds skip a model whose class does not import instead of raising; the
  semantic rebuild names it in `models_unresolved`, as the edge rebuild already did, and its
  documents keep their last tags. `untrack_document` (and every write that rebuilds) works
  while another registered model's class is gone.
- `sldb models remove <name> --with-documents` / `remove_model(..., untrack_documents=True)`:
  drops a model and its tracked documents without importing the class; the Markdown files stay.
- A write that raises halfway leaves no trace: `untrack_document` puts the document's shard,
  the models index and the store index back as they were; `remove_model` changes the registry
  first and deletes the model's files only once every rebuild succeeded.

## 0.1.7 - 2026-10-16 — `models remove`

- `sldb models remove <name>` / `sldb.api.remove_model(store, name)`: unregisters a model that
  tracks no documents, with its indexes and shards; the class is never imported, so a model
  whose code was deleted can go. A model that still tracks documents is refused (untrack them
  first). `stores check` already passes with such a model registered (0.1.5); its note now
  names the unimportable models with no documents as removable.

## 0.1.6 - 2026-10-16 — the graph as a state machine

- `--where` joins predicates with ` and ` (outside literals; no `or`, no parentheses), and
  `nonempty(f)` is `has(f)` that also rejects `[]` and `{}` (`has` keeps its meaning).
- `sldb.api.where_matches(expression, payload, subject=None)`: a `--where` predicate on a plain
  payload, tracked or not; `{field}` fills from `subject` (default: the payload). An unparseable
  part raises `WherePredicateError`, now exported from `sldb.api`.
- `sldb.api.edges_holding(store, node, subject, relation=None)`: the edges leaving a node whose
  condition (the edge's, else its type's) holds on the subject; `sldb edges show <node>
  --holds-for <doc>` is the same from the CLI. A self-loop is a valid edge (a terminal
  transition).

## 0.1.5 - 2026-10-16 — an unimportable model is named, not blamed on its documents

- `stores check`: when a model's class cannot be imported (a clean clone without the model's
  package, a consumer's CI with another `sldb` first on PATH), its fields cannot be
  re-extracted. Every document used to read as a `data_mutation` ("decide first", restore the
  file). Intact text now stands for intact fields, and the report names the unresolved models;
  changed text still fails. JSON: `models[].resolved`.
- CI: the structural gates pass (`legacy_contract` mapped to the `migracion` axis, unit coupling
  updated; the surface gate no longer compares the five-consumer total with a partial view),
  and `selfdoc check` passes (knowledge/ synced with the CLI, the store committed with it).

## 0.1.4 - 2026-10-16 — `fields update` leaves the store passing

- A field write (`fields update|append`, `sldb.api.save_document_payload`) rewrote the Markdown
  and the model's roster but not the document's record, so `stores check` failed with a
  `data_mutation` on the write sldb had just made. The shard cache handed out its own instance:
  the caller edited it in place and the save, comparing against the cache, saw no change and
  skipped the write. Loads now return a copy (`sldb.store.io.shards`), which also covers the
  semantic, sections and edges shards.

## 0.1.3 - 2026-10-16 — upgrading sldb no longer fails unchanged stores

Found on Governance's `pulse`, which installs sldb from git: both checks failed on a store whose
content had not changed.

- `stores check`: a model whose stored contract hash equals the formula sldb used before
  cecd97b (fields and template only) passes, with a note naming those models, instead of
  "contract moved" on every model. A class that really changed still fails. `stores update`
  re-seals the hash under the current formula. JSON: `models[].legacy_contract`.
- `edges check`: in a store that ran `edges init`, an edge sldb derives itself whose builtin
  type was added later (`composes`) is checked against the definition sldb ships and reported in
  `untracked_builtins`, not as an error. A store that never ran `edges init` still fails;
  authored edges still need a tracked type.

## 0.1.2 - 2026-10-16 — referencing documents of linked stores

- `stores add` links were recorded but no document lookup read them: `docs show
  alias:doc` answered `Unknown document target`. `docs show` (and `sections show|fields`,
  serve's document routes) now take `alias:ref` — name, `Model/name` or tracked path — and
  read only the store linked directly as `alias`. A bare ref still reads only the local store;
  a prefix that names no link leaves the ref whole, so existing refs resolve as before.
- Add `docs exists <[alias:]ref>` and `sldb.api.doc_status|doc_exists`: whether a reference
  resolves, from the indexes alone (no model import, nothing written). Exit 0 ok, 1 missing,
  2 ambiguous, 5 `link-missing` / `link-broken`, so a missing document is told apart from a
  sibling repo that is not there.
- `stores list` (and `sldb.api.store_links`) report each link's state: `ok`, `missing` or
  `not-a-store`; a broken link is reported, never raised.
- `stores add` records the link relative to the project root (it was absolute outside it), and
  refuses linking a store to itself, aliases outside `[A-Za-z0-9][A-Za-z0-9._-]*` and the
  reserved `local`. Links already written are read as before.
- `stores init` seals the root hash over the empty model layer: a new store, or one that
  only links others, passes `stores check` without a `stores update`.
- `docs show` of a linked doc reads its file from the linked project (`absolute_path` was
  built from the local root).

## 2026-10-01 — SLDB is the substrate again

- The README no longer calls this generation frozen: the v2 seed (`knowledge`) was frozen in
  turn and its evaluator moved to `pron`, so nothing supersedes this package. SLDB is the
  store every surface (`surface/`, `tools/graph_ui`, `tools/sldb-ui`) is a view over. <!-- gone -->
- New README section "Serving and surfaces": `sldb serve` routes grouped by what a UI needs,
  and where the surfaces and their design docs live.

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

## Working tree — `docs delete`

- Add `docs delete` (and `sldb.api.delete_document`): untrack a document **and** remove
  its Markdown file. `docs untrack` was the only way to drop a document, and it keeps
  the file on purpose — so "delete this document" meant untrack, then `rm` by hand, then
  remember that `runtime/cache/extracted.json` still describes the deleted path until
  some later full load rewrites it. `delete` does the three.
- Confirms before removing the file unless `--yes` is given; a non-interactive stdin
  answers no.
- Add `runtime_cache_disk.forget(store, predicate)` so cache entries can be dropped
  without a full store load.

## Working tree — self-documentation follow-up

- Add `selfdoc scan|sync|check` to derive CLI facts from argparse, preserve authored explanations, and synchronize tracked command/surface documents from the selected store root.
- Report obsolete documents without deleting them; check freshness without writing documents or indexes.
- Expose public parser help for the supported `init` and `example` commands.
- Split knowledge document definitions into one class per file, keeping public import references and resolving re-exported definitions for template editing.
- Separate follow-up work into self-documentation, store context/federation, and AST ownership/section contracts. No package version bump or publication is included.

## Historical pending changes

- Add reversible `rev,table[...]` template markers for rendering and extracting Markdown tables backed by `list[dict]` fields.
- Add generic cross-store document writes through linked store aliases and federated model namespaces for workflow tools such as `deskops`.

## 0.2.0 - 2026-05-16

- **Store write concurrency**: atomic writes + advisory `fcntl` locks on all index write paths; `--wait` flag for `stores update`
- **Rebuild auditability**: `RebuildReport` dataclass tracks missing docs, empty sections, and unparseable headings in both semantic and section rebuilds; `--verbose` flag for details
- **CLI deprecation surface**: old singular commands (`store`, `model`, `doc`, `ls`, `get`, etc.) emit deprecation warnings; v0.6 was the historical removal target (see freeze note above).
- **Read-side hot path**: `sections show` and `sections fields` prefer persisted index over full IR rebuild; `--rebuild` flag available on `find`/`sections find`
- **Marker ownership robustness**: field name from the canonical `parse_marker()` is validated against known payload paths; unknown markers log a warning

## 0.1.2 - 2026-04-24

- Reorganize the package into `core`, `models`, `runtime`, `cli`, `assets`, and `examples` subpackages while keeping compatibility re-exports
- Add explicit link recovery and transclusion composition with `recover` and `compose`
- Add structural store queries under `st` with `ls`, `get`, `glob`, and `find --where`
- Add store-local semantic indexing under `se` and explicit federated semantic navigation under `gse`
- Add model semantic metadata, canonical model registration, semantic equivalence mapping, and bundled tests for the new workflows

## 0.1.1 - 2026-04-24

- Add current-system architecture docs and diagrams under `docs/architecture/`
- Add feature proposal docs under `desk/` for future SLDB features: link/recover/compose, store tree indexing, semantic DAG indexing, canonical/global-local semantics
- Add desk workspace with task board, self-docs, and operating procedures

## 0.1.0 - 2026-04-21

- Rename the package and CLI from `nldb` to `sldb`
- Add safe-by-default Python marker execution with configurable unsafe mode
- Ship the SLDB example bundle and CLI workflows for extract, render, validate, init, and example
- Add release basics: MIT license, package metadata, and CI

FILE:instruccion
Cold-bundle de la tarea task-go07-anclas-a-documentos-con-hash-de-contrato: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest tests/api/test_doc_anchors.py sin fallos ni saltados
- A con subject en __doc_anchors__ guardado con doc:TaskDoc:b queda pinneado con el hash de B; editar un campo del __contract__ de B -> changed; editar fuera del contrato -> intact; borrar B -> lost; anchors check lo reporta como alertas
- modelo Review (subject en __doc_anchors__, verdict) y Task B: any(^subject: anchor_state = "intact" and verdict = "accepted") true con Review intacta y accepted; false sin Review, con verdict distinto o con el ancla changed
- valor no doc: en subject rechazado al escribir; un test de rechazo por forma invalida (tambien en from:) y por definicion de modelo invalida
- from: doc:B emite anchors/provenance_changed tras editar el contrato de B
- tests existentes de anclas de codigo, provenance, proyeccion (test_payload_projection) y lenguaje (test_predicate_language, spec GO02) sin cambios
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

