import yaml
from pathlib import Path
from sldb.models.notation.diagram_specs.component import ComponentDiagram

FIXTURE = Path(__file__).parent.parent / "fixtures" / "specs" / "component.quotation.yml"

def test_component_loads():
    data = yaml.safe_load(FIXTURE.read_text())
    d = ComponentDiagram.model_validate(data)
    assert d.id == "component.quotation"
    assert d.type.value == "component"

def test_component_nodes():
    data = yaml.safe_load(FIXTURE.read_text())
    d = ComponentDiagram.model_validate(data)
    assert "QuotationFlow" in d.data.nodes
    node = d.data.nodes["QuotationFlow"]
    assert node.kind == "core"
    assert "ClientSelection" in node.contains

def test_component_edges():
    data = yaml.safe_load(FIXTURE.read_text())
    d = ComponentDiagram.model_validate(data)
    assert len(d.data.edges) == 2
    edge = d.data.edges[0]
    assert edge.from_ == "QuotationFlow"
    assert edge.to == "Store"
    assert edge.relation == "reads_writes"
    assert edge.label == "reads/writes"
