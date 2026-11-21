"""Parser extraction must preserve executable constraints."""
import argparse

from sldb.selfdoc.parser import ParserScanner
from sldb.selfdoc.projection import provenance


def test_nested_arguments_and_required_exclusive_group():
    parser = argparse.ArgumentParser(prog="app")
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    group = sub.add_parser("docs", help="Documents")
    leaves = group.add_subparsers(dest="operation")
    leaf = leaves.add_parser("export", help="Export documents")
    exclusive = leaf.add_mutually_exclusive_group(required=True)
    exclusive.add_argument("--json", action="store_true")
    exclusive.add_argument("--yaml", action="store_true")
    leaf.add_argument("--limit", type=int, default=3, choices=[1, 3, 5])
    record = next(r for r in ParserScanner().scan(parser) if not r.group)
    by_name = {r.names[0]: r for r in record.arguments}
    assert record.path == ["docs", "export"]
    assert by_name["--verbose"].default == "false"
    assert by_name["--limit"].choices == ["1", "3", "5"]
    assert by_name["--limit"].value_type == "builtins.int"
    assert record.exclusive_groups[0].required
    assert record.exclusive_groups[0].arguments == ["json", "yaml"]


def test_hidden_parent_suppresses_descendants_but_help_omission_does_not():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers()
    sub.add_parser("public")
    hidden = sub.add_parser("old", help=argparse.SUPPRESS)
    hidden.add_subparsers().add_parser("run", help="Old command")
    assert [r.path for r in ParserScanner().scan(parser)] == [["public"]]
    assert next(r for r in ParserScanner(True).scan(parser) if r.path == ["old", "run"]).hidden


def test_contract_hash_changes_with_parser_default():
    parser = argparse.ArgumentParser()
    child = parser.add_subparsers().add_parser("run")
    option = child.add_argument("--count", default=1)
    first = provenance(ParserScanner().scan(parser)[0], "fixture:build")
    assert first == provenance(ParserScanner().scan(parser)[0], "fixture:build")
    option.default = 2
    assert first != provenance(ParserScanner().scan(parser)[0], "fixture:build")


def test_contract_hash_does_not_depend_on_terminal_width(monkeypatch):
    parser = argparse.ArgumentParser(prog="app")
    child = parser.add_subparsers().add_parser("run")
    child.add_argument("--a-long-option-name", choices=["first", "second"])
    child.add_argument("--another-long-option-name", required=True)
    monkeypatch.setenv("COLUMNS", "40")
    narrow = provenance(ParserScanner().scan(parser)[0], "fixture:build")
    monkeypatch.setenv("COLUMNS", "160")
    assert narrow == provenance(ParserScanner().scan(parser)[0], "fixture:build")


def _tree_copy(tmp_path, edit=lambda text: text):
    from pathlib import Path
    source = Path(__file__).resolve().parents[2] / "docs" / "architecture" / "current-cli-tree.md"
    copy = tmp_path / "current-cli-tree.md"
    copy.write_text(edit(source.read_text(encoding="utf-8")), encoding="utf-8")
    return copy


def test_cli_tree_document_matches_the_parser(tmp_path):
    from sldb.cli.parser import build_parser
    from sldb.selfdoc.cli_tree import compare
    assert compare(build_parser(), _tree_copy(tmp_path)) == ([], [])


def test_removing_a_subcommand_line_from_the_tree_document_names_it(tmp_path):
    from sldb.cli.parser import build_parser
    from sldb.selfdoc.cli_tree import compare
    copy = _tree_copy(tmp_path, lambda text: text.replace("├── bench\n", "").replace("│   └── show / verify\n", ""))
    missing, stale = compare(build_parser(), copy)
    assert "bench" in missing and "journal show" in missing and not stale


def test_a_command_the_parser_lacks_is_stale_and_is_an_error_finding(tmp_path):
    from sldb.cli.parser import build_parser
    from sldb.selfdoc.cli_tree import compare
    from sldb.selfdoc.report import DocumentationReport
    from sldb.selfdoc.report_findings import report_findings
    copy = _tree_copy(tmp_path, lambda text: text.replace("├── bench\n", "├── bench\n├── ghost\n│   └── haunt\n"))
    missing, stale = compare(build_parser(), copy)
    assert stale == ["ghost", "ghost haunt"] and not missing
    report = DocumentationReport(cli_tree_stale=stale)
    assert not report.ok
    assert [(f.level, f.subject) for f in report_findings(report)] == [("error", "ghost"), ("error", "ghost haunt")]
