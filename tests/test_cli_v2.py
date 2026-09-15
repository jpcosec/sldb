from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

from sldb.cli import main as cli_main
from sldb.store.io import load_documents_index, load_models_index, load_store_index


def _write_models(base: Path) -> str:
    sys.modules.pop("cli_v2_models", None)
    module = base / "cli_v2_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class RoadmapDoc(StructuredNLDoc):
    __semantics__ = {"type": ["documentation", "Readme"]}
    __template__ = """# ⸢rev•title⸥

Status: ⸢rev•status⸥

## Tasks

- ⸢rev,list•tasks⸥

## Semantic Tags

- ⸢rev,list•semantic_tags⸥
""".strip()
    title: str = Field(description="Document title.")
    status: str = Field(description="Workflow status.")
    tasks: list[str] = Field(description="Task items.")
    semantic_tags: list[str] = Field(description="Semantic tags.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def _write_federated_models(base: Path) -> str:
    sys.modules.pop("federated_models", None)
    module = base / "federated_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class RequestDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev,markdown•body⸥
""".strip()
    title: str = Field(description="Request title.")
    body: str = Field(description="Request body.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def _setup_store(tmp_path: Path) -> tuple[Path, str]:
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "repo"
    root.mkdir()
    store = root / ".sldb"
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "cli_v2_models:RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "create",
                "--model",
                "RoadmapDoc",
                "-o",
                str(root / "roadmap.md"),
                json.dumps(
                    {
                        "title": "Roadmap",
                        "status": "draft",
                        "tasks": ["Ship CLI", "Write docs"],
                        "semantic_tags": ["project.sldb.database"],
                    }
                ),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    return store, pythonpath


def _write_template(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def _model_index_path(store: Path, model_name: str) -> Path:
    entry = next(m for m in load_store_index(store).models if m.name == model_name)
    return store.parent / entry.models_index


def test_docs_create_accepts_long_inline_json_payload(tmp_path):
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "repo"
    root.mkdir()
    store = root / ".sldb"
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "cli_v2_models:RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    long_title = "x" * 300
    output = root / "long-inline.md"
    assert (
        cli_main(
            [
                "docs",
                "create",
                "--model",
                "RoadmapDoc",
                "-o",
                str(output),
                json.dumps(
                    {
                        "title": long_title,
                        "status": "draft",
                        "tasks": ["Ship CLI"],
                        "semantic_tags": ["project.sldb.database"],
                    }
                ),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    assert output.exists()
    assert f"# {long_title}" in output.read_text(encoding="utf-8")


def test_docs_create_accepts_linked_store_alias(tmp_path, monkeypatch):
    pythonpath = _write_federated_models(tmp_path)
    central = tmp_path / "central"
    target = tmp_path / "target"
    central.mkdir()
    target.mkdir()
    central_store = central / ".sldb"
    target_store = target / ".sldb"

    assert cli_main(["stores", "init", "--path", str(central)]) == 0
    assert cli_main(["stores", "init", "--path", str(target)]) == 0
    monkeypatch.chdir(central)
    assert (
        cli_main(
            [
                "models",
                "add",
                "federated_models:RequestDoc",
                "--store",
                str(target_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "stores",
                "add",
                str(target_store),
                "--name",
                "target",
                "--store",
                str(central_store),
            ]
        )
        == 0
    )

    assert (
        cli_main(
            [
                "docs",
                "create",
                "--store",
                "target",
                "--model",
                "RequestDoc",
                "-o",
                "desk/inbox/request-123.md",
                json.dumps({"title": "Need review", "body": "Please review this."}),
                "--pythonpath",
                pythonpath,
            ],
        )
        == 0
    )

    output = target / "desk" / "inbox" / "request-123.md"
    assert output.exists()
    assert "# Need review" in output.read_text(encoding="utf-8")
    docs_index = load_documents_index(
        target / ".sldb" / "core" / "documents" / "RequestDoc.yaml"
    )
    assert [doc.path for doc in docs_index.documents] == [
        "desk/inbox/request-123.md"
    ]


def test_docs_create_uses_model_from_linked_store_namespace(tmp_path, monkeypatch):
    pythonpath = _write_federated_models(tmp_path)
    central = tmp_path / "central"
    models_repo = tmp_path / "deskops"
    target = tmp_path / "target"
    central.mkdir()
    models_repo.mkdir()
    target.mkdir()
    central_store = central / ".sldb"
    models_store = models_repo / ".sldb"
    target_store = target / ".sldb"

    assert cli_main(["stores", "init", "--path", str(central)]) == 0
    assert cli_main(["stores", "init", "--path", str(models_repo)]) == 0
    assert cli_main(["stores", "init", "--path", str(target)]) == 0
    monkeypatch.chdir(central)
    assert (
        cli_main(
            [
                "models",
                "add",
                "federated_models:RequestDoc",
                "--store",
                str(models_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "stores",
                "add",
                str(models_store),
                "--name",
                "deskops",
                "--store",
                str(central_store),
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "stores",
                "add",
                str(target_store),
                "--name",
                "target",
                "--store",
                str(central_store),
            ]
        )
        == 0
    )

    assert (
        cli_main(
            [
                "docs",
                "create",
                "--store",
                "target",
                "--model",
                "deskops:RequestDoc",
                "-o",
                "desk/inbox/request-456.md",
                json.dumps({"title": "Need model", "body": "Use deskops model."}),
                "--pythonpath",
                pythonpath,
            ],
        )
        == 0
    )

    output = target / "desk" / "inbox" / "request-456.md"
    assert output.exists()
    assert "Use deskops model." in output.read_text(encoding="utf-8")
    docs_index = load_documents_index(
        target / ".sldb" / "core" / "documents" / "RequestDoc.yaml"
    )
    assert [doc.path for doc in docs_index.documents] == [
        "desk/inbox/request-456.md"
    ]


def test_help_topics(capsys):
    assert cli_main(["--help"]) == 0
    out = capsys.readouterr().out
    assert "SLDB's main workflow is:" in out
    assert "Primary surfaces:" in out
    assert "raw-find" not in out
    assert "extract, render, validate   Direct model-first operations without a store" in out

    original_argv = sys.argv[:]
    try:
        sys.argv = ["sldb", "--help"]
        assert cli_main() == 0
        out = capsys.readouterr().out
        assert "SLDB's main workflow is:" in out
        assert "raw-find" not in out
    finally:
        sys.argv = original_argv

    assert cli_main(["help"]) == 0
    out = capsys.readouterr().out
    assert "not `bash sldb ...`" in out
    assert "explore   Deep markdown docs and docstring search" in out
    assert "faq       Question-oriented onboarding answers" in out
    assert "inbox     Log unclear points or suggestions to the active project desk" in out

    assert cli_main(["help", "fields"]) == 0
    out = capsys.readouterr().out
    assert "fields append" in out
    assert "CRUD" in out
    capsys.readouterr()
    assert cli_main(["help", "sections"]) == 0
    out = capsys.readouterr().out
    assert "sections show" in out
    assert "sections find" in out
    assert "sections fields" in out
    capsys.readouterr()
    assert cli_main(["help", "explore"]) == 0
    out = capsys.readouterr().out
    assert "Deep search over markdown docs and Python docstrings" in out
    assert "--source all|docs|docstrings" in out

    assert cli_main(["find", "--help"]) == 0
    out = capsys.readouterr().out
    assert "Use `physical` for names, paths, section titles, and" in out.replace("\n", " ")
    assert "sldb find roadmap --in physical --type doc" in out
    assert "Typical shapes:" in out

    assert cli_main(["docs", "--help"]) == 0
    out = capsys.readouterr().out
    assert "`recover` and `compose` work on explicit Markdown links and" in out.replace("\n", " ")
    assert "Resolve [[links]] and report their targets." in out
    assert "Expand ![[transclusions]] into composed Markdown." in out

    assert cli_main(["docs", "recover", "--help"]) == 0
    out = capsys.readouterr().out
    assert "sldb docs recover roadmap --store .sldb" in out

    assert cli_main(["docs", "compose", "--help"]) == 0
    out = capsys.readouterr().out
    assert "Output path or - for stdout" in out

    assert cli_main(["models", "--help"]) == 0
    out = capsys.readouterr().out
    assert "list                List registered models." in out

    assert cli_main(["help", "models"]) == 0
    out = capsys.readouterr().out
    assert "models list --store .sldb" in out


def test_faq_lists_and_selects_questions(capsys):
    assert cli_main(["faq"]) == 0
    out = capsys.readouterr().out
    assert "SLDB FAQ questions:" in out
    assert "What exactly is a store?" in out

    assert cli_main(["faq", "store"]) == 0
    out = capsys.readouterr().out
    assert "What exactly is a store?" in out
    assert "A store is SLDB's metadata workspace" in out


def test_inbox_writes_desk_note(tmp_path, capsys):
    desk_root = tmp_path / "desk"
    assert (
        cli_main(
            [
                "inbox",
                "The docs should explain tracked doc names more clearly.",
                "--kind",
                "suggestion",
                "--title",
                "tracked doc names",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "Wrote" in out
    inbox_files = list((desk_root / "inbox").glob("*.md"))
    assert len(inbox_files) == 1
    text = inbox_files[0].read_text(encoding="utf-8")
    assert "kind: suggestion" in text
    assert "# tracked doc names" in text
    assert "The docs should explain tracked doc names more clearly." in text


def test_inbox_rejects_title_only_placeholder(tmp_path):
    desk_root = tmp_path / "desk"
    with pytest.raises(SystemExit) as exc:
        cli_main(
            [
                "inbox",
                "Repo-targeted note",
                "--kind",
                "unclear",
                "--desk-root",
                str(desk_root),
            ]
        )
    assert "Inbox note needs more detail" in str(exc.value)


def test_models_list_lists_registered_models(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()

    assert (
        cli_main(["models", "list", "--store", str(store)])
        == 0
    )
    out = capsys.readouterr().out
    assert "Models in" in out
    assert "RoadmapDoc | cli_v2_models:RoadmapDoc" in out
    assert "1 docs" in out

    assert (
        cli_main(["models", "list", "--store", str(store), "--format", "json"])
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["models"][0]["name"] == "RoadmapDoc"
    assert payload["models"][0]["documents"] == 1


def test_models_list_fails_on_no_store_and_no_global(tmp_path, capsys, monkeypatch):
    project = tmp_path / "no-store-project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    with pytest.raises(SystemExit) as exc:
        cli_main(["models", "list"])
    assert "No local .sldb store found" in str(exc.value)
    assert "No global store exists" in str(exc.value)
    assert "sldb stores init --path ." in str(exc.value)


def test_models_list_falls_back_to_global_when_no_local(tmp_path, capsys, monkeypatch):
    project = tmp_path / "no-store-project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    home_store_root = Path.home()
    (home_store_root / ".sldb" / "core").mkdir(parents=True, exist_ok=True)
    (home_store_root / ".sldb" / "runtime").mkdir(parents=True, exist_ok=True)
    from sldb.store.io import save_store_index
    from sldb.store.models import StoreIndex

    save_store_index(home_store_root / ".sldb", StoreIndex())

    result = cli_main(["models", "list"])
    assert result == 0
    stderr = capsys.readouterr().err
    assert "falling back to global store" in stderr


def test_inbox_lists_and_shows_notes(tmp_path, capsys):
    desk_root = tmp_path / "desk"
    assert (
        cli_main(
            [
                "inbox",
                "Semantic docs are still a bit unclear.",
                "--kind",
                "unclear",
                "--title",
                "semantic docs",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "inbox",
                "Add more examples for compose.",
                "--kind",
                "suggestion",
                "--title",
                "compose examples",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert cli_main(["inbox", "--list", "--desk-root", str(desk_root)]) == 0
    out = capsys.readouterr().out
    assert "semantic docs" in out
    assert "compose examples" in out

    assert (
        cli_main(
            [
                "inbox",
                "--show",
                "compose-examples",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "# compose examples" in out
    assert "kind: suggestion" in out
    assert "Add more examples for compose." in out


def test_inbox_defaults_to_local_store_project_desk(tmp_path, capsys, monkeypatch):
    project = tmp_path / "target-project"
    project.mkdir()
    assert cli_main(["stores", "init", "--path", str(project)]) == 0
    capsys.readouterr()

    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.chdir(other)

    assert (
        cli_main(
            [
                "inbox",
                "Route this to the target project desk.",
                "--store",
                str(project / ".sldb"),
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert str(project / "desk" / "inbox") in out
    note_files = list((project / "desk" / "inbox").glob("*.md"))
    assert len(note_files) == 1
    assert not (other / "desk").exists()


def test_inbox_auto_tracks_when_model_registered(tmp_path, capsys, monkeypatch):
    project = tmp_path / "target-project"
    project.mkdir()
    assert cli_main(["stores", "init", "--path", str(project)]) == 0
    capsys.readouterr()

    repo_pythonpath = str(Path(__file__).resolve().parents[1])
    assert (
        cli_main(
            [
                "models",
                "add",
                "desk.models:InboxNoteDoc",
                "--store",
                str(project / ".sldb"),
                "--pythonpath",
                repo_pythonpath,
            ]
        )
        == 0
    )
    capsys.readouterr()

    monkeypatch.chdir(project)
    assert (
        cli_main(
            [
                "inbox",
                "Track this inbox note automatically.",
                "--title",
                "auto track inbox",
                "--pythonpath",
                repo_pythonpath,
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "Tracked '" in out

    store = project / ".sldb"
    entry = next(m for m in load_store_index(store).models if m.name == "InboxNoteDoc")
    model_index = load_models_index(project / entry.models_index)
    docs_index = load_documents_index(project / model_index.documents_index)
    tracked = next(doc for doc in docs_index.documents if "auto-track-inbox" in doc.name)
    assert tracked.path.startswith("desk/inbox/")


def test_explore_searches_docs_and_docstrings(tmp_path, capsys):
    docs_root = tmp_path / "docs"
    code_root = tmp_path / "src"
    docs_root.mkdir()
    code_root.mkdir()

    (docs_root / "faq.md").write_text(
        "# FAQ\n\nThe store keeps metadata close to Markdown.\n",
        encoding="utf-8",
    )
    (code_root / "knowledge.py").write_text(
        '"""Store helpers for SLDB docs."""\n\n\nclass Guide:\n    """StructuredNLDoc-oriented guide surface."""\n',
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "explore",
                "store",
                "--docs-root",
                str(docs_root),
                "--code-root",
                str(code_root),
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)["results"]
    assert any(item["source"] == "docs" for item in payload)
    assert any(item["source"] == "docstrings" for item in payload)

    assert (
        cli_main(
            [
                "docs",
                "explore",
                "StructuredNLDoc",
                "--source",
                "docstrings",
                "--docs-root",
                str(docs_root),
                "--code-root",
                str(code_root),
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)["results"]
    assert payload[0]["source"] == "docstrings"
    assert payload[0]["anchor"] == "Guide"


def test_ast_show_document_has_sections(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "ast",
                "show",
                "docs/roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["document"]["name"] == "roadmap"
    titles = [section["title"] for section in payload["document"]["sections"]]
    assert "Tasks" in titles
    assert payload["document"]["ir"]["context"]["physical"]["path"] == "roadmap.md"
    assert payload["document"]["ir"]["structure"][0]["kind"] == "section"
    assert payload["document"]["ir"]["graph"]["edges"][0]["relation"] == "has_section"
    assert payload["document"]["ir"]["context_index"][0]["title"] == "Roadmap"
    assert (
        "type.documentation.Readme"
        in payload["document"]["ir"]["context_index"][1]["about"]
    )


def test_ast_show_field_nodes_have_owning_section(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "ast",
                "show",
                "docs/roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    nodes = payload["document"]["ir"]["nodes"]
    field_to_section = {node["field_path"]: node["owning_section"] for node in nodes}
    assert field_to_section["title"] == "roadmap"
    assert field_to_section["status"] == "roadmap"
    assert field_to_section["tasks"] == "roadmap/tasks"
    assert field_to_section["semantic_tags"] == "roadmap/semantic-tags"


def test_find_supports_physical_and_semantic(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "find",
                "roadmap",
                "--in",
                "physical",
                "--type",
                "doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    physical = json.loads(capsys.readouterr().out)["results"]
    assert physical[0]["doc"] == "roadmap"

    assert (
        cli_main(
            [
                "find",
                "type.documentation.Readme",
                "--in",
                "semantic",
                "--type",
                "doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    semantic = json.loads(capsys.readouterr().out)["results"]
    assert semantic[0]["semantic_tags"] == [
        "project.sldb.database",
        "type.documentation.Readme",
    ]


def test_models_template_edit_writes_draft_without_mutating_active_source(tmp_path):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    original = module_path.read_text(encoding="utf-8")
    template_path = _write_template(
        tmp_path / "updated.template.md",
        "# ⸢rev•title⸥\n\nSummary: active draft\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n\n## Semantic Tags\n\n- ⸢rev,list•semantic_tags⸥\n",
    )

    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    draft_path = module_path.with_name(module_path.name + ".temp")
    assert draft_path.exists()
    assert "Summary: active draft" in draft_path.read_text(encoding="utf-8")
    assert module_path.read_text(encoding="utf-8") == original


def test_models_validate_promotes_valid_template_draft_and_reindexes(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    template_path = _write_template(
        tmp_path / "promote.template.md",
        "# ⸢rev•title⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n\n## Semantic Tags\n\n- ⸢rev,list•semantic_tags⸥\n\n## Review\n\nReady for validation.\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--promote",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert "validated draft" in capsys.readouterr().out
    assert "## Review" in module_path.read_text(encoding="utf-8")
    assert not module_path.with_name(module_path.name + ".temp").exists()

    capsys.readouterr()
    assert (
        cli_main(["stores", "check", "--store", str(store), "--pythonpath", pythonpath])
        == 0
    )


def test_models_validate_rejects_draft_with_unknown_field_reference(tmp_path):
    store, pythonpath = _setup_store(tmp_path)
    template_path = _write_template(
        tmp_path / "invalid.template.md",
        "# ⸢rev•title⸥\n\nMissing: ⸢rev•missing_field⸥\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    with pytest.raises(SystemExit, match="references unknown fields: missing_field"):
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )


def test_models_fields_add_and_promote_bumps_model_version(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    before = load_models_index(_model_index_path(store, "RoadmapDoc")).version

    assert (
        cli_main(
            [
                "models",
                "fields",
                "add",
                "RoadmapDoc",
                "summary",
                "--type",
                "str",
                "--description",
                "Short summary.",
                "--default",
                '"Pending review"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    template_path = _write_template(
        tmp_path / "field-add.template.md",
        "# ⸢rev•title⸥\n\nSummary: ⸢rev•summary⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n\n## Semantic Tags\n\n- ⸢rev,list•semantic_tags⸥\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--promote",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    after = load_models_index(_model_index_path(store, "RoadmapDoc")).version
    assert after == before + 1
    active_source = module_path.read_text(encoding="utf-8")
    assert (
        "summary: str = Field(default='Pending review', description='Short summary.')"
        in active_source
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "show",
                "RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert f"version: {after}" in capsys.readouterr().out


def test_models_fields_remove_requires_existing_field_and_bumps_version(
    tmp_path, capsys
):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"

    with pytest.raises(SystemExit, match="Field 'missing' does not exist"):
        cli_main(
            [
                "models",
                "fields",
                "remove",
                "RoadmapDoc",
                "missing",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )

    before = load_models_index(_model_index_path(store, "RoadmapDoc")).version
    assert (
        cli_main(
            [
                "models",
                "fields",
                "remove",
                "RoadmapDoc",
                "semantic_tags",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    template_path = _write_template(
        tmp_path / "field-remove.template.md",
        "# ⸢rev•title⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--promote",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    after = load_models_index(_model_index_path(store, "RoadmapDoc")).version
    assert after == before + 1
    active_source = module_path.read_text(encoding="utf-8")
    assert "semantic_tags:" not in active_source


def test_find_section_where_predicates(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()

    assert (
        cli_main(
            [
                "find",
                "tasks",
                "--type",
                "section",
                "--where",
                '"Tasks" in about',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    titles = [r["title"] for r in results]
    assert "Tasks" in titles

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                '"Semantic Tags" in about',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Semantic Tags"

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                '"Roadmap" in breadcrumbs',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert len(results) > 1
    for r in results:
        assert "Roadmap" in r.get("breadcrumbs", [])

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                '"type.documentation.Readme" in semantic_tags',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert len(results) == 3

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                'path = "roadmap.md#roadmap"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Roadmap"

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                'path = "roadmap.md#roadmap/tasks"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Tasks"


def test_fields_update_append_and_clean(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    target = "docs/roadmap/tasks"
    assert (
        cli_main(
            [
                "fields",
                "append",
                target,
                '"Ship CLI"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "fields",
                "clean",
                target,
                "--dedupe",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "fields",
                "update",
                "docs/roadmap/status",
                '"accepted"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "show",
                "docs/roadmap/status",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    status = json.loads(capsys.readouterr().out)
    assert status["value"] == "accepted"

    assert (
        cli_main(
            [
                "fields",
                "show",
                target,
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    tasks = json.loads(capsys.readouterr().out)["value"]
    assert tasks == ["Ship CLI", "Write docs"]


def test_fields_update_can_clear_list_field(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "update",
                "docs/roadmap/tasks",
                "[]",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "show",
                "docs/roadmap/tasks",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    value = json.loads(capsys.readouterr().out)
    assert value["value"] == []


def test_models_create_stdout(tmp_path, capsys):
    template = tmp_path / "template.md"
    template.write_text("# ⸢rev•title⸥\n", encoding="utf-8")
    fields = tmp_path / "fields.yaml"
    fields.write_text(
        """
fields:
  - name: title
    type: str
    description: Document title.
""".strip()
        + "\n",
        encoding="utf-8",
    )
    assert (
        cli_main(
            [
                "models",
                "create",
                "GeneratedDoc",
                "--template",
                str(template),
                "--fields",
                str(fields),
                "--stdout",
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "class GeneratedDoc(StructuredNLDoc):" in out
    assert "title: str = Field(description=" in out
    assert "Document title." in out


def test_sections_show_command(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "sections",
                "show",
                "roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    titles = [entry["title"] for entry in payload["sections"]]
    assert "Roadmap" in titles
    assert "Tasks" in titles
    assert "Semantic Tags" in titles


def test_sections_find_command(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "sections",
                "find",
                "tasks",
                "--in",
                "semantic",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Tasks"

    assert (
        cli_main(
            [
                "sections",
                "find",
                "",
                "--where",
                '"Roadmap" in breadcrumbs',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert len(results) >= 2


def test_sections_fields_command(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "sections",
                "fields",
                "docs/roadmap/roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    fields = json.loads(capsys.readouterr().out)["fields"]
    field_paths = [f["field_path"] for f in fields]
    assert "title" in field_paths
    assert "status" in field_paths

    assert (
        cli_main(
            [
                "sections",
                "fields",
                "docs/roadmap/roadmap/tasks",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    fields = json.loads(capsys.readouterr().out)["fields"]
    field_paths = [f["field_path"] for f in fields]
    assert "tasks" in field_paths


def test_field_query_includes_owning_section(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "query",
                "title",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["owning_section"] == "roadmap"


def test_sections_show_identical_with_and_without_persisted_index(tmp_path, capsys):
    """Read-side commands produce identical section output with or without persisted index."""
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()

    assert (
        cli_main(
            [
                "sections",
                "show",
                "roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    before = json.loads(capsys.readouterr().out)

    assert (
        cli_main(
            ["stores", "update", "--store", str(store), "--pythonpath", pythonpath]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        cli_main(
            [
                "sections",
                "show",
                "roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    after = json.loads(capsys.readouterr().out)

    before_sections = before.get("sections", [])
    after_sections = after.get("sections", [])
    assert len(before_sections) == len(after_sections)
    for b, a in zip(before_sections, after_sections):
        assert b["title"] == a["title"]
        assert b["path"] == a["path"]
        assert b["breadcrumbs"] == a["breadcrumbs"]
        assert b["about"] == a["about"]


def test_find_field_shows_owning_section(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "find",
                "title",
                "--type",
                "field",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["owning_section"] == "roadmap"


def _add_summary_draft(store: Path, pythonpath: str) -> None:
    assert (
        cli_main(
            [
                "models", "fields", "add", "RoadmapDoc", "summary",
                "--type", "str", "--description", "Short summary.", "--default", '"Pending review"',
                "--store", str(store), "--pythonpath", pythonpath,
            ]
        )
        == 0
    )


@pytest.mark.parametrize("failing", ["resolve_model_ref", "cascade_hash_a"])
def test_models_promote_failure_restores_model_draft_and_indexes(tmp_path, monkeypatch, failing):
    """A promote whose reindex fails leaves the store as it was: active model, draft and indexes intact."""
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    draft_path = module_path.with_name(module_path.name + ".temp")
    _add_summary_draft(store, pythonpath)
    original, draft = module_path.read_text(encoding="utf-8"), draft_path.read_text(encoding="utf-8")
    before = load_models_index(_model_index_path(store, "RoadmapDoc")).version

    def boom(*args, **kwargs):
        raise RuntimeError("reindex failed")

    # resolve_model_ref fails before any index write; cascade_hash_a after the model indexes are saved.
    monkeypatch.setattr(f"sldb.cli.commands.model.{failing}", boom)
    monkeypatch.setattr(f"sldb.cli.commands.model_update.{failing}", boom)
    with pytest.raises((SystemExit, RuntimeError)):
        cli_main(["models", "validate", "RoadmapDoc", "--promote", "--store", str(store), "--pythonpath", pythonpath])
    monkeypatch.undo()

    assert module_path.read_text(encoding="utf-8") == original
    assert draft_path.read_text(encoding="utf-8") == draft
    assert load_models_index(_model_index_path(store, "RoadmapDoc")).version == before
    assert cli_main(["stores", "check", "--store", str(store), "--pythonpath", pythonpath]) == 0


def test_models_promote_json_output_is_pure_json(tmp_path, capsys):
    """--format json keeps stdout parseable: update's progress line must not precede the report."""
    store, pythonpath = _setup_store(tmp_path)
    _add_summary_draft(store, pythonpath)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "models", "validate", "RoadmapDoc", "--promote", "--format", "json",
                "--store", str(store), "--pythonpath", pythonpath,
            ]
        )
        == 0
    )
    report = json.loads(capsys.readouterr().out)
    assert report["promoted"] is True and report["draft"] is True
