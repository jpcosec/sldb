import json

from pathlib import Path
from textwrap import dedent

from sldb.cli import main as cli_main


def _write_models(base: Path) -> str:
    module = base / "link_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev•body⸥""".strip()
    title: str = Field(description="Document title.")
    body: str = Field(description="Document body.")


class RootDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

See [[⸢rev•linked_doc⸥]] for background.

![[⸢rev•transclusion_doc⸥]]""".strip()
    title: str = Field(description="Document title.")
    linked_doc: str = Field(description="Tracked linked document name.")
    transclusion_doc: str = Field(description="Tracked transcluded document name.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def test_recover_and_compose_links(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
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
                "models",
                "add",
                "link_models:RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    concept = tmp_path / "concept.md"
    concept.write_text("# Concept\n\nBackground info.\n", encoding="utf-8")
    constraints = tmp_path / "constraints.md"
    constraints.write_text(
        "# Constraints\n\nAlways validate first.\n", encoding="utf-8"
    )
    root = tmp_path / "root.md"
    root.write_text(
        "# Root\n\nSee [[concept]] for background.\n\n![[constraints]]\n",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(concept),
                "--model",
                "NoteDoc",
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
                "track",
                str(constraints),
                "--model",
                "NoteDoc",
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
                "track",
                str(root),
                "--model",
                "RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            str(root),
            "--store",
            str(store),
            "--format",
            "json",
            "--include-transclusions",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert recovered["root"] == "root"
    assert recovered["links"][0]["target"] == "concept"
    assert recovered["links"][0]["kind"] == "link"
    assert recovered["links"][0]["resolved"] is True
    assert recovered["links"][1]["target"] == "constraints"
    assert recovered["links"][1]["kind"] == "transclusion"
    assert recovered["unresolved"] == []

    capsys.readouterr()
    rc = cli_main(["docs", "compose", str(root), "--store", str(store)])
    composed = capsys.readouterr().out
    assert rc == 0
    assert "See [[concept]] for background." in composed
    assert "# Constraints" in composed
    assert "Always validate first." in composed


def test_docs_recover_and_compose_accept_tracked_doc_names_and_yaml(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
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
                "models",
                "add",
                "link_models:RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    concept = tmp_path / "concept.md"
    concept.write_text("# Concept\n\nBackground info.\n", encoding="utf-8")
    constraints = tmp_path / "constraints.md"
    constraints.write_text(
        "# Constraints\n\nAlways validate first.\n", encoding="utf-8"
    )
    root = tmp_path / "root.md"
    root.write_text(
        "# Root\n\nSee [[concept]] for background.\n\n![[constraints]]\n",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(concept),
                "--model",
                "NoteDoc",
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
                "track",
                str(constraints),
                "--model",
                "NoteDoc",
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
                "track",
                str(root),
                "--model",
                "RootDoc",
                "--name",
                "root-doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            "root-doc",
            "--store",
            str(store),
            "--format",
            "json",
            "--include-transclusions",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert {link["target"] for link in recovered["links"]} == {"concept", "constraints"}

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "compose",
            "root-doc",
            "--store",
            str(store),
            "--format",
            "yaml",
            "-o",
            "-",
        ]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert out.lstrip().startswith("root: root")
    assert "transclusions:" in out


# =============================================================================
# Tests for predicate links (5W1H+)
# =============================================================================


def test_parse_predicate_links():
    """Test parsing of [predicate:: [[target]]] syntax."""
    from sldb.links import parse_links

    markdown = dedent("""
    This task [implements:: [[spec-001]]].
    Another [is_solved_by:: [[solution-002]]].
    [custom_predicate:: [[some-doc]]].
    """)
    links = parse_links(
        markdown,
        {"implements": "HOW", "is_solved_by": "HOW"},
    )

    assert len(links) == 3

    # First predicate link
    assert links[0].target == "spec-001"
    assert links[0].predicate == "implements"
    assert links[0].w5h1_type == "HOW"
    assert links[0].kind == "predicate_link"

    # Second predicate link with different predicate
    assert links[1].target == "solution-002"
    assert links[1].predicate == "is_solved_by"
    assert links[1].w5h1_type == "HOW"

    # Custom predicate gets CUSTOM type
    assert links[2].target == "some-doc"
    assert links[2].predicate == "custom_predicate"
    assert links[2].w5h1_type == "CUSTOM"


def test_parse_links_uses_injected_predicate_axes():
    """Predicate classification comes from the caller, not hardcoded data."""
    from sldb.links import parse_links

    links = parse_links(
        "[depends_on:: [[target]]] [unknown:: [[other]]]",
        {"depends_on": "DEPENDENCY"},
    )

    assert links[0].predicate == "depends_on"
    assert links[0].w5h1_type == "DEPENDENCY"
    assert links[1].predicate == "unknown"
    assert links[1].w5h1_type == "CUSTOM"


def test_parse_mixed_links_with_predicates():
    """Test parsing of documents with both regular links and predicate links."""
    from sldb.links import parse_links

    markdown = dedent("""
    See [[background]] for context.

    This solution [implements:: [[spec-v2]]] and
    [grounded_by:: [[research-paper]]].

    Also check [[related-work]].
    """)
    links = parse_links(
        markdown,
        {"implements": "HOW", "grounded_by": "PROVENANCE"},
    )

    # 2 predicate links + 2 regular links = 4 total
    assert len(links) == 4

    # Check kinds
    kinds = {link.kind for link in links}
    assert "link" in kinds
    assert "predicate_link" in kinds

    # Check specific predicates
    predicate_links = [link for link in links if link.kind == "predicate_link"]
    assert len(predicate_links) == 2
    assert predicate_links[0].predicate == "implements"
    assert predicate_links[1].predicate == "grounded_by"


def test_predicate_links_with_transclusion_bang():
    """Test that [predicate:: ![[target]]] is supported."""
    from sldb.links import parse_links

    markdown = "[implements:: ![[embedded-spec]]]"
    links = parse_links(markdown, {"implements": "HOW"})

    assert len(links) == 1
    assert links[0].target == "embedded-spec"
    assert links[0].predicate == "implements"
    # Bang inside predicate link means transclusion kind
    assert links[0].kind == "transclusion"


def test_resolve_predicate_link(tmp_path):
    """Test resolving a predicate link via relative path."""
    from sldb.links import resolve_link_target

    # Create a document alongside current doc
    docs = tmp_path / "docs"
    docs.mkdir()
    spec_doc = docs / "spec-001.md"
    spec_doc.write_text("# Spec 001\n", encoding="utf-8")

    resolved = resolve_link_target(
        "docs/spec-001.md",
        tmp_path / "current.md",
        None,  # No store, use relative path
        predicate="implements",
        w5h1_type="HOW",
    )

    assert resolved.resolved is True
    assert resolved.kind == "predicate_link"
    assert resolved.predicate == "implements"
    assert resolved.w5h1_type == "HOW"
    assert resolved.source == "path"


def test_recover_predicate_links_cli(tmp_path, capsys):
    """Test that CLI recover command shows predicate info in JSON format."""
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    spec = tmp_path / "spec.md"
    spec.write_text("# Spec\n", encoding="utf-8")
    research = tmp_path / "research.md"
    research.write_text("# Research\n", encoding="utf-8")
    task = tmp_path / "task.md"
    # Use resolved links to different documents
    task.write_text(
        "# Task\n\n" + "[implements:: [[spec]]]\n" + "[grounded_by:: [[research]]]",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(spec),
                "--model",
                "NoteDoc",
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
                "track",
                str(research),
                "--model",
                "NoteDoc",
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
                "track",
                str(task),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            str(task),
            "--store",
            str(store),
            "--format",
            "json",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)

    assert rc == 0
    predicate_links = [
        link for link in recovered["links"] if link["kind"] == "predicate_link"
    ]
    assert len(predicate_links) == 2

    predicates = {link["predicate"] for link in predicate_links}
    assert predicates == {"implements", "grounded_by"}

    # Check 5W1H types
    implements_link = next(
        link for link in predicate_links if link["predicate"] == "implements"
    )
    assert implements_link["w5h1_type"] == "HOW"

    grounded_link = next(
        link for link in predicate_links if link["predicate"] == "grounded_by"
    )
    assert grounded_link["w5h1_type"] == "PROVENANCE"


# =============================================================================
# Code is not scanned for links (fenced, indented and inline code)
# =============================================================================

CODE_EXAMPLES_DOC = """# Guía de enlaces

