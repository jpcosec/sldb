"""The GraphBackend seam: goldens, the spy, eval, and the store.yaml selection."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from sldb.cli import main as cli_main
from tests.api.test_api_graph_analysis import MODELS, MODULE, AnalysisWorld

GOLDENS = Path(__file__).resolve().parents[1] / "fixtures" / "graph_goldens"
S1 = "sldb://document/Spec:s1"
S3 = "sldb://document/Spec:s3"

GOLDEN_COMMANDS = {
    "path": ["graph", "path", S3, S1],
    "cycles": ["graph", "cycles"],
    "order": ["graph", "order"],
    "components": ["graph", "components"],
    "central": ["graph", "central", "--kind", "degree"],
    "similar": ["graph", "similar", S1],
}


def _world(tmp_path: Path) -> AnalysisWorld:
    """The same store `tests/api/test_api_graph_analysis.py` builds for its `world` fixture."""
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    return AnalysisWorld(tmp_path)


def test_graph_goldens(tmp_path: Path):
    """The six `sldb graph` analyses print exactly what they printed before the seam."""
    world = _world(tmp_path)
    for name, argv in GOLDEN_COMMANDS.items():
        output = io.StringIO()
        with redirect_stdout(output):
            code = cli_main([*argv, "--store", str(world.store)])
        assert code == 0, name
        expected = (GOLDENS / f"{name}.txt").read_bytes()
        assert output.getvalue().encode("utf-8") == expected, name


# --- the seam: every command and API function asks the backend ---------------------------

def test_every_api_analysis_and_every_cli_command_calls_the_backend(tmp_path: Path):
    """The ten functions of `api/graph/analyze.py` and the six `sldb graph` commands."""
    from sldb.api.graph import (
        graph_central,
        graph_components,
        graph_cycles,
        graph_isolated,
        graph_islands,
        graph_layers,
        graph_order,
        graph_path,
        graph_paths,
        graph_similar,
    )
    from sldb.cli.commands.graph import GraphCLI
    from sldb.cli.parser import build_parser

    world = _world(tmp_path)
    api_calls = [
        ("path", lambda backend: graph_path(world.store, S3, S1, backend=backend)),
        ("paths", lambda backend: graph_paths(world.store, S3, S1, backend=backend)),
        ("cycles", lambda backend: graph_cycles(world.store, backend=backend)),
        ("order", lambda backend: graph_order(world.store, backend=backend)),
        ("layers", lambda backend: graph_layers(world.store, backend=backend)),
        ("components", lambda backend: graph_components(world.store, backend=backend)),
        ("islands", lambda backend: graph_islands(world.store, backend=backend)),
        ("isolated", lambda backend: graph_isolated(world.store, backend=backend)),
        ("central", lambda backend: graph_central(world.store, kind="degree", backend=backend)),
        ("similar", lambda backend: graph_similar(world.store, S1, backend=backend)),
    ]
    for operation, call in api_calls:
        spy = _Spy()
        call(spy)
        assert [op for op, _ in spy.operations] == [operation], operation
        assert len(spy.loads) == 1 and spy.loads[0][1] is None, operation

    cli_calls = [
        ("path", ["graph", "path", S3, S1]),
        ("cycles", ["graph", "cycles"]),
        ("order", ["graph", "order"]),
        ("components", ["graph", "components"]),
        ("central", ["graph", "central", "--kind", "degree"]),
        ("similar", ["graph", "similar", S1]),
    ]
    parser = build_parser()
    for operation, argv in cli_calls:
        spy = _Spy()
        args = parser.parse_args([*argv, "--store", str(world.store)])
        output = io.StringIO()
        with redirect_stdout(output):
            assert GraphCLI(backend=spy).run(args) == 0, operation
        assert [op for op, _ in spy.operations] == [operation], operation
        assert len(spy.loads) == 1 and spy.loads[0][1] is None, operation


class _Spy:
    """A GraphBackend that records the operations it is asked for and answers empty."""

    def __init__(self) -> None:
        self.loads: list[tuple[object, object]] = []
        self.operations: list[tuple[str, dict]] = []

    def load(self, index, projection=None) -> None:
        self.loads.append((index, projection))

    def eval(self, predicate, subject=None) -> list:
        return []

    def analyze(self, operation: str, **args):
        self.operations.append((operation, args))
        return []


# --- the composed index of this repository ----------------------------------------------

def test_the_repository_composed_index_loads_into_the_backend():
    from sldb.store.edge_index.compose import compose_edge_index
    from sldb.store.graph.backend import NetworkXBackend

    root = Path(__file__).resolve().parents[2]
    index = compose_edge_index(root / ".sldb")
    backend = NetworkXBackend()
    assert backend.load(index, None) is None
    assert index.nodes and backend.analyze("components", relations=None, node_types=None)


# --- eval: the GO02 subset, no paths ----------------------------------------------------

def test_eval_returns_one_finding_with_the_go02_shape():
    from sldb.store.edge_index.edge_index import EdgeIndex
    from sldb.store.graph.backend import NetworkXBackend

    backend = NetworkXBackend()
    backend.load(EdgeIndex(), None)
    findings = backend.eval('has(id) and status != "x"', {"id": "Task:a", "status": "open"})
    assert len(findings) == 1
    finding = findings[0]
    assert set(finding) == {"node", "holds", "clause", "seen"}
    assert finding["node"] == "Task:a"
    assert finding["holds"] == "true"
    assert finding["seen"]["status"] == "open"


def test_eval_with_a_path_is_not_implemented_yet():
    import pytest

    from sldb.store.graph.backend import NetworkXBackend

    backend = NetworkXBackend()
    with pytest.raises(NotImplementedError):
        backend.eval('any(depends_on: status = "open")', {"id": "Task:a"})


def test_eval_by_export_id_without_projection_says_so():
    import pytest

    from sldb.store.graph.backend import NetworkXBackend

    backend = NetworkXBackend()
    with pytest.raises(ValueError, match="sin proyección para Spec:s1"):
        backend.eval("has(id)", "Spec:s1")


# --- store.yaml: graph_backend selection -------------------------------------------------

def _declared(tmp_path: Path, body: str) -> Path:
    store = tmp_path / ".sldb"
    store.mkdir()
    (store / "store.yaml").write_text(body, encoding="utf-8")
    return store


def test_an_absent_graph_backend_key_means_networkx(tmp_path: Path):
    from sldb.store.graph.backend import NetworkXBackend, backend_for

    store = _declared(tmp_path, "version: 1\n")
    assert isinstance(backend_for(store), NetworkXBackend)


def test_explicit_networkx_is_accepted(tmp_path: Path):
    from sldb.store.graph.backend import NetworkXBackend, backend_for

    store = _declared(tmp_path, "version: 1\ngraph_backend: networkx\n")
    assert isinstance(backend_for(store), NetworkXBackend)


def test_another_graph_backend_fails_with_the_defined_message(tmp_path: Path):
    import pytest

    from sldb.store.graph.backend import backend_for

    store = _declared(tmp_path, "version: 1\ngraph_backend: neo4j\n")
    with pytest.raises(ValueError) as caught:
        backend_for(store)
    assert str(caught.value) == 'graph_backend neo4j no admitido; admitidos: ["networkx"]'
