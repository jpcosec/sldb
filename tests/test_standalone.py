import pytest
import json
import yaml
from importlib.resources import files
from pathlib import Path
from pydantic import Field
from sldb import (
    StructuredNLDoc,
    DataExtractor,
    AST_Handler,
    TemplateExtractor,
    SLDBRenderer,
    configure,
    reset_config,
)
from sldb.cli import main as cli_main
from sldb.examples.reference_bundle.guide_model import SLDBGuide
from sldb.runtime.validation import (
    extract_model_data,
    render_model_markdown,
    validate_model_data_roundtrip,
    validate_model_input_roundtrip,
)


class SimpleDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

## Metadata
```yaml
⸢rev,dict•meta⸥
```

* ⸢rev,list•items⸥
""".strip()
    title: str = Field(description="Document title heading.")
    meta: dict = Field(description="Metadata YAML block.")
    items: list = Field(description="Bullet list items.")


class FrontmatterFieldsDoc(StructuredNLDoc):
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    id: str = Field(description="Stable document identifier.")
    status: str = Field(description="Document lifecycle status.")
    tags: list[str] = Field(description="Semantic tags.")
    title: str = Field(description="Document title heading.")
    body: str = Field(description="Markdown body content.")


class TableMarkerDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev,table[name,status,goal]•tasks⸥
""".strip()

    title: str = Field(description="Document title heading.")
    tasks: list[dict[str, str]] = Field(description="Structured task table rows.")


class InferredTableMarkerDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev,table•tasks⸥
""".strip()

    title: str = Field(description="Document title heading.")
    tasks: list[dict[str, str]] = Field(description="Structured task table rows.")


class AdvancedMarkersDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

⸢optrev•subtitle⸥

Rendered slug: ⸢render•slug⸥
Python slug: ⸢py•title.lower().replace(' ', '-')⸥
Jinja greeting: Hello {{ title }}!

* ⸢rev,list•items⸥

```yaml
⸢optrev,dict•meta⸥
```
""".strip()
    title: str = Field(description="Main document title.")
    subtitle: str | None = Field(default=None, description="Optional subtitle block.")
    slug: str | None = Field(default=None, description="Render-only slug value.")
    items: list = Field(description="Repeated bullet list entries.")
    meta: dict | None = Field(
        default=None, description="Optional metadata mapping block."
    )


class PandocCVDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    title: str = Field(description="CV title shown in the H1 heading.")
    body: str = Field(
        description="Body after the H1, including lead paragraph, fenced div blocks, and nested headings."
    )


def _write_model_module(base_path: Path) -> str:
    module_path = base_path / "external_models.py"
    module_path.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class SimpleDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

## Metadata
```yaml
⸢rev,dict•meta⸥
```

* ⸢rev,list•items⸥
""".strip()
    title: str = Field(description="Document title heading.")
    meta: dict = Field(description="Metadata YAML block.")
    items: list = Field(description="Bullet list items.")
''',
        encoding="utf-8",
    )
    return "external_models:SimpleDoc"


def _write_input_markdown(path: Path) -> None:
    path.write_text(
        """
# My Standalone Doc

## Metadata
```yaml
version: 1.0.0
status: stable
```

* First
* Second
""".strip(),
        encoding="utf-8",
    )


def _write_data_yaml(path: Path) -> None:
    path.write_text(
        """
title: My Standalone Doc
meta:
  version: 1.0.0
  status: stable
items:
  - First
  - Second
""".strip(),
        encoding="utf-8",
    )


def test_sldb_standalone_roundtrip():
    ast = AST_Handler()
    tpl = TemplateExtractor()
    data_ext = DataExtractor()
    renderer = SLDBRenderer()

    # 1. Parsing
    markdown = """
# My Standalone Doc

## Metadata
```yaml
version: 1.0.0
status: stable
```

* First
* Second
""".strip()

    recipes = tpl.extract_nodes(ast.split_nodes(SimpleDoc.__template__))
    payload = data_ext.extract_values(ast.split_nodes(markdown), recipes)

    model = SimpleDoc(**payload)
    assert model.title == "My Standalone Doc"
    assert model.meta == {"version": "1.0.0", "status": "stable"}
    assert model.items == ["First", "Second"]

    # 2. Rendering
    rendered = renderer.render(model)
    assert "# My Standalone Doc" in rendered
    assert "version: 1.0.0" in rendered
    assert "* First" in rendered
    assert "* Second" in rendered

    payload_again = data_ext.extract_values(ast.split_nodes(rendered), recipes)
    assert payload_again == payload


def test_title_body_model_roundtrips_pandoc_fenced_divs():
    markdown = """
# Curriculum Vitae

This CV keeps Pandoc fenced div blocks intact so an external review UI can keep parsing them structurally.

::: {.job role="Staff Engineer" org="Hum Labs" dates="2021-2024"}
## Work

Built the document pipeline.

- Shipped structured review surfaces
- Kept Markdown editable
:::

::: {.education degree="MSc" org="UNLP" dates="2018-2020"}
## Education

