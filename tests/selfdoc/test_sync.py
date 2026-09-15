"""End-to-end materialization, preservation, and store queries."""
import importlib
import json

from sldb.cli.main import main
from sldb.models.knowledge_surface import CliCommandDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def test_sync_from_subdirectory_tracks_documents_and_then_is_noop(project, invoke, monkeypatch, capsys):
    child = project / "src" / "nested"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)
    code, report = invoke("sync")
    assert code == 0 and report["written"] == 2
    assert (project / "knowledge/commands/cmd-widget-run.md").exists()
    before = snapshot(project)
    assert invoke("check")[0] == 0
    assert invoke("sync")[1]["written"] == 0
    assert snapshot(project) == before
    assert main(["fields", "show", "docs/cmd-widget-run/command_path"]) == 0
    assert json.loads(capsys.readouterr().out) == {"value": "run"}
    assert main(["stores", "check", "--format", "json"]) == 0


def test_parser_drift_preserves_authored_explanations_and_examples(project, invoke):
    assert invoke("sync")[0] == 0
    path = project / "knowledge/commands/cmd-widget-run.md"
    payload = extract_model_data(CliCommandDoc, path.read_text())
    payload.update(purpose="An authored purpose.", how_it_works="An authored explanation.",
                   usage="widget run --limit 1", tags=["topic:authored"])
    path.write_text(render_model_markdown(CliCommandDoc, payload) + "\n")
    importlib.import_module("selfdoc_test_factory").DEFAULT = 7
    before = snapshot(project)
    code, report = invoke("check")
    assert code == 1 and "knowledge/commands/cmd-widget-run.md" in report["changed"]
    assert snapshot(project) == before
    assert invoke("sync")[0] == 0
    updated = extract_model_data(CliCommandDoc, path.read_text())
    for field in ("purpose", "how_it_works", "usage", "tags"):
        assert updated[field] == payload[field]
    assert '"default": "7"' in updated["arguments"]
    assert updated["provenance"] != payload["provenance"]


def test_removed_commands_are_reported_and_retained(project, invoke):
    assert invoke("sync")[0] == 0
    importlib.import_module("selfdoc_test_factory").REMOVED = True
    code, report = invoke("sync")
    assert code == 1
    assert len(report["removed"]) == 2
    assert (project / "knowledge/commands/cmd-widget-run.md").exists()


def test_removed_and_deleted_command_remains_visible_through_its_registration(project, invoke):
    assert invoke("sync")[0] == 0
    importlib.import_module("selfdoc_test_factory").REMOVED = True
    (project / "knowledge/commands/cmd-widget-run.md").unlink()
    assert "knowledge/commands/cmd-widget-run.md" in invoke("check")[1]["removed"]


def test_missing_generated_file_is_recreated_and_tracking_repaired(project, invoke):
    assert invoke("sync")[0] == 0
    (project / "knowledge/commands/cmd-widget-run.md").unlink()
    assert invoke("check")[1]["missing"] == ["knowledge/commands/cmd-widget-run.md"]
    assert invoke("sync")[0] == 0
    assert invoke("check")[0] == 0
