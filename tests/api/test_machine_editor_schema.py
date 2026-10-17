"""Real SLDB graph editor accepts the canonical machine schemas (stage 16).

Ejercita el editor genérico del grafo (la superficie de SLDB) con los schemas de la
fixture canónica: `MachineDoc`/`StateDoc`/`TransitionDoc`/`EventTypeDoc`/`GuardDoc`
declaran `__references__`/`__containment__`; el editor escribe por payload (el `/save`
de la superficie con `expected`, lock optimista) y SLDB re-renderiza y verifica el
roundtrip. Cubre:

- campos de MachineDoc/TransitionDoc rondatrip por payload (write por dirección, no Markdown);
- las aristas tipadas del grafo salen de los refs autorados tras `rebuild_edges`;
- el cambio de una transición es reversible (payload nuevo → Markdown → vuelve igual) y
  `rebuild_edges` actualiza el grafo sin pisar documento ajeno;
- conflicto concurrente (un `expected` obsoleto) se rechaza sin pisar el cambio.

Usa el API real de sldb (raíz pública + `cli.serve.save_plan.prevalidate` para el lock
optimista del editor), el mismo pin d877dad instalado en INFRA.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

from sldb import api

MODEL_ROOT = Path("/home/jp/AntonIA/repos/AgentsKBs_worktrees/rebuild-kb-cobranza")
MODULE = "kb_models.knowledge"

pytestmark = pytest.mark.skipif(not MODEL_ROOT.is_dir(), reason="needs the local kb_models checkout")


class MachineEditorWorld:
    """Un store preparado con los modelos de máquina canónica registrados (editor genérico)."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(MODEL_ROOT)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in (
            "MachineDoc",
            "StateDoc",
            "TransitionDoc",
            "EventTypeDoc",
            "GuardDoc",
            "ActionDoc",
            "RelationTypeDoc",
            "RelationDoc",
        ):
            module = {"RelationDoc": "sldb.models.relation_doc", "RelationTypeDoc": "sldb.models.relation_type_doc"}.get(model, MODULE)
            api.add_model(self.store, f"{module}:{model}", self.py)
        api.init_relations(self.store, self.py)
        self.store_path = api.open_store(self.store).store_path

    def create(self, model: str, name: str, payload: dict) -> None:
        payload = _defaults(model, name, payload)
        api.create_document(self.store, model, self.root / f"{model}" / f"{name}.md", payload, name, self.py)

    def payload(self, model: str, name: str) -> dict[str, Any]:
        return api.extract_document_payload(self.store_path, self.py, name)

    def save(self, model: str, name: str, payload: dict) -> None:
        api.save_document_payload(self.store, model, name, _defaults(model, name, payload), self.py)

    def rebuild(self) -> None:
        api.rebuild_edges(self.store, self.py)

    def edges_of(self, doc: str, relation: str | None = None) -> list:
        self.rebuild()
        return api.edges_from(self.store, doc, relation)


@pytest.fixture
def world(tmp_path: Path) -> MachineEditorWorld:
    sys.path.insert(0, str(MODEL_ROOT))
    try:
        yield MachineEditorWorld(tmp_path)
    finally:
        sys.path.remove(str(MODEL_ROOT))


def _defaults(model: str, name: str, payload: dict[str, Any]) -> dict[str, Any]:
    if model in ("RelationDoc", "RelationTypeDoc"):
        return payload
    result = {"id": name, "summary": name, **payload}
    if model in ("MachineDoc", "ActionDoc"):
        result.setdefault("version", [1, 0, 0])
    if model == "MachineDoc":
        result.setdefault("family", "consent")
        result.setdefault("initial_state_ref", "StateDoc:solicitado")
        result.setdefault("state_refs", ["StateDoc:solicitado", "StateDoc:otorgado"])
    if model == "EventTypeDoc":
        result.setdefault("machine_ref", "MachineDoc:consentimiento")
        result.setdefault("payload_schema", {"type": "object"})
    if model == "ActionDoc":
        result.pop("hash", None)
        result.setdefault("description", "Register consent")
    return result


