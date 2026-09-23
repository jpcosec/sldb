"""A bad existing document must not cause partial regeneration."""
import argparse
from pathlib import Path

import pytest

from sldb.cli.main import main
from sldb.cli.selfdoc_write import write_documents
from sldb.selfdoc.materialize import plan_documents
from sldb.selfdoc.parser import ParserScanner


def project_files(root) -> dict:
    return {p: p.read_bytes() for p in root.rglob("*") if p.is_file() and not _is_interpreter_cache(p)}


def _is_interpreter_cache(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix == ".pyc"


def records(*commands):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers()
    for command in commands:
        sub.add_parser(command, help="Run")
    return ParserScanner().scan(parser)


def test_filename_collision_is_rejected_before_writing(tmp_path):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers()
    sub.add_parser("a-b")
    sub.add_parser("a").add_subparsers().add_parser("b")
    with pytest.raises(ValueError, match="collide"):
        plan_documents(ParserScanner().scan(parser), "widget", "fixture:build", tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_invalid_existing_document_prevents_any_sync(project, invoke):
    output = project / "knowledge/commands"
    output.mkdir(parents=True)
    bad = output / "cmd-widget-run.md"
    bad.write_text("# This is not a CliCommandDoc\n")
    before = project_files(project)
    with pytest.raises(SystemExit):
        invoke("sync")
    assert project_files(project) == before


def test_before_image_guard_prevents_clobbering_concurrent_edits(tmp_path):
    plans = plan_documents(records("run"), "widget", "fixture:build", tmp_path / "knowledge")
    plans[0].path.parent.mkdir(parents=True)
    plans[0].path.write_text("A concurrent edit")
    with pytest.raises(ValueError, match="changed during planning"):
        write_documents(plans, tmp_path / ".sldb", tmp_path)
    assert plans[0].path.read_text() == "A concurrent edit"


def test_output_outside_store_is_rejected(project, invoke):
    with pytest.raises(SystemExit, match="within the store project"):
        invoke("sync", "--output", "../outside")
