import pytest
import json
import os
import subprocess
import sys
import yaml
from importlib.resources import files
from pathlib import Path
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
from sldb.templates.example_bundle.guide_model import SLDBGuide
from sldb.validation import (
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
    title: str
    meta: dict
    items: list


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
    title: str
    subtitle: str | None = None
    slug: str | None = None
    items: list
    meta: dict | None = None


def _write_model_module(base_path: Path) -> str:
    module_path = base_path / "external_models.py"
    module_path.write_text(
        '''from sldb import StructuredNLDoc


class SimpleDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

## Metadata
```yaml
⸢rev,dict•meta⸥
```

* ⸢rev,list•items⸥
""".strip()
    title: str
    meta: dict
    items: list
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

    assert "Refusing to overwrite existing file" in str(exc.value)


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
    bundle = files("sldb.templates.example_bundle")
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
    first_command = extracted["commands"][sorted(extracted["commands"].keys())[0]]
    assert first_command["commands"] == "sldb extract"
    assert "# SLDB Example Guide" in rendered
    assert "## How to extend this library" in rendered
    assert "`optrev•field`: optional reversible scalar." in rendered
    assert "Jinja2 render-only expression." in rendered
    assert "## YAML metadata block" in rendered
    assert input_valid is True
    assert data_valid is True


def test_example_bundle_self_idempotency():
    bundle = files("sldb.templates.example_bundle")
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
    assert extracted["subtitle"] is None
    assert extracted["slug"] is None
    assert extracted["items"] == ["One", "Two"]
    assert extracted["meta"] is None


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
        title: str

    try:
        rendered = render_model_markdown(FilteredDoc, {"title": "Hello"})
    finally:
        reset_config()

    assert "Allowed: HELLO" in rendered
    assert "Blocked: ⸢py•title.lower()⸥" in rendered


def test_legacy_nldb_import_shows_migration_message():
    with pytest.raises(ImportError, match="renamed to 'sldb'"):
        __import__("nldb")


def test_legacy_python_m_nldb_shows_migration_message():
    result = subprocess.run(
        [sys.executable, "-m", "nldb"],
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "PYTHONPATH": "src"},
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "renamed to 'sldb'" in result.stderr