def build_machine(world: MachineEditorWorld) -> None:
    """Fixture: una máquina de consentimiento con dos estados y una transición."""
    world.create("MachineDoc", "consentimiento", {"title": "Consentimiento"})
    world.create("EventTypeDoc", "otorgar", {"title": "Otorgar", "name": "otorgar"})
    world.create("StateDoc", "solicitado", {"machine_ref": "MachineDoc:consentimiento", "title": "Solicitado"})
    world.create("StateDoc", "otorgado", {"machine_ref": "MachineDoc:consentimiento", "title": "Otorgado"})
    world.create("ActionDoc", "registrar", {"title": "Registrar", "hash": "a" * 64})
    world.create(
        "TransitionDoc",
        "t1",
        {
            "title": "otorgar",
            "machine_ref": "MachineDoc:consentimiento",
            "source_ref": "StateDoc:solicitado",
            "target_ref": "StateDoc:otorgado",
            "event_type_ref": "EventTypeDoc:otorgar",
            "action_refs": ["ActionDoc:registrar"],
            "priority": 10,
        },
    )
    # el editor genérico agrega los miembros de la máquina por payload (aditivo)
    world.save(
        "MachineDoc",
        "consentimiento",
        {
            "title": "Consentimiento",
            "initial_state_ref": "StateDoc:solicitado",
            "state_refs": ["StateDoc:solicitado", "StateDoc:otorgado"],
            "transition_refs": ["TransitionDoc:t1"],
            "event_type_refs": ["EventTypeDoc:otorgar"],
        },
    )


def _relation_type(world: MachineEditorWorld, name: str, source: list[str], target: list[str]) -> None:
    """Declarar un tipo de relación de grafo de máquina (RelationTypeDoc en la KB)."""
    world.create(
        "RelationTypeDoc",
        f"rt-{name}",
        {
            "title": name,
            "name": name,
            "direction": "directed",
            "cardinality": "many_to_many",
            "axis": "WHERE",
            "source_types": source,
            "target_types": target,
            "condition": "",
            "description": f"{name}.",
        },
    )


def _relation(world: MachineEditorWorld, name: str, src: str, tgt: str, rtype: str) -> None:
    """Autorar una arista tipada del grafo de máquina (RelationDoc)."""
    world.create(
        "RelationDoc",
        name,
        {
            "title": name,
            "source_id": src,
            "target_id": tgt,
            "relation_type": rtype,
            "condition": "",
            "notes": "",
        },
    )


def _machine_graph_edges(world: MachineEditorWorld) -> None:
    """Autorar las 9 relaciones de grafo canónicas que usa el compilador (api-canonica)."""
    _relation_type(world, "has_state", ["MachineDoc"], ["StateDoc"])
    _relation_type(world, "starts_at", ["MachineDoc"], ["StateDoc"])
    _relation_type(world, "transition_from", ["TransitionDoc"], ["StateDoc"])
    _relation_type(world, "transition_to", ["TransitionDoc"], ["StateDoc"])
    _relation_type(world, "triggered_by", ["TransitionDoc"], ["EventTypeDoc"])
    _relation_type(world, "invokes_action", ["TransitionDoc"], ["ActionDoc"])
    _relation(world, "m-has-s", "MachineDoc:consentimiento", "StateDoc:solicitado", "has_state")
    _relation(world, "m-has-o", "MachineDoc:consentimiento", "StateDoc:otorgado", "has_state")
    _relation(
        world, "trans-from", "TransitionDoc:t1", "StateDoc:solicitado", "transition_from"
    )
    _relation(world, "trans-to", "TransitionDoc:t1", "StateDoc:otorgado", "transition_to")
    _relation(world, "trans-trig", "TransitionDoc:t1", "EventTypeDoc:otorgar", "triggered_by")
    _relation(world, "trans-act", "TransitionDoc:t1", "ActionDoc:registrar", "invokes_action")
    world.rebuild()


def _pairs(edges) -> set[tuple[str, str]]:
    return {(str(e.target), str(e.relation)) for e in edges}


def _edge_type_into(edges: set[tuple[str, str]], target: str) -> set[str]:
    return {rel for (t, rel) in edges if t == target}


