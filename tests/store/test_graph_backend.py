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
