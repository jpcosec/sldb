from __future__ import annotations

import json
from pathlib import Path

from sldb.cli import main as cli_main


def _write_models(base: Path) -> str:
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


def test_help_topics(capsys):
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

    assert (
        cli_main(
            [
                "find",
                "tasks",
                "--in",
                "semantic",
                "--type",
                "section",
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
    section = json.loads(capsys.readouterr().out)["results"]
    assert section[0]["title"] == "Tasks"
    assert "Tasks" in section[0]["about"]


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