def test_machine_doc_y_transition_fields_roundtrip_por_payload(world: MachineEditorWorld) -> None:
    """El editor escribe por payload (nunca Markdown) y SLDB verifica el roundtrip."""
    build_machine(world)
    back = world.payload("TransitionDoc", "t1")
    assert back["source_ref"] == "StateDoc:solicitado"
    assert back["target_ref"] == "StateDoc:otorgado"
    assert back["priority"] == 10
    machine = world.payload("MachineDoc", "consentimiento")
    assert machine["initial_state_ref"] == "StateDoc:solicitado"
    assert machine["transition_refs"] == ["TransitionDoc:t1"]


def test_las_aristas_tipadas_del_grafo_salen_de_los_refs_y_relaciones_autoradas(
    world: MachineEditorWorld,
) -> None:
    """El grafo real deriva references/contains de los refs y las 9 relaciones tipadas."""
    build_machine(world)
    _machine_graph_edges(world)
    # relation_doc authorados: transition_from/to, triggered_by, invokes_action, has_state
    trans = _pairs(world.edges_of("TransitionDoc:t1"))
    assert "transition_from" in _edge_type_into(trans, "sldb://document/StateDoc:solicitado")
    assert "transition_to" in _edge_type_into(trans, "sldb://document/StateDoc:otorgado")
    assert "triggered_by" in _edge_type_into(trans, "sldb://document/EventTypeDoc:otorgar")
    assert "invokes_action" in _edge_type_into(trans, "sldb://document/ActionDoc:registrar")
    mach = _pairs(world.edges_of("MachineDoc:consentimiento"))
    assert "has_state" in _edge_type_into(mach, "sldb://document/StateDoc:solicitado")
    assert "has_state" in _edge_type_into(mach, "sldb://document/StateDoc:otorgado")


def test_las_references_y_contains_salen_de_los_dunder_declarativos(world: MachineEditorWorld) -> None:
    """Los refs de campos (references/containment) aparecen como aristas estructurales."""
    build_machine(world)
    world.rebuild()
    trans = _pairs(world.edges_of("TransitionDoc:t1"))
    assert ("sldb://document/MachineDoc:consentimiento", "contains") in trans
    assert ("sldb://document/StateDoc:solicitado", "contains") in trans
    mach = _pairs(world.edges_of("MachineDoc:consentimiento"))
    assert ("sldb://document/StateDoc:solicitado", "contains") in mach
    assert ("sldb://document/TransitionDoc:t1", "contains") in mach


@pytest.mark.parametrize("source,target", [("otorgado", "solicitado"), ("solicitado", "otorgado")])
def test_el_cambio_de_transicion_es_reversible_y_actualiza_el_grafo(
    world: MachineEditorWorld, source: str, target: str
) -> None:
    """Mover los extremos de una transición roundtripea y las refs del grafo cambian.

    El genérico SLDB deriva `references` de los campos `source_ref`/`target_ref`/etc.;
    moverlos actualiza las refs estructurales. Las relaciones tipadas se re-autoran en
    los RelationDoc para mantener paridad tras el movimiento (el compilador exige la
    paridad, 03).
    """
    build_machine(world)
    _machine_graph_edges(world)
    current = world.payload("TransitionDoc", "t1")
    current["source_ref"] = f"StateDoc:{source}"
    current["target_ref"] = f"StateDoc:{target}"
    world.save("TransitionDoc", "t1", current)
    back = world.payload("TransitionDoc", "t1")  # re-extracción = reversible
    assert back["source_ref"] == f"StateDoc:{source}"
    assert back["target_ref"] == f"StateDoc:{target}"

    # re-autorar las relaciones tipadas para el nuevo extremo (paridad ref <-> grafo)
    existing_from = world.payload("RelationDoc", "trans-from")
    existing_to = world.payload("RelationDoc", "trans-to")
    existing_from["source_id"] = f"TransitionDoc:t1"
    existing_from["target_id"] = f"StateDoc:{source}"
    world.save("RelationDoc", "trans-from", existing_from)
    existing_to["source_id"] = f"TransitionDoc:t1"
    existing_to["target_id"] = f"StateDoc:{target}"
    world.save("RelationDoc", "trans-to", existing_to)

    world.rebuild()
    edges = _pairs(world.edges_of("TransitionDoc:t1"))
    assert "transition_from" in _edge_type_into(edges, f"sldb://document/StateDoc:{source}")
    assert "transition_to" in _edge_type_into(edges, f"sldb://document/StateDoc:{target}")
    # la ref estructural del campo actualizada también está presente
    assert (f"sldb://document/StateDoc:{source}", "contains") in edges
    # el extremo previo dejó de ser origen tipado
    other = "otorgado" if source == "solicitado" else "solicitado"
    assert "transition_from" not in _edge_type_into(edges, f"sldb://document/StateDoc:{other}")