Studied computational linguistics.
:::
""".strip()

    payload = extract_model_data(PandocCVDoc, markdown)
    assert payload["title"] == "Curriculum Vitae"
    assert "::: {.job role=\"Staff Engineer\"" in payload["body"]
    assert "::: {.education degree=\"MSc\"" in payload["body"]

    rendered = render_model_markdown(PandocCVDoc, payload)
    assert "::: {.job role=\"Staff Engineer\"" in rendered
    assert "::: {.education degree=\"MSc\"" in rendered

    valid, details = validate_model_input_roundtrip(PandocCVDoc, markdown)
    assert valid, details


if __name__ == "__main__":
    pytest.main([__file__])


def test_cli_extract_json(tmp_path, capsys):
    model_ref = _write_model_module(tmp_path)
    input_path = tmp_path / "input.md"
    output_path = tmp_path / "output.json"

    _write_input_markdown(input_path)

    exit_code = cli_main(
        [
            "extract",
            model_ref,
            str(input_path),
            str(output_path),
            "--pythonpath",
            str(tmp_path),
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert captured.out == ""
    assert payload == {
        "title": "My Standalone Doc",
        "meta": {"version": "1.0.0", "status": "stable"},
        "items": ["First", "Second"],
    }


def test_cli_render_markdown(tmp_path, capsys):
    model_ref = _write_model_module(tmp_path)
    data_path = tmp_path / "data.yaml"
    output_path = tmp_path / "rendered.md"

    _write_data_yaml(data_path)

    exit_code = cli_main(
        [
            "render",
            model_ref,
            str(data_path),
            str(output_path),
            "--pythonpath",
            str(tmp_path),
        ]
    )

    captured = capsys.readouterr()
    rendered = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert captured.out == ""
    assert "# My Standalone Doc" in rendered
    assert "version: 1.0.0" in rendered
    assert "* First" in rendered
    assert "* Second" in rendered


def test_cli_extract_stdout_with_explicit_format(tmp_path, capsys):
    model_ref = _write_model_module(tmp_path)
    input_path = tmp_path / "input.md"

    _write_input_markdown(input_path)

    exit_code = cli_main(
        [
            "extract",
            model_ref,
            str(input_path),
            "-",
            "--format",
            "json",
            "--pythonpath",
            str(tmp_path),
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["title"] == "My Standalone Doc"


def test_cli_validate_input_roundtrip(tmp_path, capsys):
    model_ref = _write_model_module(tmp_path)
    input_path = tmp_path / "input.md"

    _write_input_markdown(input_path)

    exit_code = cli_main(
        [
            "validate",
            model_ref,
            "--input",
            str(input_path),
            "--pythonpath",
            str(tmp_path),
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "PASS: model is idempotent in input mode" in captured.out


def test_cli_validate_data_roundtrip_json(tmp_path, capsys):
    model_ref = _write_model_module(tmp_path)
    data_path = tmp_path / "data.yaml"

    _write_data_yaml(data_path)

    exit_code = cli_main(
        [
            "validate",
            model_ref,
            "--data",
            str(data_path),
            "--format",
            "json",
            "--pythonpath",
            str(tmp_path),
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["valid"] is True
    assert payload["mode"] == "data"
    assert payload["input_data"]["title"] == "My Standalone Doc"
    assert payload["model"] == model_ref


def test_cli_init_writes_skill_file(tmp_path, capsys):
    exit_code = cli_main(["init", str(tmp_path)])

    captured = capsys.readouterr()
    skill_path = tmp_path / ".skills" / "sldb" / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert f"Wrote {skill_path}" in captured.out
    assert content.startswith("---\nname: sldb\n")
    assert (
        "Use `sldb` for StructuredNLDoc models and their Markdown documents." in content
    )
    assert (
        "For every StructuredNLDoc workflow, run `sldb validate` before finishing."
        in content
    )
    assert (
        "`sldb extract <model-ref> <input-markdown> <output-json-or-yaml>`" in content
    )


def test_cli_init_refuses_overwrite_without_force(tmp_path):
    cli_main(["init", str(tmp_path)])

    with pytest.raises(SystemExit) as exc:
        cli_main(["init", str(tmp_path)])

    assert "Use --force to replace" in str(exc.value)

def test_cli_init_force_overwrites(tmp_path):
    skill_path = tmp_path / ".skills" / "sldb" / "SKILL.md"
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    skill_path.write_text("old", encoding="utf-8")

    exit_code = cli_main(["init", str(tmp_path), "--force"])

    assert exit_code == 0
    assert (
        "Use `sldb` for StructuredNLDoc models and their Markdown documents."
        in skill_path.read_text(encoding="utf-8")
    )


def test_example_bundle_roundtrips():
    bundle = files("sldb.examples.reference_bundle")
    input_markdown = bundle.joinpath("guide.input.md").read_text(encoding="utf-8")
    input_data = yaml.safe_load(
        bundle.joinpath("guide.data.yaml").read_text(encoding="utf-8")
    )

    extracted = extract_model_data(SLDBGuide, input_markdown)
    rendered = render_model_markdown(SLDBGuide, input_data)
    input_valid, _ = validate_model_input_roundtrip(SLDBGuide, input_markdown)
    data_valid, _ = validate_model_data_roundtrip(SLDBGuide, input_data)

    assert extracted["title"] == "SLDB Example Guide"
    assert extracted["frontmatter"]["example"] is True
    assert extracted["benefits"][0] == "Human-readable source of truth."
    first_command = extracted["commands"][0]
    assert first_command["commands"] == "sldb extract"
    assert "# SLDB Example Guide" in rendered
    assert "## How to extend this library" in rendered
    assert "`optrev•field`: optional reversible scalar." in rendered
    assert "Jinja2 render-only expression." in rendered
    assert "## YAML metadata block" in rendered
    assert input_valid is True
    assert data_valid is True


def test_frontmatter_fields_render_and_extract():
    payload = {
        "id": "doc-001",
        "status": "active",
        "tags": ["system:sldb", "topic:frontmatter"],
        "title": "Frontmatter metadata",
        "body": "The body stays focused on human-readable content.",
    }

    rendered = render_model_markdown(FrontmatterFieldsDoc, payload)
    extracted = extract_model_data(FrontmatterFieldsDoc, rendered)

    assert rendered.startswith("---\nid: doc-001\nstatus: active\ntags:\n- system:sldb")
    assert extracted == payload


def test_table_marker_renders_and_extracts_explicit_columns():
    payload = {
        "title": "Task Board",
        "tasks": [
            {"name": "Model", "status": "done", "goal": "Define shape"},
            {"name": "Writer", "status": "open", "goal": "Ship docs"},
        ],
    }

    rendered = render_model_markdown(TableMarkerDoc, payload)
    extracted = extract_model_data(TableMarkerDoc, rendered)

    assert "| name | status | goal |" in rendered
    assert "| --- | --- | --- |" in rendered
    assert "| Model | done | Define shape |" in rendered
    assert extracted == payload


def test_table_marker_infers_columns_and_preserves_empty_cells():
    payload = {
        "title": "Task Board",
        "tasks": [
            {"name": "Model", "status": "", "goal": "Define shape"},
        ],
    }

    rendered = render_model_markdown(InferredTableMarkerDoc, payload)
    extracted = extract_model_data(InferredTableMarkerDoc, rendered)

    assert "| name | status | goal |" in rendered
    assert "| Model |  | Define shape |" in rendered
    assert extracted == payload


def test_example_bundle_self_idempotency():
    bundle = files("sldb.examples.reference_bundle")
    input_markdown = bundle.joinpath("guide.input.md").read_text(encoding="utf-8")

    first_payload = extract_model_data(SLDBGuide, input_markdown)
    rendered_markdown = render_model_markdown(SLDBGuide, first_payload)
    second_payload = extract_model_data(SLDBGuide, rendered_markdown)

    assert first_payload == second_payload


def test_advanced_marker_families_render_and_extract():
    reset_config()
    model = AdvancedMarkersDoc(
        title="Hello World",
        subtitle=None,
        slug="hello-world",
        items=["One", "Two"],
        meta=None,
    )

    rendered = render_model_markdown(AdvancedMarkersDoc, model.model_dump(mode="json"))
    extracted = extract_model_data(AdvancedMarkersDoc, rendered)

    assert "Rendered slug: hello-world" in rendered
    assert "Python slug: ⸢py•title.lower().replace(' ', '-')⸥" in rendered
    assert "Jinja greeting: Hello Hello World!" in rendered
    assert extracted["title"] == "Hello World"
    assert "subtitle" not in extracted  # absent optional field is dropped
    assert "slug" not in extracted
    assert extracted["items"] == ["One", "Two"]
    assert "meta" not in extracted


def test_python_markers_render_in_unsafe_mode():
    reset_config()
    configure(python_execution_mode="unsafe")

    try:
        model = AdvancedMarkersDoc(
            title="Hello World",
            subtitle=None,
            slug="hello-world",
            items=["One", "Two"],
            meta=None,
        )

        rendered = render_model_markdown(
            AdvancedMarkersDoc, model.model_dump(mode="json")
        )
    finally:
        reset_config()

    assert "Python slug: hello-world" in rendered


def test_python_markers_can_be_filtered_in_unsafe_mode():
    reset_config()
    configure(
        python_execution_mode="unsafe",
        python_expression_filter=lambda expression, data: expression == "title.upper()",
    )

    class FilteredDoc(StructuredNLDoc):
        __template__ = "Allowed: ⸢py•title.upper()⸥\nBlocked: ⸢py•title.lower()⸥"
        title: str = Field(description="Title used by python markers.")

    try:
        rendered = render_model_markdown(FilteredDoc, {"title": "Hello"})
    finally:
        reset_config()

    assert "Allowed: HELLO" in rendered
    assert "Blocked: ⸢py•title.lower()⸥" in rendered


def test_structured_nl_doc_requires_field_descriptions():
    with pytest.raises(
        TypeError,
        match="fields must define a non-empty description: title",
    ):

        class MissingDescriptionDoc(StructuredNLDoc):
            __template__ = "# ⸢rev•title⸥"
            title: str
