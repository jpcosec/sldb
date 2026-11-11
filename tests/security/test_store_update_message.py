"""SEGURIDAD resto 2, r4: `stores update` lists a tracked document the read guard does not read
under its own line with its code (`store/path-outside-root`, `store/symlink-not-read`), not under
"Skipped missing documents"; a document really missing is still listed there."""

from __future__ import annotations

from tests.security.audited import escape, make_world


def test_an_unread_document_is_named_with_its_code_and_a_missing_one_as_missing(tmp_path):
    world = make_world(tmp_path)
    escape(world, "b")
    (world.root / "memos" / "c.md").unlink()
    ran = world.cli("stores", "update", "--store", ".sldb", "--pythonpath", world.py)
    assert not world.outside_opened(ran)
    lines = ran["output"].splitlines()
    assert "Skipped unread documents: b (store/path-outside-root)" in lines
    assert "Skipped missing documents: c" in lines
    assert not any(line.startswith("Skipped missing") and "b (" in line for line in lines)


def test_a_symlink_inside_the_root_is_named_symlink_not_read(tmp_path):
    world = make_world(tmp_path)
    memos = world.root / "memos"
    (memos / "b.md").rename(memos / "real-b.md")
    (memos / "b.md").symlink_to(memos / "real-b.md")
    ran = world.cli("stores", "update", "--store", ".sldb", "--pythonpath", world.py)
    assert "Skipped unread documents: b (store/symlink-not-read)" in ran["output"].splitlines()
    assert str((memos / "real-b.md").resolve()) not in ran["opened"]
