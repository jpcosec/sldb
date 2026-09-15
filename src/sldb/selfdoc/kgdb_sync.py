"""Write regenerable Python source facts through KGDB's graph importer."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


def write_kgdb_snapshot(snapshot: dict, output: Path, command: str) -> None:
    """Atomically replace one KGDB graph through its public ingest command."""
    temporary = _snapshot_file(snapshot, output)
    try:
        _ingest(command, temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def _snapshot_file(snapshot: dict, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".json", dir=output.parent, delete=False, encoding="utf-8") as file:
        json.dump(snapshot, file); return Path(file.name)


def _ingest(command: str, temporary: Path, output: Path) -> None:
    try:
        subprocess.run([command, "ingest", "--input", str(temporary), "--output", str(output)], check=True, text=True, capture_output=True)
    except FileNotFoundError as error:
        raise ValueError(f"KGDB command not found: {command}") from error
    except subprocess.CalledProcessError as error:
        raise ValueError(error.stderr.strip() or "KGDB source graph ingestion failed") from error


def graph_is_current(snapshot: dict, output: Path) -> bool:
    """Check that KGDB retained every expected node with its source hash."""
    if not output.is_file():
        return False
    try:
        nodes = {node["id"]: node["schema"] for node in json.loads(output.read_text(encoding="utf-8"))["nodes"]}
    except (KeyError, TypeError, json.JSONDecodeError):
        return False
    expected = {node["identity"]["node_id"]: node for node in snapshot["nodes"]}
    return set(nodes) == set(expected) and all(_same_source(node, nodes[node_id]) for node_id, node in expected.items())


def _same_source(expected: dict, actual: dict | None) -> bool:
    if actual is None:
        return False
    return actual.get("source") == expected.get("source") and actual.get("ast") == expected.get("ast")