Ver [[concept]] y [implements:: [[spec-001]]].

```markdown
Un enlace se escribe [[target]] y una transclusión ![[target]].
```

~~~~
[depends_on:: [[target]]]
~~~
sigue dentro: el cierre de tildes es más corto que la apertura [[target]]
~~~~

    [[target]] en un bloque indentado

- un ítem de lista con [[item-link]]

    [[nested-link]] dentro del ítem no es código

Usa `[[target]]` o ``[[target]] con ` adentro``; un ` suelto no abre código, y [[after-tick]] cuenta.

Cierre: [[closing]].

```
bloque sin cerrar: [[target]]
"""


def test_parse_links_skips_code():
    from sldb.links import parse_links

    links = parse_links(CODE_EXAMPLES_DOC, {"implements": "HOW"})

    assert [(link.target, link.kind) for link in links] == [
        ("spec-001", "predicate_link"),
        ("concept", "link"),
        ("item-link", "link"),
        ("nested-link", "link"),
        ("after-tick", "link"),
        ("closing", "link"),
    ]


def test_parse_links_fence_rules():
    from sldb.links import parse_links

    def targets(markdown):
        return [link.target for link in parse_links(markdown)]

    assert targets("```\n[[a]]\n```\n[[b]]\n") == ["b"]
    assert targets("~~~python\n[[a]]\n~~~\n[[b]]\n") == ["b"]
    assert targets("````\n[[a]]\n```\n[[b]]\n````\n[[c]]\n") == ["c"]
    assert targets("```\n[[a]]\n~~~\n[[b]]\n") == []
    assert targets("```x``` [[a]]\n") == ["a"]
    assert targets("texto\n    [[a]] continúa el párrafo\n") == ["a"]
    assert targets("texto\n\n\t[[a]]\n\n[[b]]\n") == ["b"]
    assert targets("`` [[a]] ` `` [[b]] ```[[c]]`` [[d]]\n") == ["b", "c", "d"]
    assert targets("`abre\n\n[[a]] cierra`\n") == ["a"]