def test_el_conflicto_concurrente_se_rechaza_sin_pisar_el_cambio(world: MachineEditorWorld) -> None:
    """`expected` obsoleto => 409 del `/save`: el lock optimista no sobrescribe el cambio ajeno."""
    from sldb.cli.serve import save_plan

    build_machine(world)
    # escritor A cambia el destino y guarda
    moved = world.payload("TransitionDoc", "t1")
    moved["target_ref"] = "StateDoc:otorgado"
    world.save("TransitionDoc", "t1", moved)

    # escritor B partió del payload VIEJO (aún apuntaba a solicitado) y edita otro campo
    stale = dict(moved)
    stale["priority"] = 99
    stale_expected = {"source_ref": "StateDoc:solicitado", "target_ref": "StateDoc:solicitado"}

    change = {
        "id": "TransitionDoc:t1",
        "action": "update",
        "model": "TransitionDoc",
        "payload": stale,
        "expected": stale_expected,
    }
    existing = _existing_doc(world, "TransitionDoc", "t1")
    _path, error = save_plan.prevalidate(
        change,
        "t1",
        {"TransitionDoc:t1": existing},
        [],
        world.store_path,
        world.root,
        world.py,
    )
    assert error is not None
    assert error[1] == 409
    # y el doc real NO quedó pisado con priority 99: sigue en otorgado y priority 10
    real = world.payload("TransitionDoc", "t1")
    assert real["target_ref"] == "StateDoc:otorgado"
    assert real["priority"] == 10


def _existing_doc(world: MachineEditorWorld, model: str, name: str) -> Any:
    """Forma mínima que `prevalidate` lee del doc corriente: `.payload` y `.model_name`."""
    return _ExistingDoc(name, model, world.payload(model, name))


class _ExistingDoc:
    def __init__(self, name: str, model_name: str, payload: dict) -> None:
        self.name = name
        self.model_name = model_name
        self.payload = payload

def test_actual_nested_guard_null_assignments_and_variables_schema(world: MachineEditorWorld) -> None:
    from kb_models.knowledge import GuardDoc, MachineDoc, TransitionDoc
    from pydantic import ValidationError

    build_machine(world)
    expression = {"op": "all", "children": [
        {"op": "eq", "path": ["event", "payload", "answer"], "value": None},
        {"op": "not", "children": [{"op": "exists", "path": ["event", "payload", "missing"]}]},
    ]}
    payload = _defaults("GuardDoc", "nested", {"title": "Nested", "expression": expression})
    assert GuardDoc.model_validate(payload).expression == expression
    world.create("GuardDoc", "nested", payload)
    assert world.payload("GuardDoc", "nested")["expression"] == expression
    with pytest.raises(ValidationError):
        GuardDoc.model_validate({**payload, "expression": {"op": "eq", "path": ["event", "payload"]}})
    with pytest.raises(ValidationError):
        GuardDoc.model_validate({**payload, "expression": {"op": "eval", "code": "1"}})
    transition = world.payload("TransitionDoc", "t1")
    transition["assignments"] = {"answer": {"literal": None}, "counter": {"snapshot_path": ["event", "payload", "count"]}}
    assert TransitionDoc.model_validate(transition).assignments == transition["assignments"]
    world.save("TransitionDoc", "t1", transition)
    assert world.payload("TransitionDoc", "t1")["assignments"] == transition["assignments"]
    machine = world.payload("MachineDoc", "consentimiento")
    machine["variables_schema"] = {"type": "object", "properties": {"answer": {"type": ["string", "null"]}}}
    assert MachineDoc.model_validate(machine).variables_schema == machine["variables_schema"]
    world.save("MachineDoc", "consentimiento", machine)
    assert world.payload("MachineDoc", "consentimiento")["variables_schema"] == machine["variables_schema"]
