"""SEGURIDAD resto 2, `edges init` (builtin relation types, `stamped_file`'s callers): a symlink
where a builtin RelationTypeDoc would be written is neither followed nor written through; it is
warned with its finding (`store/symlink-not-read` or `store/path-outside-root`), not an ELOOP."""

from __future__ import annotations

from tests.security.audited import make_world


def test_a_symlink_where_a_builtin_would_be_written_is_warned_not_followed(tmp_path):
    world = make_world(tmp_path)
    target = world.root / "sldb" / "relation_types" / "references.md"
    target.parent.mkdir(parents=True)
    target.symlink_to(world.secret)
    ran = world.cli("edges", "init", "--store", ".sldb", "--pythonpath", world.py)
    assert not world.outside_opened(ran)
    assert "store/path-outside-root" in ran["output"] and "Errno 40" not in ran["output"]
    assert world.secret.read_text(encoding="utf-8").endswith("SECRET-BODY\n")
