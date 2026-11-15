import yaml
from pathlib import Path
from sldb.models.notation.diagram_specs.deployment import DeploymentDiagram

FIXTURE = Path(__file__).parent.parent / "fixtures" / "specs" / "deployment.runtime.yml"

def test_deployment_loads():
    data = yaml.safe_load(FIXTURE.read_text())
    d = DeploymentDiagram.model_validate(data)
    assert d.id == "deployment.runtime"
    assert d.type.value == "deployment"

def test_deployment_nodes():
    data = yaml.safe_load(FIXTURE.read_text())
    d = DeploymentDiagram.model_validate(data)
    assert "browser" in d.data.nodes
    assert d.data.nodes["browser"].kind == "client"
    assert "quotation_ui" in d.data.nodes["browser"].contains

def test_deployment_artifacts():
    data = yaml.safe_load(FIXTURE.read_text())
    d = DeploymentDiagram.model_validate(data)
    assert "quotation_ui" in d.data.artifacts
    assert d.data.artifacts["quotation_ui"].kind == "frontend"

def test_deployment_connections():
    data = yaml.safe_load(FIXTURE.read_text())
    d = DeploymentDiagram.model_validate(data)
    assert len(d.data.connections) == 1
    conn = d.data.connections[0]
    assert conn.from_ == "quotation_ui"
    assert conn.protocol == "HTTPS"