def test_docs_recover_ignores_links_in_code(tmp_path, capsys):
    """The sldb-ui case: example links inside code are not reported as broken."""
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", "link_models:NoteDoc", "--store", str(store), "--pythonpath", pythonpath]) == 0
    for name in ("concept", "item-link", "nested-link", "after-tick", "closing"):
        note = tmp_path / f"{name}.md"
        note.write_text(f"# {name}\n\nBody.\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(note), "--model", "NoteDoc", "--store", str(store), "--pythonpath", pythonpath]) == 0
    doc = tmp_path / "guide.md"
    doc.write_text(CODE_EXAMPLES_DOC.replace("[implements:: [[spec-001]]]", "[[concept]]"), encoding="utf-8")

    capsys.readouterr()
    rc = cli_main(["docs", "recover", str(doc), "--store", str(store), "--format", "json", "--include-transclusions"])
    recovered = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert [link["target"] for link in recovered["links"]] == ["concept", "item-link", "nested-link", "after-tick", "closing"]
    assert all(link["resolved"] for link in recovered["links"])
    assert recovered["unresolved"] == []


def _commonmark_targets(markdown):
    """Link targets outside code per the HTML that markdown-it-py renders in commonmark mode."""
    import re

    from markdown_it import MarkdownIt

    html = re.sub(r"<code[^>]*>.*?</code>", "", MarkdownIt("commonmark").render(markdown.replace("\r\n", "\n")), flags=re.S)
    return [m.group(1).strip() for m in re.finditer(r"\[\[([^\]]+)\]\]", html)]


def _assert_targets(markdown, expected):
    from sldb.links import parse_links

    assert [link.target for link in parse_links(markdown)] == expected
    assert _commonmark_targets(markdown) == expected


def test_parse_links_indented_code_in_list_item():
    """Code inside a list item starts 4 columns past the item's content, also in a sub-item."""
    _assert_targets("- item\n\n        [[code8]]\n\n- b [[real]]\n", ["real"])
    _assert_targets("- item\n  - sub\n\n          [[c]]\n", [])
    _assert_targets("- item\n  - sub\n\n      [[para]]\n", ["para"])
    _assert_targets("1. item\n\n       [[c]]\n\n[[d]]\n\n    [[e]]\n", ["d"])


def test_parse_links_escaped_backtick_is_text():
    _assert_targets("\\`[[b]]\\`\n", ["b"])
    _assert_targets("\\``[[a]]` [[b]]\n", ["b"])
    _assert_targets("\\\\`[[a]]` [[b]]\n", ["b"])


def test_parse_links_crlf_line_ends():
    _assert_targets("```\r\n[[a]]\r\n```\r\n[[b]]\r\n", ["b"])
    _assert_targets("~~~\r\n[[a]]\r\n~~~ \r\n[[b]]\r\n", ["b"])
    _assert_targets("`[[a]]\r\n\r\n[[b]]` [[c]]\r\n", ["a", "b", "c"])


def test_parse_links_fence_on_numbered_item_line_keeps_links_after_it():
    _assert_targets("1. ```python\n   x = 1\n   ```\n\nVer [[real]].\n", ["real"])


def test_parse_links_fence_on_bullet_item_line_keeps_links_after_it():
    _assert_targets("- ```\n  code\n  ```\n\nVer [[real]] y [[otro]].\n", ["real", "otro"])


def test_parse_links_fence_on_item_line_skips_its_content_before_next_item():
    _assert_targets("- ```bash\n  echo [[x]]\n  ```\n- [[item]]\n", ["item"])


def test_parse_links_fence_on_item_line_skips_its_content_before_text():
    _assert_targets("- ```\n  [[f]]\n  ```\n[[r]]\n", ["r"])


def test_parse_links_fence_in_list_item_ends_with_the_item():
    """An unclosed fence inside a list item ends with the item, not at the end of the file."""
    _assert_targets("- a\n  ```\n  [[x]]\n[[y]]\n", ["y"])
    _assert_targets("* ~~~\n  [[x]]\n\n[[y]]\n", ["y"])
    _assert_targets("- a\n  - ```\n    [[x]]\n    ```\n  [[y]]\n", ["y"])


def test_parse_links_code_span_stays_in_its_block():
    """A lone backtick does not pair with one in the next item, heading, quote or rule."""
    _assert_targets("Usa el carácter ` para abrir código; ver [[real]].\n- otro ` suelto en un ítem\n", ["real"])
    _assert_targets("- uno ` y [[real]]\n- dos ` y\n", ["real"])
    _assert_targets("Un ` suelto y [[real]].\n# Título con ` suelto\n", ["real"])
    _assert_targets("Un ` suelto y [[real]].\n> cita con ` suelto\n", ["real"])
    _assert_targets("Un ` y [[real]]\n***\notro `\n", ["real"])
    _assert_targets("Un ` suelto y [[real]].\n```\nx ` y\n```\n", ["real"])


def test_parse_links_keeps_the_source_text_and_the_order():
    """Escapes and emphasis keep their source text; predicate links come first, then the rest."""
    from sldb.links import parse_links

    markdown = "---\nrefs: [[fm]]\n---\n# T [[head]]\n\n| a |\n|---|\n| [[cell]] `[[c]]` |\n\n" \
        "<div>[[html]]</div>\n\nTexto <code>[[inline-html]]</code> [[a*b*]] y [p:: [[x\\_y]]].\n"
    links = parse_links(markdown, {"p": "HOW"})

    assert [link.raw for link in links] == [
        "[p:: [[x\\_y]]]", "[[fm]]", "[[head]]", "[[cell]]", "[[html]]", "[[inline-html]]", "[[a*b*]]",
    ]
    assert links[0].target == "x\\_y" and links[0].kind == "predicate_link"


def test_parse_links_code_cut_inside_brackets_is_not_a_link():
    from sldb.links import parse_links

    assert [link.target for link in parse_links("[[a`x`b]] [[ok]]\n")] == ["ok"]


def test_parse_links_front_matter_keeps_its_opening_line():
    """Text after a `---` on line 0 opens a front matter for markdown-it; its links still count."""
    _assert_targets("---[[b]]\n---\n\n[[a]]\n", ["b", "a"])
    _assert_targets("- --- nota [[b]]\n- otro [[c]]\n", ["b", "c"])


def test_parse_links_reads_a_front_matter_raw():
    """A front matter is read as written, as before: what looks like code there is not code."""
    from sldb.links import parse_links

    markdown = "---\nrefs: [[fm]]\nnote: '`[[tick]]`'\n---\n\n[[body]]\n"
    assert [link.target for link in parse_links(markdown)] == ["fm", "tick", "body"]


def test_parse_links_front_matter_lines_split_like_markdown_it():
    """Only CRLF, CR and LF end a line for markdown-it; str.splitlines also cuts at U+2028/U+2029,
    NEL and form feed, and would drop the last lines of the front matter."""
    for sep1, sep2 in (("\u2028", "\u2029"), ("\x85", "\x85"), ("\x0c", "\x0c")):
        _assert_targets(f"---\na{sep1}b{sep2}c\nd: [[fm]]\n---\n\n[[a]]\n", ["fm", "a"])
